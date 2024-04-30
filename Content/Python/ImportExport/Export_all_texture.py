#4.27 ExportTexture
import unreal
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
asset_data_list = asset_registry.get_assets_by_path("/Game",True)
# export_path = 'D:/ExportedTextures/'
export_path = 'D:/ExportedMeshes/'
tex_list = []
for item in asset_data_list:
    if item.asset_class == "Texture2D" :
        tex_list.append(item.package_name)
        # print(item)
        
unreal.AssetToolsHelpers.get_asset_tools().export_assets(tex_list, export_path)


#4.27 ExportMesh
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
asset_data_list = asset_registry.get_assets_by_path("/Game",True)
export_path = 'D:/ExportedMeshes/'
tex_list = []
for item in asset_data_list:
    if item.asset_class == "StaticMesh" :
        tex_list.append(item.package_name)
        # print(item)
        
unreal.AssetToolsHelpers.get_asset_tools().export_assets(tex_list, export_path)


# assetTools = unreal.AssetToolsHelpers.get_asset_tools()

import unreal

def export_textures_to_tex():
    # 获取所有纹理资产
    texture_assets = unreal.EditorAssetLibrary.list_assets('/Game', unreal.Texture2D)

    print(texture_assets)
    
    # 导出每个纹理资产为 FBX 文件
    for texture_asset in texture_assets:
        export_path = '/Game/ExportedTextures/' + texture_asset.get_name() + '.tag'
        unreal.EditorAssetLibrary.export_assets([texture_asset], export_path)

export_textures_to_tex()


import unreal

def traverse_texture_assets():
    # 获取所有纹理资产
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    class_path = unreal.TopLevelAssetPath('/Script/Engine', 'Texture2D')
    # class_path = unreal.TopLevelAssetPath('/Script/Engine', 'StaticMesh')
    # asset_data_list = asset_registry.get_assets_by_class(unreal.Texture2D)
    asset_data_list = asset_registry.get_assets_by_class(class_path)

    # 遍历每个纹理资产
    for asset_data in asset_data_list:
        asset_path = asset_data.get_asset().get_full_name()
        print(f"Texture Asset: {asset_path}")

traverse_texture_assets()



asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
path = unreal.TopLevelAssetPath('/Script/Engine', 'StaticMesh')
assets = asset_registry.get_assets_by_class(path)
print(assets)






print(asset_data_list)

texture_assets = unreal.EditorAssetLibrary.list_assets('/Game', unreal.Texture2D)

print(texture_assets)