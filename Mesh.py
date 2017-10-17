import numpy as np
import MeshData
import MaterialData
import Texture
from Shader import *
from OpenGL.GL import *

'''
this class loads .obj and .mat files from harddrive and render it on screen 

'''

class Mesh:
    def __init__(self , OBJname , MATname):  #loads .obj and .mat files
        self.meshData = []
        self.materialData = []
        self.count = 0
        self.VBOs = []
        self.VAOs = []
        self.shader = Shader("./shaders/diffuseSpec")  #loads the master shader
        self.textures = []
        self.loadMesh(OBJname)
        self.loadMaterial(MATname)
        self.loadDataInGPU()

    def loadMaterial(self , fname):                  
        for line in open(fname, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'o':
                data = []
                data = MaterialData.MaterialData()
                self.materialData.append(data)
            if values[0] == 'diffuse':
                data.diffuse = values[2]
                self.textures.append(Texture.Texture("./res/" + data.diffuse))
            if values[0] == 'specularIntensity':
                data.specularIntensity = np.float32(float(values[2]))
            if values[0] == 'specularPower':
                data.specularPower = np.float32(float(values[2]))
            if values[0] == 'reflectAmt':
                data.reflectAmt = np.float32(float(values[2]))
            if values[0] == 'reflectColor':
                data.reflectColor[0] = np.float32(float(values[1]))
                data.reflectColor[1] = np.float32(float(values[2]))
                data.reflectColor[2] = np.float32(float(values[3]))
                
            if values[0] == 'refractAmt':
                data.refractAmt = np.float32(float(values[2]))
	    if values[0] == 'refractColor':
                data.refractColor[0]= np.float32(float(values[1]))
                data.refractColor[1]= np.float32(float(values[2]))
                data.refractColor[2]= np.float32(float(values[3]))
		


    def loadMesh(self, fname):
        data = []
        for line in open(fname, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'o':
                data = []
                data = MeshData.MeshData()
                self.meshData.append(data)
                self.count = self.count + 1
                for c in values[1:]:
                    data.name += c

            if values[0] == 'v':
                data.vert_coords.append(values[1:4])
            if values[0] == 'vt':
                data.text_coords.append(values[1:3])
            if values[0] == 'vn':
                data.norm_coords.append(values[1:4])

            if values[0] == 'f':
                face_i = []
                text_i = []
                norm_i = []
                for v in values[1:4]:
                    w = v.split('/')
                    vOffset = 0
                    tOffset = 0
                    nOffset = 0
                    if (self.count >= 2):
                        for g in range(self.count - 1):
                            vOffset += len(self.meshData[g].vert_coords)
                            tOffset += len(self.meshData[g].text_coords)
                            nOffset += len(self.meshData[g].norm_coords)
                    face_i.append(int(w[0]) - 1 - vOffset)
                    text_i.append(int(w[1]) - 1 - tOffset)
                    norm_i.append(int(w[2]) - 1 - nOffset)
                data.vertex_index.append(face_i)
                data.texture_index.append(text_i)
                data.normal_index.append(norm_i)

        for k in range(self.count):
            self.meshData[k].vertex_index = [y for x in self.meshData[k].vertex_index for y in x]
            self.meshData[k].texture_index = [y for x in self.meshData[k].texture_index for y in x]
            self.meshData[k].normal_index = [y for x in self.meshData[k].normal_index for y in x]

            for i in self.meshData[k].vertex_index:
                self.meshData[k].model.extend(self.meshData[k].vert_coords[i])

            for i in self.meshData[k].texture_index:
                self.meshData[k].model.extend(self.meshData[k].text_coords[i])

            for i in self.meshData[k].normal_index:
                self.meshData[k].model.extend(self.meshData[k].norm_coords[i])

            self.meshData[k].model = np.array(self.meshData[k].model, dtype='float32')


    def loadDataInGPU(self):
        for i in range(self.count):
            texture_offset = len(self.meshData[i].vertex_index) * 12
            normal_offset = (texture_offset + len(self.meshData[i].texture_index) * 8)
            self.VAOs.append(glGenVertexArrays(1))
            glBindVertexArray(self.VAOs[i])
            self.VBOs.append(glGenBuffers(1))

            glBindBuffer(GL_ARRAY_BUFFER, self.VBOs[i])
            glBufferData(GL_ARRAY_BUFFER, self.meshData[i].model.itemsize * len(self.meshData[i].model),
                     self.meshData[i].model, GL_STATIC_DRAW)

            # position
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.meshData[i].model.itemsize * 3,
                                  ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            # texture
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.meshData[i].model.itemsize * 2,
                              ctypes.c_void_p(texture_offset))
            glEnableVertexAttribArray(1)
            #normal
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.meshData[i].model.itemsize * 3,
                                  ctypes.c_void_p(normal_offset))
            glEnableVertexAttribArray(2)

            glBindVertexArray(0)

    def renderALL(self , view, projection, model):
        self.shader.bind()
        
        for i in range(self.count):
            self.textures[i].bind(GL_TEXTURE0)
            self.shader.updateUniforms(view , projection , model ,self.materialData[i] )
            glBindVertexArray(self.VAOs[i])
            glDrawArrays(GL_TRIANGLES, 0, len(self.meshData[i].vertex_index))
            glBindVertexArray(0)













