"""
Asset : 资产  
object ： load(Asset) ===> Object 
Actor : == blueprint
"""
###
"""
unreal.EditorAssetLibrary  操作资产 (Asset)

unreal.EditorAssetLibrary.load_blueprint_class  操作类 (Class)

# Load a Blueprint asset from the Content Browser and return its generated class

unreal.EditorUtilityLibrary 操作actor 对象 (Object)


"""
###############资产Asset操作
##资源属性
assetInfos.append({
    "type": str(assetObj.asset_class),
    "object_path": str(assetObj.object_path),
    "name": str(assetObj.asset_name),
    "object": assetObj.get_asset(),
    "package_name": str(assetObj.package_name)
})
        


#加载模型
    objPath = "/Game/cube"
    mesh = unreal.EditorAssetLibrary.load_asset(objPath)
#获取材质
    i = 0
    while True:
        mat = mesh.get_material(i)
        if mat:
            allMats.append({"Material": mat, "Index": i})
        else:
            break
        i += 1
    return allMats

#获得单个材质
for matDict in allMats:
    mat = matDict["Material"]
    if mat.get_class().get_fname() == "MaterialInstance":
    #获取texture
    mat.texture_parameter_values.parameter_value

#获取贴图信息
    # print(tex.parameter_info.name)
    # print(dir(tex.parameter_value))
    # print(tex.parameter_value.get_path_name())
    #unreal.log_warning(tex["parameter_info"]["name"])

####################操作关卡中的Actor####################################
#获取关卡中的Actor
actors = unreal.EditorLevelLibrary.get_selected_level_actors()