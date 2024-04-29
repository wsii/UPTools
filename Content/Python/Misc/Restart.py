# -*- coding: utf-8 -*-
"""
自动重启引擎
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import


import sys
import subprocess
import unreal


editor_util = unreal.EditorLoadingAndSavingUtils()
sys_lib = unreal.SystemLibrary()
paths = unreal.Paths()


def main():
    # NOTE 保存对象
    check = editor_util.save_dirty_packages_with_dialog(True,True)
    if not check:
        return

    uproject = paths.get_project_file_path()
    editor = sys.executable
    
    # NOTE 启动当前引擎
    subprocess.Popen([editor,uproject,'-skipcompile'],shell=True)
    
    # NOTE 退出引擎
    sys_lib.quit_editor()
    

if __name__ == "__main__":
    main()
