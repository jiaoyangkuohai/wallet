import os
import importlib
from types import MappingProxyType


__register_models = {}

DBOps = MappingProxyType(__register_models)


def register_model(name: str):
    """
    Implement the registration of model
    :param name: The name of the custom model used to specify the model
                in the parameter
    :return:
    """
    def register_model_cls(cls):
        if name in __register_models:
            raise ValueError("Cannot register duplicate model {}".format(name))
        __register_models[name] = cls
        return cls
    return register_model_cls


for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and not file.startswith("_"):
        model_lib = file[:file.find(".py")]
        importlib.import_module('database.' + model_lib)

from database.wallet_base import DBOperation, DBField
