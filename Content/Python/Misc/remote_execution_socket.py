# https://forums.unrealengine.com/t/python-blender-maya-to-ue4-using-remote-execution/138414/1
# 添加ue python插件下的库
#D:\Epic Games\UE_4.27\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python\remote_execution.py

import sys
import os
# sys.path.append(r'D:\Epic Games\UE_4.27\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import remote_execution as remote

def executeCommand(command):
    remote_exec = remote.RemoteExecution()
    remote_exec.start()
    remote_exec.open_command_connection(remote_exec.remote_nodes)
    # exec_mode = 'EvaluateStatement' # 有返回值 不能添加赋值
    exec_mode = remote.MODE_EXEC_STATEMENT #无返回值，可以使用 = 赋值
    # exec_mode = remote.MODE_EXEC_FILE #无返回值，可以执行python文件
    rec = remote_exec.run_command(command, exec_mode=exec_mode)
    if rec['success'] == True:
        return rec['result']
    return None

#Based on the selected assets in the ue4 asset browser, return an array with asset paths
#'StaticMesh"/Game/art/Meshes/ST_gourd01.ST_gourd01"', 'StaticMesh"/Game/art/Meshes/ST_gourd02.ST_gourd02"']
def getSelectedAssetPaths():
    assetPaths = []
    # command1 = r"a=unreal.GlobalEditorUtilityBase.get_default_object().get_selected_assets();"
    # # command2 = r"print(unreal.GlobalEditorUtilityBase.get_default_object().get_selected_assets())"
    # command2 = r"print(a,123)"
    # executeCommand(command1)
    # executeCommand(command2)
    str11 ='''sss = unreal.GlobalEditorUtilityBase.get_default_object().get_selected_assets();print(sss)
    '''
    command = str11
    # command = "str(unreal.GlobalEditorUtilityBase.get_default_object().get_selected_assets())"

    result = executeCommand(command)

    if result != None:
        string = result[2:-2]
        for e in string.split():
            path =  e.replace("\\'","").replace(",","")
            assetPaths.append(path)
    return result

print(getSelectedAssetPaths())
# getSelectedAssetPaths()

# str1 = str(unreal.GlobalEditorUtilityBase.get_default_object().get_selected_assets())
# print(str1)

str ='''
    sss = unreal.GlobalEditorUtilityBase.get_default_object().get_selected_assets()
    print(sss)
    '''
