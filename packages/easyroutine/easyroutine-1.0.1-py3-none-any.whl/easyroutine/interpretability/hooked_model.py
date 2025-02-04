import torch
from transformers import GenerationConfig
from typing import (
    Union,
    Literal,
    Optional,
    List,
    Dict,
    Callable,
    Any,
)

from easyroutine.interpretability.models import (
    ModelFactory,
    TokenizerFactory,
    InputHandler,
)
from easyroutine.interpretability.token_index import TokenIndex
from easyroutine.interpretability.activation_cache import ActivationCache
from easyroutine.interpretability.utils import get_attribute_by_name
from easyroutine.interpretability.module_wrappers.manager import ModuleWrapperManager
from easyroutine.logger import Logger, LambdaLogger
from tqdm import tqdm
from dataclasses import dataclass
from easyroutine.interpretability.ablation import AblationManager

# from src.model.emu3.
from easyroutine.interpretability.utils import (
    map_token_to_pos,
    preprocess_patching_queries,
    logit_diff,
    get_attribute_from_name,
    kl_divergence_diff,
)
from easyroutine.interpretability.hooks import (
    embed_hook,
    save_resid_hook,
    projected_value_vectors_head,
    avg_attention_pattern_head,
    attention_pattern_head,
    get_module_by_path,
    process_args_kwargs_output,
    query_key_value_hook,
    head_out_hook,
)

from functools import partial
import pandas as pd


# to avoid running out of shared memory
# torch.multiprocessing.set_sharing_strategy("file_system")


@dataclass
class HookedModelConfig:
    """
    Configuration of the HookedModel

    Arguments:
        model_name (str): the name of the model to load
        device_map (Literal["balanced", "cuda", "cpu", "auto"]): the device to use for the model
        torch_dtype (torch.dtype): the dtype of the model
        attn_implementation (Literal["eager", "flash_attention_2"]): the implementation of the attention
        batch_size (int): the batch size of the model. FOR NOW, ONLY BATCH SIZE 1 IS SUPPORTED. USE AT YOUR OWN RISK
    """

    model_name: str
    device_map: Literal["balanced", "cuda", "cpu", "auto"] = "balanced"
    torch_dtype: torch.dtype = torch.bfloat16
    attn_implementation: Literal["eager", "custom_eager"] = (
        "custom_eager"  # TODO: add flash_attention_2 in custom module to support it
    )
    batch_size: int = 1


@dataclass
class ExtractionConfig:
    """
    Configuration of the extraction of the activations of the model. It store what activations you want to extract from the model.

    Arguments:
        extract_resid_in (bool): if True, extract the input of the residual stream
        extract_resid_mid (bool): if True, extract the output of the intermediate stream
        extract_resid_out (bool): if True, extract the output of the residual stream
        extract_resid_in_post_layernorm(bool): if True, extract the input of the residual stream after the layernorm
        extract_attn_pattern (bool): if True, extract the attention pattern of the attn
        extract_head_values_projected (bool): if True, extract the values vectors projected of the model
        extract_head_values (bool): if True, extract the values of the attention
        extract_head_out (bool): if True, extract the output of the heads [DEPRECATED]
        extract_attn_out (bool): if True, extract the output of the attention of the attn_heads passed
        extract_attn_in (bool): if True, extract the input of the attention of the attn_heads passed
        extract_mlp_out (bool): if True, extract the output of the mlp of the attn
        save_input_ids (bool): if True, save the input_ids in the cache
        avg (bool): if True, extract the average of the activations over the target positions
        avg_over_example (bool): if True, extract the average of the activations over the examples (it required a external cache to save the running avg)
        attn_heads (Union[list[dict], Literal["all"]]): list of dictionaries with the layer and head to extract the attention pattern or 'all' to
    """

    extract_resid_in: bool = False
    extract_resid_mid: bool = False
    extract_resid_out: bool = False
    extract_resid_in_post_layernorm: bool = False
    extract_attn_pattern: bool = False
    extract_head_values_projected: bool = False
    # TODO: add extract_head_queries_projected
    # TODO: add extract_head_keys_projected
    extract_head_keys: bool = False
    extract_head_values: bool = False
    extract_head_queries: bool = False
    extract_head_out: bool = False
    extract_attn_out: bool = False
    extract_attn_in: bool = False
    extract_mlp_out: bool = False
    save_input_ids: bool = False
    avg: bool = False
    avg_over_example: bool = False
    attn_heads: Union[list[dict], Literal["all"]] = "all"

    def is_not_empty(self):
        """
        Return True if at least one of the attributes is True, False otherwise, i.e. if the model should extract something!
        """
        return any(
            [
                self.extract_resid_in,
                self.extract_resid_mid,
                self.extract_resid_out,
                self.extract_attn_pattern,
                self.extract_head_values_projected,
                self.extract_head_keys,
                self.extract_head_values,
                self.extract_head_queries,
                self.extract_head_out,
                self.extract_attn_out,
                self.extract_attn_in,
                self.extract_mlp_out,
                self.save_input_ids,
                self.avg,
                self.avg_over_example,
            ]
        )


