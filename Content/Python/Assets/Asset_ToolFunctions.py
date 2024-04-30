# coding=utf-8
import os
import unreal
import subprocess
import sys

# if os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage") not in sys.path:
#     sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage"))
#
# from PySide.QtGui import *


def importAssets(filename, destinationPath="/Game", type="ue_asset"):
    '''
        导入资产
    :return:
    '''
    filename = unicode(filename).encode("utf-8")
    token = filename.replace("\\", "/").split("/")
    for unit in token:
        if unit.endswith("_Maya"):
            type = "fbx"
            break

    if type == "fbx":
        tasks = list()
        objectPaths = list()
        tasks.append(generateFbxImportTask(filename, destinationPath))
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
        for task in tasks:
            unreal.log("Import Task for: " + task.filename)
            for objectPath in task.imported_object_paths:
                unreal.log("Imported object: " + objectPath)
                objectPaths.append(objectPath)
        return objectPaths
    else:
        importDirs = list()
        ueAsset = ""
        basename = os.path.basename(os.path.splitext(filename)[0])
        assetDir = os.path.dirname(filename)
        assetDir = assetDir.decode("utf-8")
        allDir = os.listdir(assetDir)
        if not allDir:
            return
        for unit in allDir:
            fullPath = os.path.join(assetDir, unit)
            if fullPath.endswith(".uasset"):
                importDirs.append(fullPath)
            elif os.path.isdir(fullPath):
                qu = False
                for rootDir, dir, filename in os.walk(fullPath):
                    for f in filename:
                        if f == basename + ".uasset":
                            ueAsset = os.path.join(rootDir, basename + ".uasset").replace("\\", "/")
                            importDirs.append(fullPath)
                            qu = True
                            break
                    if qu:
                        break
        if not importDirs:
            return
        importDirs = list(set(importDirs))
        for dir in importDirs:
            dir = dir.replace("\\", "/")
            basename = os.path.basename(dir)
            contentDir = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir())
            contentDir += basename
            cmd = "xcopy \"" + dir + "\" \"" + contentDir + "\" /i /e /y"
            # cmd = cmd.decode("utf-8").encode("gbk")
            cmd = cmd.encode("gbk")
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            stout, sterr = p.communicate()
            if sterr:
                unreal.log_error(sterr)
            if stout:
                unreal.log(stout)
            # try:
            #     shutil.copytree(filename, contentDir)
            # except:
            #     unreal.log_error("copy " + filename + " --> " + contentDir + " 失败")
        return [ueAsset, importDirs]


def generateFbxImportTask(filename, destinationPath, as_skeletal=False, import_animation=False):
    '''
        生成资产导入任务
    '''
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = destinationPath
    task.replace_existing = True
    task.automated = True
    task.save = True
    task.options = unreal.FbxImportUI()
    task.options.import_materials = True
    task.options.import_textures = True
    task.options.import_as_skeletal = as_skeletal
    task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    if as_skeletal:
        task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    return task


