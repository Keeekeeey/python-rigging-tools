#-----------------------------------------------
# auto limb tool!
#-----------------------------------------------

import maya.cmds as cmds

GROUP = 'grp'
JOINT = 'JNT'

def run():
    rigCreator = autoRigTool()
    rigCreator.init_gui()

class autoRigTool:

    def __init__(self):
        self.jointHierachyCore = []
        self.radius = None
        self.jointHierachy = []
        self.limbName = None
        #edgecase, must be named BEFORE renaming funciton
        #AND not include toes now that i think of it ssdfgsd
        #how many joints are we working with?
        #check selection length
        #hard coded for defualt for now
        self.limbJoints = 4

    def init_gui(self):
        #if the UI already exists, delete it
        UI = cmds.window(title='AutoLimb', width=400)
        if cmds.window(UI, exists = True):
            cmds.deleteUI(UI, window=True)

        UI = cmds.window(title='AutoLimb', width=400)
        cmds.columnLayout(rowSpacing=20)
        cmds.text(label='Auto Limb Tool')
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        cmds.separator(height=1)
        self.masterField = cmds.textField()
        cmds.button('masterToggle', l='Select Master Group if it exists', command='select_master()')
        cmds.separator(height=10)
        cmds.text(l='Rig')
        cmds.intSliderGrp('radius', label= 'Radius, default = 5', min=1, max=100)
        cmds.button('IsArm', label= 'Arm', command='autoLimbTool()')
        cmds.button('IsLeg', label= 'Leg', command='autoLimbTool()')
        cmds.button('IsAnimal', label= 'Animal Leg', command='autoLimbTool()')
        cmds.separator(height=10)
        cmds.showWindow(UI) # shows the window

        #todo:
        #GUI == want to ask if there is a master node, if not then make its own? 
        # In general, make the GUI look nicer. 
        # Could also do a reverse spine if wanted!


    #functions

    def select_master(self, *args):
        if(cmds.ls(selection=True)):
            self.masterSelected = cmds.ls(selection=True)
            cmds.textField(self.masterField, edit=True, tx=str(self.masterSelected))
        


    def StrechCreation(self,*args):

        #-------- ik start

        #creates a distance tool from any point on the ground
        distTool = cmds.distanceDimension( sp=(0, 2, 2), ep=(1, 5, 6) )
        counter = 0
        cmds.rename('locator1',self.limbName +"_IK_strech_loc_1")
        cmds.rename('locator2',self.limbName +"_IK_strech_loc_2")
        
        #snap for the root 
        for jointName in self.jointHierachy:
            #come back and simplify. Need the counter as JointName is storing a string
            if "_Root" in jointName:
                cmds.matchTransform((self.limbName +"_IK_strech_loc_1"), (self.jointHierachy[counter]))
                rootJoint = self.jointHierachyCore[counter]
                break
            counter += 1
        #connect to the wrist or second to last joint
        cmds.matchTransform((self.limbName +"_IK_strech_loc_2"), (self.jointHierachy[len(self.jointHierachy)-2]))

        #parent loc 1 to item above root on IK 
        cmds.parent(self.limbName +"_IK_strech_loc_1",self.jointHierachyCore[(counter-1)]+"_IK")
        cmds.parent(self.limbName +"_IK_strech_loc_2",self.limbName +"_IK_control")

        #creating distance ratio between OG joints and the dist handle so we know how much to strech
        midJoint = (self.jointHierachy[len(self.jointHierachy)-3])
        endJoint = (self.jointHierachy[len(self.jointHierachy)-2])
        Ratio_PMA = cmds.createNode('plusMinusAverage', name='Ratio_PMA')
        cmds.connectAttr('{}.translateY'.format(midJoint),'{}.input1D[0]'.format(Ratio_PMA))
        cmds.connectAttr('{}.translateY'.format(endJoint),'{}.input1D[1]'.format(Ratio_PMA))
        sum = (cmds.getAttr('{}.output1D'.format(Ratio_PMA))+1)
        
        #Ratio_PMA = sum 
        strechFactor = cmds.createNode('multiplyDivide', name=self.limbName+"StrechFactor_multi")
        cmds.setAttr('{}.operation'.format(strechFactor), 2) #sets to divide
        cmds.connectAttr('{}.distance'.format(distTool),'{}.input1X'.format(strechFactor))
        cmds.setAttr('{}.input2X'.format(strechFactor),sum)
        #if strechFactor > 1, strech if < react normally
        Strechcon = cmds.createNode('condition', name=self.limbName+"_Strech_con")
        
        cmds.setAttr('{}.secondTerm'.format(Strechcon), 1) 
        cmds.setAttr('{}.operation'.format(Strechcon), 4) #sets to less than
        #hard coding colorIfTrue = 1
        cmds.setAttr('{}.colorIfTrueR'.format(Strechcon), 1)
        cmds.setAttr('{}.colorIfTrueG'.format(Strechcon), 1)  
        cmds.setAttr('{}.colorIfTrueB'.format(Strechcon), 1) 

        cmds.connectAttr('{}.outputX'.format(strechFactor),'{}.firstTerm'.format(Strechcon))

        midJoint = (self.jointHierachyCore[len(self.jointHierachy)-3])
        #sweating JUST THE ROOT AND MID
        cmds.connectAttr('{}.outColorG'.format(Strechcon),'{}.scaleY'.format(rootJoint+"_IK"))
        cmds.connectAttr('{}.outColorG'.format(Strechcon),'{}.scaleY'.format(midJoint+"_IK"))

        #-------------------- squash factor
        squashFactor = cmds.createNode('multiplyDivide', name=self.limbName+"squashFactor_multi")
        cmds.connectAttr('{}.distance'.format(distTool),'{}.input2X'.format(squashFactor))
        cmds.setAttr('{}.operation'.format(squashFactor), 2) #sets to divide
        cmds.setAttr('{}.input1X'.format(squashFactor),sum)

        cmds.connectAttr('{}.outputX'.format(strechFactor),'{}.input2Z'.format(squashFactor))

        

        #---------- ik  and squash on switch ctrl

        squashBC = cmds.createNode('blendColors', name=(self.limbName+"_squash_bc"))
        Switchctrl_name = self.jointHierachyCore[(len(self.jointHierachyCore) - 2)]+"_SWITCH_ctrl"


        cmds.connectAttr('{}.outputX'.format(strechFactor),'{}.color1G'.format(squashBC))
        cmds.connectAttr('{}.outputG'.format(squashBC),'{}.colorIfFalseG'.format(Strechcon)) 
        cmds.setAttr('{}.color2G'.format(squashBC),1)
        cmds.setAttr('{}.color2B'.format(squashBC),1)

        cmds.connectAttr('{}.strech'.format(Switchctrl_name),'{}.blender'.format(squashBC))

        squashSwitch = cmds.createNode('blendColors', name=(self.limbName+"_squashSwitch_bc"))

        cmds.connectAttr('{}.outputX'.format(squashFactor),'{}.color1R'.format(squashSwitch))
        cmds.connectAttr('{}.outputX'.format(squashFactor),'{}.color1B'.format(squashSwitch))
        cmds.setAttr('{}.color2R'.format(squashSwitch),1)
        cmds.setAttr('{}.color2B'.format(squashSwitch),1)

        cmds.connectAttr('{}.outputR'.format(squashSwitch),'{}.colorIfFalseR'.format(Strechcon))
        cmds.connectAttr('{}.outputB'.format(squashSwitch),'{}.colorIfFalseB'.format(Strechcon))

        squashSwitchFactor = cmds.createNode('multiplyDivide', name=self.limbName+"squashSwitchFactor_multi")
        cmds.connectAttr('{}.volume'.format(Switchctrl_name),'{}.input1X'.format(squashSwitchFactor))
        cmds.setAttr('{}.input2X'.format(squashSwitchFactor), 0.1)
        cmds.connectAttr('{}.outputX'.format(squashSwitchFactor),'{}.blender'.format(squashSwitch))

        volumeSwitchFactor = cmds.createNode('multiplyDivide', name=self.limbName+"squashSwitchFactorFactor_multi")
        cmds.connectAttr('{}.strech'.format(Switchctrl_name),'{}.input1X'.format(volumeSwitchFactor))
        cmds.setAttr('{}.input2X'.format(volumeSwitchFactor),0.1)
        cmds.connectAttr('{}.outputX'.format(volumeSwitchFactor), '{}.input2X'.format(squashSwitchFactor))


        #---------------- prep for squash factor fk
        cmds.connectAttr('{}.strech'.format((rootJoint+"_fk_CTRL")),'{}.scaleY'.format(rootJoint+"_fk_CTRL"))
        cmds.connectAttr('{}.strech'.format((midJoint+"_fk_CTRL")),'{}.scaleY'.format(midJoint+"_fk_CTRL"))

        #----------------- connect blend colors to blend chain
        jointSuffixList = ["_IK","_FK",]
        jointMidfixList = ["_root","_mid"]

        #for x, jointmidfix in enumerate(jointmidfixlist) CHANGE TO LATER
        x = 0 #counter
        #called x because I drafted it with x and im so tired lmao
        for jointMidfix in jointMidfixList:
            StrechBC = cmds.createNode('blendColors', name=(self.limbName+jointMidfix+"_strech_bc"))
            for jointSuffix in jointSuffixList:
                    
                    if jointSuffix == "_IK":
                        cmds.connectAttr('{}.scaleX'.format(self.jointHierachyCore[x+1]+jointSuffix),'{}.color1R'.format(StrechBC))
                        cmds.connectAttr('{}.scaleY'.format(self.jointHierachyCore[x+1]+jointSuffix),'{}.color1G'.format(StrechBC))
                        cmds.connectAttr('{}.scaleZ'.format(self.jointHierachyCore[x+1]+jointSuffix),'{}.color1B'.format(StrechBC))
                        

                    if jointSuffix == "_FK":
                        cmds.connectAttr('{}.scaleX'.format(self.jointHierachyCore[x+1]+jointSuffix),'{}.color2R'.format(StrechBC))
                        cmds.connectAttr('{}.scaleY'.format(self.jointHierachyCore[x+1]+jointSuffix),'{}.color2G'.format(StrechBC))
                        cmds.connectAttr('{}.scaleZ'.format(self.jointHierachyCore[x+1]+jointSuffix),'{}.color2B'.format(StrechBC))
                        #--------- squash factor fk set up
                        #done in here for ease of naming and connection
                        
                        FKsquashFactor = cmds.createNode('multiplyDivide', name=(self.limbName+jointMidfix+"_SquashFactor_multi")) #in here because we only want fk
                        cmds.setAttr('{}.operation'.format(FKsquashFactor), 2) #sets to divide
                        cmds.setAttr('{}.input1X'.format(FKsquashFactor), 1) 
                        cmds.setAttr('{}.input1Z'.format(FKsquashFactor), 1) 
                        cmds.connectAttr('{}.strech'.format((self.jointHierachyCore[x+1]+"_fk_CTRL")),'{}.input2X'.format(FKsquashFactor))
                        cmds.connectAttr('{}.strech'.format((self.jointHierachyCore[x+1]+"_fk_CTRL")),'{}.input2Z'.format(FKsquashFactor))
                        cmds.connectAttr('{}.outputX'.format((FKsquashFactor)),'{}.scaleX'.format(self.jointHierachyCore[x+1]+"_FK"))
                        cmds.connectAttr('{}.outputZ'.format((FKsquashFactor)),'{}.scaleZ'.format(self.jointHierachyCore[x+1]+"_FK"))
            x += 1
        
            #connect the strech bc to the blend joints directly
            
            if jointMidfix == "_mid":
                cmds.connectAttr('{}.outputR'.format(StrechBC),'{}.scaleX'.format(self.jointHierachy[len(self.jointHierachy)-3])) #midJoint
                cmds.connectAttr('{}.outputG'.format(StrechBC),'{}.scaleY'.format(self.jointHierachy[len(self.jointHierachy)-3])) #midJoint
                cmds.connectAttr('{}.outputB'.format(StrechBC),'{}.scaleZ'.format(self.jointHierachy[len(self.jointHierachy)-3])) #midJoint
                cmds.connectAttr('{}.IKFKSwitch'.format( ( self.jointHierachyCore[(len(self.jointHierachyCore) - 2)]+"_SWITCH_ctrl" )),'{}.blender'.format(StrechBC))

            if jointMidfix == "_root":
                cmds.connectAttr('{}.outputR'.format(StrechBC),'{}.scaleX'.format(self.jointHierachy[counter])) #ROOT
                cmds.connectAttr('{}.outputG'.format(StrechBC),'{}.scaleY'.format(self.jointHierachy[counter])) 
                cmds.connectAttr('{}.outputB'.format(StrechBC),'{}.scaleZ'.format(self.jointHierachy[counter]))
                cmds.connectAttr('{}.IKFKSwitch'.format( ( self.jointHierachyCore[(len(self.jointHierachyCore) - 2)]+"_SWITCH_ctrl" )),'{}.blender'.format(StrechBC))

        #connect everything to the IK 
        cmds.connectAttr('{}.outColorR'.format(Strechcon),'{}.scaleX'.format(rootJoint+"_IK"))
        cmds.connectAttr('{}.outColorR'.format(Strechcon),'{}.scaleX'.format(midJoint+"_IK"))
        cmds.connectAttr('{}.outColorB'.format(Strechcon),'{}.scaleZ'.format(rootJoint+"_IK"))
        cmds.connectAttr('{}.outColorB'.format(Strechcon),'{}.scaleZ'.format(midJoint+"_IK"))

        #renamed last because it's new name is not stored, only the og name
        cmds.rename('distanceDimension1',self.limbName +"_IK_strech_handle")


    def JointNameCoreFinder(self, *args):
        #finds the root name of the joint for easier naming convention

        
        RootCounter = 0
        for joint in self.jointHierachy:
            secondDash = joint.find('_',2)
            #goal is to store what is between those two values
            limbNameCore = joint[0:int(secondDash)]
            self.jointHierachyCore.append(limbNameCore)
            if "_Root" in joint:
                RootCounter +=1
        
        #throws an error if there is not a designated '_Root' joint
        if (RootCounter == 0):
            cmds.error("Please name at least one joint with _Root. Example : l_arm_Root_JNT instead of l_armRoot_JNT")

        return self.jointHierachyCore


    def IKCtrls(self, *args):
        
        # creates IK ctrl and parents handles under
        newctrlName = self.limbName + "_IK_control"
        #create grp then match grp
        ctrl = cmds.circle(c=(0,0,0), nr=(0,1,0),r=self.radius, ch=0, name= newctrlName)[0]
        ctrl_group=cmds.group(ctrl,name=newctrlName+'_OffSet_'+GROUP)
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideEnabled'),1)
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideColor'), 15)

        cmds.matchTransform(ctrl_group, (self.jointHierachy[len(self.jointHierachy)-2]))

        cmds.select(cl=True)
    
        #creates IK handles depending on if animal or human 
        if (cmds.checkBox('IsArm', query=True, value=True)==True) or (cmds.checkBox('IsLeg', query=True, value=True)==True):
            #if arm, it creates one IK solver
            cmds.ikHandle(n=(self.limbName + "_ikHandle"),sol="ikRPsolver", 
                        sj=(self.jointHierachyCore[1]+"_IK"), 
                        ee=(self.jointHierachyCore[3]+"_IK"), )
            #knee control offset
            cmds.parent((self.limbName + "_ikHandle"), ctrl)
            

        
        #if animal
        if (cmds.checkBox('IsAnimal', query=True, value=True)==True):
            pawCtrlName = self.limbName + "_IK_control"
            kneeCtrlName = self.limbName + "_hock_PV_control"
            #if rear leg, create an IK handle from femus to metacarpus
            if (cmds.checkBox('IsBackLeg', query=True, value=True)==True):
                cmds.ikHandle(n=(self.limbName + "_driver_ikHandle"),sol="ikRPsolver", 
                            sj=(self.jointHierachyCore[0]+"_driver"), 
                            ee=(self.jointHierachyCore[3]+"_driver"), )
                
            Kneectrl = cmds.circle(c=(0,0,0), nr=(0,1,0),r=self.radius, ch=0, name= kneeCtrlName)[0]
            Kneectrl_group=cmds.group(ctrl,name=Kneectrl+'_OffSet_'+GROUP)
            cmds.matchTransform(Kneectrl_group, (self.jointHierachy[len(self.jointHierachy)-2]))
            #need to parent to hock IK control to tibia cc
            #so tired, a little afraid I'll brain fog this so no more today

            #create main IK handle from the femur
            cmds.ikHandle(n=(self.limbName + "_knee_ikHandle"),sol="ikRPsolver", 
                            sj=(self.jointHierachyCore[0]+"_IK"), 
                            ee=(self.jointHierachyCore[2]+"_IK"), )
            #knee control offset
            cmds.group((self.limbName + "_knee_ikHandle"), n=(self.limbName + "_knee_control"))
            cmds.group((self.limbName + "_knee_control"), n=(self.limbName + "_knee_control_offset"))
            #for hockw control
            cmds.ikHandle(n=(self.limbName + "_hock_ikHandle"),sol="ikSCsolver", 
                            sj=(self.jointHierachyCore[2]+"_IK"), 
                            ee=(self.jointHierachyCore[3]+"_IK"), )
            
            #hock control offset
            cmds.group((self.limbName + "_hock_ikHandle"), n=(self.limbName + "_hock_control"))
            cmds.group((self.limbName + "_hock_control"), n=(self.limbName + "_hock_offset"))

            
            #find ankle pivot
            anklePiv = cmds.xform(self.jointHierachy[3], q=1, ws=1, piv=1)
            # Set the groups pivot to match the ankle position
            cmds.xform( ((self.limbName + "_knee_control"), (self.limbName + "_knee_control_offset")), ws=1, piv=(anklePiv[0], anklePiv[1], anklePiv[2]) )

            # Parent the ik handle and the group to the paw control
            cmds.parent( (self.limbName + "_hock_offset"), pawCtrlName )
            cmds.parent( (self.limbName + "_knee_control_offset"), pawCtrlName )
            cmds.parent( Kneectrl, pawCtrlName )

            # If its the rear leg, adjust the hierachy so the driver leg controls the ik handles
            if (cmds.checkBox('IsBackLeg', query=True, value=True)==True):
                

                cmds.parent( (self.limbName + "_knee_control_offset"), (self.jointHierachy[2] + "_driver") )
                cmds.parent( (self.limbName + "_hock_ikHandle"), (self.jointHierachy[3] + "_driver") )

                cmds.parent( (self.limbName + "_driver_ikHandle"), pawCtrlName )
                
                # Make the paw control drive the ankle joint to maintain its orientation
                cmds.orientConstraint(pawCtrlName, (self.jointHierachy[3] + "_ik"),  w=1 )
                
                # Add the pole vector to the driver IK handle if its the rear leg, if its the front add it to the knee ik handle
                cmds.poleVectorConstraint( kneeCtrlName, (self.limbName + "_driver_ikHandle"), w=1 )
            else:
                cmds.poleVectorConstraint( kneeCtrlName, (self.limbName + "_knee_ikHandle"), w=1 )

        #-----------------------------------------------------------
        

    def FKctrls(self, *args, lastJoint = "", joint = ""):
        #creates ctrl
        jointPos =""
        ctrlName= "_fk"
        newctrlName = joint + ctrlName
        #create grp then match grp
        ctrl = cmds.circle(c=(0,0,0), nr=(0,1,0),r= self.radius , ch=0, name= newctrlName+"_CTRL")[0]
        cmds.addAttr(shortName='strech', defaultValue=1.0, minValue=0.00, maxValue=10, k=True)
        ctrl_group=cmds.group(ctrl,name=newctrlName+'_OffSet_'+GROUP)

        cmds.matchTransform(ctrl_group, jointPos)
        #sets color to green
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideEnabled'),1)
        cmds.setAttr((cmds.listRelatives(ctrl, type='shape')[0] + '.overrideColor'), 14)

        cmds.select(ctrl)

        #creates joint
        newJointName =  joint + "_FK"

        #parented under CRTL by default because it's still selected
        cmds.joint(n=newJointName)
        cmds.matchTransform(newJointName, jointPos)
        #zeros ROTATION not translation im silly
        cmds.makeIdentity(newJointName, a=1,t=0,r=1,s=0)
        
        if lastJoint != "": #if there is a previous joint
            #parent ctrl_grp under last joint
            cmds.parent(ctrl_group,lastJoint)

        lastJoint = newJointName
        return lastJoint


    def dupAndRename(self,*args):
        newJointList= ["_IK","_fk",]
        lastJoint = ""
        for newJoint in newJointList:
            for x in range(self.limbJoints):
                if newJoint == "_fk":
                    jointFK = self.jointHierachyCore[x]
                    lastJoint = self.FKctrls(lastJoint, jointFK)

                else:
                    newJointName = self.jointHierachyCore[x] + newJoint
                    cmds.joint(n=newJointName)
                    cmds.matchTransform(newJointName, self.jointHierachy[x])
                    #zeros ROTATION not translation im dumb
                    cmds.makeIdentity(newJointName, a=1,t=0,r=1,s=0)
            cmds.select(cl=1)
        
        cmds.select(cl=1)
        
        
    def constrain(self, *args):

        #setup Switch
        place = len(self.jointHierachyCore) - 2
        Switchctrl_name = self.jointHierachyCore[place]+"_SWITCH_ctrl"
        Switchctrl = cmds.circle(c=(0,0,0), nr=(0,1,0),r=(self.radius + 2), degree=1,sections=4,ch=0, name= Switchctrl_name)[0]
        

        cmds.select(Switchctrl)
        cmds.addAttr(shortName='switch', longName='IKFKSwitch', defaultValue=1.0, minValue=0.00, maxValue=1, k=True)
        cmds.addAttr(shortName='strech', defaultValue=1.0, minValue=0.00, maxValue=1, k=True)
        cmds.addAttr(shortName='volume', defaultValue=10.0, minValue=0.00, maxValue=10, k=True)
        
        if (cmds.checkBox('IsArm', query=True, value=True)==True):
            cmds.addAttr(shortName='AutoShoulder', defaultValue=1.0, minValue=0.00, maxValue=1, k=True)
        

        switch_ctrl_group= cmds.group(Switchctrl,name=self.jointHierachyCore[place]+'_SWITCH_OffSet_'+GROUP)
        cmds.setAttr((cmds.listRelatives(Switchctrl, type='shape')[0] + '.overrideEnabled'),1)
        cmds.setAttr((cmds.listRelatives(Switchctrl, type='shape')[0] + '.overrideColor'), 16)

        cmds.matchTransform(switch_ctrl_group, (self.jointHierachy[len(self.jointHierachy)-2]))

        #constrain main joints to the IK and FK to BLEND

        for i in range(self.limbJoints):
            cmds.parentConstraint( (self.jointHierachyCore[i] + "_IK"),  
                                (self.jointHierachyCore[i] + "_FK"),  
                                (self.jointHierachy[i]), w = 1, mo=0)
            ParentContraintName = '{}_parentConstraint1'.format(self.jointHierachy[i])
            FKName = self.jointHierachyCore[i] + "_FKW1"
            #inside of the for loop, connect IKFKSwitch to first parent constraint
            #connecting Fk which will always be W1
            cmds.connectAttr('{}.IKFKSwitch'.format(Switchctrl_name),'{}.{}'.format(ParentContraintName,FKName))
            #connecting IK which will always be W2

            IKName = self.jointHierachyCore[i] + "_IKW0"
            multi_y = cmds.createNode('remapValue', name='SWITCH_{}_IK_REMAP'.format(self.jointHierachyCore[i]))
            cmds.setAttr('{}.value[1].value_FloatValue'.format(multi_y), 0)
            cmds.setAttr('{}.value[0].value_FloatValue'.format(multi_y), 1)
            #setAttr "SWITCH_l_armWrist_IK_REMAP.value[0].value_FloatValue" 1;
            # cmds.setAttr('{}.input2X'.format(multi_y), -1)
            cmds.connectAttr('{}.IKFKSwitch'.format(Switchctrl_name),'{}.inputValue'.format(multi_y))
            cmds.connectAttr('{}.outValue'.format(multi_y),'{}.{}'.format(ParentContraintName,IKName))
        
        #sets up visiblity toggle
        #outside of for loop because it just needs to be to parent joints
        cmds.connectAttr('{}.IKFKSwitch'.format(Switchctrl_name),'{}.visibility'.format((self.jointHierachyCore[0]+"_fk_OffSet_grp")))
        cmds.connectAttr('{}.outValue'.format(multi_y),'{}.visibility'.format((self.jointHierachyCore[0]+"_IK")))
        cmds.connectAttr('{}.outValue'.format(multi_y),'{}.visibility'.format((self.limbName+"_IK_control")))

        #creating the locs for the switch to follow and constrains
        IK_loc = cmds.spaceLocator(name= self.limbName+"_IK_SWITCH_loc")
        FK_loc = cmds.spaceLocator(name= self.limbName+"_FK_SWITCH_loc")

        cmds.matchTransform(IK_loc,self.limbName+"_IK_control")
        cmds.matchTransform(FK_loc,self.jointHierachy[len(self.jointHierachy)-2])

        cmds.parent(IK_loc,self.limbName+"_IK_control")
        cmds.parent(FK_loc,self.jointHierachyCore[len(self.jointHierachy)-2]+"_FK")

        cmds.parentConstraint((IK_loc), (FK_loc), Switchctrl, w = 1, mo=0)

        cmds.connectAttr('{}.IKFKSwitch'.format(Switchctrl),'{}_parentConstraint1.{}'.format(Switchctrl,(self.limbName+"_FK_SWITCH_locW1")))
        cmds.connectAttr('{}.outValue'.format(multi_y),'{}_parentConstraint1.{}'.format(Switchctrl_name,(self.limbName+"_IK_SWITCH_locW0")))


    def autoLimbTool(self, *args):
        #pass varible from UI

        #checking selection is vaild
        #will store everything slected in a list, and will only do
        #so if joint, no faulse flags
        selectionCheck = cmds.ls(sl=1,type="joint")
        if not selectionCheck:
            cmds.error("Please select the root joint")
        else:
            rootJoint = cmds.ls(sl=1,type="joint")[0]

        self.radius = cmds.intSliderGrp('radius', query=True, value=True)
        if self.radius != 1:
            pass
        else:
            self.radius = 5

        #which side for naming convention

        SIDE = rootJoint[0:2] #searchs first 2 str 

        if not "l_" in SIDE:
            if not "r_" in SIDE:
                if not "c_" in SIDE:
                    cmds.error("Please name your joints with either l_, r_ or c_")

        #---------------------------------------------
        #make more modular
        #bulding names
        #-------------------joint name throwing error
        if (cmds.checkBox('IsArm', query=True, value=True)==False) and (cmds.checkBox('IsLeg', query=True, value=True)==False) and (cmds.checkBox('IsAnimal', query=True, value=True)==False):
            cmds.error("Please select either Arm or Leg or Animal")
        elif (cmds.checkBox('IsArm', query=True, value=True)==True) and (cmds.checkBox('IsLeg', query=True, value=True)==True) and (cmds.checkBox('IsAnimal', query=True, value=True)==True):
            cmds.error("Please select either Arm or Leg or Animal, not both or all")
        elif (cmds.checkBox('IsArm', query=True, value=True)==True):
            limbName = SIDE +"arm"
        elif (cmds.checkBox('IsLeg', query=True, value=True)==True):
            limbName = SIDE +"leg"
        elif (cmds.checkBox('IsAnimal', query=True, value=True)==True):
            limbName = SIDE +"animal"
        
        #-----------------
        #builds list of joints, starting with root
        
        #finds children
        #ad = all decendents
        self.jointHierachy = cmds.listRelatives(rootJoint, ad=1, type="joint")
        #adds the selected joint
        self.jointHierachy.append(rootJoint)
        #reverse list order, so root -->
        self.jointHierachy.reverse()

        #clear selection
        cmds.select(cl=1)

        #creates and array with just the names for ease of naming
        self.jointHierachyCore = self.JointNameCoreFinder(self.jointHierachy)

        #-----------------------------

        
        #------------------
        cmds.select(cl=True)
        #duplicates main joint chain and creates the FK joints with their relationships
        #and creates the strech joints
        self.dupAndRename()

        #can't run as part of the dupAndRename command because IK only 
        # happens once, no need for recurresion and happens after all joints 
        # are made. Made outside of dupandRename for easier reading
        self.IKCtrls()

        #constrains Blend, IK and FKjoints as well as links attributes
        self.constrain()

        #creates strech nodes and minor connections
        self.StrechCreation()



        # #sets up IK based on given info
        # if (cmds.checkBox('IsArm', query=True, value=True)==True):
        #     #calls function that creates front
        #     IKHumanArmCtrls(limbName, jointHierachy)

        # if (cmds.checkBox('IsAnimal', query=True, value=True)==True):
        #     IKAnimalctrls(limbName, jointHierachy)


        

