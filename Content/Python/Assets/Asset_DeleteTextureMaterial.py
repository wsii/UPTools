#5.3 删除贴图、材质
import unreal

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# 获取content 选中的文件夹路径
selected_folders = unreal.EditorUtilityLibrary.get_selected_folder_paths()
# class_path_texture = unreal.TopLevelAssetPath('/Script/Engine', 'Texture2D')
# class_path_material = unreal.TopLevelAssetPath('/Script/Engine', 'Material')
# class_path_materialInstance = unreal.TopLevelAssetPath('/Script/Engine', 'MaterialInstance')

processingAssetPath = ""

selected_folders_count = 0

if (len(selected_folders) > 0):
    selected_folders_count = len(selected_folders)
else:
    #获取path_view 选中的文件夹路径
    selected_folders = unreal.EditorUtilityLibrary.get_selected_path_view_folder_paths()
    selected_folders_count = len(selected_folders)

print(selected_folders)

# 要删除的资源类型
delete_assets_type = ['Texture2D','Material','MaterialInstanceConstant']

if ( selected_folders_count> 0):
    #遍历选中的文件夹
    for i in range(selected_folders_count):
        #获取文件夹下的所有资源
        asset_list = asset_registry.get_assets_by_path(selected_folders[i],True)

        with unreal.ScopedSlowTask(selected_folders_count, processingAssetPath) as slowTask:
            slowTask.make_dialog(True)
            for item in asset_list:

                
                if item.asset_class_path.asset_name in delete_assets_type:
                    processingAssetPath = item.get_full_name()
                    print (">>> Deleting >>> %s" % processingAssetPath)
                    unreal.EditorAssetLibrary.delete_asset(item.package_name)

                if slowTask.should_cancel():
                    break

                slowTask.enter_progress_frame(1, processingAssetPath)



