#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 textureCoords;
in layout(location = 2) vec3 normal;


uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

out vec2 newTexture;
out vec3 newNormal;
out vec3 worldPos0;
out vec4 clipSpace;
void main()
{
    vec4 pos = projection * view * model * vec4(position, 1.0f);
    clipSpace = pos;
    gl_Position = pos;
    worldPos0 =vec3(view*model*vec4(position, 1.0f));
    
    newTexture = textureCoords;
    newNormal = vec3(vec4(normal,1.0f));
   
}
