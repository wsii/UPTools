import json
import os

import unreal


def getAllActors(actorClass=unreal.StaticMeshActor):
    '''
        获取指定类型的actor
    :return:
    '''
    actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(), actorClass)
    return actors


def writeAllLightInfo():
    '''
        获取灯光的位置信息
    :return:
    '''
    lgtInfo = list()
    selctedActor = unreal.EditorLevelLibrary.get_selected_level_actors()
    if selctedActor:
        pointLgt = list()
        directLgt = list()
        spotLgt = list()
        rectLgt = list()
        for ac in selctedActor:
            if ac.get_class().get_fname() == "RectLight":
                rectLgt.append(ac)
            elif ac.get_class().get_fname() == "DirectionalLight":
                directLgt.append(ac)
            elif ac.get_class().get_fname() == "SpotLight":
                spotLgt.append(ac)
            elif ac.get_class().get_fname() == "PointLight":
                pointLgt.append(ac)
    else:
        pointLgt = getAllActors(unreal.PointLight)
        directLgt = getAllActors(unreal.DirectionalLight)
        spotLgt = getAllActors(unreal.SpotLight)
        rectLgt = getAllActors(unreal.RectLight)
    if directLgt:
        for lgt in directLgt:
            locationVec = lgt.get_actor_location()
            rotateVec = lgt.get_actor_rotation()
            rotateXUnit = unreal.MathLibrary.conv_rotator_to_vector(rotateVec)
            name = lgt.get_actor_label()
            if not lgt.get_actor_label().endswith("_direct"):
                lgt.set_actor_label(name+"_direct")
                name += "_direct"
            
            lgtInfo.append({
                'type': "DirectionalLight",
                "tx": locationVec.x,
                "ty": -1 * locationVec.y,
                "tz": locationVec.z,
                "rx": rotateXUnit.x,
                "ry": -1 * rotateXUnit.y,
                "rz": rotateXUnit.z,
                "name": name
            })
    if rectLgt:
        for lgt in rectLgt:
            locationVec = lgt.get_actor_location()
            rotateVec = lgt.get_actor_rotation()
            rotateXUnit = unreal.MathLibrary.conv_rotator_to_vector(rotateVec)
            name = lgt.get_actor_label()
            if not lgt.get_actor_label().endswith("_rect"):
                lgt.set_actor_label(name + "_rect")
                name += "_rect"

            lgtInfo.append({
                'type': "RectLight",
                "tx": locationVec.x,
                "ty": -1 * locationVec.y,
                "tz": locationVec.z,
                "rx": rotateXUnit.x,
                "ry": -1 * rotateXUnit.y,
                "rz": rotateXUnit.z,
                "name": name
            })
    if spotLgt:
        for lgt in spotLgt:
            locationVec = lgt.get_actor_location()
            rotateVec = lgt.get_actor_rotation()
            rotateXUnit = unreal.MathLibrary.conv_rotator_to_vector(rotateVec)
            name = lgt.get_actor_label()
            if not lgt.get_actor_label().endswith("_spot"):
                lgt.set_actor_label(name+"_spot")
                name += "_spot"
            outAngle = lgt.spot_light_component.outer_cone_angle
            angle = lgt.spot_light_component.inner_cone_angle
            lgtInfo.append({
                'type': "SpotLight",
                "tx": locationVec.x,
                "ty": -1 * locationVec.y,
                "tz": locationVec.z,
                "rx": rotateXUnit.x,
                "ry": -1 * rotateXUnit.y,
                "rz": rotateXUnit.z,
                "name": name,
                "angle": -1*(outAngle-angle),
                "outAngle": outAngle*2,
            })
    if pointLgt:
        for lgt in pointLgt:
            locationVec = lgt.get_actor_location()
            name = lgt.get_actor_label()
            if not lgt.get_actor_label().endswith("_point"):
                lgt.set_actor_label(name+"_point")
                name += "_point"
            lgtInfo.append({
                "type": "PointLight",
                "tx": locationVec.x,
                "ty": -1 * locationVec.y,
                "tz": locationVec.z,
                "name": name
            })
    infoTxt = os.path.join(os.environ["tmp"], "ue_lgt_location.json")
    with open(infoTxt, "w") as f:
        f.write(json.dumps(lgtInfo, indent=4))


if __name__ == '__main__':
    writeAllLightInfo()
    # setLgtInfo()
