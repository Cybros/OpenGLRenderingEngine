#version 330
#define REFRACT_INDEX		vec3 (2.407, 2.426, 2.451)
#define RAY_LENGTH_MAX		20.0
#define RAY_BOUNCE_MAX		4
#define DELTA	0.01
#define PI		3.14159265359

in vec2 newTexture;
in vec3 newNormal;
in vec3 worldPos0;
in vec4 clipSpace;

out vec4 outColor;
uniform sampler2D diffuse;
uniform samplerCube skybox;
uniform sampler2D mask;

uniform float specularIntensity ;
uniform float specularPower ;
uniform float reflectAmt ;
uniform float refractAmt ;
uniform vec3 reflectColor ;
uniform vec3 refractColor ;

struct BaseLight
{
	vec3 color;
	float intensity;
};
vec4 calcLightDiffuse(BaseLight base , vec3 direction , vec3 normal)
{
	float diffuseFactor = dot(normalize(normal) , -normalize(direction));
	vec4 diffuseColor = vec4(0,0,0,0);
	
	if(diffuseFactor > 0)
	{
		diffuseColor = vec4(base.color,1)*base.intensity*diffuseFactor;
	}
	return diffuseColor;
}
vec4 calcLightSpec(BaseLight base , vec3 direction , vec3 normal)
{
	vec3 eyePos = vec3(0,0,0);

	vec3 directionToEye = normalize(eyePos-worldPos0);
	vec3 reflectDirection = normalize(reflect(direction , normal));
	vec4 specularColor = vec4(0,0,0,0);

	float specularFactor = dot(directionToEye , reflectDirection);
	if(specularFactor > 0 )
	{
		specularFactor = pow(specularFactor , specularPower);
		specularColor = vec4(base.color , 1.0)*specularFactor*specularIntensity;
	}
	return specularColor;
}
vec3 calcReflectedTexCoords(vec3 normal, vec3 worldPos)
{
	vec3 viewVector = normalize(worldPos);
	vec3 reflectedVector = reflect(viewVector , normal);
	return normalize(reflectedVector);
}
vec3 calcRefractedTexCoords(vec3 normal , vec3 worldPos , float factor)
{
	vec3 viewVector = normalize(worldPos);
	vec3 refractedVector = refract(viewVector , normal , factor);
        return normalize(refractedVector);
}

void main()
{
    vec2 ndc  = (clipSpace.xy/clipSpace.w)/2.0 + 0.5;
    vec2 maskCoords = vec2(ndc.x , ndc.y);
    vec3 direction = normalize (worldPos0);
    BaseLight b1 ;
    b1.color = vec3(1.0,1.0,1.0);
    b1.intensity = 1.0f;
    vec4 diffuseColor = texture(diffuse , newTexture);
    
    outColor = calcLightDiffuse(b1 , vec3(-1,-1,-1) , newNormal);
    
    outColor = diffuseColor;
   
}
