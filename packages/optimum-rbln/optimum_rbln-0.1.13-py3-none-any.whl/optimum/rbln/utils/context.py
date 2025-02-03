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

from contextlib import contextmanager
from pathlib import Path
from typing import Union

from optimum.exporters import TasksManager
from transformers import AutoConfig, AutoModel


@contextmanager
def override_auto_classes(config_func=None, model_func=None, skip_taskmanager=True):
    """Temporarily override Auto classes with original model classes"""
    original_config = AutoConfig.from_pretrained
    original_model = AutoModel.from_pretrained
    original_get_model_from_task = TasksManager.get_model_from_task

    def get_model_from_task(
        task: str,
        model_name_or_path: Union[str, Path],
        **kwargs,
    ):
        return model_func(model_name_or_path, **kwargs)

    def none_func(*args, **kwargs):
        return None

    try:
        AutoConfig.from_pretrained = config_func or none_func
        AutoModel.from_pretrained = model_func or none_func
        if skip_taskmanager:
            TasksManager.get_model_from_task = none_func if model_func is None else get_model_from_task
        yield
    finally:
        AutoConfig.from_pretrained = original_config
        AutoModel.from_pretrained = original_model
        TasksManager.get_model_from_task = original_get_model_from_task
