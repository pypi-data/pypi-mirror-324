##########################################################################
##  HugigngFace Model Prober
##
##  Authors:  Junsoo    Kim   ( js.kim@hyperaccel.ai        )
##  Version:  0.0.1
##  Date:     2024-11-05      ( v0.0.1, init                )
##
##########################################################################

from typing import Any, Callable, Optional, Tuple, Union, List

import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer

from llm_probe.logger import get_logger
from llm_probe.utils import get_all_module_list
from llm_probe.models import config

##########################################################################
## Definitions
##########################################################################

# Logger for llm probe framework
logger = get_logger(__name__)

##########################################################################
## Class
##########################################################################


class PTModelProbe:
    # Constructor
    def __init__(self, model: nn.Module) -> None:
        # Store the model
        self.model = model

        # Initialize the hook list
        self.hook_list: dict[nn.Module, torch.utils.hooks.RemovableHandle] = {}
        # Intermediate intermediate input/output
        self.intermediate_input: dict[nn.Module, torch.Tensor] = {}
        self.intermediate_output: dict[nn.Module, torch.Tensor] = {}

    # Set hook for intermediate data
    def set_hook(self, module: Union[str, nn.Module]) -> None:
        # For input tensor, we need to register hook function
        self.register_hook(module, self._hook_fn)

    # Set multiple hooks for intermediate data
    def set_hooks(self, module_list: list[Union[str, nn.Module]]) -> None:
        for module in module_list:
            self.set_hook(module)

    # Get intermediate input
    def get_intermediate_input(
        self, module: Union[str, nn.Module], dtype: Optional[torch.dtype] = None
    ) -> torch.Tensor:
        # Check the module type
        module = self._verify_module(module)
        # Check if the intermediate input exists
        if self.intermediate_input.get(module, None) is None:
            logger.error(f"Intermediate input for module {module} does not exist. You may need to set the hook.")
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Get the intermediate input
        data = self.intermediate_input.get(module, None)
        # Check if data is None
        if data is None:
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return data
        return data.to(dtype)

    # Get intermediate output
    def get_intermediate_output(
        self, module: Union[str, nn.Module], dtype: Optional[torch.dtype] = None
    ) -> torch.Tensor:
        # Check the module type
        module = self._verify_module(module)
        # Check if the intermediate output exists
        if self.intermediate_output.get(module, None) is None:
            logger.error(f"Intermediate output for module {module} does not exist. You may need to set the hook.")
            error_message = "Intermediate output does not exist."
            raise RuntimeError(error_message)
        # Get the intermediate output
        data = self.intermediate_output.get(module, None)
        # Check if data is None
        if data is None:
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return data
        return data.to(dtype)

    # Get intermediate weight
    def get_intermediate_weight(
        self, module: Union[str, nn.Module], dtype: Optional[torch.dtype] = None
    ) -> torch.Tensor:
        # Check the module type
        module = self._verify_module(module)
        # Check if the module has weight
        if not hasattr(module, "weight"):
            logger.error(f"Module {module} does not have a weight attribute.")
            raise RuntimeError(f"Module {module} does not have a weight attribute.")
        # Get the weight
        weight: torch.Tensor = module.weight
        # Check if the module is a linear layer
        if isinstance(module, nn.Linear):
            weight = weight.t()
        # Check if the weight is None
        if weight is None:
            error_message = "Weight does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return weight
        # Return the weight
        return weight.to(dtype)

    # Get intermediate bias
    def get_intermediate_bias(
        self, module: Union[str, nn.Module], dtype: Optional[torch.dtype] = None
    ) -> torch.Tensor:
        # Check the module type
        module = self._verify_module(module)
        # Check if the module has bias
        if not hasattr(module, "bias"):
            logger.error(f"Module {module} does not have a bias attribute.")
            raise RuntimeError(f"Module {module} not found in the model.")
        # Get the bias
        bias: torch.Tensor = module.bias
        # Check if the bias is None
        if bias is None:
            error_message = "Bias does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return bias
        # Return the bias
        return bias.to(dtype)

    # Store intermediate input and output
    def _hook_fn(self, module: nn.Module, inputs: Tuple[torch.Tensor], outputs: torch.Tensor) -> None:
        # Log the shape of the input and output
        logger.info(f"Module: {module}")
        logger.info(f"Input shape: {inputs[0].shape}")
        logger.info(f"Output shape: {outputs.shape}")
        # Store the input and output
        if self.intermediate_input.get(module, None) is None:
            self.intermediate_input[module] = inputs[0]
        else:
            self.intermediate_input[module] = torch.cat([self.intermediate_input[module], inputs[0]], dim=1)
        if self.intermediate_output.get(module, None) is None:
            self.intermediate_output[module] = outputs
        else:
            self.intermediate_output[module] = torch.cat([self.intermediate_output[module], outputs], dim=1)

    # Register custom hook function
    def register_hook(
        self, target: Union[str, nn.Module], hook_fn: Callable[[nn.Module, Tuple[torch.Tensor], Any], None]
    ) -> None:
        # Check the target type
        module = self._verify_module(target)
        # Check if the hook already exists
        if self.hook_list.get(module, None) is not None:
            logger.warning(f"Hook for module {module} already exists.")
            return
        # Register the hook
        hook = module.register_forward_hook(hook_fn)
        # Append the hook to the hook list
        self.hook_list[module] = hook

    # Remove all hooks
    def remove_hooks(self) -> None:
        # Remove all hooks
        for hook in self.hook_list.values():
            hook.remove()
        # Clear the hook list
        self.hook_list.clear()

    # Forward pass
    def forward(self, *args: Any, **kwargs: Any) -> torch.Tensor:
        output = self.model(*args, **kwargs)
        if not isinstance(output, torch.Tensor):
            error_message = "Expected the model output to be a torch.Tensor"
            raise TypeError(error_message)
        return output

    # Get all module list
    def get_all_module_list(self) -> list[nn.Module]:
        return get_all_module_list(self.model)

    # Get all module names
    def get_all_module_name(self) -> list[str]:
        return [name for name, _ in self.model.named_modules() if name]

    # Check the module type
    def _verify_module(self, module: Union[str, nn.Module]) -> nn.Module:
        # Check the module type
        # If the module is a string, find the module
        if isinstance(module, str):
            mod: nn.Module = dict(self.model.named_modules()).get(module, None)
            return mod
        if not isinstance(module, nn.Module):
            logger.error("Module must be a string or an nn.Module instance.")
            error_message = "Module must be a string or an nn.Module instance."
            raise TypeError(error_message)
        # Return the module
        return module


