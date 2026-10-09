"""Blender (bpy) side: build meshes, export GLB/FBX and render previews."""
import math
import os

import bpy
import numpy as np
from mathutils import Vector

from meshing import EMIT_MAX, palette_uv

VOXEL_M = 0.06    # 1 voxel = 6 cm (a common ~5 m tall, the Secret ~10 m)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_material(tex_paths, name="M_Brainrot", emit_strength=EMIT_MAX):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    def tex(path, colorspace):
        node = nt.nodes.new("ShaderNodeTexImage")
        img = bpy.data.images.load(os.path.abspath(path), check_existing=False)
        img.colorspace_settings.name = colorspace
        node.image = img
        node.interpolation = "Closest"
        return node

    base = tex(tex_paths["BaseColor"], "sRGB")
    orm = tex(tex_paths["ORM"], "Non-Color")
    emi = tex(tex_paths["Emissive"], "sRGB")
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(base.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(orm.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Green"], bsdf.inputs["Roughness"])
    nt.links.new(sep.outputs["Blue"], bsdf.inputs["Metallic"])
    nt.links.new(emi.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = emit_strength
    mat["textures"] = {"base": base.name, "orm": orm.name, "emi": emi.name}
    return mat


def swap_textures(mat, tex_paths):
    nt = mat.node_tree
    for key, name in (("BaseColor", "base"), ("ORM", "orm"), ("Emissive", "emi")):
        node = nt.nodes[mat["textures"][name]]
        old = node.image
        img = bpy.data.images.load(os.path.abspath(tex_paths[key]), check_existing=False)
        img.colorspace_settings.name = old.colorspace_settings.name
        node.image = img


def build_object(name, verts, quads, pals, entries, side, material, origin_vox):
    """verts in voxel units (cropped grid). origin_vox: point mapped to (0,0,0)."""
    v = (verts - np.asarray(origin_vox, float)) * VOXEL_M
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(v.tolist(), [], quads.tolist())
    mesh.validate()
    nloops = len(quads) * 4
    uvs = np.zeros((nloops, 2), np.float32)
    cols = np.zeros((nloops, 4), np.float32)
    for qi, p in enumerate(pals):
        u = palette_uv(int(p), side)
        rgb = entries[int(p)][0]
        uvs[qi * 4:qi * 4 + 4] = u
        cols[qi * 4:qi * 4 + 4] = (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0, 1.0)
    uv = mesh.uv_layers.new(name="UVMap")
    uv.data.foreach_set("uv", uvs.ravel())
    ca = mesh.color_attributes.new("Col", "BYTE_COLOR", "CORNER")
    ca.data.foreach_set("color_srgb", cols.ravel())
    for poly in mesh.polygons:
        poly.use_smooth = False
    mesh.materials.append(material)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _select_only(obj):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def export(obj, glb_path, fbx_path):
    _select_only(obj)
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB", use_selection=True,
                              export_vertex_color="NONE", export_apply=True)
    bpy.ops.export_scene.fbx(filepath=fbx_path, use_selection=True, path_mode="COPY",
                             embed_textures=True, mesh_smooth_type="FACE",
                             add_leaf_bones=False, bake_anim=False)


# ---- rendering -------------------------------------------------------------
def setup_render_scene(res=900, samples=48):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    sc.cycles.max_bounces = 6
    sc.render.resolution_x = res
    sc.render.resolution_y = res
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0

    world = bpy.data.worlds.new("World")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.62, 0.66, 0.78, 1.0)
    bg.inputs["Strength"].default_value = 0.55

    cam_data = bpy.data.cameras.new("Cam")
    cam_data.lens = 60
    cam = bpy.data.objects.new("Cam", cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam

    def light(name, kind, energy, loc, rot, size=None, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, kind)
        ld.energy = energy
        ld.color = color
        if size is not None:
            if kind == "SUN":
                ld.angle = size
            else:
                ld.size = size
        lo = bpy.data.objects.new(name, ld)
        lo.location = loc
        lo.rotation_euler = rot
        sc.collection.objects.link(lo)
        return lo

    light("Key", "SUN", 3.2, (0, 0, 10), (math.radians(48), 0, math.radians(-28)), size=math.radians(8),
          color=(1.0, 0.97, 0.92))
    light("Rim", "SUN", 2.0, (0, 0, 10), (math.radians(-60), 0, math.radians(200)), size=math.radians(4),
          color=(0.75, 0.85, 1.0))
    light("Fill", "SUN", 0.8, (0, 0, 10), (math.radians(70), 0, math.radians(60)), size=math.radians(20),
          color=(1.0, 0.9, 0.95))

    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "ShadowCatcher"
    ground.is_shadow_catcher = True
    return cam


def frame_camera(cam, obj, direction=(0.62, -1.0, 0.42), margin=1.08):
    bb = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    lo = Vector((min(p.x for p in bb), min(p.y for p in bb), min(p.z for p in bb)))
    hi = Vector((max(p.x for p in bb), max(p.y for p in bb), max(p.z for p in bb)))
    center = (lo + hi) / 2
    radius = (hi - lo).length / 2
    d = Vector(direction).normalized()
    fov = 2 * math.atan(18.0 / cam.data.lens)
    dist = radius / math.sin(fov / 2) * margin
    cam.location = center + d * dist
    look = center - cam.location
    cam.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()
    cam.data.clip_end = dist * 4


def render(path):
    bpy.context.scene.render.filepath = os.path.abspath(path)
    bpy.ops.render.render(write_still=True)
