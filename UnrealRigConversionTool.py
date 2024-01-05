#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Brandon Coffey
    Kira Smith

:synopsis:
    A tool to export maya rigs for use in Unreal Engine

:description:
    WIP

:applications:
    Maya

:see_also:
    N/A
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#


import maya.cmds as cmds


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#


def run():
    rigCreator = UnrealRig()
    rigCreator.init_gui()


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#


class UnrealRig:
    def __init__(self):
        self.windowName = 'unrealRigCreator'
        self.groupField = None
        self.jointsField = None
        self.joints = None
        self.geoField = None
        self.geo = None

    def init_gui(self):
        # Delete Existing Window if it Exists
        if cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName)

        # Create Window
        cmds.window(self.windowName,
                                  title='Unreal Rig Creator',
                                  widthHeight=(200, 400))

        # Content
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        cmds.separator(height=1)
        cmds.text(l='Group Name')
        self.groupField = cmds.textField(tx='Default')
        cmds.separator(height=10)
        cmds.text(l='Joints')
        self.jointsField = cmds.textField()
        cmds.button(l='Select Joints', command=self.select_joints)
        cmds.separator(height=10)
        cmds.text(l='Geo')
        self.geoField = cmds.textField()
        cmds.button(l='Select Geo', command=self.select_geo)
        cmds.separator(height=10)
        cmds.text(l='Rig')
        cmds.button(l='Create Rig', command=self.create_rig)
        cmds.button(l='Bind Skin', command=self.create_rig)
        cmds.separator(height=10)
        cmds.button(label='Close',
                    command=('cmds.deleteUI(\"' + self.windowName + '\", window=True)'))

        # Display Window
        cmds.showWindow(self.windowName)

    def select_joints(self, *args):
        selected = cmds.ls(selection=True)
        self.joints = cmds.listRelatives(selected, ad=True, type='joint')
        cmds.textField(self.jointsField, edit=True, tx=str(self.joints))

    def select_geo(self, *args):
        self.geo = cmds.ls(selection=True)
        cmds.textField(self.geoField, edit=True, tx=str(self.geo))

    def create_rig(self, *args):
        parent = self.verify_group()

        joints = self.joints
        unreal_joints = []
        for x in range(0, len(joints)):
            if not cmds.objExists(joints[x]):
                continue
            if cmds.objectType(joints[x], isType='joint') == 1:
                cmds.select(d=True)
                unreal_joint = cmds.joint(radius=0.15, name=('UNREAL' + joints[x]) )
                cmds.parent(unreal_joint, parent)
                cmds.parentConstraint(joints[x], unreal_joint)
                print(unreal_joint)
                unreal_joints.append(unreal_joint)

        geo = self.geo
        unreal_geos = []
        for x in range(0, len(geo)):
            cmds.select(d=True)
            unreal_geo = cmds.duplicate(geo[x])
            unreal_geo = cmds.rename(unreal_geo, 'UNREAL_' + geo[x])
            cmds.delete(unreal_geo, constructionHistory=True)
            cmds.parent(unreal_geo, parent)
            print(unreal_geo)
            unreal_geos.append(unreal_geo)

        print(unreal_joints)
        cmds.select(unreal_joints, unreal_geos)
        cmds.bindSkin( tsb=True)

    def verify_group(self):
        if not cmds.objExists('UNREAL'):
            cmds.createNode('transform', name='UNREAL')

        groupName = cmds.textField(self.groupField, q=True, text=1)
        if groupName:
            groupName = 'UNREAL_' + groupName
            if cmds.objExists(groupName):
                cmds.delete(groupName)
            cmds.createNode('transform', name=groupName)
            cmds.parent(groupName, 'UNREAL')
        else:
            groupName = 'UNREAL'

        return groupName
