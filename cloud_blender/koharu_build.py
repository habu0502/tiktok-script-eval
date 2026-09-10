import bpy, math, os, json
from mathutils import Vector
OUT=os.environ.get('BLENDER_OUT','/tmp/blender-out'); os.makedirs(OUT,exist_ok=True)
# reset
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for d in (bpy.data.materials,):
    pass

def mat(name,color,metal=0.0,rough=.45,alpha=1.0,emit=None):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,alpha); m.metallic=metal; m.roughness=rough
    if alpha<1: m.surface_render_method='DITHERED'
    if emit:
        m.use_nodes=True; bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Emission Color'].default_value=(*emit,1); bs.inputs['Emission Strength'].default_value=.6
    return m
WHITE=mat('KOHARU_White',(0.82,.88,.92),0,.32); BLACK=mat('KOHARU_Black',(.018,.025,.035),.15,.25); TEAL=mat('KOHARU_Teal',(0.02,.62,.72),.05,.28,emit=(0.02,.5,.7)); GOLD=mat('KOHARU_Gold',(.72,.48,.15),.75,.2); SKIN=mat('KOHARU_Skin',(1,.67,.56),0,.5); HAIR=mat('KOHARU_Hair',(.72,.76,.82),.05,.3); EYE=mat('KOHARU_Eye',(0.01,.65,.8),.1,.15,emit=(0,.4,.7)); CAPE=mat('KOHARU_Cape',(.7,.9,.95),0,.25,.42)

def uv(name,loc,scale,ma):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma); bpy.ops.object.shade_smooth(); return o

def cube(name,loc,scale,ma,bev=.04):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma)
    b=o.modifiers.new('Bevel','BEVEL'); b.width=bev; b.segments=2; return o

def cyl(name,a,b,r,ma):
    a,b=Vector(a),Vector(b); mid=(a+b)/2; vec=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r, depth=vec.length, location=mid); o=bpy.context.object; o.name=name; o.rotation_mode='QUATERNION'; o.rotation_quaternion=vec.to_track_quat('Z','Y'); o.data.materials.append(ma); return o
# stylized body blockout 1.67m, A-pose
uv('Head',(0,0,1.49),(.115,.105,.14),SKIN); uv('HairCap',(0,.012,1.525),(.127,.116,.15),HAIR)
# face fringe masses
for x,z,s in [(-.07,1.55,(.055,.07,.105)),(.0,1.575,(.07,.075,.11)),(.075,1.54,(.05,.065,.1))]: uv('Hair_Fringe',(x,-.075,z),s,HAIR)
# eyes front toward -Y
for x in (-.043,.043): uv('Eye',(x,-.099,1.505),(.025,.008,.014),EYE)
# torso/hips
uv('Torso',(0,0,1.20),(.155,.105,.24),WHITE); uv('Hips',(0,0,1.00),(.17,.115,.13),BLACK)
# neck
cyl('Neck',(0,0,1.34),(0,0,1.39),.045,SKIN)
# legs
for x in (-.085,.085):
    cyl('Thigh',(x,0,.98),(x,0,.66),.075,SKIN); cyl('TightsLeg',(x,0,.68),(x,0,.25),.064,BLACK); cube('Boot',(x,-.018,.13),(.075,.12,.13),BLACK,.025)
# arms A pose
for side in (-1,1):
    sx=.13*side; ex=.36*side; wx=.55*side
    cyl('UpperArm',(sx,0,1.31),(ex,0,1.12),.055,SKIN); cyl('ForeArm',(ex,0,1.12),(wx,0,1.02),.048,SKIN); uv('Hand',(wx,0,1.0),(.045,.035,.07),SKIN)
# harness
for side in (-1,1): cyl('Harness',(.055*side,-.095,1.36),(.105*side,-.108,1.12),.012,BLACK)
cyl('WaistBelt',(-.14,-.11,1.04),(.14,-.11,1.04),.018,BLACK)
# cape as layered triangular mesh sheets behind body
for side in (-1,1):
    for j in range(3):
        x=.07*side + j*.045*side
        verts=[(x,.09,1.35),(x+.18*side,.11,1.20),(x+.24*side,.13,.45),(x-.02*side,.11,.78)]
        mesh=bpy.data.meshes.new('CapeMesh'); mesh.from_pydata(verts,[],[(0,1,2,3)]); o=bpy.data.objects.new('Cape_Panel',mesh); bpy.context.collection.objects.link(o); o.data.materials.append(CAPE)
