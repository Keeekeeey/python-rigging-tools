from PySide2 import QtWidgets
from PySide2 import QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

import maya.cmds as mc


# obj constants
GROUP = 'grp'
JOINT = 'JNT'
GUIDE = 'guide'
JAW = 'JAW'

# side constraints
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'


def get_maya_main_win():
    """returns the maya main window widget"""
    main_win = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)


class Win(QtWidgets.QDialog):

    def __init__(self):
        super(Win, self).__init__(parent=get_maya_main_win())
        self.setWindowTitle(" Auto Rig Tool")
        self.rig_gen = jaw()
        self.resize(400, 100)
        self._create_ui()

    def _create_ui(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self._add_parms_form()
        self._add_rig_btns()
        self._add_btns()
        self.setLayout(self.main_lay)


    def _add_parms_form(self):
        self.form_lay = QtWidgets.QFormLayout()
        self._add_raidus_params()
        self._add_cc_radius_params()
        self._add_cc_params()
        self.main_lay.addLayout(self.form_lay)

    def _add_raidus_params(self):
        self.radius_lay = QtWidgets.QHBoxLayout()
        self.radius_dspnbx = QtWidgets.QDoubleSpinBox(value=0.5)
        self.radius_dspnbx.setRange(0.0, 900.0)
        self.radius_dspnbx.setSingleStep(1.00)
        self.radius_slider = QtWidgets.QSlider(
            orientation=QtCore.Qt.Horizontal)
        self.radius_lay.addWidget(self.radius_dspnbx)
        self.radius_lay.addWidget(self.radius_slider)
        self.form_lay.addRow("Minor Joint Radius", self.radius_lay)
        self.radius_dspnbx.valueChanged.connect(
            self._update_radius_dspnbx)
        self.radius_slider.valueChanged.connect(
            self._update_radius_dspnbx)
        
    def _add_cc_params(self):
        self.ccs_lay = QtWidgets.QHBoxLayout()
        self.cc_dspnbx = QtWidgets.QDoubleSpinBox(value=5.00)
        self.cc_dspnbx.setRange(0.0, 16.0)
        self.cc_dspnbx.setSingleStep(1.00)
        self.cc_slider = QtWidgets.QSlider(
            orientation=QtCore.Qt.Horizontal)
        self.ccs_lay.addWidget(self.cc_dspnbx)
        self.ccs_lay.addWidget(self.cc_slider)
        self.form_lay.addRow("Control Curve Color", self.ccs_lay)
        self.cc_dspnbx.valueChanged.connect(
            self._update_cc_dspnbx)
        self.cc_slider.valueChanged.connect(
            self._update_cc_dspnbx)  
        
    def _add_cc_radius_params(self):
        self.cc_radius_lay = QtWidgets.QHBoxLayout()
        self.cc_radius_dspnbx = QtWidgets.QDoubleSpinBox(value=1.00)
        self.cc_radius_dspnbx.setRange(0.0, 16.0)
        self.cc_radius_dspnbx.setSingleStep(1.00)
        self.cc_radius_slider = QtWidgets.QSlider(
            orientation=QtCore.Qt.Horizontal)
        self.cc_radius_lay.addWidget(self.cc_radius_dspnbx)
        self.cc_radius_lay.addWidget(self.cc_radius_slider)
        self.form_lay.addRow("Control Curve Radius", self.cc_radius_lay)
        self.cc_radius_dspnbx.valueChanged.connect(
            self._update_cc_radius_dspnbx)
        self.cc_radius_slider.valueChanged.connect(
            self._update_cc_radius_dspnbx)  

        
        
    def _add_rig_btns(self):
        self.rig_buttons_lay = QtWidgets.QHBoxLayout()

        self.guides_btn = QtWidgets.QPushButton("Create Guides")
        self.rig_buttons_lay.addWidget(self.guides_btn)
        self.guides_btn.clicked.connect(self.generateGuides)

        self.joints_btn = QtWidgets.QPushButton("Create Joints")
        self.rig_buttons_lay.addWidget(self.joints_btn)
        self.joints_btn.clicked.connect(self.generateJoints)

        self.main_lay.addLayout(self.rig_buttons_lay)

        
    def _add_btns(self):
        self.buttons_lay = QtWidgets.QHBoxLayout()
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self.cancel_btn.clicked.connect(self.cancel)
        self.buttons_lay.addWidget(self.cancel_btn)

        self.main_lay.addLayout(self.buttons_lay)

    def _set_rig_properties(self):
        self.rig_gen.radius = self.radius_dspnbx.value()
        self.rig_gen.ccColor = self.cc_dspnbx.value()
        self.rig_gen.ccradius = self.cc_radius_dspnbx.value()

    @QtCore.Slot()
    def _update_radius_dspnbx(self):
        print(f"spinbox set val: {float(self.radius_slider.value())}")
        self.radius_dspnbx.setValue(
            float(self.radius_slider.value()))

    @QtCore.Slot()
    def _update_radius_slider(self):
        self.radius_slider.setValue(int(self.radius_dspnbx.value()))

    @QtCore.Slot()
    def _update_cc_dspnbx(self):
        print(f"spinbox set val: {float(self.cc_slider.value())/10.0}")
        self.cc_dspnbx.setValue(
            float(self.cc_slider.value()/10.0))

    @QtCore.Slot()
    def _update_cc_slider(self):
        self.cc_slider.setValue(int(self.cc_dspnbx.value()*10.0))
    
    @QtCore.Slot()
    def _update_cc_radius_dspnbx(self):
        print(f"spinbox set val: {float(self.cc_radius_slider.value())/10.0}")
        self.cc_radius_dspnbx.setValue(
            float(self.cc_radius_slider.value()/10.0))

    @QtCore.Slot()
    def _update_cc_radius__slider(self):
        self.cc_radius_dspnbx.setValue(int(self.cc_radius_dspnbx.value()*10.0))

    @QtCore.Slot()
    def generateGuides(self):
        print("Generating Rig...")
        self._set_rig_properties()
        self.rig_gen.build()
        self.rig_gen = jaw()
        # this last line resets the table so that it can generate multiple

    def generateJoints(self):
        print("Generating Rig...")
        self._set_rig_properties()
        self.rig_gen.buildJoints()
        self.rig_gen = jaw()
        # this last line resets the table so that it can generate multiple

    @QtCore.Slot()
    def cancel(self):
        print("Canceling Rig...")
        self.close()


class jaw(object):
    
    
    def __init__(self):
        self.jaw_master_grp = ""
        self.jointHierachy = []
        self.limbName = None
        self.limbJoints = 4
        self.limbType = ""
        print('running self')
        
        

    def addOffset(self, dst, suffix='OFF'):
        # to zero out all joints while creating them

        grp_offset = mc.createNode('transform', name='{}_{}'.format(dst, suffix))
        dst_mat = mc.xform(dst, q=True, m=True, ws=True)
        mc.xform(grp_offset, m=dst_mat, ws=True)

        dst_parent = mc.listRelatives(dst, parent=True)
        if dst_parent:
            # parent offset under the destination parent
            mc.parent(grp_offset, dst_parent)
        mc.parent(dst, grp_offset)

        return grp_offset


    def createGuides( self, number = 5):

        jaw_guide_grp = mc.createNode('transform', name='{}_{}_{}_{}'.format(CENTER, JAW, GUIDE, GROUP), parent = self.jaw_master_grp)
        locs_grp = mc.createNode('transform', name='{}_{}_lip_{}_{}'.format(CENTER, JAW, GUIDE, GROUP), parent=jaw_guide_grp)
        lip_locs_grp = mc.createNode('transform', name='{}_{}_lipMinor_{}_{}'.format(CENTER, JAW, GUIDE, GROUP),parent=locs_grp)
        lip_locs_broad_grp = mc.createNode('transform', name='{}_{}lipBroad_{}_{}'.format(CENTER, JAW, GUIDE, GROUP), parent = locs_grp)

        # create locators
        for part in ['Upper', 'Lower']:
            # center is based off a fixed umber, so we can make it right away
            # CREATE THE [0] because the method creates transforms
            part_multipler = 1 if part == 'Upper' else -1
            mid_data = (0, part_multipler,0)

            mid_loc = mc.spaceLocator(name='{}_{}{}_lip_{}'.format( CENTER,JAW, part, GUIDE))[0]
            mc.parent(mid_loc, lip_locs_broad_grp)

            #mid_loc_minor = mc.spaceLocator(name='{}_{}{}_lip_{}'.format(CENTER, JAW, part, GUIDE))[0]
            #mc.parent(mid_loc_minor, lip_locs_grp)


            for side in 'LR':
                for x in range(number):
                    multiplier = x+1 if side == LEFT else -(x+1)
                    loc_data= (multiplier, part_multipler, 0)
                    loc = mc.spaceLocator(name= '{}_{}{}_lip_{}_{}'.format(side,JAW, part, x+1, GUIDE))[0]
                    mc.parent(loc,lip_locs_grp)


                    #set data
                    #set tuple to the translastion of the guides
                    mc.setAttr('{}.t'.format(loc), *loc_data)

                #setCenterData
                mc.setAttr('{}.t'.format(mid_loc), *mid_data)
        #create corners
        left_corner_loc = mc.spaceLocator(name='{}_{}Corner_lip_{}'.format(LEFT, JAW, GUIDE))[0]
        right_corner_loc = mc.spaceLocator(name='{}_{}Corner_lip_{}'.format(RIGHT, JAW, GUIDE))[0]
        mc.parent(left_corner_loc, lip_locs_broad_grp)
        mc.parent(right_corner_loc, lip_locs_broad_grp)

        mc.setAttr('{}.t'.format(left_corner_loc), *(number + 1, 0, 0))
        mc.setAttr('{}.t'.format(right_corner_loc), *(-(number + 1), 0, 0))

        mc.select(cl=True)

        #create jaw base
        jaw_base_guide_grp = mc.createNode('transform', name='{}_{}_base_{}_{}'.format(CENTER, JAW, GUIDE, GROUP),
                                            parent= jaw_guide_grp)
        jaw_guide= mc.spaceLocator(name='{}_{}_{}'.format(CENTER, JAW, GUIDE))[0]
        inverse_jaw_guide = mc.spaceLocator(name='{}_{}_inverse_{}'.format(CENTER, JAW, GUIDE))[0]

        mc.setAttr('{}.t'.format(jaw_guide), *(0, -1, -number))
        mc.setAttr('{}.t'.format(inverse_jaw_guide), *(0, 1, -number))
        mc.parent(jaw_guide, jaw_base_guide_grp)
        mc.parent(inverse_jaw_guide, jaw_base_guide_grp)

        mc.select(cl=True)




    def lip_guides(self, *args):
        # creates a list of all lip guides to be accessed later
        grp = '{}_{}_lipMinor_{}_{}'.format(CENTER, JAW, GUIDE, GROUP)
        guides = list()

        if mc.objExists(grp):
            for loc in mc.listRelatives(grp):
                guides.append(loc)
        #makes sure to add minor joints within the broad joints. these joints are created for ease of parenting
        grp = '{}_{}lipBroad_{}_{}'.format(CENTER, JAW, GUIDE, GROUP)
        if mc.objExists(grp):
            for loc in mc.listRelatives(grp):
                guides.append(loc)

        return guides


    def jaw_guides(self, *args):
        # creates a list of all jaw guides to be accessed later
        # if there is an error in these methods, it would probably be the groups search function down below. triple check they match the tut
        grp = '{}_{}_base_{}_{}'.format(CENTER, JAW, GUIDE, GROUP)
        # print('grp = ' + grp)
        guides = list()

        if mc.objExists(grp):
            for loc in mc.listRelatives(grp):
                guides.append(loc)

        return guides


    def createHierarchy(self, *args):
        
        self.jaw_master_grp = mc.createNode('transform', name='{}_{}Master_{}'.format(CENTER, JAW, GROUP))
        main_grp = mc.createNode('transform', name='{}_{}_rig_{}'.format(CENTER, JAW, GROUP), parent= self.jaw_master_grp )
        lip_grp = mc.createNode('transform', name='{}_{}Lip_{}'.format(CENTER, JAW, GROUP), parent=main_grp)
        base_grp = mc.createNode('transform', name='{}_{}Base_{}'.format(CENTER, JAW, GROUP), parent=main_grp)
        lip_minor_grp = mc.createNode('transform', name='{}_{}_lip_minor_{}'.format(CENTER, JAW, GROUP), parent=lip_grp)
        lip_broad_grp = mc.createNode('transform', name='{}_{}_lip_broad_{}'.format(CENTER, JAW, GROUP), parent=lip_grp)


    def createMinorJoints(self, *args):
        minor_joints = list()

        for guide in self.lip_guides():
            # print('guide in lip_guides = ' +guide)
            mat = mc.xform(guide, q=True, m=True, ws=True)
            jnt = mc.joint(name=guide.replace(GUIDE, JOINT))
            mc.setAttr('{}.radius'.format(jnt), (self.radius))
            mc.xform(jnt, m=mat, ws=True)

            mc.parent(jnt, '{}_{}_lip_minor_{}'.format(CENTER, JAW, GROUP))




    def createBroadJoints(self, *args):
        upper_joint = mc.joint(name='{}_{}_broadUpper_{}'.format(CENTER, JAW, JOINT))
        mc.select(cl=True)
        lower_joint = mc.joint(name='{}_{}_broadLower_{}'.format(CENTER, JAW, JOINT))
        mc.select(cl=True)
        left_joint = mc.joint(name='{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT))
        mc.select(cl=True)
        right_joint = mc.joint(name='{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT))
        mc.select(cl=True)

        # Parent joints under broad_grp

        mc.parent([upper_joint, lower_joint, left_joint, right_joint], '{}_{}_lip_broad_{}'.format(CENTER, JAW, GROUP))

        # retrieve guide postitions

        upper_pos = mc.xform('{}_{}Upper_lip_{}'.format(CENTER, JAW, GUIDE), q=True, m=True, ws=True)
        lower_pos = mc.xform('{}_{}Lower_lip_{}'.format(CENTER, JAW, GUIDE), q=True, m=True, ws=True)
        left_pos = mc.xform('{}_{}Corner_lip_{}'.format(LEFT, JAW, GUIDE), q=True, m=True, ws=True)
        right_pos = mc.xform('{}_{}Corner_lip_{}'.format(RIGHT, JAW, GUIDE), q=True, m=True, ws=True)

        # set guide postions
        mc.xform(upper_joint, m=upper_pos)
        mc.xform(lower_joint, m=lower_pos)
        mc.xform(left_joint, m=left_pos)
        mc.xform(right_joint, m=right_pos)
        mc.select(cl=True)
        # # parents to the joint group
            # mc.select(cl=True)
            # #creates a cc for the joints
        broadJointList = [upper_joint,lower_joint,left_joint, right_joint]

        
        mc.parent(self.ctrls_grp, '{}_{}Lip_{}'.format(CENTER, JAW, GROUP))

        for broadJoint in broadJointList:
                
            ctrl = mc.circle(c=(0,0,0), nr=(0,0,1),r=self.ccradius, ch=0, name= broadJoint+"_CTRL")[0]
            ctrl_group=mc.group(ctrl,name=(broadJoint.replace(GUIDE, JOINT))+'_OffSet_CTRL'+GROUP)

            mc.matchTransform(ctrl_group, broadJoint)
            mc.parent(ctrl_group, self.ctrls_grp)

            if 'Upper' not in broadJoint:
                mc.parent(ctrl_group, self.ctrls_lower_grp)
            else:
                mc.parent(ctrl_group, self.ctrls_inverse_grp)

  
            mc.connectAttr('{}.translateX'.format(ctrl),'{}.translateX'.format(broadJoint))
            mc.connectAttr('{}.translateY'.format(ctrl),'{}.translateY'.format(broadJoint))
            mc.connectAttr('{}.translateZ'.format(ctrl),'{}.translateZ'.format(broadJoint))

            mc.connectAttr('{}.rotateX'.format(ctrl),'{}.rotateX'.format(broadJoint))
            mc.connectAttr('{}.rotateY'.format(ctrl),'{}.rotateY'.format(broadJoint))
            mc.connectAttr('{}.rotateZ'.format(ctrl),'{}.rotateZ'.format(broadJoint))

            
            
            # #sets color to green
            mc.setAttr((mc.listRelatives(ctrl, type='shape')[0] + '.overrideEnabled'),1)
            mc.setAttr((mc.listRelatives(ctrl, type='shape')[0] + '.overrideColor'), self.ccColor)

            mc.setAttr('{}.radius'.format(broadJoint), 0.05)


    def createJawBase(self, *args):
        jaw_jnt = mc.joint(name='{}_{}_{}'.format(CENTER, JAW, JOINT))
        jaw_inverse_jnt = mc.joint(name='{}_{}_inverse_{}'.format(CENTER, JAW, JOINT))

        jaw_mat = mc.xform(self.jaw_guides()[0], q=True, m=True, ws=True)
        jaw_inverse_mat = mc.xform(self.jaw_guides()[1], q=True, m=True, ws=True)

        mc.xform(jaw_jnt, m=jaw_mat, ws=True)
        mc.xform(jaw_inverse_jnt, m=jaw_inverse_mat, ws=True)

        mc.parent(jaw_jnt, '{}_{}Base_{}'.format(CENTER, JAW, GROUP))
        mc.parent(jaw_inverse_jnt, '{}_{}Base_{}'.format(CENTER, JAW, GROUP))

        mc.select(cl=True)
        # add offset for clean joints

        self.addOffset(jaw_jnt, suffix='OFF')
        self.addOffset(jaw_inverse_jnt, suffix='OFF')

        self.addOffset(jaw_jnt, suffix='AUTO')
        self.addOffset(jaw_inverse_jnt, suffix='AUTO')

        self.ctrls_grp = mc.createNode('transform', name="ctrl_offset_"+GROUP)
        
        mc.matchTransform(self.ctrls_grp, jaw_inverse_jnt)
        self.ctrls_inverse_grp = mc.group(self.ctrls_grp, name='ctrl_inverse_OffSet_'+GROUP)


        self.ctrls_lower_grp = mc.group(self.ctrls_grp, name='ctrl_lower_OffSet_'+GROUP)
        mc.matchTransform(self.ctrls_lower_grp, jaw_jnt)

        mc.parent(self.ctrls_inverse_grp, '{}_{}Base_{}'.format(CENTER, JAW, GROUP))
        mc.parent(self.ctrls_lower_grp, '{}_{}Base_{}'.format(CENTER, JAW, GROUP))

        mc.connectAttr('{}_{}_inverse_{}.rotateX'.format(CENTER, JAW, JOINT),'{}.rotateX'.format(self.ctrls_inverse_grp))
        mc.connectAttr('{}_{}_inverse_{}.rotateY'.format(CENTER, JAW, JOINT),'{}.rotateY'.format(self.ctrls_inverse_grp))
        mc.connectAttr('{}_{}_inverse_{}.rotateZ'.format(CENTER, JAW, JOINT),'{}.rotateZ'.format(self.ctrls_inverse_grp))

        mc.connectAttr('{}_{}_{}.rotateX'.format(CENTER, JAW, JOINT),'{}.rotateX'.format(self.ctrls_lower_grp))
        mc.connectAttr('{}_{}_{}.rotateY'.format(CENTER, JAW, JOINT),'{}.rotateY'.format(self.ctrls_lower_grp))
        mc.connectAttr('{}_{}_{}.rotateZ'.format(CENTER, JAW, JOINT),'{}.rotateZ'.format(self.ctrls_lower_grp))

        mc.select(cl=True)


    def constrainBroadJoints(self, *args):
        jaw_joint = '{}_{}_{}'.format(CENTER, JAW, JOINT)
        inverse_jaw_joint = '{}_{}_inverse_{}'.format(CENTER, JAW, JOINT)

        broad_upper = '{}_{}_broadUpper_{}'.format(CENTER, JAW, JOINT)
        broad_lower = '{}_{}_broadLower_{}'.format(CENTER, JAW, JOINT)
        broad_left = '{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT)
        broad_right = '{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT)

        # add offsets to the broad joints
        upper_off = self.addOffset(broad_upper)
        lower_off = self.addOffset(broad_lower)
        left_off = self.addOffset(broad_left)
        right_off = self.addOffset(broad_right)

        # contraints to upper and lower
        mc.parentConstraint(jaw_joint, lower_off, mo=True)
        mc.parentConstraint(inverse_jaw_joint, upper_off, mo=True)

        # create contraints to corners
        mc.parentConstraint(upper_off, lower_off, left_off, mo=True)
        mc.parentConstraint(upper_off, lower_off, right_off, mo=True)

        mc.select(cl=True)


        # creating seal groups for the seal attribute
        # while also creating a dictonary for the minor and major joints of the lips

    def getLipParts(self, *args):
        # print('--getLipParts')
        #switching to just 'upper' ect gets rid of the list indiex issue
        upper_token = '{}Upper'.format(JAW)
        lower_token = '{}Lower'.format(JAW)
        corner_token = '{}Corner'.format(JAW)
        # upper_token = 'Upper'
        # lower_token = 'Lower'
        # corner_token = 'Corner'

        C_upper = '{}_{}_broadUpper_{}'.format(CENTER, JAW, JOINT)
        C_lower = '{}_{}_broadLower_{}'.format(CENTER, JAW, JOINT)
        L_corner= '{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT)
        R_corner = '{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT)

        lip_joints = mc.listRelatives('{}_{}Lip_{}'.format(CENTER, JAW, GROUP), allDescendents = True)
        #print('---LIP JOINTS  ')
        #print(lip_joints)
        #create a dictonary to store everything, created empty
        #keeps track of which joints influence which other joints
        lookup = {'C_upper': {}, 'C_lower': {},
                    'L_upper': {}, 'L_lower': {},
                    'R_upper': {}, 'R_lower': {},
                    'L_corner': {}, 'R_corner': {}}

        for joint in lip_joints:
            if mc.objectType(joint) != 'joint':
                continue
               
            if joint.startswith('C') and upper_token in joint:
                lookup['C_upper'][joint] = [C_upper]

            if joint.startswith('C') and lower_token in joint:
                lookup['C_lower'][joint] = [C_lower]

            if joint.startswith('L') and upper_token in joint:
                lookup['L_upper'][joint] = [C_upper, L_corner]

            if joint.startswith('L') and lower_token in joint:
                lookup['L_lower'][joint] = [C_lower, L_corner]

            if joint.startswith('R') and upper_token in joint:
                lookup['R_upper'][joint] = [C_upper, R_corner]

            if joint.startswith('R') and lower_token in joint:

                lookup['R_lower'][joint] = [C_lower, R_corner]
            if joint.startswith('L') and corner_token in joint:
                lookup['L_corner'][joint] = [L_corner]

            if joint.startswith('R') and corner_token in joint:
                lookup['R_corner'][joint] = [R_corner]

        return lookup

    def lipPart( self, part = ""):
        print('LipParts')
        lip_parts = [reversed(sorted(self.getLipParts()['L_{}'.format(part)].keys())),self.getLipParts()['C_{}'.format(part)].keys(),
                        sorted(self.getLipParts()['R_{}'.format(part)].keys())]
        
        return [joint for joint in lip_parts for joint in joint]

    def createSeal(self, part, *args):
        # running twice, once for upper and once for lower, so check before creating groups
        print('createSeal')
        seal_name = '{}_seal_{}'.format(CENTER, GROUP)
        seal_parent = seal_name if mc.objExists(seal_name) else mc.createNode('transform', name=seal_name,
                                                                                parent = '{}_{}_rig_{}'.format(CENTER, JAW, GROUP))

        part_grp = mc.createNode('transform', name=seal_name.replace('seal', 'seal_{}'.format(part)), parent = seal_parent)

        l_corner = '{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT)
        r_corner = '{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT)
        print(part)
        value = len(self.lipPart(part))

        for index, joint in enumerate(self.lipPart(part)):
            node = mc.createNode('transform', name=joint.replace('JNT', '{}_SEAL'.format(part)), parent=part_grp)
            mat = mc.xform(joint, q=True, m = True, ws = True)
            mc.xform(node, m=mat, ws=True)

            constraint = mc.parentConstraint(l_corner, r_corner, node, mo=True)[0]
            mc.setAttr('{}.interpType'.format(constraint), 2)

            #main calc left -->
            r_corner_value = float(index)/ float(value - 1)
            l_corner_value = 1 - r_corner_value

            l_corner_attr = '{}_parentConstraint1.{}W0'.format(node, l_corner)
            r_corner_attr = '{}_parentConstraint1.{}W1'.format(node, r_corner)

            mc.setAttr(l_corner_attr, l_corner_value)
            mc.setAttr(r_corner_attr, r_corner_value)

        mc.select(cl=True)

    def createJawAttrs(self, *args):

        node = mc.createNode('transform', name= 'jaw_attributes', parent= '{}_{}_rig_{}'.format(CENTER, JAW, GROUP))
        mc.addAttr(node, ln=sorted(self.getLipParts()['C_upper'].keys())[0], min=0, max=1, dv=0)
        mc.setAttr('{}.{}'.format(node, sorted(self.getLipParts()['C_upper'].keys())[0]), lock=1)

        for upper in sorted(self.getLipParts()['L_upper'].keys()):
            mc.addAttr(node, ln=upper, min=0, max=1, dv=0)
        #works with multiple array entries, so???
        mc.addAttr(node, ln=sorted(self.getLipParts()['L_corner'].keys())[0], min=0, max=1,dv=1)
        mc.setAttr('{}.{}'.format(node, sorted(self.getLipParts()['L_corner'].keys())[0]), lock=1)

        for lower in sorted(self.getLipParts()['L_lower'].keys())[::-1]:
            mc.addAttr(node, ln=lower, min=0, max=1, dv=0)

        mc.addAttr(node, ln=sorted(self.getLipParts()['C_lower'].keys())[0], min=0, max=1, dv=0)
        mc.setAttr('{}.{}'.format(node, sorted(self.getLipParts()['C_lower'].keys())[0]), lock=1)

        self.createOffestFollow()  # creates offset group for the jaw
        self.addSealAttrs()  # adds the seal and seal delay attrs to the jaw attrs group


    def createConstraints(self, *args):
        #ISSUE:: the broad joints aren't triggering the 'else' part of the statement because they have 'upper' in their names.
        #maybe lipparts is returning broad values? do we want that?
        #getLipParts isn't working as expected, not giving the correct relationships


        for value in self.getLipParts().values():
            for lip_jnt, broad_jnt in value.items():
                # getting the seal transforms
                seal_token = 'upper_SEAL' if 'Upper' in lip_jnt else 'lower_SEAL'
                lip_seal = lip_jnt.replace(JOINT, seal_token)
                # print('lip_seal '+lip_seal)
                if mc.objExists(lip_seal):
                    const = mc.parentConstraint(broad_jnt, lip_seal, lip_jnt, mo=True)[0]
                    mc.setAttr('{}.interpType'.format(const), 2)
                    # on center joints, only use seal to rev target amount, on sides, use seal to toggle the two other parent sonstraints
                    if len(broad_jnt) == 1:
                        seal_attr = '{}_parentConstraint1.{}W1'.format(lip_jnt, lip_seal)
                        rev = mc.createNode('reverse', name= lip_jnt.replace(JOINT, 'REV'))
                        mc.connectAttr(seal_attr, '{}.inputX'.format(rev))
                        mc.connectAttr('{}.outputX'.format(rev), '{}_parentConstraint1.{}W0'.format(lip_jnt, broad_jnt[0]))
                        mc.setAttr(seal_attr, 0)

                    if len(broad_jnt) == 2:
                        seal_attr = '{}_parentConstraint1.{}W2'.format(lip_jnt, lip_seal)
                        mc.setAttr(seal_attr, 0)

                        #create nodes needed for the reverse, rever for seal and jaw, and multipler
                        #honestly, walk through in node editor

                        seal_rev = mc.createNode('reverse', name=lip_jnt.replace('JNT', 'seal_REV'))
                        jaw_attr_rev = mc.createNode('reverse', name=lip_jnt.replace('JNT', 'jaw_attr_REV'))
                        seal_multi = mc.createNode('multiplyDivide', name=lip_jnt.replace('JNT', 'seal_MULTI'))
                        
                        mc.connectAttr(seal_attr, '{}.inputX'.format(seal_rev))
                        mc.connectAttr('{}.outputX'.format(seal_rev), '{}.input2X'.format(seal_multi))
                        mc.connectAttr('{}.outputX'.format(seal_rev), '{}.input2Y'.format(seal_multi))

                        mc.connectAttr('jaw_attributes.{}'.format(lip_jnt.replace(lip_jnt[0], 'L')),
                                        '{}.input1Y'.format(seal_multi))

                        mc.connectAttr('jaw_attributes.{}'.format(lip_jnt.replace(lip_jnt[0], 'L')),
                                        '{}.inputX'.format(jaw_attr_rev))

                        mc.connectAttr('{}.outputX'.format(jaw_attr_rev),
                                        '{}.input1X'.format(seal_multi))

                        #connect final multiplcation to contraint targets

                        mc.connectAttr('{}.outputX'.format(seal_multi),
                                        '{}_parentConstraint1.{}W0'.format(lip_jnt, broad_jnt[0]))
                        # looking for a parent constraint that doesn't exsist. Need to find a way to change lip_jnt to the current jnt,
                        mc.connectAttr('{}.outputY'.format(seal_multi),
                                        '{}_parentConstraint1.{}W1'.format(lip_jnt, broad_jnt[1]))



                else:
                    const = mc.parentConstraint(broad_jnt, lip_jnt, mo=True)[0]
                    mc.setAttr('{}.interpType'.format(const), 2)


    def createInitalValues(self, PART, *args):
        jaw_attr = [part for part in self.lipPart(PART) if not part.startswith('C') and not part.startswith('R')]

        value = len(jaw_attr)
        degree = 1.3
        for index, attr_name in enumerate(jaw_attr[::-1]):
            attr = 'jaw_attributes.{}'.format(attr_name)
            # print(attr)
            linear_value = float(index) / float(value -1)
            if value > 5:
                # use to get a more equal curve if more then 5
                #NEEDS TO BE TESTED
                div_value = linear_value / degree
                final_value = div_value + linear_value
                linear_value = final_value
            mc.setAttr(attr, linear_value)

    def createOffestFollow(self, *args):
        #for the jaw joint to make sure it rotatwes realisticall (moves forward when it goes down

        jaw_attr = 'jaw_attributes'

        jaw_joint = '{}_{}_{}'.format(CENTER, JAW,JOINT)
        jaw_auto = '{}_{}_{}_AUTO'.format(CENTER, JAW, JOINT)

        #add follow attributes
        mc.addAttr(jaw_attr, ln='follow_ty', min=-10, max=10, dv=0, k=True)
        mc.addAttr(jaw_attr, ln='follow_tx', min=-10, max=10, dv=0, k=True)

        unit = mc.createNode('unitConversion', name='{}_{}_follow_UNIT'.format(CENTER, JAW))

        remap_y = mc.createNode('remapValue', name='{}_{}_followY_REMAP'.format(CENTER,JAW))
        mc.setAttr('{}.inputMax'.format(remap_y), 1)

        remap_z = mc.createNode('remapValue', name='{}_{}_followY_REMAP'.format(CENTER, JAW))
        mc.setAttr('{}.inputMax'.format(remap_z), 1)

        multi_y = mc.createNode('multDoubleLinear', name='{}_{}_followY_MULT'.format(CENTER, JAW))
        mc.setAttr('{}.input2'.format(multi_y), -1)

        mc.connectAttr('{}.rx'.format(jaw_joint), '{}.input'.format(unit))
        mc.connectAttr('{}.output'.format(unit), '{}.inputValue'.format(remap_y))
        mc.connectAttr('{}.output'.format(unit), '{}.inputValue'.format(remap_z))

        mc.connectAttr('{}.follow_ty'.format(jaw_attr), '{}.input1'.format(multi_y))
        mc.connectAttr('{}.follow_tx'.format(jaw_attr), '{}.outputMax'.format(remap_z))
        mc.connectAttr('{}.output'.format(multi_y), '{}.outputMax'.format(remap_y))

        mc.connectAttr('{}.outValue'.format(remap_y), '{}.ty'.format(jaw_auto))
        mc.connectAttr('{}.outValue'.format(remap_z), '{}.tz'.format(jaw_auto))

    def addSealAttrs(self, *args):

        jaw_attr = 'jaw_attributes'
        mc.addAttr(jaw_attr, at = 'double', ln= 'L_seal', min=0, max=10, dv=0, k = True)
        mc.addAttr(jaw_attr, at='double', ln='R_seal', min=0, max=10, dv=0, k=True)

        mc.addAttr(jaw_attr, at='double', ln='L_seal_delay', min=0.1, max=10, dv=4, k=True)
        mc.addAttr(jaw_attr, at='double', ln='R_seal_delay', min=0.1, max=10, dv=4, k=True)


    def connectSeal (self, PART, *args):
        #right now, it's going through and creating 10 nodes for the r upper and l lower parts of the mouth.
        #this is throwing an error because the naming convention is diffrent, and also I have 5
        #l seal delay isn't working
        part = PART
        seal_token = 'seal_{}'.format(part)

        jaw_attrs = 'jaw_attributes'
        lip_jnts = self.lipPart(part)
        # lip_jnts is working~!
        value= len(lip_jnts)
        num_spans = value

        seal_driver = mc.createNode('lightInfo', name='C_{}_DRV'.format(seal_token))

        #create a dictioary of targets

        triggers = {'L': list(), 'R': list()}

        for side in 'LR':
            # get fall off
            delay_sub_name = '{}_{}_delay_SUB'.format(side, seal_token)
            delay_sub = mc.createNode('plusMinusAverage', name=delay_sub_name)

            mc.setAttr('{}.operation'.format(delay_sub), 2)
            mc.setAttr('{}.input1D[0]'.format(delay_sub), 10)
            mc.connectAttr('{}.{}_seal_delay'.format(jaw_attrs, side), '{}.input1D[0]'.format(delay_sub))
            #checked
            lerp = 1/ float(value -1)

            delay_div_name = '{}_{}_delay_DIV'.format(side,seal_token)
            delay_div = mc.createNode('multDoubleLinear', name=delay_div_name)
            mc.setAttr('{}.input2'.format(delay_div), lerp)
            mc.connectAttr('{}.output 1D'.format(delay_sub), '{}.input1'.format(delay_div))
            # checked

            mult_triggers = list() #start
            sub_triggers = list() #end
            #appenidng to external dictionaries
            triggers[side].append(mult_triggers)
            triggers[side].append(sub_triggers)
            #
            for index in range(value):
                index_name = 'jaw_{:02d}'.format(index)

                #create multinode
                delay_multi_name = '{}_{}_{}_delay_MULTI'.format(index_name, side, seal_token)
                delay_mult = mc.createNode('multDoubleLinear', name=delay_multi_name)
                mc.setAttr('{}.input1'.format(delay_mult), index)
                mc.connectAttr('{}.output'.format(delay_div), '{}.input2'.format(delay_mult))

                mult_triggers.append(delay_mult)
            #
                #create SUB node
                delay_sub_name = '{}_{}_{}_delay_SUB'.format(index_name, side, seal_token)
                delay_sub = mc.createNode('plusMinusAverage', name=delay_sub_name)
                mc.connectAttr('{}.output'.format(delay_mult), '{}.input1D[0]'.format(delay_sub))
                mc.connectAttr('{}.{}_seal_delay'.format(jaw_attrs, side), '{}.input1D[1]'.format(delay_sub))

                sub_triggers.append(delay_sub)

        # get constraints

        const_targets = list()

        for jnt in lip_jnts:
            attrs = mc.listAttr('{}_parentConstraint1'.format(jnt), ud=True)
            for attr in attrs:
                if 'SEAL' in attr:
                    const_targets.append('{}_parentConstraint1.{}'.format(jnt,attr))
                    #pull the enum instead of range

        # connect seal triggers to driver node
        # for left_index in range(value):
        for left_index, const_targets in enumerate(const_targets):
            right_index = num_spans - left_index - 1

            index_name = '{}_{}'.format(seal_token, left_index)
            #14:38 on connect seal p2

            l_multi_trigger, l_sub_trigger = triggers['L'][0][left_index], triggers['L'][1][left_index]
            r_multi_trigger, r_sub_trigger = triggers['R'][0][right_index], triggers['R'][1][right_index]

            # left
            l_remap_name = 'L_{}_{}_REMAP'.format(seal_token, index_name)
            l_remap = mc.createNode('remapValue', name=l_remap_name)
            mc.setAttr('{}.outputMax'.format(l_remap), 1)
            mc.setAttr('{}.value[0].value_Interp'.format(l_remap), 2)

            mc.connectAttr('{}.output'.format(l_multi_trigger), '{}.inputMin'.format(l_remap))
            mc.connectAttr('{}.output1D'.format(l_sub_trigger), '{}.inputMax'.format(l_remap))

            #connect left seal attr to input of remap
            mc.connectAttr('{}.L_seal'.format(jaw_attrs), '{}.inputValue'.format(l_remap))

            # right
            # sub 1 minus result from left remap
            r_sub_name = 'R_{}_offset_{}_SUB'.format(seal_token, index_name)
            r_sub = mc.createNode('plusMinusAverage', name=r_sub_name)
            mc.setAttr('{}.input1D[0]'.format(r_sub), 1)
            mc.setAttr('{}.operation'.format(r_sub), 2)

            #forgot the below line.. OOPS
            mc.connectAttr('{}.outValue'.format(l_remap), '{}.input1D[1]'.format(r_sub))

            r_remap_name = 'R_{}_{}_REMAP'.format(seal_token, index_name)
            r_remap = mc.createNode('remapValue', name=r_remap_name)
            mc.setAttr('{}.outputMax'.format(r_remap), 1)
            mc.setAttr('{}.value[0].value_Interp'.format(r_remap), 2)

            mc.connectAttr('{}.output'.format(r_multi_trigger), '{}.inputMin'.format(r_remap))
            mc.connectAttr('{}.output1D'.format(r_sub_trigger), '{}.inputMax'.format(r_remap))

            # connect right seal attr to input of remap
            mc.connectAttr('{}.R_seal'.format(jaw_attrs), '{}.inputValue'.format(r_remap))

            mc.connectAttr('{}.output1D'.format(r_sub), '{}.outputMax'.format(r_remap))

            # final addition of both sides

            plus_name = '{}_SUM'.format(index_name)
            plus= mc.createNode('plusMinusAverage', name=plus_name)

            mc.connectAttr('{}.outValue'.format(l_remap), '{}.input1D[0]'.format(plus))
            mc.connectAttr('{}.outValue'.format(r_remap), '{}.input1D[1]'.format(plus))

            clamp_name = '{}_CLAMP'.format(index_name)
            clamp = mc.createNode('remapValue', name = clamp_name)
            mc.connectAttr('{}.output1D'.format(plus), '{}.inputValue'.format(clamp))

            mc.addAttr(seal_driver, at='double', ln=index_name, min=0, max=1, dv=0, k=True)
            #attaching seal to each attr we created
            mc.connectAttr('{}.outValue'.format(clamp), '{}.{}'.format(seal_driver , index_name))

            #connect to the constrain targets
            mc.connectAttr('{}.{}'.format(seal_driver, index_name), const_targets)


    def createJawPin(self, *args):
        pin_driver = mc.createNode('lightInfo', name='{}_pin_DRV'.format(CENTER) )
        jaw_attr = 'jaw_attributes'

        for side in 'LR':
            mc.addAttr(jaw_attr, at='bool', ln='{}_auto_corner_pin'.format(side), k=True)
            mc.addAttr(jaw_attr, at='double', ln='{}_corner_pin'.format(side), min=-10, max = 10, dv =0, k=True)
            mc.addAttr(jaw_attr, at='double', ln='{}_input_ty'.format(side), min=-10, max=10, dv=0, k=True)

            #create clamp and connect the input _ty to it
            clamp = mc.createNode('clamp', name='{}_corner_pin_auto_CLAMP'.format(side))
            mc.setAttr('{}.minR'.format(clamp), -10)
            mc.setAttr('{}.maxR'.format(clamp), 10)

            mc.connectAttr('{}.{}_input_ty'.format(jaw_attr, side), '{}.inputR'.format(clamp))

            #create condition fot the two possible sccenerarios
            cnd = mc.createNode('condition', name='{}_corner_pin_auto_CND'.format(side))
            mc.setAttr('{}.operation'.format(cnd), 0)
            mc.setAttr('{}.secondTerm'.format(cnd), 1)

            mc.connectAttr('{}.{}_auto_corner_pin'.format(jaw_attr, side), '{}.firstTerm'.format(cnd))
            mc.connectAttr('{}.outputR'.format(clamp), '{}.colorIfTrueR'.format(cnd))
            mc.connectAttr('{}.{}_corner_pin'.format(jaw_attr, side), '{}.colorIfFalseR'.format(cnd))

            #create addition
            plus = mc.createNode('plusMinusAverage', name='{}_corner_pin_PLUS'.format(side))
            mc.setAttr('{}.input1D[1]'.format(plus), 10)
            mc.connectAttr('{}.outColorR'.format(cnd), '{}.input1D[0]'.format(plus))

            #create division
            div = mc.createNode('multDoubleLinear', name='{}_corner_pin_DIV'.format(side))
            mc.setAttr('{}.input2'.format(div), 0.05)
            mc.connectAttr('{}.output1D'.format(plus), '{}.input1'.format(div))

            #add final output attribute to the driver node
            mc.addAttr(pin_driver, at='double', ln='{}_pin'.format(side), min=0, max=1, dv=0)
            mc.connectAttr('{}.output'.format(div), '{}.{}_pin'.format(pin_driver, side))

            #connecting the driver to broad joint contrain targets
            const_pin_up = '{}_{}_broadCorner_JNT_OFF_parentConstraint1.C_{}_broadUpper_JNT_OFFW0'.format(side, JAW, JAW)
            const_pin_down = '{}_{}_broadCorner_JNT_OFF_parentConstraint1.C_{}_broadLower_JNT_OFFW1'.format(side, JAW, JAW)

            mc.connectAttr('{}.{}_pin'.format(pin_driver,side), const_pin_up)
            #creating a rev node for the inverse
            rev = mc.createNode('reverse', name='{}_corner_pin_REV'.format(side))
            mc.connectAttr('{}.{}_pin'.format(pin_driver,side), '{}.inputX'.format(rev))

            #rev to lower target
            mc.connectAttr('{}.outputX'.format(rev), const_pin_down)


        

    def build(self, *args):
        
        self.createHierarchy()
        self.createGuides()


    # Must include *args as a parameter to this function
    # in order to call reference/call it in the ui!
    # This is because, when it is called, a blank args is sent.
    def buildJoints(self, *args):
        # print('printJoints')
        mc.hide('{}_{}_guide_{}'.format(CENTER, JAW, GROUP))
        #after okay in gui
        self.createJawBase()  # creates the joints from the jaw guides
        self.createMinorJoints()  # creates the joints from the minor guides
        self.createBroadJoints()  # creates the joints from the BORAD guides
        # print(lip_guides()) # creates a list for the jaw guides, run in createMinor joints, no need
        # print(jaw_guides())
        
        self.constrainBroadJoints()
        self.getLipParts()  # access and create a libary of the joints GROUPS and where they are, as well as parenting them.  Needed for accessing the joints
        # print(lipPart('upper')) # l SHOULD BE REVERSED and this should return a list of objs that have upper int he name
        self.createSeal('upper')
        self.createSeal('lower')
        self.createJawAttrs()
        self.createConstraints()
        self.createInitalValues('upper')  # creates the weights in the jaw_attributes grp
        self.createInitalValues('lower')  # creates the weights in the jaw_attributes grp
        self.connectSeal('upper')
        self.connectSeal('lower')
        self.createJawPin()




