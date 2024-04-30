import sys
import json
import os
import subprocess
import time
import unreal

'''if os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage") not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage"))
from PySide.QtGui import *
from PySide.QtCore import *

if os.path.join(os.path.dirname(os.path.dirname(__file__)), "commonLib") not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "commonLib"))'''

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))
# sys.path.append(r'A:\Production_ST\toolKit\LibraryScript\python\interaction')
import assetToolFunctions

reload(assetToolFunctions)

import suCmd

reload(suCmd)
jsonFile = r"D:/UE4Cool.json"


def getLibPath():
    '''
        获取资产库的根路径
    :return:
    '''
    assetLib = ""
    cmd = 'wmic process where name="IExe.exe" get executablepath'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    stout, sterr = p.communicate()
    exePath = stout.replace("ExecutablePath", "")
    exePath = exePath.strip()
    if exePath:
        assetLibDir = os.path.join(os.path.dirname(os.path.dirname(exePath)), "scripts", "startup", "libPath.txt")
        with open(assetLibDir, "r") as file:
            assetLib = str(file.read()).strip()
    return assetLib


def getSceneDes():
    '''
        获取场景资产位置信息
    :return:
    '''
    with open(jsonFile, "r") as f:
        content = f.read()
    allTrans = json.loads(content)
    return allTrans


def handleImport():
    '''
        处理场景导入
    :return:
    '''
    allTrans = getSceneDes()
    if not allTrans:
        return
    libPath = getLibPath()
    if not libPath:
        unreal.log_error(u"没有打开资产库")
        return
    errorFile = list()
    quantity_steps_in_slow_task = len(allTrans)
    with unreal.ScopedSlowTask(quantity_steps_in_slow_task, u"正在导入资源....") as slow_task:
        slow_task.make_dialog(True)
        for index, objs in enumerate(allTrans):
            slow_task.enter_progress_frame(1, u"正在导入中...." + str(index) + "/" + str(quantity_steps_in_slow_task))
            path = objs["path"]
            importPath = path.replace("\\", "/")
            # importPath = importPath.decode("gbk")
            reInfo = assetToolFunctions.importAssets(importPath)
            if not reInfo:
                errorFile.append(importPath)
                continue
            ueAsset = reInfo[0]
            if ueAsset.startswith("/Game"):
                objPath = ueAsset
                texInfo = suCmd.getAllTexPathOfFbx(importPath)
                texUassets = suCmd.importAllTex(objPath, texInfo)
                suCmd.connectMaterials(objPath, texUassets, importPath)
            else:
                objPath = os.path.splitext(ueAsset.replace("\\", "/").replace(os.path.dirname(path), "/Game"))[0]
            objs["objectPath"] = objPath
    with open(jsonFile, "w") as f:
        f.write(json.dumps(allTrans, indent=4))
        f.close()
    if errorFile:
        unreal.CustomBlueprintFunctionLibrary.message_dialog(u"don\'t exist asset\n {}".format("\n".join(errorFile)))


if __name__ == '__main__':
    # app = QApplication.instance()
    # if not app:
    #    app = QApplication(sys.argv)
    # iw = ImportSceneDescriptionWindow()
    handleImport()
    # unreal.parent_external_window_to_slate(iw.winId())
    # iw.show()
