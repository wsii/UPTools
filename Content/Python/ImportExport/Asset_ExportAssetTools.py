import os
import unreal
import shutil
import subprocess
import sys

sys.setrecursionlimit(60000)

if os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage") not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage"))

if os.path.join(os.path.dirname(os.path.dirname(__file__)), "commonLib") not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "commonLib"))
from PySide.QtGui import *
import screen_grap

reload(screen_grap)


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
        assetLibDir = os.path.join(os.path.dirname(os.path.dirname(exePath)), "scripts", "startup", "curPath.txt")
        with open(assetLibDir, "r") as file:
            assetLib = str(file.read()).strip()
    return assetLib


class ExportAssetWindow(QWidget):
    def __init__(self):
        super(ExportAssetWindow, self).__init__()

        self.depAssets = list()

        self.radioBtn1 = QRadioButton(u"缩略图")
        self.radioBtn1.setChecked(False)
        self.radioBtn2 = QRadioButton(u"截图")
        self.radioBtn2.setChecked(True)
        self.btnGrp = QButtonGroup()
        self.btnGrp.addButton(self.radioBtn1, 11)
        self.btnGrp.addButton(self.radioBtn2, 22)
        self.radBtnLay = QHBoxLayout()
        self.radBtnLay.addWidget(self.radioBtn1)
        self.radBtnLay.addWidget(self.radioBtn2)
        self.radBtnLay.addStretch()

        self.exportBtn = QPushButton(u"导出")
        self.exportBtn.clicked.connect(self.exportAsset)
        self.exportLay = QHBoxLayout()
        self.exportLay.addStretch()
        self.exportLay.addWidget(self.exportBtn)

        self.mainLay = QVBoxLayout()
        self.mainLay.addLayout(self.radBtnLay)
        self.mainLay.addLayout(self.exportLay)

        self.setLayout(self.mainLay)
        self.setWindowTitle(u"导出资产工具")
        self.resize(250, 50)

    def screenshotCmd(self, res, filename):
        '''
            场景截图
        :return:
        '''
        # 两种图片只出来一张
        task = unreal.AutomationLibrary().take_high_res_screenshot(res, res, filename.replace("\\", "/"))
        return task.is_task_done()

    def buildExportTask(self, assetPath, exportPath, fbxOpt):
        '''
            创建导出任务
        :param assetPath: 资产路径
        :param exportPath: 导出路径
        :param fbxOpt: fbx导出选项
        :return:
        '''
        loadedAsset = unreal.EditorAssetLibrary.load_asset(assetPath)
        task = unreal.AssetExportTask()
        task.set_editor_property("object", loadedAsset)
        task.set_editor_property("filename", exportPath)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_identical", True)
        task.set_editor_property("options", fbxOpt)
        return task

    def getAssetPath(self):
        '''
            获得选择的ue资产路径
        :return:
        '''
        allSelObj = unreal.EditorUtilityLibrary.get_selected_asset_data()
        assetInfos = list()
        for assetObj in allSelObj:
            assetInfos.append({
                "type": str(assetObj.asset_class),
                "object_path": str(assetObj.object_path),
                "name": str(assetObj.asset_name),
                "object": assetObj.get_asset(),
                "package_name": str(assetObj.package_name)
            })
        return assetInfos

    def getDepAssets(self, pkgPath, depAssets):
        '''
            获取给定资产的依赖
        :return:
        '''
        depAssets.append(pkgPath)
        areOpt = unreal.AssetRegistryDependencyOptions()
        areHelp = unreal.AssetRegistryHelpers()
        are = areHelp.get_asset_registry()
        for unit in are.get_dependencies(pkgPath, areOpt):
            unit = str(unit)
            if unit not in depAssets:
                if not unit.startswith("/Engine") and not unit.startswith("/Script"):
                    self.getDepAssets(unit, depAssets)

    def MigrateAssets(self, assets, dstRootDir):
        '''
            迁移资产
        :return:
        '''
        self.depAssets = list()
        self.getDepAssets(assets, self.depAssets)
        self.depAssets = list(set(self.depAssets))
        dstRootDir = dstRootDir.replace("\\", "/")
        quantity_steps_in_slow_task = len(self.depAssets)
        if not self.depAssets:
            return
        with unreal.ScopedSlowTask(quantity_steps_in_slow_task, u"正在导出中....") as slow_task:
            slow_task.make_dialog(True)
            for index, unit in enumerate(self.depAssets):
                if slow_task.should_cancel():
                    break
                # 进入循环帧
                slow_task.enter_progress_frame(1, u"正在导出中...." + str(index) + "/" + str(quantity_steps_in_slow_task))
                unit = str(unit)
                unreal.EditorAssetLibrary.save_asset(unit, True)
                proDir = os.path.abspath(unreal.Paths.project_dir()).replace("\\", "/")
                if str(unit).startswith("/Game"):
                    objPath = "/Content/" + unit[5:]+ ".uasset"
                else:
                    # objPath = str(unit)
                    return
                src = proDir + objPath
                # objPath = objPath[:lstrip("/Content")]
                objPath = objPath[8:]
                dst = dstRootDir + "/" + objPath
                if not os.path.exists(os.path.dirname(dst)):
                    os.makedirs(os.path.dirname(dst))
                if not os.path.exists(src):
                    continue
                shutil.copy2(src, dst)

    def exportAsset(self):
        '''
            从ue4的内容编辑器导出对应资源
        :return: 状态
        '''
        exportRootPath = getLibPath()
        if not exportRootPath:
            unreal.log_warning(u"没有启动资产库软件")
            QMessageBox.warning(self, u"警告", u"没有启动资产库软件")
            return
        exportRootPath = exportRootPath.decode('gbk')

        allAssetInfos = self.getAssetPath()
        if not allAssetInfos:
            unreal.log_warning(u"没有选择需要导出的资源")
            QMessageBox.warning(self, u"警告", u"没有选择需要导出的资源")
            return

        screenshotPath = ""
        if self.btnGrp.checkedId() == 22:
            screenshotPath = screen_grap.displaySceenshot(unreal=unreal)

        errorFile = list()

        for asset in allAssetInfos:
            assetPathDir = os.path.join(exportRootPath, "file", asset["name"])
            if not os.path.exists(assetPathDir):
                os.makedirs(assetPathDir)
            assetIconDir = os.path.join(exportRootPath, "icon")
            if not os.path.exists(assetIconDir):
                os.makedirs(assetIconDir)
            assetIconPath = os.path.join(assetIconDir, asset["name"] + ".png")

            assetPathFilename = os.path.join(assetPathDir, asset["name"] + ".fbx")
            fbxOpt = unreal.FbxExportOption()
            fbxOpt.collision = False
            task = self.buildExportTask(asset["object_path"], assetPathFilename, fbxOpt)
            result = unreal.Exporter.run_asset_export_task(task)
            if not result:
                errorFile.append(task.filename)
                unreal.log_error("Failed to export {}".format(task.filename))
                for error_msg in task.errors:
                    unreal.log_error("{}".format(error_msg))
                continue
            if screenshotPath:
                shutil.copy2(screenshotPath, assetIconPath)
            else:
                isOk = unreal.CustomBlueprintFunctionLibrary.export_thubnail_texture2d(asset['object'], assetIconPath.replace(".png", ".jpg"))
                if not isOk:
                    unreal.log_error(u"导出缩略图失败")
                    continue
            self.MigrateAssets(asset["package_name"], assetPathDir)
        if errorFile:
            unreal.CustomBlueprintFunctionLibrary.message_dialog("Failed to export {}".format("\n".join(errorFile)))


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ew = ExportAssetWindow()
    unreal.parent_external_window_to_slate(ew.winId())
    ew.show()
