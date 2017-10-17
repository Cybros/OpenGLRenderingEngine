from PIL import Image
from OpenGL.GL import *
import numpy
'''
    loads a 3d texture ( Cube Map ) from file into memory
'''
class Texture3D:
    def __init__(self , fname):
        self.texture_id = 0
        self.width= 0
        self.height= 0
	self.loadTexture(fname)
    def loadTexture(self , fname):
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture_id)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_REPEAT)
        # Set texture filtering parameters
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
        # load image
	images = []
        images.append(Image.open(fname + "/posx.jpg"))
	images.append(Image.open(fname + "/negx.jpg"))
	images.append(Image.open(fname + "/posy.jpg"))
	images.append(Image.open(fname + "/negy.jpg"))
	images.append(Image.open(fname + "/posz.jpg"))
	images.append(Image.open(fname + "/negz.jpg"))
        self.width = images[0].size[0]
        self.height = images[0].size[1]
	
	for i in range(6):
            images[i] = images[i].transpose(Image.FLIP_TOP_BOTTOM)
	    images[i] = numpy.array(list(images[i].getdata()), numpy.uint8)
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, self.width, self.height, 0, GL_RGB,
                     GL_UNSIGNED_BYTE, images[i])
        
        #glGenerateMipmap(GL_TEXTURE_CUBE_MAP)
        glEnable(GL_TEXTURE_CUBE_MAP)
    def bind(self , id):
        glActiveTexture(id)
        glBindTexture(GL_TEXTURE_CUBE_MAP , self.texture_id)
