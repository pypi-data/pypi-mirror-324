# Copyright 2024 Rebellions Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Portions of this software are licensed under the Apache License,
# Version 2.0. See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.

# All other portions of this software, including proprietary code,
# are the intellectual property of Rebellions Inc. and may not be
# copied, modified, or distributed without prior written permission
# from Rebellions Inc.

import copy
import json
from collections import UserDict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import torch


DEFAULT_COMPILED_MODEL_NAME = "compiled_model"
DEFAULT_MOD_NAME = "default"


@dataclass
class RBLNRuntimeConfig:
    compiled_model_name: str = DEFAULT_COMPILED_MODEL_NAME
    rbln_mod_name: str = DEFAULT_MOD_NAME
    input_info: List[Tuple[str, Tuple[int], Optional[str]]] = None
    batch_size: Optional[int] = None
    fusion: Optional[bool] = None
    npu: Optional[str] = None
    tensor_parallel_size: Optional[int] = None

    @staticmethod
    def normalize_dtype(dtype):
        """
        framework's dtype to string.
        i.e. torch.float32 -> "float32"
        """
        if isinstance(dtype, str):
            return dtype
        else:
            dtype: str = repr(dtype).split(".")[-1]
            if dtype.endswith("'>"):  # numpy
                dtype = dtype[:-2]
            return dtype

    def __post_init__(self):
        self.input_info = [(i[0], i[1], RBLNRuntimeConfig.normalize_dtype(i[2]) or "float32") for i in self.input_info]

    def update(self, **kwargs):
        self.compiled_model_name = kwargs.get("compiled_model_name", self.compiled_model_name)
        self.rbln_mod_name = kwargs.get("rbln_mod_name", self.rbln_mod_name)
        self.input_info = kwargs.get("input_info", self.input_info)
        self.batch_size = kwargs.get("batch_size", self.batch_size)
        self.fusion = kwargs.get("fusion", self.fusion)
        self.npu = kwargs.get("npu", self.npu)
        self.tensor_parallel_size = kwargs.get("tensor_parallel_size", self.tensor_parallel_size)
        return self

    def get_dummy_inputs(self, fill=0):
        dummy = []
        for name, shape, dtype in self.input_info:
            dummy.append(
                torch.fill(torch.zeros(*shape, dtype=getattr(torch, dtype)), fill)
                if len(shape) > 0
                else torch.tensor(fill, dtype=getattr(torch, dtype))
            )
        return tuple(dummy)

    def asdict(self):
        return asdict(self)


class RBLNConfig(UserDict):
    def __init__(self, runtime_cfgs: Dict[str, List[RBLNRuntimeConfig]], _rbln_meta: Dict[str, Any] = None):
        """Configurations for RBLN model compilation and inference.

        Args:
            _rbln_meta (Dict[str, Any], optional):
                     Any rbln-specific configurations.
                     (i.e. max_seq_len for language models, image_size for image models).
                     Defaults to None.
        """
        super().__init__(runtime_cfgs)
        if _rbln_meta:
            self.meta = _rbln_meta
        else:
            self.meta: Dict[str, Any] = {}

    @staticmethod
    def from_rbln_configs(rbln_configs: List["RBLNConfig"], names: Optional[List[str]] = None) -> "RBLNConfig":
        # assume each rbln_config has exact one rbln_runtime_config
        names = [None] * len(rbln_configs) if names is None else names
        runtime_cfgs = []
        for name, cfg in zip(names, rbln_configs):
            if len(cfg) > 1:
                msg = (
                    "`from_rbln_configs` requires exact one `RBLNRuntimeConfig` for each `RBLNConfig`."
                    f"But got {len(cfg)} `RBLNRuntimeConfig`."
                )
                raise RuntimeError(msg)

            runtime_cfg = cfg[list(cfg.keys())[0]][0]
            runtime_cfg = copy.deepcopy(runtime_cfg)
            if name is not None:
                runtime_cfg.compiled_model_name = name
            runtime_cfgs.append(runtime_cfg)

        metas = [cfg.meta for cfg in rbln_configs]
        merged_meta = {k: v for meta in metas for k, v in meta.items()}

        return RBLNConfig.from_rbln_runtime_configs(runtime_cfgs, _rbln_meta=merged_meta)

    @staticmethod
    def from_rbln_runtime_configs(
        rbln_runtime_configs: List[RBLNRuntimeConfig],
        _rbln_meta: Dict[str, Any] = None,
    ) -> "RBLNConfig":
        cfgs: Dict[str, List[RBLNRuntimeConfig]] = {}
        for rbln_runtime_config in rbln_runtime_configs:
            if rbln_runtime_config.compiled_model_name in cfgs:
                cfgs[rbln_runtime_config.compiled_model_name].append(rbln_runtime_config)
            else:
                cfgs[rbln_runtime_config.compiled_model_name] = [rbln_runtime_config]
        return RBLNConfig(cfgs, _rbln_meta=_rbln_meta)

    def save(self, dir_path: str):
        dir_path = Path(dir_path)
        data = self.asdict()
        data.update({"rbln_config_meta": self.meta})
        with open(dir_path / "rbln_config.json", "w") as jsonf:
            json.dump(data, jsonf, indent=2)

    @staticmethod
    def load(dir_path: str) -> "RBLNConfig":
        dir_path = Path(dir_path)
        with open(dir_path / "rbln_config.json", "r") as jsonf:
            config_file = json.load(jsonf)
        return RBLNConfig.fromdict(config_file)

    def asdict(self):
        dic = {k: [asdict(cfg) for cfg in cfgs] for k, cfgs in self.data.items()}
        return dic

    @staticmethod
    def fromdict(dic: dict):
        runtime_cfgs = {
            k: [RBLNRuntimeConfig(**cfg) for cfg in cfgs] for k, cfgs in dic.items() if k != "rbln_config_meta"
        }
        if "rbln_config_meta" in dic:
            meta = dic["rbln_config_meta"]
        else:
            meta = None
        return RBLNConfig(runtime_cfgs, _rbln_meta=meta)
