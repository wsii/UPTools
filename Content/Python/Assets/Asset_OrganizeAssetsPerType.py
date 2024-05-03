#										_
#									   (_)
#  _ __ ___   __ _ _ __ ___   ___  _ __  _  ___ _ __ ___
# | '_ ` _ \ / _` | '_ ` _ \ / _ \| '_ \| |/ _ \ '_ ` _ \
# | | | | | | (_| | | | | | | (_) | | | | |  __/ | | | | |
# |_| |_| |_|\__,_|_| |_| |_|\___/|_| |_|_|\___|_| |_| |_|
#					www.mamoniem.com
#					  www.ue4u.xyz
#Copyright 2022 Muhammad A.Moniem (@_mamoniem). All Rights Reserved.
#

import unreal

# 获取content 选中的文件夹路径
selected_folders = unreal.EditorUtilityLibrary.get_selected_folder_paths()

selected_folders_count = 0

if (len(selected_folders) > 0):
    selected_folders_count = len(selected_folders)
else:
    #获取path_view 选中的文件夹路径
    selected_folders = unreal.EditorUtilityLibrary.get_selected_path_view_folder_paths()
    selected_folders_count = len(selected_folders)

print(selected_folders)

# workingPath = "/Game/"
workingPath = selected_folders[0]


@unreal.uclass()
class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
    pass

editorAssetLib = GetEditorAssetLibrary()

allAssets = editorAssetLib.list_assets(workingPath, True, False)
allAssetsCount = len(allAssets)

selectedAssetPath = workingPath

with unreal.ScopedSlowTask(allAssetsCount, selectedAssetPath) as slowTask:
    slowTask.make_dialog(True)
    for asset in allAssets:
        _assetData = editorAssetLib.find_asset_data(asset)
        _assetName = _assetData.get_asset().get_name()
        _assetPathName = _assetData.get_asset().get_path_name()
        _assetClassName = _assetData.get_asset().get_class().get_name()

        _targetPathName = workingPath+"%s%s%s%s%s%s" % ("/",_assetClassName, "/", _assetName, ".", _assetName)


        editorAssetLib.rename_asset(_assetPathName, _targetPathName)

        if slowTask.should_cancel():
            break
        slowTask.enter_progress_frame(1, asset)