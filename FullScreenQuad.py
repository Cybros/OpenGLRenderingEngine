import numpy as np
from OpenGL.GL import *
from Shader import *
from MaterialData import*
import pyrr

'''
   objects of this class can draw a fullscreen 2d plane covering whole screen . 
'''

class FullScreenQuad:

    def __init__(self , fname):
        self.shader = Shader(fname)
        self.mat = MaterialData()
        self.identityMat = pyrr.matrix44.create_identity()
        vertices = [-1 , 1 , -1 , -1 , 1 , 1 , 1 ,  -1]
        vertices =  np.array(vertices, dtype='float32')
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo);
        glBufferData(GL_ARRAY_BUFFER,8*4 , vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None);

        glBindVertexArray(0);

    def renderFullScreenQuad(self):
        self.shader.bind()
        self.shader.updateUniforms(self.identityMat , self.identityMat ,self.identityMat , self.mat)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
        glBindVertexArray(0);
