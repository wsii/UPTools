import unreal


def createMatGrap(mat):
    '''
        创建材质网络
    :return:
    '''
    unreal.MaterialEditingLibrary.delete_all_material_expressions(mat)
    # 创建基础颜色网络
    texExpressionDiff = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                 unreal.MaterialExpressionTextureSampleParameter2D,
                                                                                 -800, -500)
    multiplyExpDiff = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply,
                                                                               -500, -500)
    staticSwitchParExpDiff = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                      unreal.MaterialExpressionStaticSwitchParameter,
                                                                                      -300, -500)
    vecParExpInt = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                            unreal.MaterialExpressionVectorParameter,
                                                                            -500, -400)
    vecParExpValue = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                              unreal.MaterialExpressionVectorParameter,
                                                                              -300, -400)
    # grpExpDiff = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionComment, -850,
    #                                                                       -550)
    # 设置默认值
    # grpExpDiff.set_editor_property("text", u"基础颜色")
    texExpressionDiff.set_editor_property("texture", None)
    texExpressionDiff.set_editor_property("group", u"基础颜色")
    texExpressionDiff.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
    texExpressionDiff.set_editor_property("parameter_name", "diffmap")
    vecParExpInt.set_editor_property("default_value", unreal.LinearColor(1.0, 1.0, 1.0, 0.0))
    vecParExpInt.set_editor_property("parameterName", "diffint")
    vecParExpInt.set_editor_property("group", u"基础颜色")
    vecParExpValue.set_editor_property("default_value", unreal.LinearColor(0.0, 0.0, 0.0, 0.0))
    vecParExpValue.set_editor_property("parameterName", "DiffuseValue")
    vecParExpValue.set_editor_property("group", u"基础颜色")
    staticSwitchParExpDiff.set_editor_property("parameterName", "UseDiffuseMap?")
    staticSwitchParExpDiff.set_editor_property("group", u"基础颜色")

    # 连接表达式
    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionDiff, "RGB", multiplyExpDiff, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(vecParExpInt, "", multiplyExpDiff, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(multiplyExpDiff, "", staticSwitchParExpDiff, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(vecParExpValue, "", staticSwitchParExpDiff, "False")
    unreal.MaterialEditingLibrary.connect_material_property(staticSwitchParExpDiff, "",
                                                            unreal.MaterialProperty.MP_BASE_COLOR)

    # 创建金属反射网络
    texExpressionMet = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                unreal.MaterialExpressionTextureSampleParameter2D,
                                                                                -1600, 500)
    mulExpMet = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply, -500,
                                                                         -100)
    scaParValue1Exp = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                               unreal.MaterialExpressionScalarParameter,
                                                                               -500, 0)
    staticSwitchParExpMet = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                     unreal.MaterialExpressionStaticSwitchParameter,
                                                                                     -300, -100)
    scaParValue0Exp = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                               unreal.MaterialExpressionScalarParameter,
                                                                               -300, 0)
    # 设置默认值
    texExpressionMet.set_editor_property("texture", None)
    texExpressionMet.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
    texExpressionMet.set_editor_property("parameter_name", "MetallicMap")
    texExpressionMet.set_editor_property("group", u"金属反射")
    scaParValue1Exp.set_editor_property("parameter_name", "MetallicMultiply")
    scaParValue1Exp.set_editor_property("default_value", 1.0)
    scaParValue1Exp.set_editor_property("group", u"金属反射")
    scaParValue0Exp.set_editor_property("parameter_name", "MetallicValue")
    scaParValue0Exp.set_editor_property("default_value", 0.0)
    scaParValue0Exp.set_editor_property("group", u"金属反射")
    staticSwitchParExpMet.set_editor_property("parameter_name", "UseMetallicMap?")
    staticSwitchParExpMet.set_editor_property("group", u"金属反射")
    # 连接表达式
    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionMet, "R", mulExpMet, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue1Exp, "", mulExpMet, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(mulExpMet, "", staticSwitchParExpMet, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue0Exp, "", staticSwitchParExpMet, "False")
    unreal.MaterialEditingLibrary.connect_material_property(staticSwitchParExpMet, "",
                                                            unreal.MaterialProperty.MP_METALLIC)

    # 创建高光网络
    texExpressionSpe = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                unreal.MaterialExpressionTextureSampleParameter2D,
                                                                                -800, 200)
    mulExpSpe = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply, -500,
                                                                         200)
    scaParValue0ExpSpe = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                  unreal.MaterialExpressionScalarParameter,
                                                                                  -500, 300)
    staticSwitchParExpSpe = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                     unreal.MaterialExpressionStaticSwitchParameter,
                                                                                     -300, 200)
    scaParValue1ExpSpe = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                  unreal.MaterialExpressionScalarParameter,
                                                                                  -300, 300)
    # 设置默认值
    texExpressionSpe.set_editor_property("texture", None)
    texExpressionSpe.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
    texExpressionSpe.set_editor_property("parameter_name", "HighlightsMap")
    texExpressionSpe.set_editor_property("group", u"高光")
    scaParValue0ExpSpe.set_editor_property("parameter_name", "HighlightsMultiply")
    scaParValue0ExpSpe.set_editor_property("default_value", 1.0)
    scaParValue0ExpSpe.set_editor_property("group", u"高光")
    staticSwitchParExpSpe.set_editor_property("parameter_name", "UseHighlightsMap?")
    staticSwitchParExpSpe.set_editor_property("group", u"高光")
    scaParValue1ExpSpe.set_editor_property("default_value", 0.5)
    scaParValue1ExpSpe.set_editor_property("parameter_name", "HighlightsValue")
    scaParValue1ExpSpe.set_editor_property("group", u"高光")

    # 连接表达式
    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionSpe, "RGB", mulExpSpe, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue0ExpSpe, "", mulExpSpe, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(mulExpSpe, "", staticSwitchParExpSpe, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue1ExpSpe, "", staticSwitchParExpSpe, "False")
    unreal.MaterialEditingLibrary.connect_material_property(staticSwitchParExpSpe, "",
                                                            unreal.MaterialProperty.MP_SPECULAR)

    # 创建粗糙度节点网络
    topMulExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply,
                                                                            -800, 500)
    scaParValue0ExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                  unreal.MaterialExpressionScalarParameter,
                                                                                  -800, 600)
    staticSwitchParExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                     unreal.MaterialExpressionStaticSwitchParameter,
                                                                                     -500, 500)
    scaParValue1ExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                  unreal.MaterialExpressionScalarParameter,
                                                                                  -500, 600)
    staticSwitchParExpDetaRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                         unreal.MaterialExpressionStaticSwitchParameter,
                                                                                         -300, 500)

    # texCoordExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
    #                                                                           unreal.MaterialExpressionTextureCoordinate,
    #                                                                           -1000, 700)
    # scaParValueTilExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
    #                                                                                 unreal.MaterialExpressionScalarParameter,
    #                                                                                 -1000, 800)
    # mulExpBtomRou = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply,
    #                                                                          -900, 700)
    texExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                         unreal.MaterialExpressionTextureSampleParameter2D,
                                                                         -800, 720)
    # oneMExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionOneMinus, -600,
    #                                                                       700)
    mulExpBtom2Rou = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply,
                                                                              -500, 700)
    scaParValueStrExpRou = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                    unreal.MaterialExpressionScalarParameter,
                                                                                    -500, 800)
    # mulExpBtom3Rou = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply,
    #                                                                           -300, 700)
    # 设置默认值
    scaParValue0ExpRou.set_editor_property("parameter_name", "RoughnesMultiply")
    scaParValue0ExpRou.set_editor_property("default_value", 1.0)
    scaParValue0ExpRou.set_editor_property("group", u"粗糙度")
    staticSwitchParExpRou.set_editor_property("parameter_name", "UseRoughnessMap?")
    staticSwitchParExpRou.set_editor_property("group", u"粗糙度")
    scaParValue1ExpRou.set_editor_property("parameter_name", "RoughnesValue")
    scaParValue1ExpRou.set_editor_property("default_value", 0.5)
    scaParValue1ExpRou.set_editor_property("group", u"粗糙度")
    staticSwitchParExpDetaRou.set_editor_property("parameter_name", "UseDetaRoughnessMap?")
    staticSwitchParExpDetaRou.set_editor_property("group", u"粗糙度")
    # scaParValueTilExpRou.set_editor_property("parameter_name", "RoughnessTiling")
    # scaParValueTilExpRou.set_editor_property("default_value", 1.0)
    # scaParValueTilExpRou.set_editor_property("group", u"粗糙度")
    texExpRou.set_editor_property("texture", None)
    texExpRou.set_editor_property("parameter_name", "DetailRoughnessMap")
    texExpRou.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
    texExpRou.set_editor_property("group", u"粗糙度")
    scaParValueStrExpRou.set_editor_property("parameter_name", "DetaRoughnessStrength")
    scaParValueStrExpRou.set_editor_property("default_value", 1.0)
    scaParValueStrExpRou.set_editor_property("group", u"粗糙度")

    # 连接表达式
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue0ExpRou, "", topMulExpRou, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(topMulExpRou, "", staticSwitchParExpRou, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue1ExpRou, "", staticSwitchParExpRou, "False")
    unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpRou, "", staticSwitchParExpDetaRou,
                                                               "False")
    # unreal.MaterialEditingLibrary.connect_material_expressions(texCoordExpRou, "", mulExpBtomRou, "A")
    # unreal.MaterialEditingLibrary.connect_material_expressions(scaParValueTilExpRou, "", mulExpBtomRou, "B")
    # unreal.MaterialEditingLibrary.connect_material_expressions(mulExpBtomRou, "", texExpRou, "UVs")
    # unreal.MaterialEditingLibrary.connect_material_expressions(texExpRou, "RGB", oneMExpRou, "")
    unreal.MaterialEditingLibrary.connect_material_expressions(texExpRou, "RGB", mulExpBtom2Rou, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValueStrExpRou, "", mulExpBtom2Rou, "B")
    # unreal.MaterialEditingLibrary.connect_material_expressions(mulExpBtom2Rou, "", mulExpBtom3Rou, "B")
    # unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpRou, "", mulExpBtom3Rou, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(mulExpBtom2Rou, "", staticSwitchParExpDetaRou, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionMet, "G", topMulExpRou, "A")
    unreal.MaterialEditingLibrary.connect_material_property(staticSwitchParExpDetaRou, "",
                                                            unreal.MaterialProperty.MP_ROUGHNESS)

    # 创建材质ooc网络
    mulExpAo = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply, -600,
                                                                        1000)
    scaParValue0ExpAo = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                 unreal.MaterialExpressionScalarParameter,
                                                                                 -600, 1100)
    staticSwitchParExpAo = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                    unreal.MaterialExpressionStaticSwitchParameter,
                                                                                    -300, 1000)
    scaParValue1ExpAo = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                 unreal.MaterialExpressionScalarParameter,
                                                                                 -300, 1100)
    scaParValue0ExpAo.set_editor_property("parameter_name", "OCCMultiply")
    scaParValue0ExpAo.set_editor_property("default_value", 1.0)
    scaParValue0ExpAo.set_editor_property("group", "occ")
    staticSwitchParExpAo.set_editor_property("parameter_name", "UseOCCMap?")
    staticSwitchParExpAo.set_editor_property("group", "occ")
    scaParValue1ExpAo.set_editor_property("parameter_name", "OCCValue")
    scaParValue1ExpAo.set_editor_property("default_value", 1.0)
    scaParValue1ExpAo.set_editor_property("group", "occ")

    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionMet, "B", mulExpAo, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue0ExpAo, "", mulExpAo, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(mulExpAo, "", staticSwitchParExpAo, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue1ExpAo, "", staticSwitchParExpAo, "False")
    unreal.MaterialEditingLibrary.connect_material_property(staticSwitchParExpAo, "",
                                                            unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)

    # 创建自发光节点网络
    texExpressionEm = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                               unreal.MaterialExpressionTextureSampleParameter2D,
                                                                               -1100, 1300)
    staticSwitchParExpEm = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                    unreal.MaterialExpressionStaticSwitchParameter,
                                                                                    -800, 1300)
    scaParValue0ExpEm = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                 unreal.MaterialExpressionScalarParameter,
                                                                                 -800, 1400)
    mulExpEm = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply, -600,
                                                                        1300)
    vecParmEm = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionVectorParameter,
                                                                         -600, 1400)
    staticSwitch2ParExpEm = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                     unreal.MaterialExpressionStaticSwitchParameter,
                                                                                     -400, 1300)
    numExpEm = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionConstant, -400,
                                                                        1400)
    texExpressionEm.set_editor_property("texture", None)
    texExpressionEm.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
    texExpressionEm.set_editor_property("parameter_name", "EmissiveMap")
    texExpressionEm.set_editor_property("group", u"自发光")
    staticSwitchParExpEm.set_editor_property("parameter_name", "UseEmissiveMap?")
    staticSwitchParExpEm.set_editor_property("group", u"自发光")
    scaParValue0ExpEm.set_editor_property("parameter_name", "EmissiveScale")
    scaParValue0ExpEm.set_editor_property("default_value", 1.0)
    scaParValue0ExpEm.set_editor_property("group", u"自发光")
    vecParmEm.set_editor_property("parameter_name", "Emissivecolor")
    vecParmEm.set_editor_property("default_value", unreal.LinearColor(1.0, 1.0, 1.0, 0.0))
    vecParmEm.set_editor_property("group", u"自发光")
    staticSwitch2ParExpEm.set_editor_property("parameter_name", "UseEmissive?")
    staticSwitch2ParExpEm.set_editor_property("group", u"自发光")

    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionEm, "RGB", staticSwitchParExpEm, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValue0ExpEm, "", staticSwitchParExpEm, "False")
    unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpEm, "", mulExpEm, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(vecParmEm, "", mulExpEm, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(mulExpEm, "", staticSwitch2ParExpEm, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(numExpEm, "", staticSwitch2ParExpEm, "False")
    unreal.MaterialEditingLibrary.connect_material_property(staticSwitch2ParExpEm, "",
                                                            unreal.MaterialProperty.MP_EMISSIVE_COLOR)

    # 创建法线节点网络
    # texCoordExpNor = unreal.MaterialEditingLibrary.create_material_expression(mat,
    #                                                                           unreal.MaterialExpressionTextureCoordinate,
    #                                                                           -1300, 1700)
    # mulExp1Nor = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply, -1100,
    #                                                                       1700)
    # scaParValueTilExpNor = unreal.MaterialEditingLibrary.create_material_expression(mat,
    #                                                                                 unreal.MaterialExpressionScalarParameter,
    #                                                                                 -1100, 1800)
    texExpressionNor = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                unreal.MaterialExpressionTextureSampleParameter2D,
                                                                                -900, 1700)
    matFuncNor = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                          unreal.MaterialExpressionMaterialFunctionCall,
                                                                          -600, 1700)
    scaParValueStrExpNor = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                    unreal.MaterialExpressionScalarParameter,
                                                                                    -600, 1800)
    staticSwitchParExpNor = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                     unreal.MaterialExpressionStaticSwitchParameter,
                                                                                     -400, 1700)
    cons3dExpNor = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                            unreal.MaterialExpressionConstant3Vector,
                                                                            -400, 1800)
    # scaParValueTilExpNor.set_editor_property("parameter_name", "NormalTiling")
    # scaParValueTilExpNor.set_editor_property("default_value", 1.0)
    # scaParValueTilExpNor.set_editor_property("group", u"法线纹理")
    texExpressionNor.set_editor_property("parameter_name", "DetailNormalMap")
    texExpressionNor.set_editor_property("texture", None)
    texExpressionNor.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
    texExpressionNor.set_editor_property("group", u"法线纹理")
    texFuncAsset = unreal.load_asset("/Engine/Functions/Engine_MaterialFunctions01/Texturing/FlattenNormal")
    matFuncNor.set_editor_property("materialFunction", texFuncAsset)
    scaParValueStrExpNor.set_editor_property("parameter_name", "DetailNormalStrenqth")
    scaParValueStrExpNor.set_editor_property("default_value", 2.0)
    scaParValueStrExpNor.set_editor_property("group", u"法线纹理")
    staticSwitchParExpNor.set_editor_property("parameter_name", "UseNormale?")
    staticSwitchParExpNor.set_editor_property("group", u"法线纹理")
    cons3dExpNor.set_editor_property("constant", unreal.LinearColor(0.0, 0.0, 1.0))

    # unreal.MaterialEditingLibrary.connect_material_expressions(texCoordExpNor, "", mulExp1Nor, "A")
    # unreal.MaterialEditingLibrary.connect_material_expressions(scaParValueTilExpNor, "", mulExp1Nor, "B")
    # unreal.MaterialEditingLibrary.connect_material_expressions(mulExp1Nor, "", texExpressionNor, "UVs")
    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionNor, "RGB", matFuncNor, "Normal")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValueStrExpNor, "", matFuncNor, "Flatness")
    unreal.MaterialEditingLibrary.connect_material_expressions(matFuncNor, "", staticSwitchParExpNor, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(cons3dExpNor, "", staticSwitchParExpNor, "False")
    unreal.MaterialEditingLibrary.connect_material_property(staticSwitchParExpNor, "",
                                                            unreal.MaterialProperty.MP_NORMAL)

    # 创建贴图偏移节点网络
    texExpressionOffset = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                   unreal.MaterialExpressionTextureSampleParameter2D,
                                                                                   -2600, 500)
    bumpExpOffset = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                             unreal.MaterialExpressionBumpOffset,
                                                                             -2300, 500)
    scaParValueDepExpOffset = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                       unreal.MaterialExpressionScalarParameter,
                                                                                       -2300, 700)
    staticSwitchParExpOffset = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                        unreal.MaterialExpressionStaticSwitchParameter,
                                                                                        -2000, 500)
    texCoordExpOffset = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                 unreal.MaterialExpressionTextureCoordinate,
                                                                                 -2150, 700)
    scaParValueExpOffset = unreal.MaterialEditingLibrary.create_material_expression(mat,
                                                                                    unreal.MaterialExpressionScalarParameter,
                                                                                    -2200, 800)
    mulExpOffset = unreal.MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionMultiply,
                                                                            -2000,
                                                                            700)
    texExpressionOffset.set_editor_property("texture", None)
    texExpressionOffset.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
    texExpressionOffset.set_editor_property("parameter_name", "HeightMap")
    texExpressionOffset.set_editor_property("group", u"深度偏移")
    scaParValueDepExpOffset.set_editor_property("parameter_name", "ParallaxDepth")
    scaParValueDepExpOffset.set_editor_property("default_value", 0.0)
    scaParValueDepExpOffset.set_editor_property("group", u"深度偏移")
    staticSwitchParExpOffset.set_editor_property("parameter_name", "UseParallaxMap?")
    staticSwitchParExpOffset.set_editor_property("group", u"深度偏移")
    scaParValueExpOffset.set_editor_property("parameter_name", "Tiling")
    scaParValueExpOffset.set_editor_property("default_value", 1.0)
    scaParValueExpOffset.set_editor_property("group", u"深度偏移")

    unreal.MaterialEditingLibrary.connect_material_expressions(texExpressionOffset, "R", bumpExpOffset, "Height")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValueDepExpOffset, "", bumpExpOffset,
                                                               "HeightRatioInput")
    unreal.MaterialEditingLibrary.connect_material_expressions(bumpExpOffset, "", staticSwitchParExpOffset, "True")
    unreal.MaterialEditingLibrary.connect_material_expressions(mulExpOffset, "", staticSwitchParExpOffset, "False")
    unreal.MaterialEditingLibrary.connect_material_expressions(texCoordExpOffset, "", mulExpOffset, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(scaParValueExpOffset, "", mulExpOffset, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpOffset, "", texExpressionMet, "UVs")
    unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpOffset, "", texExpressionDiff, "UVs")
    unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpOffset, "", texExpressionEm, "UVs")
    unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpOffset, "", texExpressionNor, "UVs")
    unreal.MaterialEditingLibrary.connect_material_expressions(staticSwitchParExpOffset, "", texExpRou, "UVs")

    texNodes = {
        "Base_Color": texExpressionDiff,
        "Metallic": texExpressionMet,
        "Specular": texExpressionSpe,
        "Roughness": texExpRou,
        "Emissive_Color": texExpressionEm,
        "Normal": texExpressionNor,
        "Height": texExpressionOffset,
        "Base_Color_Value": vecParExpValue
    }
    return texNodes


if __name__ == '__main__':
    mat = unreal.load_asset('/Game/material/aa.aa')
    createMatGrap(mat)
