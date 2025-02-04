##########################################################################
##  HugigngFace Model Config Parser
##
##  Authors:  Junsoo    Kim   ( js.kim@hyperaccel.ai        )
##  Version:  0.0.10
##  Date:     2025-01-15      ( v0.0.10, init               )
##
##########################################################################

from typing import Union, List
from transformers import AutoModelForCausalLM

from llm_probe.models.gpt2 import cfg as gpt2_cfg
from llm_probe.models.llama import cfg as llama_cfg

##########################################################################
## Function
##########################################################################


def config(model: AutoModelForCausalLM, key: str) -> Union[int, float, str, List[int]]:
    # Get the model architecture
    architectures = model.config.architectures

    # Check if the model architecture is in the configuration table
    if "GPT2LMHeadModel" in architectures:
        cfg = gpt2_cfg
    elif "LlamaForCausalLM" in architectures:
        cfg = llama_cfg
    else:
        err_msg = f"Unsupported model architecture: {architectures}"
        raise NotImplementedError(err_msg)

    # Check if the key is in the configuration table
    if key not in cfg:
        err_msg = f"Invalid key: {key} in this architecture"
        raise ValueError(err_msg)
    # Check if the key is in the model configuration
    if not hasattr(model.config, cfg[key]):
        err_msg = f"Invalid key: {key} in this model"
        raise ValueError(err_msg)
    return getattr(model.config, cfg[key])


##########################################################################
