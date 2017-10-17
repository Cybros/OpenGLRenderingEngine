from PIL import Image
from OpenGL.GL import *
import numpy

'''
    loads a 2d texture from file into memory
'''
class Texture:
    def __init__(self , fname):
        self.texture_id = 0
        self.width= 0
        self.height= 0
	self.loadTexture(fname)
    def loadTexture(self , fname):
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)
        # load image
        image = Image.open(fname)
        self.width = image.size[0]
        self.height = image.size[1]

        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)

        img_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB,
                     GL_UNSIGNED_BYTE, img_data)
        glEnable(GL_TEXTURE_2D)
    def bind(self , id):
        glActiveTexture(id)
        glBindTexture(GL_TEXTURE_2D , self.texture_id)
