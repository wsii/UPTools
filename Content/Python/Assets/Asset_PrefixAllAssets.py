#										_
#									   (_)
#  _ __ ___   __ _ _ __ ___   ___  _ __  _  ___ _ __ ___
# | '_ ` _ \ / _` | '_ ` _ \ / _ \| '_ \| |/ _ \ '_ ` _ \
# | | | | | | (_| | | | | | | (_) | | | | |  __/ | | | | |
# |_| |_| |_|\__,_|_| |_| |_|\___/|_| |_|_|\___|_| |_| |_|
#					www.mamoniem.com
#					  www.ue4u.xyz
#Copyright 2022 Muhammad A.Moniem (@_mamoniem). All Rights Reserved.
#

import unreal

#You can set the prefix of your choice here
prefixAnimationBlueprint    = "ABP_"
prefixAnimationSequence     = "AS_"
prefixAnimation             = "A_"
prefixBlendSpace            = "BS_"
prefixBlueprint             = "BP_"
prefixCurveFloat            = "CF_"
prefixCurveLinearColor      = "CL_"
prefixLevel                 = "L_"
prefixMaterial              = "M_"
prefixMaterialFunction      = "MF_"
prefixMaterialInstance      = "MI_"
prefixParticleSystem        = "NS_"
prefixPhysicsAsset          = "PA_"
prefixSkeletalMesh          = "SKM_"
prefixSkeleton              = "SK_"
prefixSoundCue              = "SC_"
prefixSoundWave             = "SW_"
prefixStaticMesh            = "SM_"
prefixTexture2D             = "T_"
prefixTextureCube           = "HDRI_"


# 获取content 选中的文件夹路径
selected_folders = unreal.EditorUtilityLibrary.get_selected_folder_paths()

selected_folders_count = 0

if (len(selected_folders) > 0):
    selected_folders_count = len(selected_folders)
else:
    #获取path_view 选中的文件夹路径
    selected_folders = unreal.EditorUtilityLibrary.get_selected_path_view_folder_paths()
    selected_folders_count = len(selected_folders)

print(selected_folders)

# workingPath = "/Game/"
workingPath = selected_folders[0]

@unreal.uclass()
class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
    pass

def GetProperPrefix(className):
    _prefix = ""
    if className == "AnimBlueprint":
        _prefix = prefixAnimationBlueprint
    elif className == "AnimSequence":
        _prefix = prefixAnimationSequence
    elif className == "Animation":
        _prefix = prefixAnimation
    elif className == "BlendSpace1D":
        _prefix = prefixBlendSpace
    elif className == "Blueprint":
        _prefix = prefixBlueprint
    elif className == "CurveFloat":
        _prefix = prefixCurveFloat
    elif className == "CurveLinearColor":
        _prefix = prefixCurveLinearColor
    elif className == "Material":
        _prefix = prefixMaterial
    elif className == "MaterialFunction":
        _prefix = prefixMaterialFunction
    elif className == "MaterialInstance":
        _prefix = prefixMaterialInstance
    elif className == "ParticleSystem":
        _prefix = prefixParticleSystem
    elif className == "PhysicsAsset":
        _prefix = prefixPhysicsAsset
    elif className == "SkeletalMesh":
        _prefix = prefixSkeletalMesh
    elif className == "Skeleton":
        _prefix = prefixSkeleton
    elif className == "SoundCue":
        _prefix = prefixSoundCue
    elif className == "SoundWave":
        _prefix = prefixSoundWave
    elif className == "StaticMesh":
        _prefix = prefixStaticMesh
    elif className == "Texture2D":
        _prefix = prefixTexture2D
    elif className == "TextureCube":
        _prefix = prefixTextureCube
    else:
        _prefix = ""

    return _prefix

editorAssetLib = GetEditorAssetLibrary()

allAssets = editorAssetLib.list_assets(workingPath, True, False)
allAssetsCount = len(allAssets)

selectedAssetPath = workingPath

with unreal.ScopedSlowTask(allAssetsCount, selectedAssetPath) as slowTask:
    slowTask.make_dialog(True)
    for asset in allAssets:
        _assetData = editorAssetLib.find_asset_data(asset)
        _assetName = _assetData.get_asset().get_name()
        _assetPathName = _assetData.get_asset().get_path_name()
        _assetPathOnly = _assetPathName.replace((_assetName + "." + _assetName), "")
        _assetClassName = _assetData.get_asset().get_class().get_name()
        _assetPrefix = GetProperPrefix(_assetClassName)


        if _assetPrefix in _assetName:
            continue
        elif _assetPrefix == "":
            continue
        else:
            _targetPathName = _assetPathOnly + ("%s%s%s%s%s%s%s" % (_assetPrefix, "_", _assetName, ".", _assetPrefix, "_", _assetName))

            editorAssetLib.rename_asset(_assetPathName, _targetPathName)
            print (">>> Renaming [%s] to [%s]" % (_assetPathName, _targetPathName))

        if slowTask.should_cancel():
            break
        slowTask.enter_progress_frame(1, asset)