##########################################################################
##  Utility functions for LLM Probe
##
##  Authors:  Junsoo    Kim   ( js.kim@hyperaccel.ai        )
##  Version:  0.0.1
##  Date:     2024-11-05      ( v0.0.1, init                )
##
##########################################################################

from typing import List

import torch

from llm_probe.logger import get_logger

##########################################################################
## Definitions
##########################################################################

# Logger for llm probe framework
logger = get_logger(__name__)

# Default word size for print_hex
DEFAULT_WORD_SIZE = 64

##########################################################################
## Functions
##########################################################################


# Print all valid module name
def print_all_module_name(model: torch.nn.Module) -> None:
    # Print all modules with for loop
    for name, _ in model.named_modules():
        print(name)  # noqa: T201


# Get all valid module class
def get_all_module_list(model: torch.nn.Module) -> List[torch.nn.Module]:
    # Get all modules with for loop
    module_list = []
    for _, module in model.named_modules():
        module_list.append(module)
    return module_list


# Print tensor data with hexa-decimal format
def print_hex(data: torch.Tensor, word_size: int = DEFAULT_WORD_SIZE) -> None:
    data = data.contiguous().flatten()
    numel_word = word_size // data.element_size()
    # Add zero padding to align the data
    if data.numel() % numel_word != 0:
        zero_padding = numel_word - (data.numel() % numel_word)
        zeros = torch.zeros(zero_padding, dtype=data.dtype, device=data.device)
        data = torch.cat([data, zeros], dim=0)
    # Reshape the tensor data
    data = data.reshape(-1, numel_word)
    # Print header
    n_line = (word_size * 2) + 12
    print("-" * n_line)  # noqa: T201
    # Print the hexa-decimal format line by line
    for i in range(data.shape[0]):
        # Byte address
        print(f"0x{i * word_size:08x}:", end=" ")  # noqa: T201
        # Byte data
        print(data[i].detach().numpy().tobytes().hex())  # noqa: T201
    # Print footer
    print("-" * n_line)  # noqa: T201


##########################################################################
