#version 330
in layout(location = 0) vec2 position;


uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

out vec2 newTextureCoords;
void main()
{
    gl_Position = vec4(position , 0, 1);
    newTextureCoords = vec2((position.x+1.0)/2.0, (-position.y+1.0)/2.0);

}
