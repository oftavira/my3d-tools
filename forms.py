import bpy
import random

# Clear mesh objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

def create_wood_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create nodes
    texture_coord = nodes.new('ShaderNodeTexCoord')
    wave_texture = nodes.new('ShaderNodeTexWave')
    wave_texture.wave_type = 'RINGS'
    wave_texture.inputs["Scale"].default_value = 4.0

    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    principled_bsdf.inputs["Base Color"].default_value = [0.4, 0.27, 0.13, 1]

    material_output = nodes.new('ShaderNodeOutputMaterial')

    # Link nodes
    mat.node_tree.links.new(texture_coord.outputs["Object"], wave_texture.inputs["Vector"])
    mat.node_tree.links.new(wave_texture.outputs["Color"], principled_bsdf.inputs["Base Color"])
    mat.node_tree.links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])

    return mat

def create_stone_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    noise_texture = nodes.new('ShaderNodeTexNoise')
    noise_texture.inputs["Scale"].default_value = 10.0
    noise_texture.inputs["Detail"].default_value = 16.0

    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    principled_bsdf.inputs["Base Color"].default_value = [0.6, 0.6, 0.6, 1]
    principled_bsdf.inputs["Roughness"].default_value = 0.8

    material_output = nodes.new('ShaderNodeOutputMaterial')

    # Link nodes
    mat.node_tree.links.new(noise_texture.outputs["Color"], principled_bsdf.inputs["Base Color"])
    mat.node_tree.links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])

    return mat

def create_nature_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    voronoi_texture = nodes.new('ShaderNodeTexVoronoi')
    voronoi_texture.inputs["Scale"].default_value = 8.0

    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    principled_bsdf.inputs["Base Color"].default_value = [0.1, 0.5, 0.1, 1]  # Green color

    material_output = nodes.new('ShaderNodeOutputMaterial')

    # Link nodes
    mat.node_tree.links.new(voronoi_texture.outputs["Color"], principled_bsdf.inputs["Base Color"])
    mat.node_tree.links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])

    return mat

# Create three spheres with specific materials
materials = [create_wood_material("WoodMaterial"), create_stone_material("StoneMaterial"), create_nature_material("NatureMaterial")]

for i, mat in enumerate(materials):
    bpy.ops.mesh.primitive_uv_sphere_add(location=(i*3, 0, 0))
    sphere = bpy.context.active_object
    sphere.data.use_auto_smooth = True
    bpy.ops.object.shade_smooth()
    sphere.data.materials.append(mat)
