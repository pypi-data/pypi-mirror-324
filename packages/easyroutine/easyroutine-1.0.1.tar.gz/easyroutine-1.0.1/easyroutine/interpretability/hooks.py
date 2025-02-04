# Description: This file contains the hooks used to extract the activations of the model
import torch
from copy import deepcopy
import pandas as pd
from typing import List, Callable, Union
from einops import rearrange, einsum
from easyroutine.interpretability.utils import repeat_kv, get_module_by_path
from easyroutine.interpretability.activation_cache import ActivationCache
from functools import partial
import re
import torch.nn as nn
import einops


def process_args_kwargs_output(args, kwargs, output):
    if output is not None:
        if isinstance(output, tuple):
            b = output[0]
        else:
            b = output
    else:
        if len(args) > 0:
            b = args[0]
        else:
            candidate_keys = ["hidden_states"]
            for key in candidate_keys:
                if key in kwargs:
                    b = kwargs[key]
                    break
    return b  # type:ignore


# 2. Retrieving the module


def create_dynamic_hook(pyvene_hook: Callable, **kwargs):
    r"""
    DEPRECATED: pyvene is not used anymore.
    This function is used to create a dynamic hook. It is a wrapper around the pyvene_hook function.
    """
    partial_hook = partial(pyvene_hook, **kwargs)

    def wrap(*args, **kwargs):
        return partial_hook(*args, **kwargs)

    return wrap


def embed_hook(module, input, output, cache, cache_key):
    r"""
    Hook function to extract the embeddings of the tokens. It will save the embeddings in the cache (a global variable out the scope of the function)
    """
    if output is None:
        b = input[0]
    else:
        b = output
    cache[cache_key] = b.data.detach().clone()
    return b


# Define a hook that saves the activations of the residual stream
def save_resid_hook(
    module,
    args,
    kwargs,
    output,
    cache: ActivationCache,
    cache_key,
    token_index,
    avg: bool = False,
):
    r"""
    It save the activations of the residual stream in the cache. It will save the activations in the cache (a global variable out the scope of the function)
    """
    b = process_args_kwargs_output(args, kwargs, output)

    # slice the tensor to get the activations of the token we want to extract
    cache[cache_key] = b.data.detach().clone()[..., token_index, :]

    if avg:
        cache[cache_key] = torch.mean(cache[cache_key], dim=-2, keepdim=True)


def query_key_value_hook(
    module,
    args,
    kwargs,
    output,
    cache: ActivationCache,
    cache_key,
    token_index,
    layer,
    head_dim,
    num_key_value_groups:int,
    head: Union[str, int] = "all",
    avg: bool = False,
):
    r"""
    Same as save_resid_hook but for the query, key and value vectors, it just have a reshape to have the head dimension.
    """
    b = process_args_kwargs_output(args, kwargs, output)
    input_shape = b.shape[:-1]
    hidden_shape = (*input_shape, -1, head_dim)
    b = b.view(hidden_shape).transpose(1, 2)
    # cache[cache_key] = b.data.detach().clone()[..., token_index, :]

    info_string = "Shape: batch seq_len d_head"
 

    heads = [idx for idx in range(b.size(1))] if head == "all" else [head]
    for head_idx in heads:
        # compute group index
        group_idx = head_idx // (b.size(1) // num_key_value_groups)
        if "values_" in cache_key or "keys_" in cache_key:
            cache.add_with_info(
                f"{cache_key}L{layer}H{head_idx}",
                b.data.detach().clone()[:, group_idx, token_index, :],
                info_string,
            )
        else:
            cache.add_with_info(
                f"{cache_key}L{layer}H{head_idx}",
                b.data.detach().clone()[:, head_idx, token_index, :],
                info_string,
            )


def avg_hook(
    module,
    args,
    kwargs,
    output,
    cache,
    cache_key,
    last_image_idx,
    end_image_idx,
):
    r"""
    It save the activations of the residual stream in the cache. It will save the activations in the cache (a global variable out the scope of the function)
    """
    b = process_args_kwargs_output(args, kwargs, output)

    img_avg = torch.mean(
        b.data.detach().clone()[:, 1 : last_image_idx + 1, :],
        dim=1,
    )
    text_avg = torch.mean(b.data.detach().clone()[:, end_image_idx:, :], dim=1)
    all_avg = torch.mean(b.data.detach().clone()[:, :, :], dim=1)

    cache[f"avg_{cache_key}"] = torch.cat(
        [img_avg.unsqueeze(1), text_avg.unsqueeze(1), all_avg.unsqueeze(1)], dim=1
    )


