import unreal

# {enabled: True, 
# preserve_area: False, 
# explicit_tangents: False, 
# position_precision: -2147483648, 
# normal_precision: -1, 
# tangent_precision: -1, 
# keep_percent_triangles: 1.000000, 
# trim_relative_error: 0.000000, 
# fallback_target: RelativeError, 
# fallback_percent_triangles: 1.000000, 
# fallback_relative_error: 1.000000, 
# displacement_uv_channel: 0}>


def edit_nanite (static_mesh):
    mesh_nanite_settings = unreal.MeshNaniteSettings()
    mesh_nanite_settings = static_mesh.get_editor_property("nanite_settings")
    mesh_nanite_settings.fallback_target = unreal.NaniteFallbackTarget.RELATIVE_ERROR
    mesh_nanite_settings.fallback_relative_error = 0

    # print(mesh_nanite_settings)
    static_mesh.set_editor_property("nanite_settings",mesh_nanite_settings)
    # print(static_mesh.get_editor_property("nanite_settings"))
    unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)
# 获取路径中所有资源的列表。


# 将它们全部装入内存。
# all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]

utilityBase = unreal.GlobalEditorUtilityBase.get_default_object()
all_assets = utilityBase.get_selected_assets()
# 过滤该列表，使之只包含静态网格体。
static_mesh_assets = unreal.EditorFilterLibrary.by_class(all_assets, unreal.StaticMesh)
# 在列表中的每个静态网格体上运行上面的函数。
list(map(edit_nanite, static_mesh_assets))