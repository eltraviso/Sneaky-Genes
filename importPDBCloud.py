import bpy
import os

from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator


class OT_TestOpenFilebrowser(Operator, ImportHelper):

    bl_idname = "test.open_filebrowser"
    bl_label = "Import"

    def execute(self, context):        
        atomCount = 0
        atomRef = ""
        
        #isolate filename and use that to name molecule and 
        refName = os.path.basename(self.filepath)    
        filename, extension = os.path.splitext(self.filepath)
        refName = refName[:len(refName) - len(extension)]
        
        #declare empty vertex groups
        hydrogens = []
        carbons = []
        nitrogens = []
        oxygens = []
        phosphorous = []
        sulfur = []

        #make cube, merge all to central point
        bpy.ops.mesh.primitive_cube_add(enter_editmode=True)
        bpy.ops.mesh.merge(type='CENTER')

        #select and rename object
        obj = bpy.context.active_object
        obj.name = refName
        me = obj.data

        #open file
        print(self.filepath)
        readFile = open(self.filepath)
        
        #read each line of the file, import if line starts with ATOM
        for line in readFile:
            #clean up extra formatting spaces, tabs
            while line.find("  ") != -1:
                line = line.replace("  ", " ")
            
            #split line into array
            lineArray = line.split(" ",-1)
            
            if lineArray[0] == "ATOM":
                #duplicate vertex if it's not the first one
                if atomCount != 0:
                    bpy.ops.mesh.duplicate(mode=1)
                
                #switch back to object mode for vertex assignment
                bpy.ops.object.mode_set(mode = 'OBJECT')
                
                #deselect everything unless it's the first point
                if atomCount != 0:
                    bpy.context.active_object.select_set(False)
                
                for vertex in bpy.context.active_object.data.vertices:
                    vertex.select = False
                me.vertices[atomCount].select = True
                
                #add vertex to proper atom group
                if lineArray[2].find("H") != -1:
                    hydrogens.append(atomCount)
                elif lineArray[2].find("C") != -1:
                    carbons.append(atomCount)
                elif lineArray[2].find("N") != -1:
                    nitrogens.append(atomCount)
                elif lineArray[2].find("O") != -1:
                    oxygens.append(atomCount)
                elif lineArray[2].find("P") != -1:
                    phosphorous.append(atomCount)
                elif lineArray[2].find("SD") != -1:
                    sulfur.append(atomCount)
                
                selectedVerts = [v for v in bpy.context.active_object.data.vertices if v.select]
                
                for vert in selectedVerts:
                    vert.co = (float(lineArray[6]),float(lineArray[7]),float(lineArray[8]))            
                
                #switch back to edit mode
                bpy.ops.object.mode_set(mode = 'EDIT')
                
                atomCount = atomCount+1    

        readFile.close()

        bpy.ops.object.mode_set(mode = 'OBJECT')

        #create appropriate vertex groups and assign points
        if len(hydrogens) != 0:
            obj.vertex_groups.new(name = refName + "_H")
            obj.vertex_groups[refName + "_H"].add(hydrogens,1.0,'ADD')

        if len(carbons) != 0:
            obj.vertex_groups.new(name = refName + "_C")
            obj.vertex_groups[refName + "_C"].add(carbons,1.0,'ADD')

        if len(nitrogens) != 0:
            obj.vertex_groups.new(name = refName + "_N")
            obj.vertex_groups[refName + "_N"].add(nitrogens,1.0,'ADD')

        if len(oxygens) != 0:
            obj.vertex_groups.new(name = refName + "_O")
            obj.vertex_groups[refName + "_O"].add(oxygens,1.0,'ADD')

        if len(phosphorous) != 0:
            obj.vertex_groups.new(name = refName + "_P")
            obj.vertex_groups[refName + "_P"].add(phosphorous,1.0,'ADD')
        
        if len(sulfur) != 0:
            obj.vertex_groups.new(name = refName + "_S")
            obj.vertex_groups[refName + "_S"].add(sulfur,1.0,'ADD')

        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_TestOpenFilebrowser)


def unregister():
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)


if __name__ == "__main__":
    register()

    bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')