def head_out_hook(
    module,
    args,
    kwargs,
    output,
    cache,
    cache_key,
    token_index,
    layer,
    num_heads,
    head_dim,
    o_proj_weight,
    o_proj_bias,
    head: Union[str, int] = "all",
    avg: bool = False,
):
    b = process_args_kwargs_output(args, kwargs, output)
    
    bsz, seq_len, hidden_size = b.shape
    b = b.view(bsz, seq_len, num_heads, head_dim)
    # reshape the weights to have the head dimension
    o_proj_weight = einops.rearrange(
        o_proj_weight,
        "(num_heads head_dim) d_model -> num_heads head_dim d_model",
        num_heads=num_heads,
        head_dim=head_dim
    )
    
    # apply the projection
    projected_values = einsum(
        b,
        o_proj_weight,
        "batch seq_len num_head d_head, num_head head_dim d_model -> batch seq_len num_head d_model",
    )
    
    if o_proj_bias is not None:
        projected_values = projected_values + o_proj_bias
        
    # slice for token index
    projected_values = projected_values[:, token_index, :,:]
    
    if avg:
        projected_values = torch.mean(projected_values, dim=-2, keepdim=True)
    
    heads = [idx for idx in range(num_heads)] if head == "all" else [head]
    for head_idx in heads:
        cache.add_with_info(
            f"{cache_key}L{layer}H{head_idx}",
            projected_values[:, :, int(head_idx),:],
            "Shape: batch selected_inputs_ids_len, d_model",
        )
        # cache[f"{cache_key}L{layer}H{head_idx}"] = projected_values[:,:, int(head_idx),:] 
        

def zero_ablation(tensor):
    r"""
    Set the attention values to zero
    """
    return torch.zeros_like(tensor)


# b.copy_(attn_matrix)
def ablate_attn_mat_hook(
    module,
    args,
    kwargs,
    output,
    ablation_queries: pd.DataFrame,
):
    r"""
    Hook function to ablate the tokens in the attention
    mask. It will set to 0 the value vector of the
    tokens to ablate
    """
    # Get the shape of the attention matrix
    b = process_args_kwargs_output(args, kwargs, output)
    batch_size, num_heads, seq_len_q, seq_len_k = b.shape

    q_positions = ablation_queries["queries"].iloc[0]

    # Used during generation
    if seq_len_q < len(q_positions):
        q_positions = 0

    k_positions = ablation_queries["keys"].iloc[0]

    # Create boolean masks for queries and keys
    q_mask = torch.zeros(seq_len_q, dtype=torch.bool, device=b.device)
    q_mask[q_positions] = True  # Set positions to True

    k_mask = torch.zeros(seq_len_k, dtype=torch.bool, device=b.device)
    k_mask[k_positions] = True  # Set positions to TrueW

    # Create a 2D mask using outer product
    head_mask = torch.outer(q_mask, k_mask)  # Shape: (seq_len_q, seq_len_k)

    # Expand mask to match the dimensions of the attention matrix
    # Shape after expand: (batch_size, num_heads, seq_len_q, seq_len_k)
    head_mask = (
        head_mask.unsqueeze(0).unsqueeze(0).expand(batch_size, num_heads, -1, -1)
    )

    # Apply the ablation function directly to the attention matrix
    b[head_mask] = zero_ablation(b[head_mask])
    return b


def ablate_tokens_hook_flash_attn(
    module,
    args,
    kwargs,
    output,
    ablation_queries: pd.DataFrame,
    num_layers: int = 32,
):
    r"""
    same of ablate_tokens_hook but for flash attention. This apply the ablation on the values vectors instead of the attention mask
    """
    b = process_args_kwargs_output(args, kwargs, output)
    batch_size, seq, d_model = b.shape
    if seq == 1:
        return b
    values = b.clone().data
    device = values.device

    ablation_queries.reset_index(
        drop=True, inplace=True
    )  # Reset index to avoid problems with casting to tensor
    head_indices = torch.tensor(
        ablation_queries["head"], dtype=torch.long, device=device
    )
    pos_indices = torch.tensor(
        ablation_queries["keys"], dtype=torch.long, device=device
    )
    # if num_layers != len(head_indices) or not torch.all(pos_indices == pos_indices[0]) :
    #     raise ValueError("Flash attention ablation should be done on all heads at the same layer and at the same token position")
    # if seq < pos_indices[0]:
    #     # during generation the desired value vector has already been ablated
    #     return b
    pos_indices = pos_indices[0]
    # Use advanced indexing to set the specified slices to zero
    values[..., pos_indices, :] = 0

    b.copy_(values)

    #!!dirty fix

    return b


