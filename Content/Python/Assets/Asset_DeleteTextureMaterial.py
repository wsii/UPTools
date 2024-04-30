import unreal

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# 获取当前编辑器选择的文件夹路径列表
selected_folders = unreal.EditorUtilityLibrary.get_selected_folder_paths()

asset_list = asset_registry.get_assets_by_path(selected_folders[0],True)

processingAssetPath = ""

allAssetsCount = len(selected_folders)
if ( allAssetsCount > 0):
    with unreal.ScopedSlowTask(allAssetsCount, processingAssetPath) as slowTask:
        slowTask.make_dialog(True)
        for item in asset_list:
            processingAssetPath = item
            print (">>> Deleting >>> %s" % item)
            if item.asset_class == "Texture2D" :
                # unreal.EditorAssetLibrary.delete_asset.delete_asset(item)
                print (">>> Deleting >>> %s" % item)
            
            if item.asset_class == "Material" :
                # unreal.EditorAssetLibrary.delete_asset.delete_asset(item)
                print (">>> Deleting >>> %s" % item)

            if item.asset_class == "MaterialInstance" :
                # unreal.EditorAssetLibrary.delete_asset.delete_asset(item)
                print (">>> Deleting >>> %s" % item)

            if slowTask.should_cancel():
                break
            slowTask.enter_progress_frame(1, processingAssetPath)