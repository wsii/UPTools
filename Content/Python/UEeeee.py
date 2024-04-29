# coding:utf-8
# 导入预先准备好的相机文件

import unreal
import os


def addLiveLinkSourece():
    # 判断livelink源是否已添加成功
    
    sourceSubname = []
    source = unreal.LiveLinkComponent()
    sourceSubname = source.get_available_subject_names()
    if len(sourceSubname) == 0:
        loginName = os.getlogin()
        macName = loginName.upper() 
        # livelink连接源机器
        provid = unreal.ProviderPollResult()
        provid.set_editor_property("machine_name",macName) 
        # provid.get_editor_property("machine_name") 
        provid.set_editor_property("name", "Maya Live Link MessageBus") 
        provid_source = unreal.LiveLinkMessageBusFinder.connect_to_provider(provid) 
    else:
        pass


def copyLiveLinkPack():
    # 文件放入指定的路径中
    path = unreal.Paths.project_content_dir() 
    liveLinkpath = os.path.join(path,"LiveLink_pack")
    if not os.path.exists(liveLinkpath):
        os.makedirs(liveLinkpath)

    livelinkCAMpath = "L:\Technology\Module\LiveLink_pack"
    cmd = 'xcopy "%s" "%s" /c /d /s /f /i /y'%(livelinkCAMpath.replace("/","\\"),liveLinkpath.replace("/","\\"))
    # print(cmd)
    os.system(cmd)



def creatActorObj(actor_obj,new_actor_label):
    actorLocation = unreal.Vector(0,0,0)
    actorRotation = unreal.Rotator(0,0,0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(actor_obj,actorLocation,actorRotation)
    actor.set_actor_label(new_actor_label, mark_dirty=True)
    return  actor

def  creatActorClass(actor_class =unreal.Actor):
    # 创建一个actor
    actor_location = unreal.Vector(0.0, 0.0, 0.0)
    actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    actor_c = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class,actor_location,actor_rotation)
    actor_c.set_mobility(unreal.ComponentMobility.MOVABLE)
    return actor_c



def  loadAsset(path,new_actor_label):
    actor_obj = unreal.EditorAssetLibrary.load_asset(path)
    actor = creatActorObj(actor_obj,new_actor_label)
    actor.set_actor_label(new_actor_label, mark_dirty=True)
    return  actor


def addLiveLinkCamBP(actor_name):
    # 相机无法设置可移动
    # 直接链接Maya的livelink
    # Maya相机名称对应UE对应名称
    path = "/Game/livelink_pack/aLiveLink_Cam_BP"
    role_type = unreal.LiveLinkCameraRole
    actor = loadAsset(path,actor_name)
    addLiveLinkComponent(actor,actor_name,role_type,is_cam=True)


def addVfxshiyi(actor_name):
    # 添加特效示意
    # 直接链接Maya的livelink
    role_type = unreal.LiveLinkTransformRole
    path = "/Game/LiveLink_pack/vfxshiyi/vfxshiyi"
    actor = loadAsset(path,actor_name)
    actor.set_mobility(unreal.ComponentMobility.MOVABLE)

    addLiveLinkComponent(actor,actor_name,role_type,is_cam=False)

# 创建livelink 并设置对应的subject Representation
def addLiveLinkComponent(actor,actor_name,role_type,is_cam=False):
    if is_cam == False:
        so_subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        # ------选中的actor对象----------
        # actor =  unreal.VRScoutingInteractor.get_selected_actors()[0]
        root_sub_object = so_subsystem.k2_gather_subobject_data_for_instance(actor)[0]
        new_class=unreal.LiveLinkComponentController
        new_sub_object = so_subsystem.add_new_subobject(unreal.AddNewSubobjectParams(
            parent_handle=root_sub_object,
            new_class=new_class,
        ))

    actor_comp= actor.get_components_by_class(unreal.LiveLinkComponentController)[0]
    link_subname = unreal.LiveLinkSubjectName(actor_name)
    # unreal.LiveLinkCameraRole 相机切换角色    unreal.LiveLinkTransformRole  变换      光照 unreal.LiveLinkLightRole
    actor_add_comp = unreal.LiveLinkSubjectRepresentation(subject=link_subname,role=role_type)
    actor_comp.subject_representation = actor_add_comp




    # 创建light
