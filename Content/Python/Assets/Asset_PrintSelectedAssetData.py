#5.3 删除贴图、材质
import unreal

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# 获取当前编辑器选择的文件夹路径列表
selected_asset= unreal.EditorUtilityLibrary.get_selected_asset_data()
print(selected_asset)
