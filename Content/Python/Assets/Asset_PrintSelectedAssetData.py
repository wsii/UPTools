#5.3 打印选中资产的数据
import unreal

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# 获取当前编辑器选择的文件夹路径列表
selected_asset= unreal.EditorUtilityLibrary.get_selected_asset_data()
print(selected_asset)