def creatLightShiYi(light_node_type,light_name):
    # maya中的灯光name
    role_type = unreal.LiveLinkLightRole
    # 平行光
    if light_node_type == "directionalLight":
        light_type = unreal.DirectionalLight
    elif light_node_type == "pointLight":
        light_type = unreal.PointLight
    elif light_node_type == "spotLight":
        light_type = unreal.SpotLight 
    elif light_node_type == "areaLight":
        # 区域光
        light_type = unreal.RectLight
    light_actor = creatActorClass(actor_class =light_type)
    light_actor.set_mobility(unreal.ComponentMobility.MOVABLE)
    # 添加对应的light livelink
    addLiveLinkComponent(light_actor,light_name,role_type,is_cam=False)  


def creatText(text_name):
    # 文字
    role_type = unreal.LiveLinkTransformRole
    actor_class = unreal.TextRenderActor
    text_actor = creatActorClass(actor_class=actor_class)
    
    text_actor.set_mobility(unreal.ComponentMobility.MOVABLE)
    text_actor.set_actor_label(text_name, mark_dirty=True)
    # 添加对应的light livelink
    addLiveLinkComponent(text_actor,text_name,role_type,is_cam=False)  
    



def staticActorAddToActor(actor,parent_actor):
    # 设置actor的可移动属性
    actor.set_mobility(unreal.ComponentMobility.MOVABLE)
    # 获取actor的名字(-----------)
    # actorName= actor.get_actor_label(create_if_none=True)
    socket_name= unreal.Name()
    location_rule= unreal.AttachmentRule.KEEP_RELATIVE
    rotation_rule = unreal.AttachmentRule.KEEP_WORLD
    scale_rule = unreal.AttachmentRule.KEEP_WORLD
    weld_simulated_bodies = True
    # 将staticActor添加到acotr下面
    actor.attach_to_actor(parent_actor, socket_name, location_rule, rotation_rule, scale_rule, weld_simulated_bodies)



def run():

    # addLiveLinkSourece()
    copyLiveLinkPack()
    # livelink-Maya连接显示
    livelink_Component = unreal.LiveLinkComponent()
    subject_name_list = livelink_Component.get_available_subject_names()
    # 获取大纲里面的actor 类型staticmesh、获取源文件路径
    all_actor= unreal.EditorUtilityLibrary.get_selected_assets()
    # 获取大纲里面的actor 类型staticMeshActor
    get_actor_all= unreal.EditorLevelLibrary.get_all_level_actors()
    all_lebal_actor = list()
    # 获取所有的大纲里面显示的actor
    for a in get_actor_all:
        lablename=a.get_actor_label(create_if_none=True)
        if lablename not in all_lebal_actor:
            all_lebal_actor.append(lablename)

    for sn in subject_name_list:
        str_sn = str(sn)
        str_sn_low = str_sn.lower()
        # 获取大纲视图里面的actor   
        if str_sn != "EditorActiveCamera":
            # 创建相机、灯光、示意
            if str_sn not in all_lebal_actor:
                if "cut" in str_sn_low:
                    addLiveLinkCamBP(str_sn)
                # print(str_sn,"----------------",i)
                if "light" in str_sn_low:
                    light_node_type = ""
                    if "directionallight" in str_sn_low:
                        light_node_type = "directionalLight"
                    if "pointlight" in str_sn_low:
                        light_node_type = "pointLight"
                    if "spotlight" in str_sn_low:
                        light_node_type = "spotLight"
                    if "arealight" in str_sn_low:
                        light_node_type = "areaLight"
                    if light_node_type != "":
                        creatLightShiYi(light_node_type,str_sn)

                if "shiyi" in str_sn_low:
                    # print("shiyi")
                    addVfxshiyi(str_sn)

                if "text" in str_sn_low:
                    creatText(str_sn)


        for a in get_actor_all:
            parent_actor = a.get_attach_parent_actor()
            actor_lable_name = "" 
            # print(type)
            if parent_actor == None:
                actor_lable_name = a.get_actor_label(create_if_none=True)
                _lableName = actor_lable_name.split("_")[0]+"_"
                # print(_lableName)
                str_sn_lable =_lableName +  str_sn.split(":")[-1]
                # print("str_sn_lable",str_sn_lable)
                if actor_lable_name == str_sn_lable:
                    proxy_actor = creatActorClass()
                    try:
                        staticActorAddToActor(a,proxy_actor)
                        role_type = unreal.LiveLinkTransformRole
                        addLiveLinkComponent(proxy_actor,sn,role_type)
                    except:
                        pass


run()
