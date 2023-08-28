import bpy
import random

# Clear mesh objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

def create_random_material(name):
    """Create a new material with randomized parameters for a diverse and realistic look."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add a Principled BSDF shader and connect it to the material output
    principled_shader = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Add a noise texture for random normal roughness
    noise_texture = nodes.new(type='ShaderNodeTexNoise')
    noise_texture.inputs["Scale"].default_value = random.uniform(2.0, 15.0)  # Randomize the scale of the noise
    
    # Add a bump node to use the noise texture as a normal map
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = random.uniform(0.2, 1.0)  # Randomize the strength of the bump effect
    mat.node_tree.links.new(noise_texture.outputs["Color"], bump.inputs["Height"])
    mat.node_tree.links.new(bump.outputs["Normal"], principled_shader.inputs["Normal"])
    
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(principled_shader.outputs["BSDF"], material_output.inputs["Surface"])
    
    # Randomize parameters of the Principled BSDF
    principled_shader.inputs["Base Color"].default_value = (random.random(), random.random(), random.random(), 1)
    principled_shader.inputs["Subsurface"].default_value = random.random()
    principled_shader.inputs["Metallic"].default_value = random.random()
    principled_shader.inputs["Specular"].default_value = random.random()
    principled_shader.inputs["Roughness"].default_value = random.uniform(0.1, 0.9)
    principled_shader.inputs["Anisotropic"].default_value = random.random()
    principled_shader.inputs["Sheen"].default_value = random.random()
    principled_shader.inputs["Sheen Tint"].default_value = random.random()
    principled_shader.inputs["Clearcoat"].default_value = random.random()
    principled_shader.inputs["Clearcoat Roughness"].default_value = random.uniform(0.1, 0.9)
    principled_shader.inputs["IOR"].default_value = random.uniform(1.1, 2.5)  # Values typically range from 1 for air to 2.5 for some crystals
    
    return mat

# Create nine spheres with random materials
for i in range(3):
    for j in range(3):
        # Create a sphere
        bpy.ops.mesh.primitive_uv_sphere_add(location=(i*3, j*3, 0))
        sphere = bpy.context.active_object
        sphere.data.use_auto_smooth = True  # Enable auto-smooth
        bpy.ops.object.shade_smooth()  # Smooth shading
        
        # Assign a random material
        mat = create_random_material(f"Material_{i}_{j}")
        sphere.data.materials.append(mat)