# star hairpin proxy
cube('StarHairpin',(.09,-.105,1.61),(.025,.01,.025),GOLD,.005); bpy.context.object.rotation_euler[1]=math.radians(45)
# pouch
cube('MedicalPouch',(-.16,-.08,1.02),(.055,.035,.075),WHITE,.012)
# drone
uv('DroneBody',(.48,.12,1.48),(.11,.095,.095),WHITE); uv('DroneFace',(.48,.035,1.49),(.072,.018,.055),BLACK)
for side in (-1,1):
    cube('DroneFin',(.48+.11*side,.12,1.50),(.055,.018,.035),WHITE,.012); bpy.context.object.rotation_euler[1]=math.radians(25*side)
uv('DroneGlow',(.48,.012,1.49),(.025,.008,.025),TEAL)
# armature skeleton
bpy.ops.object.armature_add(enter_editmode=True, location=(0,0,0)); arm=bpy.context.object; arm.name='Koharu_Rig'; arm.data.name='Koharu_RigData'
eb=arm.data.edit_bones; root=eb[0]; root.name='root'; root.head=(0,0,0); root.tail=(0,0,.12)
def bone(name,head,tail,parent=None):
    b=eb.new(name); b.head=head; b.tail=tail; b.parent=parent; return b
pel=bone('hips',(0,0,.9),(0,0,1.05),root); sp=bone('spine',(0,0,1.05),(0,0,1.28),pel); neck=bone('neck',(0,0,1.28),(0,0,1.42),sp); head=bone('head',(0,0,1.42),(0,0,1.60),neck)
for side,label in [(-1,'L'),(1,'R')]:
    ua=bone('upper_arm.'+label,(.11*side,0,1.30),(.35*side,0,1.12),sp); fa=bone('forearm.'+label,(.35*side,0,1.12),(.55*side,0,1.02),ua); bone('hand.'+label,(.55*side,0,1.02),(.62*side,0,.99),fa)
    th=bone('thigh.'+label,(.08*side,0,.98),(.08*side,0,.62),pel); sh=bone('shin.'+label,(.08*side,0,.62),(.08*side,0,.20),th); bone('foot.'+label,(.08*side,0,.20),(.08*side,-.16,.08),sh)
bpy.ops.object.mode_set(mode='OBJECT')
# metadata
arm['character']='Shirase Koharu'; arm['prototype']='automated blockout'; arm['height_m']=1.67
# ground and studio
bpy.ops.mesh.primitive_plane_add(size=5, location=(0,0,0)); ground=bpy.context.object; ground.name='Ground'; ground.data.materials.append(mat('Ground',(.035,.045,.06),0,.6))
# camera
bpy.ops.object.camera_add(location=(2.6,-4.5,2.05)); cam=bpy.context.object; bpy.context.scene.camera=cam
def point(o,t): o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
point(cam,(0,0, .9)); cam.data.lens=72
for loc,energy,size in [((2,-2,4),1100,3.0),((-2,-1,2.5),700,2.5),((0,2,3),900,2.0)]:
    bpy.ops.object.light_add(type='AREA',location=loc); l=bpy.context.object; l.data.energy=energy; l.data.size=size; point(l,(0,0,1))
scene=bpy.context.scene; scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=600; scene.render.resolution_y=800; scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'; scene.world.color=(.012,.018,.03)
# save/export/render
blend=os.path.join(OUT,'koharu_prototype.blend'); bpy.ops.wm.save_as_mainfile(filepath=blend)
# select character excluding ground/lights/camera
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
    if o.type in {'MESH','ARMATURE'} and o.name!='Ground': o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'koharu_prototype.glb'),export_format='GLB',use_selection=True,export_apply=True)
scene.render.filepath=os.path.join(OUT,'koharu_front.png'); bpy.ops.render.render(write_still=True)
# side/back renders
for name,loc in [('side',(4.5,0,1.75)),('back',(0,4.5,1.75))]:
    cam.location=loc; point(cam,(0,0,.9)); scene.render.filepath=os.path.join(OUT,'koharu_'+name+'.png'); bpy.ops.render.render(write_still=True)
# validation
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name!='Ground']; tris=sum(len(p.vertices)-2 for o in meshes for p in o.data.polygons); mats=len({m.name for o in meshes for m in o.data.materials if m})
report={'Blender':bpy.app.version_string,'character':'Shirase Koharu','stage':'AUTOMATED_BLOCKOUT','mesh_objects':len(meshes),'triangles':tris,'materials':mats,'armatures':len([o for o in bpy.context.scene.objects if o.type=='ARMATURE']),'exports':{'blend':os.path.exists(blend),'glb':os.path.exists(os.path.join(OUT,'koharu_prototype.glb'))},'renders':['front','side','back'],'gate_status':{'G0':True,'G1':'manual/vision review required','G2':'manual/vision review required','G3':False,'G4':False,'G5':True,'G6':False}}
with open(os.path.join(OUT,'koharu_validation.json'),'w') as f: json.dump(report,f,indent=2,ensure_ascii=False)
print('KOHARU_AUTOMATED_BLOCKOUT_COMPLETE',report)
