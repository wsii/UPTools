import unreal
import os

export_path = r"/Game/test"
root_package_path = "/Game/"
asset_data_array = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(root_package_path)
unreal.log(len(asset_data_array))


for asset_data in asset_data_array:
    asset_name = asset_data.get_editor_property('asset_name')
    path = os.path.join(export_path, "%s.tag" % asset_name)
    exporter = unreal.TextureExporterTGA()
    task = unreal.AssetExportTask()
    task.set_editor_property("object", asset_data.get_asset())
    task.set_editor_property("filename", path)
    task.set_editor_property("exporter", exporter)
    task.set_editor_property("automated", True)
    task.set_editor_property("prompt", False)
    task.set_editor_property("replace_identical", True)
    task.set_editor_property("write_empty_files", True)
    # task.set_editor_property("errors", errors)


    ret = unreal.Exporter.run_asset_export_task(task)
    unreal.log(ret)
    errors = task.get_editor_property("errors")
    unreal.log(errors)