def ablate_heads_hook(
    module,
    args,
    kwargs,
    output,
    ablation_queries: pd.DataFrame,
):
    r"""
    Hook function to ablate the heads in the attention
    mask. It will set to 0 the output of the heads to
    ablate
    """
    b = process_args_kwargs_output(args, kwargs, output)
    attention_matrix = b.clone().data

    for head in ablation_queries["head"]:
        attention_matrix[0, head, :, :] = 0

    b.copy_(attention_matrix)
    return b


def ablate_pos_keep_self_attn_hook(
    module,
    args,
    kwargs,
    output,
    ablation_queries: pd.DataFrame,
):
    r"""
    Hook function to ablate the tokens in the attention
    mask but keeping the self attn weigths.
    It will set to 0 the row of tokens to ablate except for
    the las position
    """
    b = process_args_kwargs_output(args, kwargs, output)
    Warning("This function is deprecated. Use ablate_attn_mat_hook instead")
    attn_matrix = b.data
    # initial_shape = attn_matrix.shape

    for head, pos in zip(
        ablation_queries["head"], ablation_queries["pos_token_to_ablate"]
    ):
        attn_matrix[0, head, pos, :-1] = 0

    b.copy_(attn_matrix)

    return b


def ablate_tokens_hook(*args, **kwargs):
    raise NotImplementedError(
        "This function will be discaderd keeping only for backward compatibility"
    )


def ablate_images_hook(*args, **kwargs):
    raise NotImplementedError(
        "This function will be discaderd keeping only for backward compatibility"
    )


def ablate_image_image_hook(*args, **kwargs):
    raise NotImplementedError(
        "This function will be discaderd keeping only for backward compatibility"
    )


