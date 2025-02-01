"""Registry for T2T models."""

import functools
import inspect
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple, Union

import catalogue

from databricks.kie.t2t_models.all_t2t_models import *  # pylint: disable=wildcard-import
from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel
from databricks.kie.t2t_schema import T2TSystemParams


@dataclass
class T2TModelConfig:
    """Model config for model in T2T model registry."""
    name: str
    is_default: bool
    model: BaseT2TModel


class T2TModelRegistry(catalogue.Registry):
    """A thin wrapper around catalogue.Registry to add T2T models."""

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.default_model: Optional[Tuple[str, Callable[[T2TSystemParams], BaseT2TModel]]] = None

    def register(self,
                 name: str,
                 *,
                 to_register: Union[Callable[[T2TSystemParams], BaseT2TModel], BaseT2TModel],
                 is_default: bool = False):
        """Register a model to the registry."""
        if is_default and self.default_model:
            raise ValueError("Only one default model can be registered")

        if isinstance(to_register, BaseT2TModel):
            func = to_register.create_from_system_param
        else:
            func = to_register

        # Inspect function signature
        sig = inspect.signature(func)
        params = sig.parameters

        # Get non-bounded arguments (exclude self/cls)
        non_bounded_args = [
            p for p in params.values() if p.kind not in (p.VAR_POSITIONAL, p.VAR_KEYWORD, p.KEYWORD_ONLY)
        ]

        if len(non_bounded_args) != 1:
            raise ValueError(f"Function {func.__name__} must have exactly 1 non-bounded argument")

        # Check argument type annotation
        arg = non_bounded_args[0]
        if arg.annotation != T2TSystemParams:
            raise ValueError("Argument of registered function must be 1 argument of type T2TSystemParams")

        if is_default:
            self.default_model = (name, func)

        return super().register(name, func=func)


model_registry = T2TModelRegistry("t2t_model_registry")


def create_t2t_model_list(task_spec: T2TSystemParams) -> List[T2TModelConfig]:
    """Create a list of T2TModelConfig objects from the registry given a task spec."""
    models = []
    for name, func in model_registry.get_all().items():
        model = func(task_spec)
        if model is None:
            continue

        is_default = model_registry.default_model and name == model_registry.default_model[0]
        models.append(T2TModelConfig(name=name, is_default=is_default, model=model))
    return models


################################################################################
# Manually add models to T2T Model Registry
#
# NOTE: Class can be added using decorators.
################################################################################

model_registry.register("prompt_tuning_model_gpt_4o_cot",
                        to_register=functools.partial(T2TPromptTuningModel.create_from_system_param,
                                                      model_id="gpt-4o-2024-08-06-text2text",
                                                      use_cot=True),
                        is_default=True)
model_registry.register("prompt_tuning_model_gpt_4o",
                        to_register=functools.partial(T2TPromptTuningModel.create_from_system_param,
                                                      model_id="gpt-4o-2024-08-06-text2text",
                                                      use_cot=False),
                        is_default=False)
