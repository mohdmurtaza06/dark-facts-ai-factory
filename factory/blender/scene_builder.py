"""Generic topic-aware Blender scene builder for DARK FACTS cloud renders."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

def args():
    a={"storyboard":None,"out":"frames","fps":12,"width":480,"height":854}
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    i=0
    while i<len(av):
        k=av[i].lstrip("-")
        if k in a and i+1<len(av):
            a[k]=int(av[i+1]) if k in ("fps","width","height") else av[i+1]; i+=2
        else: i+=1
    return a

def mat(name, color, emission=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    if bs:
        bs.inputs["Base Color"].default_value=(*color,1)
        bs.inputs["Roughness"].default_value=.35
        if emission:
            bs.inputs["Emission Color"].default_value=(*color,1)
            bs.inputs["Emission Strength"].default_value=emission
    return m

def smooth(o):
    if hasattr(o.data,"polygons"):
        for p in o.data.polygons: p.use_smooth=True

def sphere(name, loc, scale, color, emission=0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(mat(name+"_mat",color,emission)); smooth(o); return o

def text_obj(body, loc, size, color):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90),0,0))
    o=bpy.context.object; o.data.body=body; o.data.size=size
    o.data.align_x="CENTER"; o.data.materials.append(mat("type_"+str(len(bpy.data.objects)),color,1.2))
    return o

def clear():
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)

def environment(theme, palette):
    c1=palette[0]
    world=bpy.data.worlds.new("DarkFactsWorld"); bpy.context.scene.world=world
    world.use_nodes=True; world.node_tree.nodes["Background"].inputs[0].default_value=(*c1,1)
    world.node_tree.nodes["Background"].inputs[1].default_value=.28
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,-1.6))
    floor=bpy.context.object; floor.data.materials.append(mat("ground",tuple(x*.28 for x in c1)))
    for i in range(42):
        ang=i*2.399; rad=1.8+(i%7)*.42; z=-.2+(i%9)*.32
        sphere("particle",(math.cos(ang)*rad, math.sin(ang)*.4, z),(.018,.018,.018),(0.35,.72,.95),1.0)
    if theme=="space":
        for i in range(20):
            x=math.sin(i*4.1)*3.5; z=math.cos(i*2.3)*3.2
            sphere("star",(x,1.8,z),(.025,.025,.025),(.8,.88,1),1.5)

def subject(profile, action, frame0, frame1):
    kind=profile.get("subject","object"); theme=profile.get("theme","abstract")
    c=profile.get("palette",[(.2,.4,.8),(.8,.3,.5)])[0]
    accent=profile.get("palette",[(.2,.4,.8),(.8,.3,.5)])[1]
    root=bpy.data.objects.new("SubjectRoot",None); bpy.context.collection.objects.link(root)
    root.location=(0,0,.25)
    if kind=="planet":
        body=sphere("Planet",(0,0,.4),(1.05,1.05,1.05),c)
        bpy.ops.mesh.primitive_torus_add(major_radius=1.55,minor_radius=.055,major_segments=64,minor_segments=10,location=(0,0,.35),rotation=(math.radians(72),0,0))
        ring=bpy.context.object; ring.name="PlanetRing"; ring.data.materials.append(mat("ring",accent,0.25))
        body.parent=root; ring.parent=root
        for i in range(3):
            sphere("moon_"+str(i),(1.7*math.cos(i*2.1),.2,1.2*math.sin(i*2.1)),(.12,.12,.12),accent,.3)
    elif kind=="creature":
        body=sphere("CreatureBody",(0,0,.35),(.72,.42,.48),c)
        head=sphere("CreatureHead",(.55,-.02,.63),(.38,.35,.36),accent)
        body.parent=root; head.parent=root
        for side in (-1,1):
            eye=sphere("Eye",(.68,-.32,.75+side*.08),(.07,.045,.07),(1,1,1),.2); eye.parent=root
            for j in range(2):
                limb=sphere("Limb",(-.2+side*.28,-.02,-.15-j*.18),(.12,.15,.4),accent)
                limb.rotation_euler[1]=side*.45; limb.parent=root
    elif kind=="fossil":
        sphere("FossilCore",(0,0,.35),(.85,.2,.65),c)
        for i in range(7):
            a=i*.48
            sphere("FossilRib",(math.cos(a)*.55,-.08,.3+math.sin(a)*.38),(.12,.12,.12),accent)
    elif kind=="microbe":
        sphere("MicrobeCore",(0,0,.35),(.72,.72,.72),c)
        for i in range(14):
            a=i*math.tau/14
            p=sphere("MicrobeSpore",(math.cos(a)*.95,math.sin(a)*.35,.35+math.sin(a*2)*.6),(.13,.13,.13),accent,.25); p.parent=root
    elif kind=="energy":
        for i in range(5):
            p=sphere("EnergyOrb",(math.sin(i*1.25)*.75,0,.2+i*.22),(.24,.24,.24),accent,1.0); p.parent=root
        for i in range(4):
            bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=.035,depth=1.5,location=(math.sin(i*1.8)*.35,0,.4))
            o=bpy.context.object; o.rotation_euler[1]=(-.5+i*.32); o.data.materials.append(mat("bolt"+str(i),accent,1.5)); o.parent=root
    else:
        sphere("MysteryObject",(0,0,.35),(.7,.7,.7),c,.3)
        for i in range(4):
            p=sphere("Orbit",(math.cos(i*math.pi/2)*1.15,.1,.35+math.sin(i*math.pi/2)*.8),(.16,.16,.16),accent,.4); p.parent=root
    for f, z, s in ((frame0,0,.86),( (frame0+frame1)//2,.12,1.08),(frame1,0,1.0)):
        root.location=(0,0,.25+z); root.scale=(s,s,s); root.keyframe_insert(data_path="location",frame=f); root.keyframe_insert(data_path="scale",frame=f)
    return root

def camera(frame0,frame1,kind):
    bpy.ops.object.camera_add(location=(0,-7,1.0)); cam=bpy.context.object
    cam.data.lens=42; bpy.context.scene.camera=cam
    for f, x in ((frame0,-.25),(frame1,.25)):
        cam.location=(x,-7,1.0); cam.rotation_euler=(Vector((0,0,.45))-cam.location).to_track_quat("-Z","Y").to_euler()
        cam.keyframe_insert(data_path="location",frame=f); cam.keyframe_insert(data_path="rotation_euler",frame=f)
    return cam

def lighting():
    for loc,power,size in [((3,-4,5),900,4),((-4,-1,2),500,3)]:
        bpy.ops.object.light_add(type="AREA",location=loc); l=bpy.context.object; l.data.energy=power; l.data.shape="DISK"; l.data.size=size
    sc=bpy.context.scene; sc.render.engine="BLENDER_WORKBENCH"
    sc.display.shading.light="STUDIO"; sc.display.shading.color_type="MATERIAL"
    sc.display.shading.show_shadows=True; sc.display.shading.show_cavity=True
    sc.render.image_settings.file_format="PNG"; sc.render.image_settings.color_mode="RGB"
    sc.render.use_persistent_data=True

def main():
    a=args()
    if not a["storyboard"]: raise SystemExit("--storyboard is required")
    sb=json.loads(Path(a["storyboard"]).read_text(encoding="utf-8"))
    out=Path(a["out"]); out.mkdir(parents=True,exist_ok=True)
    sc=bpy.context.scene; sc.render.resolution_x=a["width"]; sc.render.resolution_y=a["height"]; sc.render.resolution_percentage=100; sc.render.fps=a["fps"]
    global_frame=1; scene_map=[]
    for item in sb["scenes"]:
        clear(); profile=item.get("visual_profile",sb.get("visual_profile",{}))
        environment(profile.get("theme","abstract"),profile.get("palette",[(.1,.15,.3),(.4,.2,.5)]))
        fcount=max(1,round(item["duration"]*a["fps"])); f0=global_frame; f1=f0+fcount-1
        subject(profile,item.get("action","reveal"),f0,f1)
        label=(item.get("on_screen_text") or sb.get("topic","DARK FACTS")).replace("\n"," ")[:52]
        text_obj(label,(0,-1.0,1.75),.22,(.95,.96,1.0))
        camera(f0,f1,item.get("camera",{}).get("type","push_in")); lighting()
        sc.frame_start=f0; sc.frame_end=f1; sc.render.filepath=str(out/"f")
        print("Rendering",item["id"],"frames",f0,"to",f1,flush=True)
        bpy.ops.render.render(animation=True)
        scene_map.append({"id":item["id"],"frame_start":f0,"frame_end":f1,"duration":item["duration"]})
        global_frame=f1+1
    (out/"scene_map.json").write_text(json.dumps({"fps":a["fps"],"width":a["width"],"height":a["height"],"total_frames":global_frame-1,"scenes":scene_map},indent=2))
    print("DONE frames:",global_frame-1,flush=True)

if __name__=="__main__": main()