class HFModelProbe(PTModelProbe):
    # Constructor
    def __init__(self, model: AutoModel, tokenizer: AutoTokenizer) -> None:
        super().__init__(model)
        self.tokenizer = tokenizer
        self.output_ids: torch.Tensor = None
        # Intermediate intermediate cos/sin for rotary embedding
        self.intermediate_cos: dict[nn.Module, torch.Tensor] = {}
        self.intermediate_sin: dict[nn.Module, torch.Tensor] = {}

    # Get model architecture
    def get_architecture(self) -> str:
        return config(self.model, "architecture")[0]

    # Get begin-of-sequence token id
    def get_bos_token_id(self) -> int:
        return self.tokenizer.bos_token_id

    # Get end-of-sequence token id
    def get_eos_token_id(self) -> int:
        return self.tokenizer.eos_token_id

    # Get `hidden_act` value
    def get_hidden_act(self) -> str:
        return config(self.model, "hidden_act")

    # Get `hidden_size` value
    def get_hidden_size(self) -> int:
        return config(self.model, "hidden_size")

    # Get `intermediate_size` value
    def get_intermediate_size(self) -> int:
        return config(self.model, "intermediate_size")

    # Get `max_length` value
    def get_max_length(self) -> int:
        return config(self.model, "max_length")

    # Get `num_attention_heads` value
    def get_num_attention_heads(self) -> int:
        return config(self.model, "num_attention_heads")

    # Get `num_key_value_heads` value
    def get_num_key_value_heads(self) -> int:
        return config(self.model, "num_key_value_heads")

    # Get `rope_base` value
    def get_rope_base(self) -> float:
        return config(self.model, "rope_base")

    # Get `num_hidden_layers` value
    def get_num_hidden_layers(self) -> int:
        return config(self.model, "num_hidden_layers")

    # Get `norm_eps` value
    def get_norm_eps(self) -> int:
        return config(self.model, "norm_eps")

    # Get `vocab_size` value
    def get_vocab_size(self) -> int:
        return config(self.model, "vocab_size")

    # Get input ids
    def get_input_ids(self, inputs: Union[str, List[str]], dtype: Optional[torch.dtype] = None) -> Any:
        # Check the input type
        if isinstance(inputs, str):
            inputs = [inputs]
        # Set the padding token to eos token
        self.tokenizer.pad_token = self.tokenizer.eos_token
        # Tokenize the batched inputs
        input_ids = self.tokenizer(inputs, return_tensors="pt", padding=True, truncation=True)["input_ids"]
        # Check the dtype
        if dtype is None:
            return input_ids
        # Return the input
        return input_ids.to(dtype)

    # Get output ids
    def get_output_ids(self, dtype: Optional[torch.dtype] = None) -> torch.Tensor:
        # Check the dtype
        if dtype is None:
            return self.output_ids
        # Return the output
        return self.output_ids.to(dtype)

    # Text generation
    def generate(self, input_ids: torch.Tensor, **kwargs: Any) -> torch.Tensor:
        self.output_ids = self.model.generate(input_ids, **kwargs)
        if not isinstance(self.output_ids, torch.Tensor):
            error_message = "Expected the model output to be a torch.Tensor"
            raise TypeError(error_message)
        return self.output_ids

    # Set hook for intermediate data
    def set_hook(self, module: Union[str, nn.Module], *, is_rotary_emb: bool = False) -> None:
        # For input tensor, we need to register hook function
        if is_rotary_emb:
            self.register_hook(module, self._rotary_emb_hook_fn)
        else:
            self.register_hook(module, self._hook_fn)

    # Store intermediate input and output
    def _rotary_emb_hook_fn(
        self, module: nn.Module, inputs: Tuple[torch.Tensor], outputs: Tuple[torch.Tensor, torch.Tensor]
    ) -> None:
        # Log the shape of the input and output
        logger.info(f"Module: {module}")
        logger.info(f"Input shape: {inputs[0].shape}")
        logger.info(f"RopE cos shape: {outputs[0].shape}")
        logger.info(f"RopE sin shape: {outputs[1].shape}")
        # Store the cos and sin
        if self.intermediate_cos.get(module, None) is None:
            self.intermediate_cos[module] = outputs[0]
        else:
            self.intermediate_cos[module] = torch.cat([self.intermediate_cos[module], outputs[0]], dim=1)
        if self.intermediate_sin.get(module, None) is None:
            self.intermediate_sin[module] = outputs[1]
        else:
            self.intermediate_sin[module] = torch.cat([self.intermediate_sin[module], outputs[1]], dim=1)

    # Get intermediate cos for rotary embedding
    def get_intermediate_cos(self, module: Union[str, nn.Module], dtype: Optional[torch.dtype] = None) -> torch.Tensor:
        # Check the module type
        module = self._verify_module(module)
        # Check if the intermediate cos exists
        if self.intermediate_cos.get(module, None) is None:
            logger.error(f"Intermediate cos for module {module} does not exist. You may need to set the hook.")
            error_message = "Intermediate cos does not exist."
            raise RuntimeError(error_message)
        # Get the intermediate cos
        data = self.intermediate_cos.get(module, None)
        # Check if data is None
        if data is None:
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return data
        # Return the input
        return data.to(dtype)

    # Get intermediate sin for rotary embedding
    def get_intermediate_sin(self, module: Union[str, nn.Module], dtype: Optional[torch.dtype] = None) -> torch.Tensor:
        # Check the module type
        module = self._verify_module(module)
        # Check if the intermediate sin exists
        if self.intermediate_sin.get(module, None) is None:
            logger.error(f"Intermediate sin for module {module} does not exist. You may need to set the hook.")
            error_message = "Intermediate sin does not exist."
            raise RuntimeError(error_message)
        # Get the intermediate sin
        data = self.intermediate_sin.get(module, None)
        # Check if data is None
        if data is None:
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return data
        # Return the input
        return data.to(dtype)


##########################################################################
