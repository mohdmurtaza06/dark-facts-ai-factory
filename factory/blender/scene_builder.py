"""DARK FACTS V2 Blender headless scene builder — purple octopus episode."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--")+1:] if "--" in argv else []
    a = {"storyboard": None, "out": "frames", "fps": 12, "width": 480, "height": 854}
    i = 0
    while i < len(argv):
        if argv[i] in ("--storyboard","--out","--fps","--width","--height") and i+1 < len(argv):
            key = argv[i][2:]
            a[key] = int(argv[i+1]) if key in ("fps","width","height") else argv[i+1]
            i += 2
        else:
            i += 1
    return a

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for b in list(coll):
            coll.remove(b)

def mat(name, color, emission=0.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.4
    if emission > 0 and "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    m.node_tree.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    m.diffuse_color = (*color, 1.0)
    return m

def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True

def create_octopus(location=(0, 0, 0.8), scale=1.0, animate_tentacles=True, frame_start=1, frame_end=24):
    body_c, accent_c = (0.55, 0.25, 0.70), (0.85, 0.40, 0.75)
    body_mat, accent_mat = mat("oct_body", body_c), mat("oct_accent", accent_c)
    eye_mat, pupil_mat = mat("oct_eye", (0.98, 0.98, 1.0)), mat("oct_pupil", (0.05, 0.05, 0.1))
    root = bpy.data.objects.new("OctopusRoot", None)
    bpy.context.collection.objects.link(root)
    root.location = location
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45*scale, location=(0, 0, 0))
    body = bpy.context.active_object
    body.name = "OctBody"
    body.scale = (1.1, 0.95, 0.9)
    body.data.materials.append(body_mat)
    smooth(body)
    body.parent = root
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28*scale, location=(0, 0.05*scale, 0.3*scale))
    head = bpy.context.active_object
    head.data.materials.append(body_mat)
    smooth(head)
    head.parent = root
    for side, x in (("L", -0.16), ("R", 0.16)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12*scale, location=(x*scale, -0.32*scale, 0.15*scale))
        eye = bpy.context.active_object
        eye.scale = (1.0, 0.7, 1.15)
        eye.data.materials.append(eye_mat)
        smooth(eye)
        eye.parent = root
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.055*scale, location=(x*scale, -0.40*scale, 0.15*scale))
        pupil = bpy.context.active_object
        pupil.data.materials.append(pupil_mat)
        smooth(pupil)
        pupil.parent = root
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025*scale, location=((x-0.03)*scale, -0.42*scale, 0.2*scale))
        hi = bpy.context.active_object
        hi.data.materials.append(mat(f"hi_{side}", (1, 1, 1), 1.5))
        hi.parent = root
    for i in range(8):
        angle = i * math.pi * 2 / 8 + 0.2
        tx, ty = math.cos(angle) * 0.28 * scale, math.sin(angle) * 0.28 * scale
        bpy.ops.mesh.primitive_cylinder_add(radius=0.055*scale, depth=0.7*scale, location=(tx, ty, -0.4*scale))
        t = bpy.context.active_object
        t.name = f"Tentacle_{i}"
        t.rotation_euler = (0.9 + 0.15*(i % 3), 0.1*math.sin(angle), angle)
        t.data.materials.append(body_mat if i % 2 == 0 else accent_mat)
        smooth(t)
        t.parent = root
        if animate_tentacles:
            for f, phase in ((frame_start, 0.0), (frame_end, 1.0)):
                wave = 0.25 * math.sin(phase * math.pi * 2 + i * 0.8)
                t.rotation_euler = (0.9 + wave, 0.1*math.sin(angle + phase), angle + wave * 0.3)
                t.keyframe_insert(data_path="rotation_euler", frame=f)
    for f, z in ((frame_start, 0.0), ((frame_start+frame_end)//2, 0.06*scale), (frame_end, 0.0)):
        root.location = (location[0], location[1], location[2] + z)
        root.keyframe_insert(data_path="location", frame=f)
    root.location = location
    return root

def create_diver(location=(-0.8, -0.5, 0.6), scale=0.5):
    suit = mat("suit", (0.15, 0.35, 0.55))
    skin = mat("skin", (0.9, 0.75, 0.6))
    tank = mat("tank", (0.8, 0.2, 0.15))
    root = bpy.data.objects.new("DiverRoot", None)
    bpy.context.collection.objects.link(root)
    root.location = location
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.3*scale))
    body = bpy.context.active_object
    body.scale = (0.25*scale, 0.15*scale, 0.4*scale)
    body.data.materials.append(suit)
    smooth(body)
    body.parent = root
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14*scale, location=(0, 0, 0.65*scale))
    head = bpy.context.active_object
    head.data.materials.append(skin)
    smooth(head)
    head.parent = root
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16*scale, location=(0, -0.02*scale, 0.65*scale))
    helm = bpy.context.active_object
    helm.scale = (1.05, 0.9, 1.05)
    helm.data.materials.append(mat("glass", (0.6, 0.85, 0.95), 0.3))
    smooth(helm)
    helm.parent = root
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07*scale, depth=0.35*scale, location=(0, 0.12*scale, 0.35*scale))
    tk = bpy.context.active_object
    tk.data.materials.append(tank)
    smooth(tk)
    tk.parent = root
    return root

def create_heart(location, scale=0.14, glow=True, frame_start=1, frame_end=24, phase=0.0):
    m = mat(f"heart_{location[0]:.2f}", (0.95, 0.12, 0.22), emission=2.5 if glow else 0.0)
    root = bpy.data.objects.new("HeartRoot", None)
    bpy.context.collection.objects.link(root)
    root.location = location
    bpy.ops.mesh.primitive_uv_sphere_add(radius=scale*0.5, location=(-scale*0.28, 0, scale*0.2))
    a = bpy.context.active_object
    a.data.materials.append(m)
    smooth(a)
    a.parent = root
    bpy.ops.mesh.primitive_uv_sphere_add(radius=scale*0.5, location=(scale*0.28, 0, scale*0.2))
    b = bpy.context.active_object
    b.data.materials.append(m)
    smooth(b)
    b.parent = root
    bpy.ops.mesh.primitive_ico_sphere_add(radius=scale*0.42, location=(0, 0, -scale*0.3))
    c = bpy.context.active_object
    c.scale = (1.0, 0.7, 1.3)
    c.data.materials.append(m)
    smooth(c)
    c.parent = root
    for f in (frame_start, (frame_start+frame_end)//2, frame_end):
        t = (f - frame_start) / max(1, frame_end - frame_start)
        pulse = 1.0 + 0.18 * abs(math.sin(t * math.pi * 4 + phase))
        root.scale = (pulse, pulse, pulse)
        root.keyframe_insert(data_path="scale", frame=f)
    return root

def create_ocean(theme="deep_ocean"):
    bpy.ops.mesh.primitive_plane_add(size=24, location=(0, 0, -0.8))
    floor = bpy.context.active_object
    floor.data.materials.append(mat("floor", (0.04, 0.1, 0.18)))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=14, location=(0, 0, 2))
    dome = bpy.context.active_object
    dome.scale = (1, 1, 0.65)
    dome.data.materials.append(mat("dome", (0.02, 0.06, 0.14)))
    for i, pos in enumerate([(-2.0, 1.5, -0.3), (1.8, 1.8, -0.2), (-0.5, 2.2, -0.4), (2.2, 0.8, -0.3)]):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.3+i*0.04, location=pos)
        rock = bpy.context.active_object
        rock.scale = (1, 1, 1.5+i*0.15)
        rock.data.materials.append(mat(f"coral{i}", (0.85, 0.35+i*0.08, 0.3)))
        smooth(rock)
    for i in range(20):
        ang = i * 0.9
        r = 1.2 + (i % 6) * 0.35
        z = 0.2 + (i % 8) * 0.22
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, location=(math.cos(ang)*r, math.sin(ang)*r*0.5, z))
        p = bpy.context.active_object
        p.data.materials.append(mat(f"pl{i}", (0.4, 0.9, 0.95), 0.9))

def setup_lights():
    bpy.ops.object.light_add(type="AREA", location=(3, -3, 5))
    k = bpy.context.active_object
    k.data.energy = 300
    k.data.size = 5
    bpy.ops.object.light_add(type="AREA", location=(-3, -1, 3))
    f = bpy.context.active_object
    f.data.energy = 100
    f.data.size = 6
    bpy.ops.object.light_add(type="SPOT", location=(0, 4, 5))
    r = bpy.context.active_object
    r.data.energy = 250
    r.rotation_euler = (math.radians(55), 0, math.pi)
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.04, 0.1, 0.18, 1.0)
    bg.inputs[1].default_value = 0.5

def setup_camera(cam_def, f0, f1):
    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam
    cam.data.lens = cam_def.get("lens", 35)
    cam.data.clip_end = 80
    ctype = cam_def.get("type", "static")
    if ctype in ("dolly_in", "push_in"):
        start, end = Vector(cam_def["start"]), Vector(cam_def["end"])
        for f, pos in ((f0, start), (f1, end)):
            cam.location = pos
            cam.rotation_euler = (Vector((0, 0, 1.0)) - pos).to_track_quat("-Z", "Y").to_euler()
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
    elif ctype in ("orbit", "hero_orbit"):
        center = Vector(cam_def.get("center", (0, 0, 1.0)))
        radius = cam_def.get("radius", 3.5)
        for f, t in ((f0, 0.0), (f1, 0.6)):
            ang = t * math.pi * 2
            pos = center + Vector((math.sin(ang)*radius, -math.cos(ang)*radius, 0.5))
            cam.location = pos
            cam.rotation_euler = (center - pos).to_track_quat("-Z", "Y").to_euler()
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
    elif ctype == "side_track":
        s, e = Vector(cam_def["start"]), Vector(cam_def["end"])
        for f, pos in ((f0, s), (f1, e)):
            cam.location = pos
            cam.rotation_euler = (math.radians(80), 0, 0)
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
    elif ctype == "dramatic_low":
        pos = Vector(cam_def.get("pos", (0, -2, 0.5)))
        target = Vector(cam_def.get("target", (0, 0, 1.0)))
        cam.location = pos
        cam.rotation_euler = (target - pos).to_track_quat("-Z", "Y").to_euler()
    else:
        cam.location = (0, -3, 1.4)
        cam.rotation_euler = (math.radians(85), 0, 0)
    return cam

def setup_render(out_dir, fps, width, height, f0, f1):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "MATERIAL"
    sc.display.shading.show_shadows = True
    sc.display.shading.show_cavity = True
    sc.display.shading.cavity_type = "BOTH"
    sc.render.resolution_x = width
    sc.render.resolution_y = height
    sc.render.resolution_percentage = 100
    sc.render.fps = fps
    sc.frame_start = f0
    sc.frame_end = f1
    sc.render.filepath = str(out_dir / "f")
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.use_persistent_data = True

def main():
    args = parse_args()
    if not args["storyboard"]:
        print("ERROR: --storyboard required")
        sys.exit(1)
    sb = json.loads(Path(args["storyboard"]).read_text(encoding="utf-8"))
    out_dir = Path(args["out"])
    out_dir.mkdir(parents=True, exist_ok=True)
    fps, width, height = args["fps"], args["width"], args["height"]
    global_frame = 1
    scene_map = []
    for sc in sb["scenes"]:
        clear_scene()
        create_ocean()
        setup_lights()
        n_frames = max(1, int(round(sc["duration"] * fps)))
        f0, f1 = global_frame, global_frame + n_frames - 1
        objs = sc.get("objects", [])
        action = sc.get("action", "")
        if "diver" in objs or action == "diver_discovers":
            diver = create_diver(location=(-0.9, -0.3, 0.5))
            diver.location = (-1.2, -0.5, 0.5)
            diver.keyframe_insert("location", frame=f0)
            diver.location = (-0.5, -0.2, 0.55)
            diver.keyframe_insert("location", frame=f1)
        if any("octopus" in o for o in objs) or action in (
            "octopus_approaches", "octopus_swims", "hero_pose", "anatomical_reveal", "hearts_function"
        ):
            scale = 0.85 if "xray" in str(objs) else 1.0
            octo = create_octopus(
                location=(0.3, 0.2, 0.7), scale=scale,
                animate_tentacles=True, frame_start=f0, frame_end=f1,
            )
            if action == "octopus_approaches":
                octo.location = (0.5, 1.5, 0.7)
                octo.keyframe_insert("location", frame=f0)
                octo.location = (0.2, 0.0, 0.75)
                octo.keyframe_insert("location", frame=f1)
            elif action == "octopus_swims":
                octo.location = (-1.5, 0.3, 0.7)
                octo.keyframe_insert("location", frame=f0)
                octo.location = (1.5, 0.1, 0.8)
                octo.keyframe_insert("location", frame=f1)
            elif action == "hero_pose":
                octo.location = (0, 0, 0.8)
                octo.keyframe_insert("location", frame=f0)
                octo.rotation_euler = (0, 0, 0.3)
                octo.keyframe_insert("rotation_euler", frame=f1)
        if any("heart" in o for o in objs) or action in ("anatomical_reveal", "hearts_function"):
            for hx, hz, phase in [(-0.35, 1.1, 0), (0.0, 1.25, 1.0), (0.35, 1.1, 2.0)]:
                create_heart(
                    location=(hx, -0.15, hz), scale=0.13, glow=True,
                    frame_start=f0, frame_end=f1, phase=phase,
                )
        setup_camera(sc["camera"], f0, f1)
        setup_render(out_dir, fps, width, height, f0, f1)
        print(f"Rendering scene '{sc['id']}' frames {f0}-{f1} ({n_frames})")
        bpy.context.scene.frame_start = f0
        bpy.context.scene.frame_end = f1
        bpy.ops.render.render(animation=True)
        scene_map.append({
            "id": sc["id"], "frame_start": f0, "frame_end": f1,
            "duration": sc["duration"], "narration": sc["narration"],
        })
        global_frame = f1 + 1
    meta = {
        "fps": fps, "width": width, "height": height,
        "total_frames": global_frame - 1, "scenes": scene_map,
        "fact_id": sb.get("fact_id"),
    }
    (out_dir / "scene_map.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"DONE: {global_frame - 1} frames -> {out_dir}")

if __name__ == "__main__":
    main()
