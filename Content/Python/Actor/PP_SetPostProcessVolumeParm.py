import sys
import os

if os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage") not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyPackage"))

from PySide.QtGui import *

import unreal


class PostProcessSetParmWindow(QWidget):
    def __init__(self):
        super(PostProcessSetParmWindow, self).__init__()

        self.btnGrp = QButtonGroup()
        self.btnGrp.buttonClicked.connect(self.setBlendWeight)
        self.refreshBtn = QPushButton(u"刷新")
        self.refreshBtn.clicked.connect(self.handleRefresh)
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.refreshBtn)
        self.hLayout.addStretch()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.hLayout)

        self.setLayout(self.mainLayout)
        self.setWindowTitle(u"设置混合权重值")
        self.resize(260, 100)
        self.addRadioBtnGrp()

    def clearAllBtn(self):
        for index in range(len(self.btnGrp.buttons())):
            btn = self.btnGrp.button(index)
            self.btnGrp.removeButton(btn)

        for index in range(self.mainLayout.count(), 0, -1):
            item = self.mainLayout.itemAt(index)
            if item:
                item.widget().deleteLater()

    def handleRefresh(self):
        checkId = self.btnGrp.checkedId()
        if checkId == -1:
            self.clearAllBtn()
            self.addRadioBtnGrp()
            self.setBlendWeight()
            return
        button = self.btnGrp.button(checkId)
        oldNode = button.node
        self.clearAllBtn()
        self.addRadioBtnGrp()
        btnCount = len(self.btnGrp.buttons())
        for index in range(btnCount):
            btn = self.btnGrp.button(index)
            if btn.node == oldNode:
                btn.setChecked(True)
                break
        self.setBlendWeight()

    def setBlendWeight(self):
        '''
            设置属性值
        :return:
        '''
        btnCount = len(self.btnGrp.buttons())
        for index in range(btnCount):
            btn = self.btnGrp.button(index)
            if index == self.btnGrp.checkedId():
                self.setBlendWeightCmd(btn.node, 1)
            else:
                self.setBlendWeightCmd(btn.node, 0)

    def setBlendWeightCmd(self, actor, value):
        actor.set_editor_property("blend_weight", value)

    def addRadioBtnGrp(self):
        allNames = self.getAllPostProcessActors().keys()
        allNames.sort()
        for index, unit in enumerate(allNames):
            roBtn = QRadioButton(unit, self)
            roBtn.node = self.getAllPostProcessActors()[unit]
            self.btnGrp.addButton(roBtn, index)
            self.mainLayout.addWidget(roBtn)
            index += 1

    def getAllPostProcessActors(self):
        '''
            获取所有后期处理体积actor
        :return:
        '''
        actorinfo = dict()
        for actor in self.getAllActors():
            name = actor.get_actor_label()
            actorinfo[name] = actor
        return actorinfo

    def getAllActors(self):
        '''
            获取指定类型的actor
        :return:
        '''
        # actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        # if not actors:
        actors = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),
                                                                unreal.PostProcessVolume)
        return actors


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ps = PostProcessSetParmWindow()
    unreal.parent_external_window_to_slate(ps.winId())
    ps.show()
