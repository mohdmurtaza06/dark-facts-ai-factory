import bpy, math, random, os
from mathutils import Vector
random.seed(17)
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
def mat(name,color,rough=.55,metallic=0,subsurface=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True; p=m.node_tree.nodes.get("Principled BSDF"); p.inputs["Base Color"].default_value=(*color,1); p.inputs["Roughness"].default_value=rough; p.inputs["Metallic"].default_value=metallic
 if "Subsurface Weight" in p.inputs:p.inputs["Subsurface Weight"].default_value=subsurface
 return m
skin=mat("warm peach skin",(.62,.31,.22),.42,0,.08); skinhi=mat("skin highlights",(.9,.55,.4),.4,0,.08); hair=mat("deep chestnut hair",(.055,.025,.018),.32); hairhi=mat("hair warm strands",(.16,.065,.03),.38)
hood=mat("petrol teal hoodie",(.018,.13,.16),.78); seam=mat("hoodie seam",(.07,.27,.29),.7); pants=mat("charcoal trousers",(.025,.035,.055),.82); shoe=mat("dark sneakers",(.012,.018,.025),.45)
white=mat("eye whites",(.92,.86,.76),.25); iris=mat("hazel iris",(.19,.09,.035),.23); pupil=mat("pupil",(.008,.006,.005),.12); mouthmat=mat("mouth interior",(.13,.025,.03),.6); metal=mat("aged iron",(.035,.05,.07),.35,.72); brick=mat("wet blue brick",(.025,.045,.075),.85); warm=mat("lamp amber",(1,.43,.12),.25)
def uv(name,loc,scale,material,seg=40,rings=28):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o
def cyl(name,a,b,r,material):
 a,b=Vector(a),Vector(b); d=b-a; bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=d.length,location=(a+b)/2); o=bpy.context.object; o.name=name; o.rotation_mode="QUATERNION"; o.rotation_quaternion=d.to_track_quat("Z","Y"); o.data.materials.append(material); be=o.modifiers.new("soft edges","BEVEL"); be.width=r*.4; be.segments=3; o.modifiers.new("weighted normals","WEIGHTED_NORMAL"); return o
def curve(name,pts,bevel,material):
 c=bpy.data.curves.new(name,"CURVE"); c.dimensions="3D"; c.bevel_depth=bevel; c.bevel_resolution=4; s=c.splines.new("BEZIER"); s.bezier_points.add(len(pts)-1)
 for p,co in zip(s.bezier_points,pts):p.co=co;p.handle_left_type="AUTO";p.handle_right_type="AUTO"
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(material);return o
ground=mat("rain dark asphalt",(.018,.027,.04),.28,.18); bpy.ops.mesh.primitive_plane_add(size=200); bpy.context.object.data.materials.append(ground)
for side in [-1,1]:
 for i in range(5):
  y=-1+i*4.2;bpy.ops.mesh.primitive_cube_add(size=1,location=(side*5.4,y,5.2+random.uniform(-.3,.5)));o=bpy.context.object;o.name="alley masonry";o.dimensions=(3.5,4.5,11+random.uniform(-1,2));bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(brick)
  for z in [3.3,6.1,8.7]:
   bpy.ops.mesh.primitive_cube_add(size=1,location=(side*3.62,y,z));w=bpy.context.object;w.dimensions=(.08,1,1.45);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);w.data.materials.append(metal)
for i in range(6):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,13+i*4,3.5));o=bpy.context.object;o.dimensions=(9,4,7);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(brick)
# Full-body original stylized character, facing camera
for x in [-.29,.29]:
 uv("trouser leg",(x,.02,1),(.22,.25,.95),pants);uv("sneaker",(x,-.12,.18),(.25,.42,.16),shoe);uv("rubber sole",(x,-.13,.09),(.255,.42,.055),seam)
