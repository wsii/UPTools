import unreal


def enable_virtualtexture_stream (textrue_asset):

    print(textrue_asset)
    textrue_asset.set_editor_property("virtual_texture_streaming",True)
    # print(static_mesh.get_editor_property("nanite_settings"))
    unreal.EditorAssetLibrary.save_loaded_asset(textrue_asset)
# 获取路径中所有资源的列表。


# 将它们全部装入内存。
# all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]

utilityBase = unreal.GlobalEditorUtilityBase.get_default_object()
all_assets = utilityBase.get_selected_assets()
# 过滤该列表，使之只包含材质贴图。
static_texture_assets = unreal.EditorFilterLibrary.by_class(all_assets, unreal.Texture)
# 在列表中的每个静态网格体上运行上面的函数。
list(map(enable_virtualtexture_stream, static_texture_assets))