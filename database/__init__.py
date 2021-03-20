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


from database.sqlite_operation import SqliteDBOperation
from database.mysql_peration import MySQLDBOperation
from database.wallet_base import DBOperation
