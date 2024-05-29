# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import unreal
import os
import sys

# 注册python扩展蓝图
import Misc.PyBPFunctionLibrary


import json
import codecs
import platform
import posixpath
import traceback
import subprocess

from subprocess import PIPE, Popen
from threading import Thread
from functools import partial
from collections import OrderedDict, defaultdict

try:
    from Queue import Queue
except:
    from queue import Queue



DIR = os.path.dirname(__file__)
if DIR not in sys.path:
    sys.path.append(DIR) 
    
MENU_ADD_TIME = 0.2


menus = unreal.ToolMenus.get()


FORMAT_ARGS = {
    "Content": DIR
}

COMMAND_TYPE = {
    "COMMAND": unreal.ToolMenuStringCommandType.COMMAND,
    "PYTHON": unreal.ToolMenuStringCommandType.PYTHON,
    "CUSTOM": unreal.ToolMenuStringCommandType.CUSTOM,
}

INSERT_TYPE = {
    "AFTER": unreal.ToolMenuInsertType.AFTER,
    "BEFORE": unreal.ToolMenuInsertType.BEFORE,
    "DEFAULT": unreal.ToolMenuInsertType.DEFAULT,
    "FIRST": unreal.ToolMenuInsertType.FIRST,
}

MENU_TYPE = {
    "BUTTON_ROW": unreal.MultiBoxType.BUTTON_ROW,
    "MENU": unreal.MultiBoxType.MENU,
    "MENU_BAR": unreal.MultiBoxType.MENU_BAR,
    "TOOL_BAR": unreal.MultiBoxType.TOOL_BAR,
    #"TOOL_MENU_BAR": unreal.MultiBoxType.TOOL_MENU_BAR,
    "UNIFORM_TOOL_BAR": unreal.MultiBoxType.UNIFORM_TOOL_BAR,
    "VERTICAL_TOOL_BAR": unreal.MultiBoxType.VERTICAL_TOOL_BAR,
}

ENTRY_TYPE = {
    "BUTTON_ROW": unreal.MultiBlockType.BUTTON_ROW,
    "EDITABLE_TEXT": unreal.MultiBlockType.EDITABLE_TEXT,
    "HEADING": unreal.MultiBlockType.HEADING,
    "MENU_ENTRY": unreal.MultiBlockType.MENU_ENTRY,
    #"MENU_SEPARATOR": unreal.MultiBlockType.MENU_SEPARATOR,
    "NONE": unreal.MultiBlockType.NONE,
    "TOOL_BAR_BUTTON": unreal.MultiBlockType.TOOL_BAR_BUTTON,
    "TOOL_BAR_COMBO_BUTTON": unreal.MultiBlockType.TOOL_BAR_COMBO_BUTTON,
    #"TOOL_BAR_SEPARATOR": unreal.MultiBlockType.TOOL_BAR_SEPARATOR,
    "WIDGET": unreal.MultiBlockType.WIDGET,
}

ACTION_TYPE = {
    "BUTTON": unreal.UserInterfaceActionType.BUTTON,
    "CHECK": unreal.UserInterfaceActionType.CHECK,
    "COLLAPSED_BUTTON": unreal.UserInterfaceActionType.COLLAPSED_BUTTON,
    "NONE": unreal.UserInterfaceActionType.NONE,
    "RADIO_BUTTON": unreal.UserInterfaceActionType.RADIO_BUTTON,
    "TOGGLE_BUTTON": unreal.UserInterfaceActionType.TOGGLE_BUTTON,
}

HOTKEY_TYPE = {
    "COMMAND":lambda command: partial(unreal.SystemLibrary.execute_console_command,None,command),
    "PYTHON": lambda command: partial(lambda c:eval(compile(c, '<string>', 'exec')),command),
    "SCRIPT":lambda command: getattr(hotkey,command) if hasattr(hotkey,command) else partial(unreal.SystemLibrary.execute_console_command,None,"Hotkey 配置失败 -> %s 找不到" % command),
}

