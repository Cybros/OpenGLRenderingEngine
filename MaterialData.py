import numpy as np

'''
   just a placeholder for storing material values 
'''
class MaterialData:
    def __init__(self):
        self.diffuse = "None"
        self.specularIntensity = 0.0
        self.specularPower = 0.0

        self.reflectAmt = 0.0
	self.reflectColor = [0.0 , 0.0 , 0.0]
        self.refractAmt = 0.0
        self.refractColor = [0.0 , 0.0 , 0.0]
