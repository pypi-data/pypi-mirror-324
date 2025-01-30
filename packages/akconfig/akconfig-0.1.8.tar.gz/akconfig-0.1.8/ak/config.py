import json
import logging
import os
from datetime import datetime
from typing import Any

import click
from colored import Fore, Style
from terminaltables import AsciiTable

"""
AKConfig

A configuration management for python projects.
supports following types: int, str, dict, list, float, tuple

Example:
export VAR_A="HELLO YOU"
--- file.py -->
from ak.config import AKConfig
VAR_A = "HELLO WORLD"
VAR_B = 100
VAR_C = True
VAR_D = ("a", "b", "c", "d")
VAR_E = "SECRET"
VARS_MASK = ["VAR_E"]
config = (('VAR_A', 'HELLO ME'),)
cfg = AKConfig(
    global_vars=globals(),
    config_args=config,
    mask_keys=VARS_MASK,
    force_env_vars=True,
    uncolored=True,
)
# print(cfg.VAR_A)
cfg.print_config()
<< --- file.py --
"""


class AKConfig:
    def __init__(
        self,
        global_vars: dict = {},
        config_args: tuple | None = None,
        mask_keys: list | None = None,
        force_env_vars: bool = True,
        uncolored: bool = False,
    ):
        self.keys = AKConfig.GetGlobals(global_vars)
        self.mask_keys = mask_keys
        self.mask_values = []
        self.global_vars = global_vars
        self.click: click = (
            self.global_vars["click"] if "click" in self.global_vars else None
        )
        self.force_env_vars = force_env_vars
        self.uncolored = uncolored
        if self.click is not None:
            _args = AKConfig.GetARgVars(
                self.click,
                *[
                    k.__dict__["name"]
                    for k in self.click.get_current_context()
                    .__dict__["command"]
                    .__dict__["params"]
                ],
            )
            for _arg in _args:
                _val = _arg["value"]
                setattr(self, _arg["name"], _val)
                self.keys.append(_arg["name"])
        for key in self.keys:
            if self.global_vars and key in self.global_vars:
                val = self.global_vars[key]
                if force_env_vars is True and key in os.environ:
                    val = AKConfig.Cast(os.getenv(key), val)
                setattr(self, key, val)
        if config_args and len(config_args) > 0:
            self.arguments(config_args)

    def set(self, attrib: str, input_value: Any | None):
        if hasattr(self, attrib) and input_value is not None:
            if isinstance(input_value, type(getattr(self, attrib))):
                setattr(self, attrib, input_value)
                logging.info(f"> Set: {attrib}={input_value}")

    def arguments(self, input_value: tuple):
        cfg = dict(input_value)
        if len(cfg) > 0:
            for k, v in cfg.items():
                if k in self.keys and k in self.global_vars:
                    _val = AKConfig.Cast(v, self.global_vars[k])
                    try:
                        self.set(k, _val)
                    except:
                        logging.error("!Could not cast {} {}.".format(k, v))

    def get_attributes(self, with_value: bool = False):
        return [
            x
            for x in [
                (
                    ({v: getattr(self, v)} if with_value else v)
                    if not str(v).startswith("_")
                    and callable(getattr(self, v)) is False
                    and v != "global_vars"
                    else None
                )
                for v in dir(self)
            ]
            if x is not None
        ]

    def get_config(
        self, add_type: bool = False, mask_length: int | None = 5, fill: str = "*"
    ):
        def _m(v: str):
            if isinstance(mask_length, int):
                return fill * mask_length
            else:
                return fill * len(v)

        o = {}
        for k in self.keys:
            v = getattr(self, k)
            if self.mask_keys and k in self.mask_keys and isinstance(v, str):
                o[k] = _m(k)
                self.mask_values.append(v)
            else:
                o[k] = getattr(self, k)

        def _p(oi: Any):
            r = {}
            for k, v in oi.items():
                if isinstance(v, str):
                    r[k] = v
                    for s in self.mask_values:
                        r[k] = str(v).replace(s, _m(k))
                elif isinstance(v, dict):
                    i = {}
                    for ki, vi in v.items():
                        if isinstance(vi, dict):
                            i[ki] = _p(vi)
                        elif isinstance(vi, str):
                            if len(self.mask_values) > 0:
                                for p in self.mask_values:
                                    i[ki] = vi.replace(p, _m(ki))
                            else:
                                i[ki] = vi
                        else:
                            i[ki] = vi
                    if k not in r:
                        r[k] = {}
                    r[k].update(i)
                elif isinstance(v, list):
                    a = []
                    for l in v:
                        if isinstance(l, str):
                            if len(self.mask_values) > 0:
                                for t in self.mask_values:
                                    a.append(l.replace(t, _m(k)))
                            else:
                                a.append(l)
                        elif isinstance(l, dict):
                            a.append(_p(l))
                        else:
                            a.append(l)
                    if k not in r:
                        r[k] = []
                    r[k] = list(set(a))
                else:
                    r[k] = v
            return r

        ret = _p(o)
        if add_type is True:
            ret_a = ret.copy()
            ret_n = {}
            for k, v in ret_a.items():
                ret_n[
                    "{} ({})".format(k, AKConfig._TypedCol(v, True, self.uncolored))
                ] = v
            return ret_n
        else:
            return ret

    def print_config(self):
        print(
            AKConfig.CreateTable(
                entries=self.get_config(True, 5),
                title="AKCONFIG VARIABLES",
                footing_row=["Date", "{}".format(datetime.now())],
                uncolored=self.uncolored,
            )
        )

    def get_arg_envvar(self, *var_names) -> list:
        if self.click is not None:
            return AKConfig.GetARgVars(self.click, *var_names)
        else:
            return []

    @staticmethod
    def GetARgVars(clk: click, *var_names) -> list:
        res = []
        for opt in clk.get_current_context().__dict__["command"].__dict__["params"]:
            param_dict = opt.__dict__
            param_name = param_dict["name"]
            if param_name in var_names:
                if "envvar" in param_dict:
                    var_name = param_dict["envvar"]
                    if var_name is not None:
                        res.append(
                            {
                                "name": var_name,
                                "value": click.get_current_context().__dict__["params"][
                                    param_name
                                ],
                                "default": param_dict["default"],
                                "global_env": os.getenv(var_name),
                                "type": param_dict["type"],
                            }
                        )
        return res

    @staticmethod
    def Cast(val: Any, in_type: Any):
        if type(in_type) == int:
            return int(val)
        elif type(in_type) == bool:
            return True if str(val).lower().capitalize() == "True" else False
        elif type(in_type) == dict:
            return json.loads(str(val).strip())
        elif type(in_type) == list:
            return [str(i).strip() for i in str(val).split(",")]
        elif type(in_type) == float:
            return float(val)
        elif type(in_type) == tuple:
            return tuple([str(i).strip() for i in str(val).split(",")])
        else:
            return str(val)

    @staticmethod
    def Col(val, fore_256: str = "white", uncolored: bool = False):
        """
        https://dslackw.gitlab.io/colored/tables/colors/
        """
        if uncolored is False:
            return "{}{}{}".format(
                getattr(Fore, fore_256), str(val), getattr(Style, "reset")
            )
        else:
            return str(val)

    @staticmethod
    def CreateTable(
        entries: dict,
        title: str = "",
        footing_row: list | None = None,
        uncolored: bool = False,
    ):
        """
        check: https://robpol86.github.io/terminaltables/
        """
        tab = []
        tab.append(["NAME", "VALUE"])
        for k, v in entries.items():
            tab.append([k, AKConfig._TypedCol(v, False, uncolored)])
        if footing_row is not None:
            tab.append(footing_row)
        table = AsciiTable(table_data=tab, title=title)
        if footing_row is not None:
            table.inner_footing_row_border = True
        table.inner_heading_row_border = True
        return table.table

    @staticmethod
    def GetEnv(env_key: str, empty: Any | str = ""):
        return empty if os.getenv(env_key) is None else os.getenv(env_key)

    @staticmethod
    def GetGlobals(global_vars: dict) -> list:
        return [
            i
            for i in [
                (
                    k
                    if isinstance(v, (int, str, dict, list, float, tuple))
                    and not str(k).startswith("__")
                    else None
                )
                for k, v in global_vars.copy().items()
            ]
            if i is not None
        ]

    @staticmethod
    def _TypedCol(val: Any, as_type_name: bool = False, uncolored: bool = False):
        """
        check: https://dslackw.gitlab.io/colored/tables/colors/
        """
        v = type(val).__name__ if as_type_name else val
        if type(val) == str or v == "str":
            return AKConfig.Col(v, fore_256="light_blue", uncolored=uncolored)
        elif type(val) == bool or v == "bool":
            return AKConfig.Col(
                v,
                fore_256=("light_green" if val == True else "light_red"),
                uncolored=uncolored,
            )
        elif type(val) == list or v == "list":
            return AKConfig.Col(v, fore_256="light_magenta", uncolored=uncolored)
        elif type(val) == dict or v == "dict":
            return AKConfig.Col(v, fore_256="light_cyan", uncolored=uncolored)
        elif type(val) == int or v == "int":
            return AKConfig.Col(v, fore_256="light_yellow", uncolored=uncolored)
        elif type(val) == float or v == "float":
            return AKConfig.Col(v, fore_256="light_sea_green", uncolored=uncolored)
        elif type(val) == tuple or v == "tuple":
            return AKConfig.Col(v, fore_256="light_steel_blue", uncolored=uncolored)
        else:
            return val
