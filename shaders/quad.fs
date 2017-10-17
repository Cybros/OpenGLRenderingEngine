#version 330
in vec2 newTextureCoords;

out vec4 outColor;
uniform sampler2D samplerTexture;

void main()
{
    outColor = texture2D(samplerTexture, newTextureCoords);
}