class HookedModel:
    """
    This class is a wrapper around the huggingface model that allows to extract the activations of the model. It is support
    advanced mechanistic intepretability methods like ablation, patching, etc.
    """

    def __init__(self, config: HookedModelConfig, log_file_path: Optional[str] = None):
        self.logger = Logger(
            logname="HookedModel",
            level="info",
            log_file_path=log_file_path,
        )

        self.config = config
        self.hf_model, self.hf_language_model, self.model_config = (
            ModelFactory.load_model(
                model_name=config.model_name,
                device_map=config.device_map,
                torch_dtype=config.torch_dtype,
                attn_implementation="eager"
                if config.attn_implementation == "custom_eager"
                else config.attn_implementation,
            )
        )
        self.base_model = None
        self.module_wrapper_manager = ModuleWrapperManager(model=self.hf_model)

        tokenizer, processor = TokenizerFactory.load_tokenizer(
            model_name=config.model_name,
            torch_dtype=config.torch_dtype,
            device_map=config.device_map,
        )
        self.hf_tokenizer = tokenizer
        self.input_handler = InputHandler(model_name=config.model_name)
        if processor is True:
            self.processor = tokenizer
            self.text_tokenizer = self.processor.tokenizer  # type: ignore
        else:
            self.processor = None
            self.text_tokenizer = tokenizer

        self.first_device = next(self.hf_model.parameters()).device
        device_num = torch.cuda.device_count()
        self.logger.info(
            f"Model loaded in {device_num} devices. First device: {self.first_device}",
            std_out=True,
        )
        self.act_type_to_hook_name = {
            "resid_in": self.model_config.residual_stream_input_hook_name,
            "resid_out": self.model_config.residual_stream_hook_name,
            "resid_mid": self.model_config.intermediate_stream_hook_name,
            "attn_out": self.model_config.attn_out_hook_name,
            "attn_in": self.model_config.attn_in_hook_name,
            "values": self.model_config.head_value_hook_name,
            # Add other act_types if needed
        }
        self.additional_hooks = []
        self.assert_all_modules_exist()

        if self.config.attn_implementation == "custom_eager":
            self.logger.info(
                """
                            The model is using the custom eager attention implementation that support attention matrix hooks because I get config.attn_impelemntation == 'custom_eager'. If you don't want this, you can call HookedModel.restore_original_modules. 
                            However, we reccomend using this implementation since the base one do not contains attention matrix hook resulting in unexpected behaviours. 
                            """,
                std_out=True,
            )
            self.set_custom_modules()

    def __repr__(self):
        return f"""HookedModel(model_name={self.config.model_name}):
        {self.hf_model.__repr__()}
    """

    @classmethod
    def from_pretrained(cls, model_name: str, **kwargs):
        return cls(HookedModelConfig(model_name=model_name, **kwargs))

    def assert_module_exists(self, component: str):
        # Remove '.input' or '.output' from the component
        component = component.replace(".input", "").replace(".output", "")

        # Check if '{}' is in the component, indicating layer indexing
        if "{}" in component:
            for i in range(0, self.model_config.num_hidden_layers):
                attr_name = component.format(i)

                try:
                    get_attribute_by_name(self.hf_model, attr_name)
                except AttributeError:
                    try:
                        if attr_name in self.module_wrapper_manager:
                            self.set_custom_modules()
                            get_attribute_by_name(self.hf_model, attr_name)
                            self.restore_original_modules()
                    except AttributeError:
                        raise ValueError(
                            f"Component '{attr_name}' does not exist in the model. Please check the model configuration."
                        )
        else:
            try:
                get_attribute_by_name(self.hf_model, component)
            except AttributeError:
                raise ValueError(
                    f"Component '{component}' does not exist in the model. Please check the model configuration."
                )

    def assert_all_modules_exist(self):
        # get the list of all attributes of model_config
        all_attributes = [attr_name for attr_name in self.model_config.__dict__.keys()]
        # save just the attributes that have "hook" in the name
        hook_attributes = [
            attr_name for attr_name in all_attributes if "hook" in attr_name
        ]
        for hook_attribute in hook_attributes:
            self.assert_module_exists(getattr(self.model_config, hook_attribute))

    def set_custom_modules(self):
        self.logger.info("Setting custom modules.", std_out=True)
        self.module_wrapper_manager.substitute_attention_module(self.hf_model)

    def restore_original_modules(self):
        self.logger.info("Restoring original modules.", std_out=True)
        self.module_wrapper_manager.restore_original_attention_module(self.hf_model)

    def use_full_model(self):
        if self.processor is not None:
            self.logger.info("Using full model capabilities", std_out=True)
        else:
            if self.base_model is not None:
                self.hf_model = self.base_model
            self.logger.info("Using full text only model capabilities", std_out=True)

    def use_language_model_only(self):
        if self.hf_language_model is None:
            self.logger.warning(
                "The model does not have a separate language model that can be used",
                std_out=True,
            )
        else:
            self.base_model = self.hf_model
            self.hf_model = self.hf_language_model
            self.logger.info("Using only language model capabilities", std_out=True)

    def get_tokenizer(self):
        return self.hf_tokenizer

    def get_text_tokenizer(self):
        r"""
        If the tokenizer is a processor, return just the tokenizer. If the tokenizer is a tokenizer, return the tokenizer

        Args:
            None

        Returns:
            tokenizer: the tokenizer of the model
        """
        if self.processor is not None:
            if not hasattr(self.processor, "tokenizer"):
                raise ValueError("The processor does not have a tokenizer")
            return self.processor.tokenizer  # type: ignore
        return self.hf_tokenizer

    def get_processor(self):
        r"""
        Return the processor of the model (None if the model does not have a processor, i.e. text only model)

        Args:
            None

        Returns:
            processor: the processor of the model
        """
        if self.processor is None:
            raise ValueError("The model does not have a processor")
        return self.processor

    def get_lm_head(self):
        return get_attribute_by_name(self.hf_model, self.model_config.unembed_matrix)

    def get_last_layernorm(self):
        return get_attribute_by_name(self.hf_model, self.model_config.last_layernorm)

    def eval(self):
        r"""
        Set the model in evaluation mode
        """
        self.hf_model.eval()

    def device(self):
        r"""
        Return the device of the model. If the model is in multiple devices, it will return the first device

        Args:
            None

        Returns:
            device: the device of the model
        """
        return self.first_device

    def register_forward_hook(self, component: str, hook_function: Callable):
        r"""
        Add a new hook to the model. The hook will be called in the forward pass of the model.

        Args:
            component (str): the component of the model where the hook will be added.
            hook_function (Callable): the function that will be called in the forward pass of the model. The function must have the following signature:
                def hook_function(module, input, output):
                    pass

        Returns:
            None

        Examples:
            >>> def hook_function(module, input, output):
            >>>     # your code here
            >>>     pass
            >>> model.register_forward_hook("model.layers[0].self_attn", hook_function)
        """
        self.additional_hooks.append(
            {
                "component": component,
                "intervention": hook_function,
            }
        )

    def to_string_tokens(
        self,
        tokens: Union[list, torch.Tensor],
    ):
        r"""
        Transform a list or a tensor of tokens in a list of string tokens.

        Args:
            tokens (Union[list, torch.Tensor]): the tokens to transform in string tokens

        Returns:
            string_tokens (list): the list of string tokens

        Examples:
            >>> tokens = [101, 1234, 1235, 102]
            >>> model.to_string_tokens(tokens)
            ['[CLS]', 'hello', 'world', '[SEP]']
        """
        if isinstance(tokens, torch.Tensor):
            if tokens.dim() == 1:
                tokens = tokens.tolist()
            else:
                tokens = tokens.squeeze().tolist()
        string_tokens = []
        for tok in tokens:
            string_tokens.append(self.hf_tokenizer.decode(tok))  # type: ignore
        return string_tokens

    def create_hooks(
        self,
        inputs,
        cache: ActivationCache,
        token_index: List,
        token_dict: Dict,
        # string_tokens: List[str],
        extraction_config: ExtractionConfig = ExtractionConfig(),
        patching_queries: Optional[Union[dict, pd.DataFrame]] = None,
        ablation_queries: Optional[Union[dict, pd.DataFrame]] = None,
        batch_idx: Optional[int] = None,
        external_cache: Optional[ActivationCache] = None,
    ):
        r"""
        Create the hooks to extract the activations of the model. The hooks will be added to the model and will be called in the forward pass of the model.

        Arguments:
            inputs (dict): dictionary with the inputs of the model (input_ids, attention_mask, pixel_values ...)
            cache (ActivationCache): dictionary where the activations of the model will be saved
            extracted_token_position (list[str]): list of tokens to extract the activations from (["last", "end-image", "start-image", "first"])
            string_tokens (list[str]): list of string tokens
            pivot_positions (Optional[list[int]]): list of split positions of the tokens
            extraction_config (ExtractionConfig): configuration of the extraction of the activations of the model (default = ExtractionConfig())
            ablation_queries (Optional[Union[dict, pd.DataFrame]]): dictionary or dataframe with the ablation queries to perform during forward pass
            patching_queries (Optional[Union[dict, pd.DataFrame]]): dictionary or dataframe with the patching queries to perform during forward pass
            batch_idx (Optional[int]): index of the batch in the dataloader
            external_cache (Optional[ActivationCache]): external cache to use in the forward pass

        Returns:
            hooks (list[dict]): list of dictionaries with the component and the intervention to perform in the forward pass of the model
        """
        hooks = []

        # compute layer and head indexes
        if (
            isinstance(extraction_config.attn_heads, str)
            and extraction_config.attn_heads == "all"
        ):
            layer_indexes = [i for i in range(0, self.model_config.num_hidden_layers)]
            head_indexes = ["all"] * len(layer_indexes)
        elif isinstance(extraction_config.attn_heads, list):
            layer_head_indexes = [
                (el["layer"], el["head"]) for el in extraction_config.attn_heads
            ]
            layer_indexes = [el[0] for el in layer_head_indexes]
            head_indexes = [el[1] for el in layer_head_indexes]
        else:
            raise ValueError(
                "attn_heads must be 'all' or a list of dictionaries as [{'layer': 0, 'head': 0}]"
            )

        if extraction_config.extract_resid_out:
            # assert that the component exists in the model
            hooks += [
                {
                    "component": self.model_config.residual_stream_hook_name.format(i),
                    "intervention": partial(
                        save_resid_hook,
                        cache=cache,
                        cache_key=f"resid_out_{i}",
                        token_index=token_index,
                        avg=extraction_config.avg,
                    ),
                }
                for i in range(0, self.model_config.num_hidden_layers)
            ]
        if extraction_config.extract_resid_in:
            # assert that the component exists in the model
            hooks += [
                {
                    "component": self.model_config.residual_stream_input_hook_name.format(
                        i
                    ),
                    "intervention": partial(
                        save_resid_hook,
                        cache=cache,
                        cache_key=f"resid_in_{i}",
                        token_index=token_index,
                        avg=extraction_config.avg,
                    ),
                }
                for i in range(0, self.model_config.num_hidden_layers)
            ]

        if extraction_config.extract_resid_in_post_layernorm:
            hooks += [
                {
                    "component": self.model_config.residual_stream_input_post_layernorm_hook_name.format(
                        i
                    ),
                    "intervention": partial(
                        save_resid_hook,
                        cache=cache,
                        cache_key=f"resid_in_post_layernorm_{i}",
                        token_index=token_index,
                        avg=extraction_config.avg,
                    ),
                }
                for i in range(0, self.model_config.num_hidden_layers)
            ]

        if extraction_config.save_input_ids:
            hooks += [
                {
                    "component": self.model_config.embed_tokens,
                    "intervention": partial(
                        embed_hook,
                        cache=cache,
                        cache_key="input_ids",
                    ),
                }
            ]

        if extraction_config.extract_head_queries:
            hooks += [
                {
                    "component": self.model_config.head_query_hook_name.format(i),
                    "intervention": partial(
                        query_key_value_hook,
                        cache=cache,
                        cache_key="queries_",
                        token_index=token_index,
                        head_dim=self.model_config.head_dim,
                        avg=extraction_config.avg,
                        layer=i,
                        head=head,
                        num_key_value_groups=self.model_config.num_key_value_groups,
                    ),
                }
                for i, head in zip(layer_indexes, head_indexes)
            ]

        if extraction_config.extract_head_values:
            hooks += [
                {
                    "component": self.model_config.head_value_hook_name.format(i),
                    "intervention": partial(
                        query_key_value_hook,
                        cache=cache,
                        cache_key="values_",
                        token_index=token_index,
                        head_dim=self.model_config.head_dim,
                        avg=extraction_config.avg,
                        layer=i,
                        head=head,
                        num_key_value_groups=self.model_config.num_key_value_groups,
                    ),
                }
                for i, head in zip(layer_indexes, head_indexes)
            ]

        if extraction_config.extract_head_keys:
            hooks += [
                {
                    "component": self.model_config.head_key_hook_name.format(i),
                    "intervention": partial(
                        query_key_value_hook,
                        cache=cache,
                        cache_key="keys_",
                        token_index=token_index,
                        head_dim=self.model_config.head_dim,
                        avg=extraction_config.avg,
                        layer=i,
                        head=head,
                        num_key_value_groups=self.model_config.num_key_value_groups,
                    ),
                }
                for i, head in zip(layer_indexes, head_indexes)
            ]

        if extraction_config.extract_head_out:
            hooks += [
                {
                    "component": self.model_config.attn_o_proj_input_hook_name.format(
                        i
                    ),
                    "intervention": partial(
                        head_out_hook,
                        cache=cache,
                        cache_key="head_out_",
                        token_index=token_index,
                        avg=extraction_config.avg,
                        layer=i,
                        head=head,
                        num_heads=self.model_config.num_attention_heads,
                        head_dim=self.model_config.head_dim,
                        o_proj_weight=get_attribute_from_name(
                            self.hf_model,
                            self.model_config.attn_out_proj_weight.format(i),
                        ),
                        o_proj_bias=get_attribute_from_name(
                            self.hf_model,
                            self.model_config.attn_out_proj_bias.format(i),
                        ),
                    ),
                }
                for i, head in zip(layer_indexes, head_indexes)
            ]

        if extraction_config.extract_attn_in:
            hooks += [
                {
                    "component": self.model_config.attn_in_hook_name.format(i),
                    "intervention": partial(
                        save_resid_hook,
                        cache=cache,
                        cache_key=f"attn_in_{i}",
                        token_index=token_index,
                        avg=extraction_config.avg,
                    ),
                }
                for i in range(0, self.model_config.num_hidden_layers)
            ]

        if extraction_config.extract_attn_out:
            hooks += [
                {
                    "component": self.model_config.attn_out_hook_name.format(i),
                    "intervention": partial(
                        save_resid_hook,
                        cache=cache,
                        cache_key=f"attn_out_{i}",
                        token_index=token_index,
                        avg=extraction_config.avg,
                    ),
                }
                for i in range(0, self.model_config.num_hidden_layers)
            ]

        # if extraction_config.extract_avg:
        #     # Define a hook that saves the activations of the residual stream
        #     raise NotImplementedError(
        #         "The hook for the average is not working with token_index as a list"
        #     )

        #     # hooks.extend(
        #     #     [
        #     #         {
        #     #             "component": self.model_config.residual_stream_hook_name.format(
        #     #                 i
        #     #             ),
        #     #             "intervention": partial(
        #     #                 avg_hook,
        #     #                 cache=cache,
        #     #                 cache_key="resid_avg_{}".format(i),
        #     #                 last_image_idx=last_image_idxs, #type
        #     #                 end_image_idx=end_image_idxs,
        #     #             ),
        #     #         }
        #     #         for i in range(0, self.model_config.num_hidden_layers)
        #     #     ]
        #     # )
        if extraction_config.extract_resid_mid:
            hooks += [
                {
                    "component": self.model_config.intermediate_stream_hook_name.format(
                        i
                    ),
                    "intervention": partial(
                        save_resid_hook,
                        cache=cache,
                        cache_key=f"resid_mid_{i}",
                        token_index=token_index,
                        avg=extraction_config.avg,
                    ),
                }
                for i in range(0, self.model_config.num_hidden_layers)
            ]

            # if we want to extract the output of the heads
        if extraction_config.extract_mlp_out:
            hooks += [
                {
                    "component": self.model_config.mlp_out_hook_name.format(i),
                    "intervention": partial(
                        save_resid_hook,
                        cache=cache,
                        cache_key=f"mlp_out_{i}",
                        token_index=token_index,
                        avg=extraction_config.avg,
                    ),
                }
                for i in range(0, self.model_config.num_hidden_layers)
            ]

        # PATCHING
        if patching_queries:
            token_to_pos = partial(
                map_token_to_pos,
                _get_token_index=token_dict,
                # string_tokens=string_tokens,
                hf_tokenizer=self.hf_tokenizer,
                inputs=inputs,
            )
            patching_queries = preprocess_patching_queries(
                patching_queries=patching_queries,
                map_token_to_pos=token_to_pos,
                model_config=self.model_config,
            )

            def make_patch_tokens_hook(patching_queries_subset):
                """
                Creates a hook function to patch the activations in the
                current forward pass.
                """

                def patch_tokens_hook(
                    module, args, kwargs, output
                ):  # TODO: Move to hook.py
                    b = process_args_kwargs_output(args, kwargs, output)
                    # Modify the tensor without affecting the computation graph
                    act_to_patch = b.detach().clone()
                    for pos, patch in zip(
                        patching_queries_subset["pos_token_to_patch"],
                        patching_queries_subset["patching_activations"],
                    ):
                        act_to_patch[0, pos, :] = patching_queries_subset[
                            "patching_activations"
                        ].values[0]

                    if output is None:
                        if isinstance(input, tuple):
                            return (act_to_patch, *input[1:])
                        elif input is not None:
                            return act_to_patch
                    else:
                        if isinstance(output, tuple):
                            return (act_to_patch, *output[1:])
                        elif output is not None:
                            return act_to_patch
                    raise ValueError("No output or input found")

                return patch_tokens_hook

            # Group the patching queries by 'layer' and 'act_type'
            grouped_queries = patching_queries.groupby(["layer", "activation_type"])

            for (layer, act_type), group in grouped_queries:
                hook_name_template = self.act_type_to_hook_name.get(
                    act_type[:-3]
                )  # -3 because we remove {}
                if not hook_name_template:
                    raise ValueError(f"Unknown activation type: {act_type}")
                    # continue  # Skip unknown activation types

                hook_name = hook_name_template.format(layer)
                hook_function = partial(make_patch_tokens_hook(group))

                hooks.append(
                    {
                        "component": hook_name,
                        "intervention": hook_function,
                    }
                )

        if ablation_queries is not None:
            # TODO: debug and test the ablation. Check with ale
            token_to_pos = partial(
                map_token_to_pos,
                _get_token_index=token_dict,
                # string_tokens=string_tokens,
                hf_tokenizer=self.hf_tokenizer,
                inputs=inputs,
            )
            if self.config.batch_size > 1:
                raise ValueError("Ablation is not supported with batch size > 1")
            ablation_manager = AblationManager(
                model_config=self.model_config,
                token_to_pos=token_to_pos,
                inputs=inputs,
                model_attn_type=self.config.attn_implementation,
                ablation_queries=pd.DataFrame(ablation_queries)
                if isinstance(ablation_queries, dict)
                else ablation_queries,
            )
            hooks.extend(ablation_manager.main())

        if extraction_config.extract_head_values_projected:
            hooks += [
                {
                    "component": self.model_config.head_value_hook_name.format(i),
                    "intervention": partial(
                        projected_value_vectors_head,
                        cache=cache,
                        token_index=token_index,
                        layer=i,
                        num_attention_heads=self.model_config.num_attention_heads,
                        num_key_value_heads=self.model_config.num_key_value_heads,
                        hidden_size=self.model_config.hidden_size,
                        d_head=self.model_config.head_dim,
                        out_proj_weight=get_attribute_from_name(
                            self.hf_model,
                            f"{self.model_config.attn_out_proj_weight.format(i)}",
                        ),
                        out_proj_bias=get_attribute_from_name(
                            self.hf_model,
                            f"{self.model_config.attn_out_proj_bias.format(i)}",
                        ),
                        head=head,
                        avg=extraction_config.avg,
                    ),
                }
                for i, head in zip(layer_indexes, head_indexes)
            ]

        if extraction_config.extract_attn_pattern:
            if extraction_config.avg:
                if external_cache is None:
                    self.logger.warning(
                        """The external_cache is None. The average could not be computed since missing an external cache where store the iterations.
                        """
                    )
                elif batch_idx is None:
                    self.logger.warning(
                        """The batch_idx is None. The average could not be computed since missing the batch index.
                       
                        """
                    )
                else:
                    # move the cache to the same device of the model
                    external_cache.to(self.first_device)
                    hooks += [
                        {
                            "component": self.model_config.attn_matrix_hook_name.format(
                                i
                            ),
                            "intervention": partial(
                                avg_attention_pattern_head,
                                token_index=token_index,
                                layer=i,
                                attn_pattern_current_avg=external_cache,
                                batch_idx=batch_idx,
                                cache=cache,
                                # avg=extraction_config.avg,
                                extract_avg_value=extraction_config.extract_head_values_projected,
                            ),
                        }
                        for i in range(0, self.model_config.num_hidden_layers)
                    ]
            else:
                hooks += [
                    {
                        "component": self.model_config.attn_matrix_hook_name.format(i),
                        "intervention": partial(
                            attention_pattern_head,
                            token_index=token_index,
                            cache=cache,
                            layer=i,
                            head=head,
                        ),
                    }
                    for i, head in zip(layer_indexes, head_indexes)
                ]

            # if additional hooks are not empty, add them to the hooks list
        if self.additional_hooks:
            hooks += self.additional_hooks
        return hooks

    @torch.no_grad()
    def forward(
        self,
        inputs,
        target_token_positions: List[str] = ["last"],
        pivot_positions: Optional[List[int]] = None,
        extraction_config: ExtractionConfig = ExtractionConfig(),
        ablation_queries: Optional[List[dict]] = None,
        patching_queries: Optional[List[dict]] = None,
        external_cache: Optional[ActivationCache] = None,
        attn_heads: Union[list[dict], Literal["all"]] = "all",
        batch_idx: Optional[int] = None,
        move_to_cpu: bool = False,
    ) -> ActivationCache:
        r"""
        Forward pass of the model. It will extract the activations of the model and save them in the cache. It will also perform ablation and patching if needed.

        Args:
            inputs (dict): dictionary with the inputs of the model (input_ids, attention_mask, pixel_values ...)
            target_token_positions (list[str]): list of tokens to extract the activations from (["last", "end-image", "start-image", "first"])
            pivot_positions (Optional[list[int]]): list of split positions of the tokens
            extraction_config (ExtractionConfig): configuration of the extraction of the activations of the model
            ablation_queries (Optional[pd.DataFrame | None]): dataframe with the ablation queries to perform during forward pass
            patching_queries (Optional[pd.DataFrame | None]): dataframe with the patching queries to perform during forward pass
            external_cache (Optional[ActivationCache]): external cache to use in the forward pass
            attn_heads (Union[list[dict], Literal["all"]]): list of dictionaries with the layer and head to extract the attention pattern or 'all' to
            batch_idx (Optional[int]): index of the batch in the dataloader
            move_to_cpu (bool): if True, move the activations to the cpu

        Returns:
            cache (ActivationCache): dictionary with the activations of the model

        Examples:
            >>> inputs = {"input_ids": torch.tensor([[101, 1234, 1235, 102]]), "attention_mask": torch.tensor([[1, 1, 1, 1]])}
            >>> model.forward(inputs, target_token_positions=["last"], extract_resid_out=True)
            {'resid_out_0': tensor([[[0.1, 0.2, 0.3, 0.4]]], grad_fn=<CopyBackwards>), 'input_ids': tensor([[101, 1234, 1235, 102]]), 'mapping_index': {'last': [0]}}
        """

        if target_token_positions is None and extraction_config.is_not_empty():
            raise ValueError(
                "target_token_positions must be passed if we want to extract the activations of the model"
            )
        cache = ActivationCache()
        string_tokens = self.to_string_tokens(
            self.input_handler.get_input_ids(inputs).squeeze()
        )
        token_index, token_dict = TokenIndex(
            self.config.model_name, pivot_positions=pivot_positions
        ).get_token_index(
            tokens=target_token_positions,
            string_tokens=string_tokens,
            return_type="all",
        )
        assert isinstance(token_index, list), "Token index must be a list"
        assert isinstance(token_dict, dict), "Token dict must be a dict"

        hooks = self.create_hooks(  # TODO: add **kwargs
            inputs=inputs,
            token_dict=token_dict,
            token_index=token_index,
            cache=cache,
            extraction_config=extraction_config,
            ablation_queries=ablation_queries,
            patching_queries=patching_queries,
            batch_idx=batch_idx,
            external_cache=external_cache,
        )

        hook_handlers = self.set_hooks(hooks)
        inputs = self.input_handler.prepare_inputs(
            inputs, self.first_device, self.config.torch_dtype
        )
        # forward pass
        output = self.hf_model(
            **inputs,
            # output_original_output=True,
            # output_attentions=extract_attn_pattern,
        )

        cache["logits"] = output.logits[:, -1]
        # since attention_patterns are returned in the output, we need to adapt to the cache structure
        if move_to_cpu:
            cache.cpu()
            if external_cache is not None:
                external_cache.cpu()

        mapping_index = {}
        current_index = 0
        for token in target_token_positions:
            mapping_index[token] = []
            if isinstance(token_dict, int):
                mapping_index[token].append(current_index)
                current_index += 1
            elif isinstance(token_dict, dict):
                for idx in range(len(token_dict[token])):
                    mapping_index[token].append(current_index)
                    current_index += 1
            elif isinstance(token_dict, list):
                for idx in range(len(token_dict)):
                    mapping_index[token].append(current_index)
                    current_index += 1
            else:
                raise ValueError("Token dict must be an int, a dict or a list")
        cache["mapping_index"] = mapping_index

        self.remove_hooks(hook_handlers)

        return cache

    def __call__(self, *args, **kwds) -> ActivationCache:
        r"""
        Call the forward method of the model
        """
        return self.forward(*args, **kwds)

    def predict(self, k=10, **kwargs):
        out = self.forward(**kwargs)
        logits = out["logits"]
        probs = torch.softmax(logits, dim=-1)
        probs = probs.squeeze()
        topk = torch.topk(probs, k)
        # return a dictionary with the topk tokens and their probabilities
        string_tokens = self.to_string_tokens(topk.indices)
        token_probs = {}
        for token, prob in zip(string_tokens, topk.values):
            if token not in token_probs:
                token_probs[token] = prob.item()
        return token_probs
        # return {
        #     token: prob.item() for token, prob in zip(string_tokens, topk.values)
        # }

    def get_module_from_string(self, component: str):
        r"""
        Return a module from the model given the string of the module.

        Args:
            component (str): the string of the module

        Returns:
            module (torch.nn.Module): the module of the model

        Examples:
            >>> model.get_module_from_string("model.layers[0].self_attn")
            BertAttention(...)
        """
        return self.hf_model.retrieve_modules_from_names(component)

    def set_hooks(self, hooks: List[Dict[str, Any]]):
        r"""
        Set the hooks in the model

        Args:
            hooks (list[dict]): list of dictionaries with the component and the intervention to perform in the forward pass of the model

        Returns:
            hook_handlers (list): list of hook handlers
        """

        if len(hooks) == 0:
            return []

        hook_handlers = []
        for hook in hooks:
            component = hook["component"]
            hook_function = hook["intervention"]

            # get the last module string (.input or .output) and remove it from the component string
            last_module = component.split(".")[-1]
            # now remove the last module from the component string
            component = component[: -len(last_module) - 1]
            # check if the component exists in the model
            try:
                self.assert_module_exists(component)
            except ValueError as e:
                self.logger.warning(
                    f"Error: {e}. Probably the module {component} do not exists in the model. If the module is the attention_matrix_hook, try callig HookedModel.set_custom_hooks() or setting attn_implementation == 'custom_eager'.  Now we will skip the hook for the component {component}",
                    std_out=True,
                )
                continue
            if last_module == "input":
                hook_handlers.append(
                    get_module_by_path(
                        self.hf_model, component
                    ).register_forward_pre_hook(
                        partial(hook_function, output=None), with_kwargs=True
                    )
                )
            elif last_module == "output":
                hook_handlers.append(
                    get_module_by_path(self.hf_model, component).register_forward_hook(
                        hook_function, with_kwargs=True
                    )
                )

        return hook_handlers

    def remove_hooks(self, hook_handlers):
        """
        Remove all the hooks from the model
        """
        for hook_handler in hook_handlers:
            hook_handler.remove()

    @torch.no_grad()
    def generate(
        self,
        inputs,
        generation_config: Optional[GenerationConfig] = None,
        target_token_positions: Optional[List[str]] = None,
        return_text: bool = False,
        **kwargs,
    ) -> ActivationCache:
        r"""
        __WARNING__: This method could be buggy in the return dict of the output. Pay attention!

        Generate new tokens using the model and the inputs passed as argument
        Args:
            inputs (dict): dictionary with the inputs of the model {"input_ids": ..., "attention_mask": ..., "pixel_values": ...}
            generation_config (Optional[GenerationConfig]): original hf dataclass with the generation configuration
            **kwargs: additional arguments to control hooks generation (i.e. ablation_queries, patching_queries)
        Returns:
            output (ActivationCache): dictionary with the output of the model

        Examples:
            >>> inputs = {"input_ids": torch.tensor([[101, 1234, 1235, 102]]), "attention_mask": torch.tensor([[1, 1, 1, 1]])}
            >>> model.generate(inputs)
            {'sequences': tensor([[101, 1234, 1235, 102]])}
        """
        # Initialize cache for logits
        # TODO FIX THIS. IT is not general and it is not working
        # raise NotImplementedError("This method is not working. It needs to be fixed")
        hook_handlers = None
        if target_token_positions is not None:
            string_tokens = self.to_string_tokens(
                self.input_handler.get_input_ids(inputs).squeeze()
            )
            token_index, token_dict = TokenIndex(
                self.config.model_name, pivot_positions=None
            ).get_token_index(tokens=[], string_tokens=string_tokens, return_type="all")
            assert isinstance(token_index, list), "Token index must be a list"
            assert isinstance(token_dict, dict), "Token dict must be a dict"
            hooks = self.create_hooks(
                inputs=inputs,
                token_dict=token_dict,
                token_index=token_index,
                cache=ActivationCache(),
                **kwargs,
            )
            hook_handlers = self.set_hooks(hooks)

        inputs = self.input_handler.prepare_inputs(inputs, self.first_device)

        output = self.hf_model.generate(
            **inputs,  # type: ignore
            generation_config=generation_config,
            output_scores=False,  # type: ignore
        )
        if hook_handlers:
            self.remove_hooks(hook_handlers)
        if return_text:
            return self.hf_tokenizer.decode(output[0], skip_special_tokens=True)  # type: ignore
        return output  # type: ignore

    @torch.no_grad()
    def extract_cache(
        self,
        dataloader,
        target_token_positions: List[str],
        batch_saver: Callable = lambda x: None,
        move_to_cpu_after_forward: bool = True,
        # save_other_batch_elements: bool = False,
        **kwargs,
    ):
        r"""
        Method to extract the activations of the model from a specific dataset. Compute a forward pass for each batch of the dataloader and save the activations in the cache.

        Args:
            dataloader (iterable): dataloader with the dataset. Each element of the dataloader must be a dictionary that contains the inputs that the model expects (input_ids, attention_mask, pixel_values ...)
            extracted_token_position (list[str]): list of tokens to extract the activations from (["last", "end-image", "start-image", "first"])
            batch_saver (Callable): function to save in the cache the additional element from each elemtn of the batch (For example, the labels of the dataset)
            move_to_cpu_after_forward (bool): if True, move the activations to the cpu right after the any forward pass of the model
            **kwargs: additional arguments to control hooks generation, basically accept any argument handled by the `.forward` method (i.e. ablation_queries, patching_queries, extract_resid_in)

        Returns:
            final_cache: dictionary with the activations of the model. The keys are the names of the activations and the values are the activations themselve

        Examples:
            >>> dataloader = [{"input_ids": torch.tensor([[101, 1234, 1235, 102]]), "attention_mask": torch.tensor([[1, 1, 1, 1]]), "labels": torch.tensor([1])}, ...]
            >>> model.extract_cache(dataloader, extracted_token_position=["last"], batch_saver=lambda x: {"labels": x["labels"]})
            {'resid_out_0': tensor([[[0.1, 0.2, 0.3, 0.4]]], grad_fn=<CopyBackwards>), 'labels': tensor([1]), 'mapping_index': {'last': [0]}}
        """

        self.logger.info("Extracting cache", std_out=True)

        # get the function to save in the cache the additional element from the batch sime

        self.logger.info("Forward pass started", std_out=True)
        all_cache = ActivationCache()  # a list of dictoionaries, each dictionary contains the activations of the model for a batch (so a dict of tensors)
        attn_pattern = (
            ActivationCache()
        )  # Initialize the dictionary to hold running averages

        example_dict = {}
        n_batches = 0  # Initialize batch counter

        for batch in tqdm(dataloader, total=len(dataloader), desc="Extracting cache:"):
            # log_memory_usage("Extract cache - Before batch")
            # tokens, others = batch
            # inputs = {k: v.to(self.first_device) for k, v in tokens.items()}

            # get input_ids, attention_mask, and if available, pixel_values from batch (that is a dictionary)
            # then move them to the first device
            inputs = self.input_handler.prepare_inputs(batch, self.first_device)
            others = {k: v for k, v in batch.items() if k not in inputs}

            cache = self.forward(
                inputs,
                target_token_positions=target_token_positions,
                pivot_positions=batch.get("pivot_positions", None),
                external_cache=attn_pattern,
                batch_idx=n_batches,
                **kwargs,
            )
            # possible memory leak from here -___--------------->
            additional_dict = batch_saver(others)
            if additional_dict is not None:
                # cache = {**cache, **additional_dict}
                cache.update(additional_dict)

            if move_to_cpu_after_forward:
                cache.cpu()

            n_batches += 1  # Increment batch counter# Process and remove "pattern_" keys from cache
            all_cache.cat(cache)

            del cache
            inputs = self.input_handler.prepare_inputs(batch, "cpu")
            del inputs
            torch.cuda.empty_cache()

        self.logger.info(
            "Forward pass finished - started to aggregate different batch", std_out=True
        )
        all_cache.update(attn_pattern)
        all_cache["example_dict"] = example_dict
        self.logger.info("Aggregation finished", std_out=True)

        torch.cuda.empty_cache()
        return all_cache

    @torch.no_grad()
    def compute_patching(
        self,
        target_token_positions: List[str],
        # counterfactual_dataset,
        base_dataloader,
        target_dataloader,
        patching_query=[
            {
                "patching_elem": "@end-image",
                "layers_to_patch": [1, 2, 3, 4],
                "activation_type": "resid_in_{}",
            }
        ],
        base_dictonary_idxs: Optional[List[List[int]]] = None,
        target_dictonary_idxs: Optional[List[List[int]]] = None,
        return_logit_diff: bool = False,
        batch_saver: Callable = lambda x: None,
        **kwargs,
    ) -> ActivationCache:
        r"""
        Method for activation patching. This substitutes the activations of the model
        with the activations of the counterfactual dataset.

        It performs three forward passes:
        1. Forward pass on the base dataset to extract the activations of the model (cat).
        2. Forward pass on the target dataset to extract clean logits (dog)
        [to compare against the patched logits].
        3. Forward pass on the target dataset to patch (cat) into (dog)
        and extract the patched logits.

        Args:
            target_token_positions (list[str]): List of tokens to extract the activations from.
            base_dataloader (torch.utils.data.DataLoader): Dataloader with the base dataset. (dataset where we sample the activations from)
            target_dataloader (torch.utils.data.DataLoader): Dataloader with the target dataset. (dataset where we patch the activations)
            patching_query (list[dict]): List of dictionaries with the patching queries. Each dictionary must have the keys "patching_elem", "layers_to_patch" and "activation_type". The "patching_elem" is the token to patch, the "layers_to_patch" is the list of layers to patch and the "activation_type" is the type of the activation to patch. The activation type must be one of the following: "resid_in_{}", "resid_out_{}", "resid_mid_{}", "attn_in_{}", "attn_out_{}", "values_{}". The "{}" will be replaced with the layer index.
            base_dictonary_idxs (list[list[int]]): List of list of integers with the indexes of the tokens in the dictonary that we are interested in. It's useful to extract the logit difference between the clean logits and the patched logits.
            target_dictonary_idxs (list[list[int]]): List of list of integers with the indexes of the tokens in the dictonary that we are interested in. It's useful to extract the logit difference between the clean logits and the patched logits.
            return_logit_diff (bool): If True, it will return the logit difference between the clean logits and the patched logits.


        Returns:
            final_cache (ActivationCache): dictionary with the activations of the model. The keys are the names of the activations and the values are the activations themselve

        Examples:
            >>> model.compute_patching(
            >>>     target_token_positions=["end-image", " last"],
            >>>     base_dataloader=base_dataloader,
            >>>     target_dataloader=target_dataloader,
            >>>     base_dictonary_idxs=base_dictonary_idxs,
            >>>     target_dictonary_idxs=target_dictonary_idxs,
            >>>     patching_query=[
            >>>         {
            >>>             "patching_elem": "@end-image",
            >>>             "layers_to_patch": [1, 2, 3, 4],
            >>>             "activation_type": "resid_in_{}",
            >>>         }
            >>>     ],
            >>>     return_logit_diff=False,
            >>>     batch_saver=lambda x: None,
            >>> )
            >>> print(final_cache)
            {
                "resid_out_0": tensor of shape [batch, seq_len, hidden_size] with the activations of the residual stream of layer 0
                "resid_mid_0": tensor of shape [batch, seq_len, hidden_size] with the activations of the residual stream of layer 0
                ....
                "logit_diff_variation": tensor of shape [batch] with the logit difference variation
                "logit_diff_in_clean": tensor of shape [batch] with the logit difference in the clean logits
                "logit_diff_in_patched": tensor of shape [batch] with the logit difference in the patched logits
            }
        """
        self.logger.info("Computing patching", std_out=True)

        self.logger.info("Forward pass started", std_out=True)
        self.logger.info(
            f"Patching elements: {[q['patching_elem'] for q in patching_query]} at {[query['activation_type'][:-3] for query in patching_query]}",
            std_out=True,
        )

        # get a random number in the range of the dataset to save a random batch
        all_cache = ActivationCache()
        # for each batch in the dataset
        for index, (base_batch, target_batch) in tqdm(
            enumerate(zip(base_dataloader, target_dataloader)),
            desc="Computing patching on the dataset:",
            total=len(base_dataloader),
        ):
            torch.cuda.empty_cache()
            inputs = self.input_handler.prepare_inputs(base_batch, self.first_device)

            # set the right arguments for extract the patching activations
            activ_type = [query["activation_type"][:-3] for query in patching_query]

            args = {
                "extract_resid_out": True,
                "extract_resid_in": False,
                "extract_resid_mid": False,
                "extract_attn_in": False,
                "extract_attn_out": False,
                "extract_head_values": False,
                "extract_head_out": False,
                "extract_avg_attn_pattern": False,
                "extract_avg_values_vectors_projected": False,
                "extract_head_values_projected": False,
                "extract_avg": False,
                "ablation_queries": None,
                "patching_queries": None,
                "external_cache": None,
                "attn_heads": "all",
                "batch_idx": None,
                "move_to_cpu": False,
            }

            if "resid_in" in activ_type:
                args["extract_resid_in"] = True
            if "resid_out" in activ_type:
                args["extract_resid_out"] = True
            if "resid_mid" in activ_type:
                args["extract_intermediate_states"] = True
            if "attn_in" in activ_type:
                args["extract_attn_in"] = True
            if "attn_out" in activ_type:
                args["extract_attn_out"] = True
            if "values" in activ_type:
                args["extract_head_values"] = True
            # other cases

            # first forward pass to extract the base activations
            base_cache = self.forward(
                inputs=inputs,
                target_token_positions=target_token_positions,
                pivot_positions=base_batch.get("pivot_positions", None),
                extraction_config=ExtractionConfig(**args),
                ablation_queries=args["ablation_queries"],
                patching_queries=args["patching_queries"],
                external_cache=args["external_cache"],
                batch_idx=args["batch_idx"],
                move_to_cpu=args["move_to_cpu"],
            )

            # extract the target activations
            target_inputs = self.input_handler.prepare_inputs(
                target_batch, self.first_device
            )

            requested_position_to_extract = []
            for query in patching_query:
                query["patching_activations"] = base_cache
                if (
                    query["patching_elem"].split("@")[1]
                    not in requested_position_to_extract
                ):
                    requested_position_to_extract.append(
                        query["patching_elem"].split("@")[1]
                    )
                query["base_activation_index"] = base_cache["mapping_index"][
                    query["patching_elem"].split("@")[1]
                ]

            # second forward pass to extract the clean logits
            target_clean_cache = self.forward(
                target_inputs,
                target_token_positions=requested_position_to_extract,
                pivot_positions=target_batch.get("pivot_positions", None),
                # move_to_cpu=True,
            )

            # merge requested_position_to_extract with extracted_token_positio
            # third forward pass to patch the activations
            target_patched_cache = self.forward(
                target_inputs,
                target_token_positions=list(
                    set(target_token_positions + requested_position_to_extract)
                ),
                pivot_positions=target_batch.get("pivot_positions", None),
                patching_queries=patching_query,
                **kwargs,
            )

            if return_logit_diff:
                if base_dictonary_idxs is None or target_dictonary_idxs is None:
                    raise ValueError(
                        "To compute the logit difference, you need to pass the base_dictonary_idxs and the target_dictonary_idxs"
                    )
                self.logger.info("Computing logit difference", std_out=True)
                # get the target tokens (" cat" and " dog")
                base_targets = base_dictonary_idxs[index]
                target_targets = target_dictonary_idxs[index]

                # compute the logit difference
                result_diff = logit_diff(
                    base_label_tokens=[s for s in base_targets],
                    target_label_tokens=[c for c in target_targets],
                    target_clean_logits=target_clean_cache["logits"],
                    target_patched_logits=target_patched_cache["logits"],
                )
                target_patched_cache["logit_diff_variation"] = result_diff[
                    "diff_variation"
                ]
                target_patched_cache["logit_diff_in_clean"] = result_diff[
                    "diff_in_clean"
                ]
                target_patched_cache["logit_diff_in_patched"] = result_diff[
                    "diff_in_patched"
                ]

            # compute the KL divergence
            result_kl = kl_divergence_diff(
                base_logits=base_cache["logits"],
                target_clean_logits=target_clean_cache["logits"],
                target_patched_logits=target_patched_cache["logits"],
            )
            for key, value in result_kl.items():
                target_patched_cache[key] = value

            target_patched_cache["base_logits"] = base_cache["logits"]
            target_patched_cache["target_clean_logits"] = target_clean_cache["logits"]
            # rename logits to target_patched_logits
            target_patched_cache["target_patched_logits"] = target_patched_cache[
                "logits"
            ]
            del target_patched_cache["logits"]

            target_patched_cache.cpu()

            # all_cache.append(target_patched_cache)
            all_cache.cat(target_patched_cache)

        self.logger.info(
            "Forward pass finished - started to aggregate different batch", std_out=True
        )
        # final_cache = aggregate_cache_efficient(all_cache)

        self.logger.info("Aggregation finished", std_out=True)
        return all_cache
