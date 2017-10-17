import glfw
from Shader import *
import numpy
import pyrr
from PIL import Image
from Mesh import *
from Texture import *
import time
import cv2
from FullScreenQuad import *


def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():

    if not glfw.init():
        return

    w_width, w_height = 800, 600

    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)
    #glfw.hide_window(window)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    obj = Mesh("./res/crate.obj" , "./res/box.mat")


    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


    scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([2.0, 2.0, 2.0]))
    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -10.0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(70.0, (float)(w_width) / float(w_height), 0.1, 100.0)
    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))
    model = pyrr.matrix44.multiply(scale , model)

    glClearColor(0.2, 0.3, 0.2, 1.0)


    while not glfw.window_should_close(window):

        rot_y = pyrr.Matrix44.from_y_rotation(0.01 * numpy.fabs(numpy.cos(glfw.get_time())))
        rot_x = pyrr.Matrix44.from_x_rotation(0.01 * numpy.fabs(numpy.sin(glfw.get_time())))
        model = pyrr.matrix44.multiply(rot_y , model)
        model = pyrr.matrix44.multiply(rot_x , model)
        start = time.time()
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
       
        obj.renderALL(view, projection, model)
        glfw.swap_buffers(window)


    glfw.terminate()
if __name__ == "__main__":
    main()
