from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from omegaconf import OmegaConf  # @manual
from pytorch_lightning.plugins import PLUGIN, PLUGIN_INPUT
from pytorch_lightning.plugins.precision import FullyShardedNativeMixedPrecisionPlugin
from pytorch_lightning.plugins.training_type import DDPFullyShardedPlugin, DDPPlugin
from torch.distributed.algorithms.ddp_comm_hooks import (
    default_hooks as default,
    powerSGD_hook as powerSGD,
)
from torchrecipes.core.conf import TrainerConf


@dataclass
class DDPPluginConf:
    # DDP communication setting for contorlling gradients commnication
    # state for passed into hook which is used to maintain and update state info
    ddp_comm_state: Optional[object] = None
    # short name for communication hook callable function
    ddp_comm_hook: Optional[str] = None
    # short name for communication hook wrapper to support combination with `ddp_comm_hook`
    ddp_comm_wrapper: Optional[str] = None
    # whether find unused parameter, in lightning trainer, by default, it is true,
    # but it would have performance hit
    # see https://pytorch-lightning.readthedocs.io/en/latest/benchmarking/performance.html#when-using-ddp-set-find-unused-parameters-false
    find_unused_parameters: bool = True


DDP_CUSTOMIZED_PLUGIN_CONF = {
    "ddp_find_unused_parameters_false": DDPPluginConf(
        find_unused_parameters=False,
    ),
    "ddp_fp16_compress": DDPPluginConf(ddp_comm_hook=default.fp16_compress_hook),
    "ddp_power_sgd_1k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=1000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
    ),
    "ddp_power_sgd_3k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=3000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
    ),
    "ddp_power_sgd_5k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=5000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
    ),
    "ddp_power_sgd_7k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=7000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
    ),
    "ddp_power_sgd_10k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=10000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
    ),
    "ddp_fp16_compress_wrapper_power_sgd_1k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=1000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
    "ddp_fp16_compress_wrapper_power_sgd_3k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=3000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
    "ddp_fp16_compress_wrapper_power_sgd_5k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=5000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
    "ddp_fp16_compress_wrapper_power_sgd_7k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=7000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
    "ddp_fp16_compress_wrapper_power_sgd_10k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=10000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
    "ddp_batched_power_sgd_1k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=1000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.batched_powerSGD_hook,
    ),
    "ddp_batched_power_sgd_3k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=3000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.batched_powerSGD_hook,
    ),
    "ddp_batched_power_sgd_5k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=5000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.batched_powerSGD_hook,
    ),
    "ddp_fp16_compress_wrapper_batched_power_sgd_1k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=1000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.batched_powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
    "ddp_fp16_compress_wrapper_batched_power_sgd_3k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=3000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.batched_powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
    "ddp_fp16_compress_wrapper_batched_power_sgd_5k": DDPPluginConf(
        ddp_comm_state=powerSGD.PowerSGDState(
            process_group=None,
            start_powerSGD_iter=5000,
            orthogonalization_epsilon=0,  # setting to 0 for accuracy reason
        ),
        ddp_comm_hook=powerSGD.batched_powerSGD_hook,
        ddp_comm_wrapper=default.fp16_compress_wrapper,
    ),
}

# to allow flexible combination of different techniques, like whether to
# find unused parameters or whether to apply communication hook etc.
def merge_ddp_plugin_conf(ddp_plugin_conf_list: List[DDPPluginConf]) -> DDPPluginConf:
    merged_ddp_plugin_conf = DDPPluginConf()
    for ddp_plugin_conf in ddp_plugin_conf_list:
        for attr, val in ddp_plugin_conf.__dict__.items():
            if val is not None:
                setattr(merged_ddp_plugin_conf, attr, val)
    return merged_ddp_plugin_conf


# get fully sharded training type plugin and precision plugin
def get_fully_sharded_plugins(
    precision: int, reshard_after_forward: bool = True, cpu_offload: bool = False
) -> List[PLUGIN]:
    # training type plugin
    fully_sharded_plugins: List[PLUGIN] = [
        DDPFullyShardedPlugin(
            cpu_offload=cpu_offload,
            reshard_after_forward=reshard_after_forward,
        )
    ]
    if precision == 16:
        # precision plugin
        fully_sharded_plugins.append(
            FullyShardedNativeMixedPrecisionPlugin(precision=16, device="gpu")
        )
    return fully_sharded_plugins


def convert_trainer_plugins(
    precision: int,
    plugins: List[str],
) -> List[PLUGIN_INPUT]:
    """
    Util function to convert the plugin short name to corresponding Plugin instance.

    Traversing and processing the given ``plugins`` list as follows:
        1. plugin is `ddp_fully_sharded` ==> ``DDPFullyShardedPlugin``
            if ``precision`` is 16, will also add ``FullyShardedNativeMixedPrecisionPlugin``
        2. plugin is map key for ``DDP_CUSTOMIZED_PLUGIN_CONF`` ==> corresponding ``DDPPlugin``
            if there are multiple plugins match keys in ``DDP_CUSTOMIZED_PLUGIN_CONF``, will use
            ``merge_ddp_plugin_conf`` to merge to one ``DDPPlugin``
        3. otherwise, remain as original short name
    """

    ddp_plugin_conf_list = []
    converted_plugins = []
    for plugin in plugins:
        if plugin == "ddp_fully_sharded":
            # process fully sharded plugin
            converted_plugins.extend(
                get_fully_sharded_plugins(
                    precision=precision,
                )
            )
        elif plugin == "ddp_fully_sharded_not_reshard":
            # process fully sharded plugin
            converted_plugins.extend(
                get_fully_sharded_plugins(
                    precision=precision,
                    reshard_after_forward=False,
                )
            )
        elif plugin == "ddp_fully_sharded_cpu_offload":
            # process fully sharded plugin
            converted_plugins.extend(
                get_fully_sharded_plugins(
                    precision=precision,
                    cpu_offload=True,
                )
            )
        elif plugin in DDP_CUSTOMIZED_PLUGIN_CONF:
            # get customized DDPPlugin if applicable
            ddp_plugin_conf_list.append(DDP_CUSTOMIZED_PLUGIN_CONF[plugin])
        else:
            # remain as short name
            converted_plugins.append(plugin)

    # merge ddp_plugin_conf_list
    if len(ddp_plugin_conf_list) > 0:
        ddp_plugin_conf = merge_ddp_plugin_conf(ddp_plugin_conf_list)
        ddp_plugin = DDPPlugin(
            ddp_comm_state=ddp_plugin_conf.ddp_comm_state,
            ddp_comm_hook=ddp_plugin_conf.ddp_comm_hook,
            ddp_comm_wrapper=ddp_plugin_conf.ddp_comm_wrapper,
            find_unused_parameters=ddp_plugin_conf.find_unused_parameters,
        )
        converted_plugins.append(ddp_plugin)
    return converted_plugins


def get_trainer_params(trainer_conf: TrainerConf) -> Dict[str, Any]:
    trainer_params = OmegaConf.to_container(trainer_conf, resolve=True) or {}
    assert isinstance(trainer_params, Dict)
    plugins = trainer_params.get("plugins", []) or []
    trainer_params["plugins"] = convert_trainer_plugins(
        trainer_params.get("precision", 32),
        plugins,
    )
    return {str(key): value for key, value in trainer_params.items()}
