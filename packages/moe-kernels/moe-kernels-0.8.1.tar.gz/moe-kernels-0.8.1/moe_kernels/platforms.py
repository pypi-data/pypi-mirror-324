from typing import Callable, ParamSpec, TypeVar
import os
from functools import lru_cache, wraps

import torch

IS_ROCM = torch.version.hip is not None

if not IS_ROCM:
    import pynvml

_P = ParamSpec("_P")
_R = TypeVar("_R")


def with_nvml_context(fn: Callable[_P, _R]) -> Callable[_P, _R]:

    @wraps(fn)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        pynvml.nvmlInit()
        try:
            return fn(*args, **kwargs)
        finally:
            pynvml.nvmlShutdown()

    return wrapper


def device_id_to_physical_device_id(device_id: int) -> int:
    if "CUDA_VISIBLE_DEVICES" in os.environ:
        device_ids = os.environ["CUDA_VISIBLE_DEVICES"].split(",")
        if device_ids == [""]:
            raise RuntimeError(
                "CUDA_VISIBLE_DEVICES is set to empty string,"
                " which means GPU support is disabled."
            )
        physical_device_id = device_ids[device_id]
        return int(physical_device_id)
    else:
        return device_id


class CudaPlatform:
    @classmethod
    @lru_cache(maxsize=8)
    @with_nvml_context
    def get_device_name(cls, device_id: int = 0) -> str:
        physical_device_id = device_id_to_physical_device_id(device_id)
        return cls._get_physical_device_name(physical_device_id)

    @classmethod
    def _get_physical_device_name(cls, device_id: int = 0) -> str:
        handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)
        return pynvml.nvmlDeviceGetName(handle)


class RocmPlatform:
    @classmethod
    @lru_cache(maxsize=8)
    def get_device_name(cls, device_id: int = 0) -> str:
        return torch.cuda.get_device_name(device_id)


current_platform = RocmPlatform() if IS_ROCM else CudaPlatform()
