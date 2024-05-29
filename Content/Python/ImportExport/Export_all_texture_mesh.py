
# 5.3

import unreal

import argparse
import sys

arg = sys.argv

# print("第一个参数：", arg[1])

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

mesh_class_path = unreal.TopLevelAssetPath('/Script/Engine', 'StaticMesh')
texture_class_path = unreal.TopLevelAssetPath('/Script/Engine', 'Texture2D')
asset_mesh_list = asset_registry.get_assets_by_class(mesh_class_path)
asset_texture_list = asset_registry.get_assets_by_class(texture_class_path)


asset_list = []
exprot_asset_list = []


# 获取content 选中的文件夹路径
selected_folders = unreal.EditorUtilityLibrary.get_selected_folder_paths()

processingAssetPath = ""

selected_folders_count = 0

if (len(selected_folders) > 0):
    selected_folders_count = len(selected_folders)
else:
    #获取path_view 选中的文件夹路径
    selected_folders = unreal.EditorUtilityLibrary.get_selected_path_view_folder_paths()
    selected_folders_count = len(selected_folders)

# print(selected_folders)

# 要导出的资源类型
assets_type = ['Texture2D','StaticMesh',]

if ( selected_folders_count> 0):
    #遍历选中的文件夹
    for i in range(selected_folders_count):
        #获取文件夹下的所有资源
        asset_list = asset_registry.get_assets_by_path(selected_folders[i],True)

        with unreal.ScopedSlowTask(selected_folders_count, processingAssetPath) as slowTask:
            slowTask.make_dialog(True)
            for item in asset_list:

                if item.asset_class_path.asset_name in assets_type:

                    processingAssetPath = item.get_full_name()
                    print (">>> Deleting full_name >>> %s" % processingAssetPath)
                    print (">>> package_name >>> %s" % item.package_name)
                    # unreal.EditorAssetLibrary.delete_asset(item.package_name)
                    exprot_asset_list.append(item.package_name)

                if slowTask.should_cancel():
                    break

                slowTask.enter_progress_frame(1, processingAssetPath)

#导出路径
export_path = arg[1]
# export_path = 'D:/ExportedMeshes/'
        
unreal.AssetToolsHelpers.get_asset_tools().export_assets(exprot_asset_list, export_path)