uv("hoodie torso",(0,.03,2.28),(.69,.38,.91),hood);uv("hood draped back",(0,.31,2.82),(.48,.28,.47),seam)
cyl("left sleeve",(-.48,.02,2.72),(-.64,-.08,1.88),.22,hood);cyl("right sleeve",(.48,.02,2.72),(.55,-.08,1.9),.22,hood)
uv("left hand",(-.38,-.27,1.78),(.16,.14,.13),skin);uv("right hand",(.17,-.29,1.79),(.16,.14,.13),skin)
for x in [-.13,.13]:curve("hood drawstring",[(x,-.355,2.95),(x*1.05,-.39,2.6),(x*1.1,-.39,2.4)],.018,seam)
curve("hoodie pocket",[(-.4,-.345,2.18),(-.28,-.39,2),(0,-.4,1.96),(.28,-.39,2),(.4,-.345,2.18)],.018,seam)
uv("neck",(0,-.01,3.22),(.24,.23,.31),skin);uv("head",(0,-.08,3.75),(.48,.42,.66),skin,64,48)
for x in [-.47,.47]:uv("ear",(x,-.07,3.72),(.12,.12,.2),skin)
for x in [-.24,.24]:uv("cheek",(x,-.465,3.55),(.19,.055,.13),skinhi)
uv("nose",(0,-.51,3.67),(.105,.13,.16),skinhi)
for x in [-.19,.19]:
 uv("eye socket",(x,-.472,3.91),(.155,.075,.205),skinhi);uv("eye white",(x,-.535,3.91),(.125,.06,.16),white);uv("iris",(x+.012,-.586,3.90),(.064,.026,.085),iris);uv("pupil",(x+.018,-.607,3.90),(.032,.016,.052),pupil);uv("eye glint",(x-.005,-.622,3.945),(.018,.009,.023),white,20,12)
for x in [-.19,.19]:curve("worried eyebrow",[(x-.12,-.56,4.13),(x,-.59,4.19),(x+.12,-.56,4.12)],.035,hair)
uv("open anxious mouth",(0,-.493,3.39),(.105,.035,.13),mouthmat);uv("lower lip",(0,-.525,3.31),(.075,.025,.035),skinhi)
uv("hair cap",(0,-.055,4.27),(.5,.43,.31),hair,64,40)
for i in range(11):
 x=-.39+i*.078;z=4.35+.08*math.sin(i*.55);uv("swept hair lock",(x,-.13,z),(.13,.34,.16+.035*math.sin(i)),hair if i%3 else hairhi,28,18)
for x in [-.43,.43]:uv("side hair",(x,-.02,3.98),(.11,.25,.25),hair)
cyl("lamp post",(-3.5,1.5,.1),(-3.5,1.5,6.8),.075,metal);curve("lamp arm",[(-3.5,1.5,6.7),(-3.25,1.5,7.25),(-2.7,1.5,7.45),(-2.2,1.5,7.35)],.055,metal)
uv("lamp shade",(-2.2,1.5,7.22),(.34,.34,.16),metal);uv("glowing lamp",(-2.2,1.5,7),(.22,.22,.22),warm)
water=mat("puddle reflections",(.035,.09,.13),.12,.55)
for x,y,sx,sy in [(-1.8,-1.5,.8,.3),(1.8,2,.65,.22),(-2.4,5,.9,.25)]:uv("puddle",(x,y,.018),(sx,sy,.012),water)
world=bpy.context.scene.world or bpy.data.worlds.new("night blue world");bpy.context.scene.world=world;world.use_nodes=True;world.node_tree.nodes["Background"].inputs[0].default_value=(.018,.035,.075,1);world.node_tree.nodes["Background"].inputs[1].default_value=.28
def area(name,loc,power,color,size,target):
 d=bpy.data.lights.new(name,"AREA");d.energy=power;d.color=color;d.shape="DISK";d.size=size;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
area("warm key",(-3,-4,6),850,(1,.56,.34),4,(0,0,2.8));area("cool fill",(3,-2,4.5),650,(.28,.52,1),4,(0,0,3));area("hair rim",(0,3,6),1200,(.2,.48,1),3,(0,0,3.5))
ld=bpy.data.lights.new("streetlamp pool","POINT");ld.energy=550;ld.color=(1,.43,.16);ld.shadow_soft_size=1.2;lo=bpy.data.objects.new("streetlamp pool",ld);bpy.context.collection.objects.link(lo);lo.location=(-2.2,1.4,6.8)
cd=bpy.data.cameras.new("portrait camera");cam=bpy.data.objects.new("portrait camera",cd);bpy.context.collection.objects.link(cam);cam.location=(0,-10.5,3.5);cam.rotation_euler=(Vector((0,.3,2.55))-Vector(cam.location)).to_track_quat("-Z","Y").to_euler();cd.lens=52;cd.dof.use_dof=True;cd.dof.focus_distance=10.2;cd.dof.aperture_fstop=2.8
scene=bpy.context.scene;scene.camera=cam;scene.render.engine="CYCLES";scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=540;scene.render.resolution_y=960;scene.render.resolution_percentage=100;scene.render.image_settings.file_format="PNG";scene.view_settings.view_transform="AgX";scene.render.filepath=os.environ.get("OUTPUT","/tmp/dark-facts-style-test.png");bpy.ops.render.render(write_still=True)
