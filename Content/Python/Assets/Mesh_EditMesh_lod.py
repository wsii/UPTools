import unreal

# 我们定义一个函数，该函数为指定的静态网格体资源生成新的LOD。
def apply_lods(static_mesh):
    # 检查网格体是否足够复杂。
    number_of_vertices = unreal.EditorStaticMeshLibrary.get_number_verts(static_mesh, 0)
    if number_of_vertices < 10:
        return
    # print("treating asset: " + static_mesh.get_name())
    # print("existing LOD count: " + str(unreal.EditorStaticMeshLibrary.get_lod_count(static_mesh)))
    # 设置用于自动生成细节层级的选项。
    options = unreal.EditorScriptingMeshReductionOptions()
    # 我们请求三个细节层级。各个细节层级拥有：
    # - 在该LOD层级上，应该保留来自详尽网格体的三角形的百分比
    # - 此细节层级会显示时的屏幕空间阈值。
    options.reduction_settings = [ unreal.EditorScriptingMeshReductionSettings(1.0, 1.0),
        # unreal.EditorScriptingMeshReductionSettings(0.8, 0.75),
        # unreal.EditorScriptingMeshReductionSettings(0.6, 0.5),
        unreal.EditorScriptingMeshReductionSettings(0.6, 0.25)
        # unreal.EditorScriptingMeshReductionSettings(0.4, 0.25),
        # unreal.EditorScriptingMeshReductionSettings(0.2, 0.1)
    ]
    # 使用上述设置的屏幕空间阈值，而非自动计算。
    options.auto_compute_lod_screen_size = False
    # 在静态网格体资源上设置选项。
    unreal.EditorStaticMeshLibrary.set_lods(static_mesh, options)
    # 保存更改。
    unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)
    print("new LOD count: " + str(unreal.EditorStaticMeshLibrary.get_lod_count(static_mesh)))
# 获取路径中所有资源的列表。


# 将它们全部装入内存。
# all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]

utilityBase = unreal.GlobalEditorUtilityBase.get_default_object()
all_assets = utilityBase.get_selected_assets()
# 过滤该列表，使之只包含静态网格体。
static_mesh_assets = unreal.EditorFilterLibrary.by_class(all_assets, unreal.StaticMesh)
# 在列表中的每个静态网格体上运行上面的函数。
list(map(apply_lods, static_mesh_assets))