def projected_value_vectors_head(
    module,
    args,
    kwargs,
    output,
    layer,
    cache,
    token_index,
    num_attention_heads: int,
    num_key_value_heads: int,
    hidden_size: int,
    d_head: int,
    out_proj_weight,
    out_proj_bias,
    head: Union[str, int] = "all",
    act_on_input=False,
    expand_head: bool = True,
    avg=False,
):
    r"""
    Hook function to extract the values vectors of the heads. It will extract the values vectors and then project them with the final W_O projection
    As the other hooks, it will save the activations in the cache (a global variable out the scope of the function)

    Args:
        b: the input of the hook function. It's the output of the values vectors of the heads
        s: the state of the hook function. It's the state of the model
        layer: the layer of the model
        head: the head of the model. If "all" is passed, it will extract all the heads of the layer
        expand_head: bool to expand the head dimension when extracting the values vectors and the attention pattern. If true, in the cache we will have a key for each head, like "value_L0H0", "value_L0H1", ...
                        while if False, we will have only one key for each layer, like "value_L0" and the dimension of the head will be taken into account in the tensor.

    """
    # first get the values vectors
    b = process_args_kwargs_output(args, kwargs, output)

    values = b.data.detach().clone()  # (batch, num_heads,seq_len, head_dim)

    # reshape the values vectors to have a separate dimension for the different heads
    values = rearrange(
        values,
        "batch seq_len (num_key_value_heads d_heads) -> batch num_key_value_heads seq_len d_heads",
        num_key_value_heads=num_key_value_heads,
        d_heads=d_head,
    )

    #        "batch seq_len (num_key_value_heads d_heads) -> batch seq_len num_key_value_heads d_heads",

    values = repeat_kv(values, num_attention_heads // num_key_value_heads)

    values = rearrange(
        values,
        "batch num_head seq_len d_model -> batch seq_len num_head d_model",
    )

    # reshape in order to get the blocks for each head
    out_proj_weight = out_proj_weight.t().view(
        num_attention_heads,
        d_head,
        hidden_size,
    )

    # apply bias if present (No in Chameleon)
    if out_proj_bias is not None:
        out_proj_bias = out_proj_bias.view(1, 1, 1, hidden_size)

    # apply the projection for each head
    projected_values = einsum(
        values,
        out_proj_weight,
        "batch seq_len num_head d_head, num_head d_head d_model -> batch seq_len num_head d_model",
    )
    if out_proj_bias is not None:
        projected_values = projected_values + out_proj_bias

    # rearrange the tensor to have dimension that we like more
    projected_values = rearrange(
        projected_values,
        "batch seq_len num_head d_model -> batch num_head seq_len d_model",
    )

    # slice for token index
    projected_values = projected_values[:, :, token_index, :]

    if avg:
        projected_values = torch.mean(projected_values, dim=-1, keepdim=True)

    # post-process the values vectors
    if head == "all":
        for head_idx in range(num_attention_heads):
            cache[f"projected_value_L{layer}H{head_idx}"] = projected_values[
                :, head_idx
            ]
    else:
        cache[f"projected_value_L{layer}H{head}"] = projected_values[:, int(head)]


def avg_attention_pattern_head(
    module,
    args,
    kwargs,
    output,
    token_index,
    layer,
    attn_pattern_current_avg,
    batch_idx,
    cache,
    avg: bool = False,
    extract_avg_value: bool = False,
    act_on_input=False,
):
    """
    Hook function to extract the average attention pattern of the heads. It will extract the attention pattern and then average it.
    As the other hooks, it will save the activations in the cache (a global variable out the scope of the function)

    Args:
        - b: the input of the hook function. It's the output of the attention pattern of the heads
        - s: the state of the hook function. It's the state of the model
        - layer: the layer of the model
        - head: the head of the model
        - attn_pattern_current_avg: the current average attention pattern
    """
    # first get the attention pattern
    b = process_args_kwargs_output(args, kwargs, output)

    attn_pattern = b.data.detach().clone()  # (batch, num_heads,seq_len, seq_len)
    # attn_pattern = attn_pattern.to(torch.float32)
    num_heads = attn_pattern.size(1)
    for head in range(num_heads):
        key = f"avg_pattern_L{layer}H{head}"
        if key not in attn_pattern_current_avg:
            attn_pattern_current_avg[key] = attn_pattern[:, head, token_index][
                :, :, token_index
            ]
        else:
            attn_pattern_current_avg[key] += (
                attn_pattern[:, head, token_index][:, :, token_index]
                - attn_pattern_current_avg[key]
            ) / (batch_idx + 1)
        attn_pattern_current_avg[key] = attn_pattern_current_avg[key]
        # var_key = f"M2_pattern_L{layer}H{head}"
        # if var_key not in attn_pattern_current_avg:
        #     attn_pattern_current_avg[var_key] = torch.zeros_like(attn_pattern[:, head])
        # attn_pattern_current_avg[var_key] = attn_pattern_current_avg[var_key] + (attn_pattern[:, head] - attn_pattern_current_avg[key]) * (attn_pattern[:, head] - attn_pattern_current_avg[var_key])

        if extract_avg_value:
            value_key = f"projected_value_L{layer}H{head}"
            try:
                values = cache[value_key]
            except KeyError:
                print(f"Values not found for {value_key}")
                return
            # get the attention pattern for the values
            value_norm = torch.norm(values, dim=-1)

            norm_matrix = (
                value_norm.unsqueeze(1).expand_as(attn_pattern[:, head]).transpose(1, 2)
            )

            norm_matrix = norm_matrix * attn_pattern[:, head]

            if value_key not in attn_pattern_current_avg:
                attn_pattern_current_avg[value_key] = norm_matrix[..., token_index, :]
            else:
                attn_pattern_current_avg[value_key] += (
                    norm_matrix[..., token_index, :]
                    - attn_pattern_current_avg[value_key]
                ) / (batch_idx + 1)

            # remove values from cache
            del cache[value_key]


def attention_pattern_head(
    module,
    args,
    kwargs,
    output,
    token_index,
    layer,
    cache,
    head: Union[str, int] = "all",
    act_on_input=False,
):
    """
    Hook function to extract the attention pattern of the heads. It will extract the attention pattern.
    As the other hooks, it will save the activations in the cache (a global variable out the scope of the function)

    Args:
        - b: the input of the hook function. It's the output of the attention pattern of the heads
        - s: the state of the hook function. It's the state of the model
        - layer: the layer of the model
        - head: the head of the model
        - expand_head: bool to expand the head dimension when extracting the values vectors and the attention pattern. If true, in the cache we will have a key for each head, like "pattern_L0H0", "pattern_L0H1", ...
                        while if False, we will have only one key for each layer, like "pattern_L0" and the dimension of the head will be taken into account in the tensor.

    """
    # first get the attention pattern
    b = process_args_kwargs_output(args, kwargs, output)

    attn_pattern = b.data.detach().clone()  # (batch, num_heads,seq_len, seq_len)

    if head == "all":
        for head_idx in range(attn_pattern.size(1)):
            key = f"pattern_L{layer}H{head_idx}"
            cache[key] = attn_pattern[:, head_idx, token_index][:, :, token_index]
    else:
        cache[f"pattern_L{layer}H{head}"] = attn_pattern[:, head, token_index][
            :, :, token_index
        ]
