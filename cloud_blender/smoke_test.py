import bpy
import math
import os

OUT = os.environ.get("BLENDER_OUT", "/tmp/blender-out")
os.makedirs(OUT, exist_ok=True)

# Clean scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Test mesh.
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=(0, 0, 1.0))
obj = bpy.context.active_object
obj.name = "CloudBlender_TestSphere"
bpy.ops.object.shade_smooth()

bev = obj.modifiers.new("MicroBevel", "BEVEL")
bev.width = 0.03
bev.segments = 2

mat = bpy.data.materials.new("CloudBlenderMaterial")
mat.diffuse_color = (0.08, 0.32, 0.8, 1.0)
mat.metallic = 0.25
mat.roughness = 0.28
obj.data.materials.append(mat)

# Ground.
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
plane = bpy.context.active_object
plane.name = "Ground"
ground_mat = bpy.data.materials.new("GroundMaterial")
ground_mat.diffuse_color = (0.12, 0.12, 0.14, 1.0)
ground_mat.roughness = 0.65
plane.data.materials.append(ground_mat)

# Camera.
bpy.ops.object.camera_add(location=(4.2, -4.2, 3.2))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

def point_at(o, target=(0, 0, 1.0)):
    direction = mathutils.Vector(target) - o.location
    o.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

import mathutils
point_at(cam)
cam.data.lens = 55

# Lights.
bpy.ops.object.light_add(type="AREA", location=(3, -2, 5))
key = bpy.context.active_object
key.data.energy = 900
key.data.shape = "DISK"
key.data.size = 4.0
point_at(key)

bpy.ops.object.light_add(type="AREA", location=(-3, 1, 2.5))
fill = bpy.context.active_object
fill.data.energy = 450
fill.data.size = 3.0
point_at(fill)

# Render setup.
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 320
scene.render.resolution_y = 320
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(OUT, "smoke_render.png")
scene.world.color = (0.025, 0.025, 0.035)

# Save and export.
blend_path = os.path.join(OUT, "cloud_blender_smoke.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(
    filepath=os.path.join(OUT, "cloud_blender_smoke.glb"),
    export_format="GLB",
    export_apply=True,
)

bpy.ops.render.render(write_still=True)

with open(os.path.join(OUT, "verification.txt"), "w", encoding="utf-8") as f:
    f.write(f"Blender={bpy.app.version_string}\n")
    f.write(f"Objects={len(bpy.data.objects)}\n")
    f.write(f"Blend={blend_path}\n")
    f.write("SmokeTest=PASS\n")

print("CLOUD_BLENDER_SMOKE_TEST_PASS")
