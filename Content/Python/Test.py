import unreal

fred_asset = unreal.EditorAssetLibrary.load_asset("/Script/Blutility.EditorUtilityWidgetBlueprint'/UPTools/EditorUtility/EUW_RunPy.EUW_RunPy'")

eus = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
tab = eus.spawn_and_register_tab(fred_asset)


print(tab)

