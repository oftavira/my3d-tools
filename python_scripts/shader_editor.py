import bpy

# Get the active shader node tree
tree = bpy.context.active_object.active_material.node_tree

# Clear existing nodes in the Shader Editor
for node in tree.nodes:
    tree.nodes.remove(node)

# Create the Shader Editor nodes
tex_coord_node = tree.nodes.new(type='ShaderNodeTexCoord')
tex_coord_node.location = (-400, 400)

mapping_node = tree.nodes.new(type='ShaderNodeMapping')
mapping_node.location = (-200, 400)

normal_map_node = tree.nodes.new(type='ShaderNodeNormalMap')
normal_map_node.location = (0, 400)

displacement_node = tree.nodes.new(type='ShaderNodeDisplacement')
displacement_node.location = (200, 400)

image_texture_nodes = []
image_texture_locations = [(-400, 200), (-200, 200), (0, 200), (200, 200)]

for i in range(4):
    image_texture_node = tree.nodes.new(type='ShaderNodeTexImage')
    image_texture_node.location = image_texture_locations[i]
    image_texture_nodes.append(image_texture_node)

# Create Principled BSDF and Material Output nodes
principled_bsdf_node = tree.nodes.new(type='ShaderNodeBsdfPrincipled')
principled_bsdf_node.location = (400, 0)

material_output_node = tree.nodes.new(type='ShaderNodeOutputMaterial')
material_output_node.location = (600, 0)

# Connect the nodes as specified
tree.links.new(tex_coord_node.outputs['UV'], mapping_node.inputs['Vector'])

for i in range(4):
    tree.links.new(mapping_node.outputs['Vector'], image_texture_nodes[i].inputs['Vector'])

tree.links.new(image_texture_nodes[0].outputs['Color'], principled_bsdf_node.inputs['Base Color'])
tree.links.new(image_texture_nodes[1].outputs['Color'], principled_bsdf_node.inputs['Roughness'])

tree.links.new(image_texture_nodes[2].outputs['Color'], normal_map_node.inputs['Color'])
tree.links.new(normal_map_node.outputs['Normal'], principled_bsdf_node.inputs['Normal'])

tree.links.new(image_texture_nodes[3].outputs['Color'], displacement_node.inputs['Height'])
tree.links.new(displacement_node.outputs['Displacement'], material_output_node.inputs['Displacement'])

# Connect Principled BSDF to Material Output
tree.links.new(principled_bsdf_node.outputs['BSDF'], material_output_node.inputs['Surface'])

# Select the Displacement node for easy access
displacement_node.select = True
tree.nodes.active = displacement_node
