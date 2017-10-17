from OpenGL.GL import *
import OpenGL.GL.shaders

'''
   loads shader from file into memory
'''

class Shader:

    def __init__(self , fname):
        self.uniformMap = {}
        self.shaderProgram = self.compile_shader(fname)
        view_loc = glGetUniformLocation(self.shaderProgram, "view")
        proj_loc = glGetUniformLocation(self.shaderProgram, "projection")
        model_loc = glGetUniformLocation(self.shaderProgram, "model")
	
        specularIntensity_loc = glGetUniformLocation(self.shaderProgram, "specularIntensity")
        specularPower_loc = glGetUniformLocation(self.shaderProgram, "specularPower")

        reflectAmt_loc = glGetUniformLocation(self.shaderProgram, "reflectAmt")
        refractAmt_loc = glGetUniformLocation(self.shaderProgram, "refractAmt")
        reflectColor_loc = glGetUniformLocation(self.shaderProgram, "reflectColor")
        refractColor_loc = glGetUniformLocation(self.shaderProgram, "refractColor")
        diffuse_loc = glGetUniformLocation(self.shaderProgram, "diffuse")
        skybox_loc = glGetUniformLocation(self.shaderProgram, "skybox")
        mask_loc = glGetUniformLocation(self.shaderProgram, "mask")
        self.uniformMap["view"] = view_loc
        self.uniformMap["projection"] = proj_loc
        self.uniformMap["model"] = model_loc
	self.uniformMap["specularIntensity"] = specularIntensity_loc
	self.uniformMap["specularPower"] = specularPower_loc
	self.uniformMap["reflectAmt"] = reflectAmt_loc
	self.uniformMap["refractAmt"] = refractAmt_loc
        self.uniformMap["reflectColor"] = reflectColor_loc
        self.uniformMap["refractColor"] = refractColor_loc
        self.uniformMap["diffuse"] = diffuse_loc
        self.uniformMap["skybox"] = skybox_loc
        self.uniformMap["mask"] = mask_loc

    def updateUniforms(self , view , proj , model , mat):
        self.setUniformMat4("view" , view)
        self.setUniformMat4("projection" , proj)
        self.setUniformMat4("model" , model)
	self.setUniformFloat("specularIntensity" , mat.specularIntensity)
	self.setUniformFloat("specularPower" , mat.specularPower)
	self.setUniformFloat("reflectAmt" , mat.reflectAmt)
	self.setUniformFloat("refractAmt" , mat.refractAmt)
        self.setUniformVec3("reflectColor" , mat.reflectColor[0] , mat.reflectColor[1] ,  mat.reflectColor[2])
        self.setUniformVec3("refractColor" , mat.refractColor[0] , mat.refractColor[1] , mat.refractColor[2])
        self.setUniformSampler("diffuse" , 0);
        self.setUniformSampler("skybox" , 1);
        self.setUniformSampler("mask" , 2);

    def setUniformMat4(self , uName , value):
        glUniformMatrix4fv(self.uniformMap[uName], 1, GL_FALSE, value)
    def setUniformMat3(self , uName , value):
        glUniformMatrix4fv(self.uniformMap[uName], 1, GL_FALSE, value)
    def setUnifromVec4(self , uName , x , y , z ,w ):
        glUniform4f(self.uniformMap[uName], x, y, z, w)
    def setUniformVec3(self , uName , x , y , z ):
        glUniform3f(self.uniformMap[uName], x, y, z)
    def setUniformFloat(self , uName , x):
        glUniform1f(self.uniformMap[uName], x)
    def setUniformSampler(self , uName , x):
        glUniform1i(self.uniformMap[uName], x);

    def bind(self):
        glUseProgram(self.shaderProgram)

    def load_shader(self , shader_file):
        shader_source = ""
        with open(shader_file) as f:
            shader_source = f.read()
        f.close()
        return str.encode(shader_source)

    def compile_shader(self ,fname):
        vert_shader = self.load_shader(fname + ".vs")
        frag_shader = self.load_shader(fname + ".fs")

        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))
        return shader