def handle_menu(data):
    """
    handle_menu 递归生成菜单
    """
    menu = data.get("menu")
    if not menu:
        return

    for section, config in data.get("section", {}).items():
        config = config if isinstance(config, dict) else {"label": config}
        config.setdefault("label", "untitle")
        # NOTE 如果存在 insert_type 需要将字符串转换
        insert = INSERT_TYPE.get(config.get("insert_type", "").upper())
        if insert:
            config["insert_type"] = insert
        insert_name = config.get("insert_name")
        config["insert_name"] = insert_name if insert_name else "None"
        menu.add_section(section, **config)

    for prop, value in data.get("property", {}).items():
        if prop == "menu_owner" or value == "":
            continue
        elif prop == "menu_type":
            value = MENU_TYPE.get(value.upper())
        menu.set_editor_property(prop, value)

    for entry_name, config in data.get("entry", {}).items():
        prop = config.get("property", {})

        for k, v in prop.items():
            # NOTE 跳过 owner 和 script_object
            prop.pop("owner") if not prop.get("owner") is None else None
            prop.pop("script_object") if not prop.get(
                "script_object") is None else None

            if v == '':
                prop.pop(k)
            elif k == "insert_position":
                position = INSERT_TYPE.get(v.get("position", "").upper())
                v["position"] = position if position else unreal.ToolMenuInsertType.FIRST
                v["name"] = v.get("name", "")
                prop[k] = unreal.ToolMenuInsert(**v)
            elif k == "type":
                typ = ENTRY_TYPE.get(str(v).upper())
                prop[k] = typ if typ else unreal.MultiBlockType.MENU_ENTRY
            elif k == "user_interface_action_type":
                typ = ACTION_TYPE.get(str(v).upper())
                prop.update({k: typ}) if typ else prop.pop(k)

        prop.setdefault("name", entry_name)
        prop.setdefault("type", unreal.MultiBlockType.MENU_ENTRY)
        entry = unreal.ToolMenuEntry(**prop)
        tooltip = config.get('tooltip')
        entry.set_tool_tip(tooltip) if tooltip else None

        entry.set_label(config.get('label', "untitle"))
        typ = COMMAND_TYPE.get(config.get("type", "").upper(), 0)

        command = config.get('command', '').format(**FORMAT_ARGS)
        entry.set_string_command(typ, "", string=command)
        menu.add_menu_entry(config.get('section', ''), entry)

    for entry_name, config in data.get("sub_menu", {}).items():
        init = config.get("init", {})
        owner = menu.get_name()
        section_name = init.get("section", "")
        name = init.get("name", entry_name)
        label = init.get("label", "")
        tooltip = init.get("tooltip", "")
        menu = menu.add_sub_menu(
            owner, section_name, name, label, tooltip)
        config.setdefault('menu', menu)
        handle_menu(config)


def read_json(json_path):
    try:
        with open(json_path, 'r',encoding='utf-8') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

    except:
        data = {}
    return data


def create_menu():
    # NOTE 读取 menu json 配置
    json_path = posixpath.join(DIR, "menu.json")
    menu_json = read_json(json_path)
    print(json_path)

    fail_menus = {}
    # NOTE https://forums.unrealengine.com/development-discussion/python-scripting/1767113-making-menus-in-py
    for tool_menu, config in menu_json.items():
        print(tool_menu)
        # NOTE 获取主界面的主菜单位置
        menu = menus.find_menu(tool_menu)

        if not menu:
            fail_menus.update({tool_menu: config})
            continue
        config.setdefault('menu', menu)

        handle_menu(config)

    # NOTE 刷新组件
    menus.refresh_all_widgets()

    return fail_menus


if __name__ == "__main__":

    fail_menus = create_menu()
    if fail_menus:
        global __tick_menu_elapsed__
        __tick_menu_elapsed__ = 0

        def timer_add_menu(menu_dict, delta):
            global __tick_menu_elapsed__
            __tick_menu_elapsed__ += delta

            # NOTE avoid frequently executing
            if __tick_menu_elapsed__ < MENU_ADD_TIME:
                return

            __tick_menu_elapsed__ = 0

            # NOTE all menu added the clear the tick callback
            if not menu_dict:
                global __py_add_menu_tick__
                unreal.unregister_slate_post_tick_callback(__py_add_menu_tick__)
                return

            flag = False
            menu_list = []
            for tool_menu, config in menu_dict.items():
                menu = menus.find_menu(tool_menu)
                if not menu:
                    continue
                menu_list.append(tool_menu)
                flag = True
                config.setdefault("menu", menu)
                handle_menu(config)

            if flag:
                [menu_dict.pop(m) for m in menu_list]
                menus.refresh_all_widgets()

        # NOTE register custom menu
        callback = partial(timer_add_menu, fail_menus)
        global __py_add_menu_tick__
        __py_add_menu_tick__ = unreal.register_slate_post_tick_callback(callback)
        __QtAppQuit__ = partial(
            unreal.unregister_slate_post_tick_callback, __py_add_menu_tick__
        )

