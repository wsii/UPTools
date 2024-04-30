# coding=utf-8
import json
import os

import unreal


def getLgtInfoFromMaya():
    filePath = os.path.join(os.environ["tmp"], "maya_lgt_location.json")
    if not os.path.exists(filePath):
        return
    with open(filePath) as f:
        lgtInfo = json.loads(f.read())
    return lgtInfo


def setLgtInfo():
    '''
        设置来自maya的灯光位置信息
    :return:
    '''
    lgtInfo = getLgtInfoFromMaya()
    if not lgtInfo:
        # unreal.CustomBlueprintFunctionLibrary.message_dialog("Unable to get light information from file")
        unreal.log_warning(u"没有灯光信息去设置")
        return
    for lgt in lgtInfo:
        locatorVec = unreal.Vector(lgt["tx"], lgt["ty"], lgt["tz"])
        if lgt["type"] == "pointLight":
            actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),
                                                                    unreal.PointLight)
            isExist = False
            newActor = None
            for actor in actors:
                if actor.get_actor_label() == lgt["name"]:
                    isExist = True
                    newActor = actor
                    break
            if isExist:
                newActor.set_actor_location(locatorVec, False, False)
            else:
                newActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight, locatorVec)
                newActor.set_actor_label(lgt["name"])
            lightComp = newActor.get_editor_property("PointLightComponent")
            lightComp.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
        elif lgt["type"] == "spotLight":
            rotation = unreal.MathLibrary.conv_vector_to_rotator(unreal.Vector(lgt["rx"], lgt["ry"], lgt["rz"]))
            actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),
                                                                    unreal.SpotLight)
            isExist = False
            newActor = None
            for actor in actors:
                if actor.get_actor_label() == lgt["name"]:
                    isExist = True
                    newActor = actor
                    break
            if isExist:
                newActor.set_actor_location_and_rotation(locatorVec, rotation, False, False)
            else:
                newActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SpotLight, locatorVec, rotation)
                newActor.set_actor_label(lgt["name"])
            newActor.spot_light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
            if lgt.get("angle") is not None:
                newActor.spot_light_component.set_inner_cone_angle(lgt["angle"])
                newActor.spot_light_component.set_outer_cone_angle(lgt["outAngle"])
        elif lgt["type"] == "directionalLight":
            rotation = unreal.MathLibrary.conv_vector_to_rotator(unreal.Vector(lgt["rx"], lgt["ry"], lgt["rz"]))
            actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),
                                                                    unreal.DirectionalLight)
            isExist = False
            newActor = None
            for actor in actors:
                if actor.get_actor_label() == lgt["name"]:
                    isExist = True
                    newActor = actor
                    break
            if isExist:
                newActor.set_actor_location_and_rotation(locatorVec, rotation, False, False)
            else:
                newActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, locatorVec,
                                                                            rotation)
                newActor.set_actor_label(lgt["name"])
            lightComp = newActor.get_editor_property("DirectionalLightComponent")
            lightComp.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
        elif lgt["type"] == "areaLight":
            rotation = unreal.MathLibrary.conv_vector_to_rotator(unreal.Vector(lgt["rx"], lgt["ry"], lgt["rz"]))
            actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),
                                                                    unreal.RectLight)
            isExist = False
            newActor = None
            for actor in actors:
                if actor.get_actor_label() == lgt["name"]:
                    isExist = True
                    newActor = actor
                    break
            if isExist:
                newActor.set_actor_location_and_rotation(locatorVec, rotation, False, False)
            else:
                newActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.RectLight, locatorVec,
                                                                            rotation)
                newActor.set_actor_label(lgt["name"])
            lightComp = newActor.get_editor_property("RectLightComponent")
            lightComp.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
    # 删除文件
    filePath = os.path.join(os.environ["tmp"], "maya_lgt_location.json").replace("\\", "/")
    if os.path.exists(filePath):
        try:
            os.remove(filePath)
        except:
            unreal.log_error(u"删除灯光信息文件失败")


if __name__ == '__main__':
    setLgtInfo()
