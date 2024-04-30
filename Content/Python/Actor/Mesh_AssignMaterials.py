import unreal


def getAllActors(actorClass=unreal.StaticMeshActor):
    '''
        获取指定类型的actor
    :return:
    '''
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if not actors:
        actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(), actorClass)
    return actors


def assignMaterials():
    '''
        指定材质
    :return:
    '''
    allSelObj = unreal.EditorUtilityLibrary.get_selected_asset_data()
    if not allSelObj:
        # unreal.CustomBlueprintFunctionLibrary.message_dialog("You need to select a material!")
        unreal.log_error(u"需要选择一个材质")
        return
    elif allSelObj[0].asset_class not in ["Material", "MaterialInstanceConstant"]:
        # unreal.CustomBlueprintFunctionLibrary.message_dialog("You need to select a material!")
        unreal.log_error(u"需要选择一个材质")
        return
    newMat = unreal.load_asset(allSelObj[0].object_path)
    actors = getAllActors()
    for actor in actors:
        if 'StaticMeshActor' not in str(actor.__class__):
            continue
        allMats = actor.static_mesh_component.get_materials()
        for mat in allMats:
            unreal.EditorLevelLibrary.replace_mesh_components_materials_on_actors([actor], mat, newMat)


if __name__ == '__main__':
    assignMaterials()
