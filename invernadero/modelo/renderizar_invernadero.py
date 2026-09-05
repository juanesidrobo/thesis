"""Blender 5.2: treinta citricos, nueve sensores y seis vistas reproducibles.

blender --background --python invernadero/modelo/renderizar_invernadero.py
Anadir -- --preview para reducir resolucion y muestras.
Anadir -- --render-only para usar el .blend guardado sin reconstruir geometria.
La escena actual se reemplaza; ejecutar en un archivo nuevo.
"""
import math
import random
import sys
import time
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'renders'
PREVIEW = '--preview' in sys.argv
random.seed(24)


def material(name, color, roughness=0.5, metallic=0, noise=False):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs[0], output.inputs['Surface'])
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    if noise:
        tex = nodes.new('ShaderNodeTexNoise')
        tex.inputs['Scale'].default_value = 95
        bump = nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.23
        bump.inputs['Distance'].default_value = 0.025
        mat.node_tree.links.new(tex.outputs['Fac'], bump.inputs['Height'])
        mat.node_tree.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def finish(obj, name, mat):
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def box(name, loc, size, mat, bevel=0.015):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = finish(bpy.context.object, name, mat)
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new('Aristas suaves', 'BEVEL')
        mod.width, mod.segments = bevel, 3
        obj.modifiers.new('Normales', 'WEIGHTED_NORMAL')
    return obj


def rod(name, a, b, radius, mat, top=None):
    a, b = Vector(a), Vector(b)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=radius,
                                   radius2=radius if top is None else top,
                                   depth=(b-a).length, location=(a+b)/2)
    obj = finish(bpy.context.object, name, mat)
    obj.rotation_euler = (b-a).to_track_quat('Z', 'Y').to_euler()
    for face in obj.data.polygons:
        face.use_smooth = len(face.vertices) == 4
    return obj


def cable(name, points, mat, radius=0.009):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth, curve.bevel_resolution = radius, 3
    spline = curve.splines.new('BEZIER')
    spline.bezier_points.add(len(points)-1)
    for p, co in zip(spline.bezier_points, points):
        p.co = co
        # Vector handles prevent long cable runs from overshooting into pots.
        p.handle_left_type = p.handle_right_type = 'VECTOR'
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def leaf_geometry(vertices, faces, origin, direction, length, width):
    origin, direction = Vector(origin), Vector(direction).normalized()
    side = direction.cross(Vector((0, 0, 1))).normalized()
    start = len(vertices)
    # Lanceolate outline and raised midrib rather than spherical leaf clusters.
    for t, w in [(0, 0), (.25, .75), (.52, 1), (.8, .65), (1, 0)]:
        center = origin + direction * length * t
        center.z += math.sin(t * math.pi) * length * .12
        for s in (-1, 0, 1):
            p = center + side * width * w * s
            p.z -= abs(s) * width * .18
            vertices.append(tuple(p))
    for row in range(4):
        for col in range(2):
            a = start + row*3 + col
            faces.append((a, a+1, a+4, a+3))


def leaves(name, specs, mats):
    vertices, faces = [], []
    for spec in specs:
        leaf_geometry(vertices, faces, *spec)
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for mat in mats:
        mesh.materials.append(mat)
    for face in mesh.polygons:
        face.material_index = (face.index // 8) % len(mats)
        face.use_smooth = True
    mod = obj.modifiers.new('Curvatura suave de hojas', 'SUBSURF')
    mod.levels = 1
    return obj


def text(name, body, loc, size, mat, rotation=None):
    curve = bpy.data.curves.new(name, 'FONT')
    curve.body, curve.size = body, size
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    if rotation is not None:
        obj.rotation_euler = rotation
    obj.data.materials.append(mat)
    return obj


def camera(name, loc, target, scale):
    bpy.ops.object.camera_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z', 'Y').to_euler()
    obj.data.type, obj.data.ortho_scale = 'ORTHO', scale
    obj.data.lens = 48
    return obj


def overlay(cam, title, subtitle, rows, ink, colors):
    result = []
    width = cam.data.ortho_scale
    height = width * bpy.context.scene.render.resolution_y / bpy.context.scene.render.resolution_x
    paper = material('Fondo rotulos ' + cam.name, (.83,.86,.81), 1)
    nodes = paper.node_tree.nodes
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (.83,.86,.81,1)
    paper.node_tree.links.new(emission.outputs[0], next(n for n in nodes if n.type == 'OUTPUT_MATERIAL').inputs['Surface'])
    for y, h in [(.433,.115),(-.431,.105)]:
        if y < 0 and not rows:
            continue
        obj = box('Fondo rotulo', (0,0,0), (width, height*h, .001), paper, 0)
        obj.parent = cam
        obj.location = (0,y*height,-1.02)
        obj.visible_shadow = False
        obj.visible_diffuse = False
        obj.visible_glossy = False
        result.append(obj)
    for body, x, y, size, mat in [
        (title, -.46, .44, .026, ink),
        (subtitle, -.46, .402, .012, ink),
        *[(body, -.46 + (i % 2)*.49, -.40-(i//2)*.034, .014, colors[i])
          for i, body in enumerate(rows)],
    ]:
        obj = text('Rotulo_' + body, body, (0, 0, 0), width*size, mat)
        obj.parent = cam
        obj.location = (x*width, y*height, -1)
        obj.visible_shadow = False
        obj.visible_diffuse = False
        obj.visible_glossy = False
        result.append(obj)
    return result


def render_views():
    """Render persisted scenes; stage PNGs before replacing OneDrive-synced files."""
    scenes = sorted(bpy.data.scenes,key=lambda s:s.name)
    for scene in scenes:
        scene.cycles.samples = 16 if PREVIEW else 48
        scene.render.resolution_percentage = 50 if PREVIEW else 100
        # Keep labels away from the canopies in both overall views.
        if scene.name in ('01_Invernadero','02_Distribucion'):
            for obj in scene.objects:
                if obj.type != 'FONT' or not obj.name.startswith('Rotulo_'+scene.name+'_'):
                    continue
                body = obj.data.body
                if ' / S' in body:
                    tag = body.split(' / ')[1]
                    row,number = int(tag[1]),int(tag[-2:])
                    x,y = (-1.8,0,1.8)[row-1],-5.85+(number-1)*1.3
                    obj.location = (x-.75,y-.25,2.3) if scene.name == '02_Distribucion' else (x-.25,y-.30,2.35)
                    obj.data.size = .23 if scene.name == '02_Distribucion' else .28
                elif body == 'RPI':
                    obj.location = (3.20,-.28,2.10) if scene.name == '02_Distribucion' else (2.4,.1,2.50)
                elif body == 'HG':
                    obj.location = (.72,.30,.46)
                elif body in ('HA','TA') and scene.name == '02_Distribucion':
                    obj.location.x = 3.1
        elif scene.name.startswith(('03_','04_','05_')):
            sid = {'03_':'A-H','04_':'B-H','05_':'C-H'}[scene.name[:3]]
            source = scene.objects['Sensor_'+sid].location
            anchor = source+Vector((-.65,-.05,.18))
            label = next(o for o in scene.objects if o.type == 'FONT' and o.data.body == sid)
            label.location = anchor
            guide = scene.objects['Guia_'+sid]
            depth = max(v.co.z for v in guide.data.vertices)-min(v.co.z for v in guide.data.vertices)
            guide.location = (source+anchor)/2
            guide.rotation_euler = (anchor-source).to_track_quat('Z','Y').to_euler()
            guide.scale.z = (anchor-source).length/depth
        elif scene.name == '06_Raspberry_Pi':
            # Only the approach to the enclosure is shown in this close-up.
            # Complete sensor-to-hub curves remain in the overall/plan scenes.
            for obj in list(scene.objects):
                if not obj.name.startswith('Conexion_'):
                    continue
                curve = bpy.data.curves.new('DetalleRPI_'+obj.name,'CURVE')
                curve.dimensions,curve.bevel_depth,curve.bevel_resolution = '3D',.010,3
                spline = curve.splines.new('POLY')
                points = obj.data.splines[0].bezier_points[-4:]
                spline.points.add(len(points)-1)
                for point,original in zip(spline.points,points):
                    point.co = (*original.co,1)
                curve.materials.append(obj.data.materials[0])
                detail = bpy.data.objects.new('DetalleRPI_'+obj.name,curve)
                scene.collection.objects.link(detail)
                scene.collection.objects.unlink(obj)
    # End the schematic digital link inside, not just in front of, the interface block.
    digital = bpy.data.objects.get('RPI_Enlace_digital')
    if digital:
        digital.data.splines[0].bezier_points[0].co = (2.57,.055,1.50)
    bpy.context.window.scene = scenes[0]
    for scene in scenes:
        for obj in scene.objects:
            if obj.hide_render:
                obj.hide_set(True,view_layer=scene.view_layers[0])
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.shading.color_type = 'MATERIAL'
                area.spaces.active.region_3d.view_perspective = 'CAMERA'
    # Save all view states before starting the expensive render step.
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'invernadero_mejorado.blend'))
    for scene in scenes:
        destination = Path(scene.render.filepath)
        staged = destination.with_name(destination.stem+'.rendering.png')
        bpy.ops.render.render(scene=scene.name)
        result = next(image for image in bpy.data.images if image.type == 'RENDER_RESULT')
        result.save_render(str(staged),scene=scene)
        for attempt in range(5):
            try:
                staged.replace(destination)
                break
            except PermissionError:
                if attempt == 4:
                    raise
                time.sleep(2)
        print('PNG guardado: '+str(destination),flush=True)


def main():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    construction = bpy.context.scene
    for scene in list(bpy.data.scenes):
        if scene != construction:
            bpy.data.scenes.remove(scene)
    random.seed(24)
    metal = material('Aluminio satinado', (.49,.55,.58), .28, .8)
    clay = material('Terracota porosa', (.48,.19,.08), .85, noise=True)
    soil = material('Sustrato cafe casi negro', (.007,.003,.001), .97, noise=True)
    nodes = soil.node_tree.nodes
    tex = next(n for n in nodes if n.type == 'TEX_NOISE')
    tex.inputs['Scale'].default_value = 130
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (.0015,.0006,.0002,1)
    ramp.color_ramp.elements[1].color = (.014,.0055,.0018,1)
    soil.node_tree.links.new(tex.outputs['Fac'], ramp.inputs[0])
    soil.node_tree.links.new(ramp.outputs[0], next(n for n in nodes if n.type == 'BSDF_PRINCIPLED').inputs['Base Color'])
    bark = material('Corteza', (.16,.085,.027), .9, noise=True)
    greens = [material('Hoja citrico %s' % i, c, .36) for i,c in enumerate(
        [(.09,.23,.018), (.17,.32,.025), (.24,.39,.038), (.055,.16,.012)])]
    gravel = material('Grava caliza', (.42,.43,.38), .95, noise=True)
    white = material('Carcasa blanca', (.87,.9,.87), .3)
    dark = material('Cable y juntas', (.009,.014,.016), .7)
    ink = material('Texto grafito', (.025,.065,.068), .7)
    blue = material('Humedad ambiente azul', (.025,.30,.64))
    orange = material('Temperatura ambiente naranja', (.85,.24,.025))
    red = material('Temperatura hoja rojo', (.7,.055,.035))
    teal = material('Humedad suelo turquesa', (.015,.36,.25))
    gold = material('Suelo general ocre', (.50,.29,.035))
    pcb = material('Placa Raspberry Pi', (.012,.15,.035), .6)
    label_mats = {}
    for mat in [ink,blue,orange,red,teal,gold]:
        label = bpy.data.materials.new('Rotulo ' + mat.name)
        label.use_nodes = True
        label.node_tree.nodes.clear()
        emission = label.node_tree.nodes.new('ShaderNodeEmission')
        emission.inputs[0].default_value = mat.diffuse_color
        output = label.node_tree.nodes.new('ShaderNodeOutputMaterial')
        label.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])
        label_mats[mat.name] = label
    film = material('Cubierta translucida', (.81,.87,.83), .5)
    nodes = film.node_tree.nodes
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    mix = nodes.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = .075
    film.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
    film.node_tree.links.new(next(n for n in nodes if n.type == 'BSDF_PRINCIPLED').outputs[0], mix.inputs[2])
    film.node_tree.links.new(mix.outputs[0], next(n for n in nodes if n.type == 'OUTPUT_MATERIAL').inputs['Surface'])

    box('Entorno', (0,0,-.15), (200,200,.12), material('Fondo piedra', (.72,.74,.69), 1))
    box('Lecho de grava', (0,0,-.025), (6.1,14.5,.18), gravel)
    # Shared meshes for stones and soil clods; no external texture files.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1)
    pebble = finish(bpy.context.object, 'Grava_0000', gravel)
    for i in range(5200):
        obj = pebble if i == 0 else bpy.data.objects.new('Grava_%04d' % i, pebble.data)
        if i:
            bpy.context.collection.objects.link(obj)
        obj.location = (random.uniform(-2.97,2.97),random.uniform(-7.15,7.15),.07)
        r = random.uniform(.023,.058)
        obj.scale = (r,r*.8,r*.65)
        obj.rotation_euler = (random.random(),random.random(),random.random()*6)
    ground_objects = set(bpy.data.objects)

    before = set(bpy.data.objects)
    for x in (-3,3):
        for y in (-7.2,-4.8,-2.4,0,2.4,4.8,7.2):
            rod('Estructura_poste', (x,y,.05), (x,y,2.65), .04, metal)
            box('Placa anclaje', (x,y,.1), (.17,.17,.055), metal)
        for z in (.14,2.65):
            rod('Estructura_larguero', (x,-7.2,z), (x,7.2,z), .035, metal)
    for y in (-7.2,-4.8,-2.4,0,2.4,4.8,7.2):
        rod('Estructura_cabio', (-3,y,2.65), (0,y,3.35), .04, metal)
        rod('Estructura_cabio', (0,y,3.35), (3,y,2.65), .04, metal)
    rod('Estructura_cumbrera', (0,-7.2,3.35), (0,7.2,3.35), .04, metal)
    for y in (-7.2,7.2):
        rod('Estructura_base', (-3,y,.14), (3,y,.14), .035, metal)
    for name,loc,size in [('Fondo',(0,7.2,1.39),(6,.012,2.5)),
                          ('Izquierda',(-3,0,1.39),(.012,14.4,2.5)),
                          ('Frente',(0,-7.2,1.39),(6,.012,2.5)),
                          ('Derecha',(3,0,1.39),(.012,14.4,2.5))]:
        obj = box('Cubierta_' + name, loc, size, film, 0)
        obj.hide_render = name in ('Frente','Derecha')
    for x in (-1.5,1.5):
        obj = box('Cubierta_techo', (x,0,3), (math.hypot(3,.7),14.4,.012), film, 0)
        obj.rotation_euler.y = math.copysign(math.atan2(.7,3),x)
        obj.hide_render = True
    structure_objects = set(bpy.data.objects)-before

    pots, plants, positions = [], {}, {}
    clod_mesh = pebble.data.copy()
    clod_mesh.materials.clear()
    clod_mesh.materials.append(soil)
    instrumented = ('S1-P01','S2-P05','S3-P10')
    for row,x in enumerate((-1.8,0,1.8),1):
        for number in range(1,11):
            y = -5.85 + (number-1)*1.3
            tag = 'S%d-P%02d' % (row,number)
            before = set(bpy.data.objects)
            pot = rod(tag+'_Maceta', (x,y,.09), (x,y,.58), .24, clay, .34)
            pot['surco'], pot['planta'], pot['instrumentada'] = row,number,tag in instrumented
            pots.append(pot)
            bpy.ops.mesh.primitive_torus_add(major_radius=.328, minor_radius=.027,
                                            major_segments=48, minor_segments=12, location=(x,y,.57))
            finish(bpy.context.object,tag+'_Borde',clay)
            rod(tag+'_Tierra', (x,y,.571), (x,y,.585), .308, soil)
            for i in range(85):
                a, r = random.uniform(0,math.tau), .30*math.sqrt(random.random())
                obj = bpy.data.objects.new(tag+'_Terron_%02d' % i, clod_mesh)
                bpy.context.collection.objects.link(obj)
                obj.location = (x+math.cos(a)*r,y+math.sin(a)*r,.586)
                s = random.uniform(.006,.016)
                obj.scale = (s,s*.8,s*.48)
                obj.rotation_euler.z = a
            box(tag+'_Placa', (x,y-.315,.43), (.28,.018,.095), white, .008)
            text(tag, tag, (x-.12,y-.329,.41), .052, ink, (math.pi/2,0,0))
            h = random.uniform(1.45,1.72)
            rod(tag+'_Tronco', (x,y,.57), (x+.025,y,h), .033, bark, .012)
            specs = []
            for j in range(18):
                angle = j*2.399 + random.uniform(-.2,.2)
                reach = random.uniform(.29,.47)*(1 if j < 10 else .65)
                a = Vector((x,y,.86+(j/18)*.71))
                b = a+Vector((math.cos(angle)*reach,math.sin(angle)*reach,random.uniform(.18,.35)))
                rod(tag+'_Rama', a,b,.009,bark,.003)
                for k in range(11):
                    p = a.lerp(b,.18+k*.075)
                    theta = angle+(1 if k%2 else -1)*random.uniform(.5,1.25)
                    specs.append((p,(math.cos(theta),math.sin(theta),random.uniform(-.25,.6)),
                                  random.uniform(.16,.26),random.uniform(.038,.062)))
            leaves(tag+'_Follaje',specs,greens)
            plants[tag] = set(bpy.data.objects)-before
            positions[tag] = Vector((x,y,0))

    # Open-front enclosure shows the hub and interface board, not direct analog GPIO wiring.
    before = set(bpy.data.objects)
    cx = 2.4
    box('RPI_Caja_fondo', (cx,.15,1.32), (1.04,.07,.80), white)
    for x in (cx-.50,cx+.50):
        box('RPI_Caja_lateral', (x,-.015,1.32), (.045,.36,.80), white)
    for z in (.94,1.70):
        box('RPI_Caja_tapa', (cx,-.015,z), (1.04,.36,.045), white)
    box('RPI_Placa', (cx-.15,.084,1.42), (.48,.026,.30), pcb, .009)
    box('RPI_Procesador', (cx-.17,.060,1.43), (.10,.027,.10), metal, .004)
    for x in (cx-.32,cx-.20,cx-.08):
        box('RPI_Puerto_USB_RED', (x,.027,1.31), (.085,.085,.065), metal, .003)
    box('RPI_GPIO', (cx-.15,.056,1.55), (.34,.035,.025), dark, .002)
    for i in range(20):
        rod('RPI_Pin_GPIO', (cx-.31+i*.016,.032,1.55), (cx-.31+i*.016,.020,1.55), .003, gold)
    box('RPI_Interfaces_ADC', (cx+.26,.055,1.40), (.20,.035,.30), dark)
    box('RPI_Bornera', (cx,.045,1.11), (.84,.06,.11), teal, .006)
    for x in (cx-.3,cx+.3):
        rod('RPI_Pedestal', (x,.10,.09), (x,.10,.95), .026, metal)
    text('RPI_Titulo','RASPBERRY PI', (cx-.43,-.205,1.72), .10, ink, (math.pi/2,0,0))
    text('RPI_Interfaces_rotulo','INTERFACES', (cx+.17,.029,1.43), .029, white, (math.pi/2,0,0))
    ports = []
    for i in range(9):
        p = Vector((cx-.39+i*.0975,-.07,.855))
        ports.append(p)
        obj = rod('RPI_Entrada_%02d' % (i+1),p,p+Vector((0,0,.09)),.026,dark)
        obj['puerto'] = i+1
        rod('RPI_Prensaestopa',p+Vector((0,0,.035)),p+Vector((0,0,.065)),.033,metal)
        text('RPI_Numero_%02d' % (i+1),str(i+1), (p.x-.014,-.201,.945), .043, ink, (math.pi/2,0,0))
        cable('RPI_Interior_%02d' % (i+1), [p+Vector((0,0,.09)),(p.x,-.02,1.055),(p.x,.015,1.11)],dark,.007)
    cable('RPI_Enlace_interfaces',[(cx+.20,.02,1.16),(cx+.26,.005,1.23),(cx+.26,.02,1.30)],dark,.012)
    cable('RPI_Enlace_digital',[(cx+.17,.055,1.50),(cx+.08,-.01,1.57),(cx-.02,.025,1.55)],dark,.010)
    # The removable door is retained in the editable file but absent from renders.
    door = box('RPI_Puerta_desmontada',(cx,-.21,1.32),(1.04,.035,.80),white)
    door.hide_render = True
    hub_objects = set(bpy.data.objects)-before

    sensors, sensor_objects, connections = [], {}, []
    for i,(sid,y,mat,variable) in enumerate([
        ('HA',-1.05,blue,'Humedad relativa ambiente'),('TA',1.05,orange,'Temperatura ambiente')]):
        before = set(bpy.data.objects)
        x,z = 2.65,1.88
        rod(sid+'_Soporte',(x,y,.09),(x,y,z),.019,metal)
        rod(sid+'_Nucleo',(x,y,z-.1),(x,y,z+.12),.06,dark)
        for j in range(6):
            rod(sid+'_Abrigo',(x,y,z-.09+j*.048),(x,y,z-.065+j*.048),.14,white,.10)
        rod(sid+'_Color',(x,y,z-.145),(x,y,z-.1),.079,mat)
        source = Vector((x,y,z-.145))
        sensors.append(dict(id=sid,source=source,plant='',variable=variable,mat=mat,
                            route=[source,(x,y,.20),(2.87,y,.16),(2.87,0,.16)]))
        sensor_objects[sid] = set(bpy.data.objects)-before

    before = set(bpy.data.objects)
    rod('HG_Parche_suelo',(0.9,0,.06),(0.9,0,.09),.28,soil)
    for dx in (-.04,.04):
        rod('HG_Electrodo_enterrado',(.9+dx,0,-.06),(.9+dx,0,.17),.008,metal)
    box('HG_Cabezal',(.9,0,.22),(.18,.11,.13),gold)
    source = Vector((.99,0,.22))
    sensors.append(dict(id='HG',source=source,plant='',variable='Humedad suelo general',mat=gold,
                        route=[source,(1.07,0,.17),(1.2,0,.16)]))
    sensor_objects['HG'] = set(bpy.data.objects)-before

    for group,tag in zip(('A','B','C'),instrumented):
        x,y,_ = positions[tag]
        before = set(bpy.data.objects)
        leaf_origin = Vector((x+.12,y-.32,1.39))
        direction = Vector((.34,-.29,.09))
        rod(tag+'_Rama_instrumentada',(x,y,1.08),leaf_origin,.009,bark,.004)
        leaves(tag+'_Hoja_instrumentada',[(leaf_origin,direction,.46,.10)],[greens[2]])
        clip = Vector((x+.32,y-.49,1.46))
        for dz in (-.022,.022):
            box(group+'_Pinza_hoja',clip+Vector((0,0,dz)),(.13,.055,.026),white,.01)
        box(group+'_Pinza_color',clip+Vector((.02,-.033,.023)),(.06,.012,.02),red,.004)
        rod(group+'_Contacto_hoja',clip-Vector((0,0,.018)),clip+Vector((0,0,.012)),.008,metal)
        source = clip+Vector((.065,0,0))
        sid = group+'-T'
        sensors.append(dict(id=sid,source=source,plant=tag,variable='Temperatura hoja',mat=red,
                            route=[source,(x+.52,y-.50,1.15),(x+.43,y-.37,.64),
                                   (x+.44,y-.37,.17),(x+.62,y-.37,.16),(x+.62,0,.16)]))
        sensor_objects[sid] = set(bpy.data.objects)-before
        before = set(bpy.data.objects)
        probe = Vector((x-.14,y-.12,.67))
        for dx in (-.026,.026):
            rod(group+'_Sonda_suelo_enterrada',(probe.x+dx,probe.y,.42),(probe.x+dx,probe.y,.66),.007,metal)
        box(group+'_Cabezal_suelo',probe,(.12,.065,.14),teal,.012)
        box(group+'_Etiqueta_suelo',probe+Vector((0,-.035,.01)),(.085,.008,.065),white,.003)
        text(group+'_H','H',(probe.x-.025,probe.y-.041,probe.z-.012),.049,ink,(math.pi/2,0,0))
        source = probe+Vector((0,0,.07))
        sid = group+'-H'
        sensors.append(dict(id=sid,source=source,plant=tag,variable='Humedad suelo maceta',mat=teal,
                            route=[source,(x-.23,y-.22,.79),(x-.26,y-.36,.66),
                                   (x-.26,y-.39,.17),(x+.65,y-.40,.16),(x+.65,.035,.16)]))
        sensor_objects[sid] = set(bpy.data.objects)-before

    for i,sensor in enumerate(sensors):
        sid = sensor['id']
        # One continuous curve per sensor, ending at its individual cable gland.
        lane = -.16+i*.035
        route = sensor['route'] + [(2.95,lane,.16),(ports[i].x,lane,.20),
                                   (ports[i].x,-.07,.75),ports[i]]
        obj = cable('Conexion_'+sid,route,dark,.010)
        obj['sensor_id'],obj['destino'],obj['puerto'] = sid,'Raspberry Pi / interfaces',i+1
        obj['planta'] = sensor['plant']
        sensor['cable'],sensor['port'] = obj,ports[i]
        connections.append(obj)
        marker = bpy.data.objects.new('Sensor_'+sid,None)
        bpy.context.collection.objects.link(marker)
        marker.location = sensor['source']
        marker['variable'],marker['planta'],marker['puerto'] = sensor['variable'],sensor['plant'],i+1
        marker.empty_display_size = .08
        sensor_objects[sid].add(marker)
        rod('RPI_Marca_'+sid,ports[i]+Vector((0,0,.01)),ports[i]+Vector((0,0,.029)),.028,sensor['mat'])
    hub_objects.update(o for o in bpy.data.objects if o.name.startswith('RPI_Marca_'))
    # Low side rails make the central cable crossing visually intentional.
    for y in (-.24,.24):
        box('Canaleta_central',(.58,y,.12),(4.85,.025,.07),metal,.006)
    before = set(bpy.data.objects)
    for name,loc,power,size in [('Luz principal',(0,-3,9),2300,8),
                               ('Luz fondo',(0,6,8),1900,7),('Relleno',(-5,0,5),1100,6)]:
        bpy.ops.object.light_add(type='AREA',location=loc)
        light = bpy.context.object
        light.name,light.data.energy,light.data.shape,light.data.size = name,power,'DISK',size
        light.rotation_euler = (Vector((0,loc[1],0))-light.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.light_add(type='SUN',location=(0,0,8))
    bpy.context.object.data.energy = 1.1
    bpy.context.object.data.angle = .15
    bpy.context.object.rotation_euler = (.4,-.5,-.4)
    lights = set(bpy.data.objects)-before
    world = bpy.data.worlds.new('Luz ambiental')
    world.use_nodes = True
    background = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
    background.inputs['Color'].default_value = (.65,.72,.80,1)
    background.inputs['Strength'].default_value = .45

    assert len(pots) == 30
    assert all(sum(p['surco'] == row for p in pots) == 10 for row in (1,2,3))
    assert {p.name.removesuffix('_Maceta') for p in pots if p['instrumentada']} == set(instrumented)
    assert len(sensors) == len(connections) == len(ports) == 9
    for sensor in sensors:
        points = sensor['cable'].data.splines[0].bezier_points
        assert (points[0].co-sensor['source']).length < 1e-5
        assert (points[-1].co-sensor['port']).length < 1e-5
    assert all(sum(s['plant'] == tag for s in sensors) == 2 for tag in instrumented)

    all_geometry = set(bpy.data.objects)
    general = camera('Camara_general',(19,-12,16),(0,0,1.0),21.7)
    plan = camera('Camara_distribucion',(0,0,25),(0,0,0),18.6)
    plan.rotation_euler = (0,0,math.pi/2)
    views = [dict(name='01_Invernadero',cam=general,objects=all_geometry,res=(2400,1600),
                  file='render_invernadero_mejorado.png',title='INVERNADERO / 30 CITRICOS',
                  subtitle='3 surcos de 10 plantas  /  9 sensores cableados  /  centro Raspberry Pi',
                  rows=['A  S1-P01 / suelo + hoja','B  S2-P05 / suelo + hoja',
                        'C  S3-P10 / suelo + hoja','HA + TA + HG / sensores generales'],
                  colors=[teal,teal,teal,blue]),
             dict(name='02_Distribucion',cam=plan,objects=all_geometry-structure_objects,res=(2400,1600),
                  file='distribucion_sensores.png',title='DISTRIBUCION / RED DE SENSORES',
                  subtitle='Entrada a la izquierda  /  plantas 01 a 10 hacia el fondo  /  vista sin cubierta',
                  rows=['A  Surco 1 / planta 01','B  Surco 2 / planta 05',
                        'C  Surco 3 / planta 10','RPI  Centro de conexiones / 9 entradas'],
                  colors=[teal,teal,teal,ink])]
    for i,(group,tag,filename) in enumerate(zip(('A','B','C'),instrumented,
            ('detalle_sensores_planta.png','detalle_surco2_planta05.png','detalle_surco3_planta10.png')),3):
        p = positions[tag]
        cam = camera('Camara_'+tag,p+Vector((2.7,-4.7,3.1)),p+Vector((0,-.1,1.05)),3.25)
        objects = ground_objects | lights | plants[tag] | sensor_objects[group+'-T'] | sensor_objects[group+'-H']
        objects |= {s['cable'] for s in sensors if s['plant'] == tag}
        views.append(dict(name='%02d_%s' % (i,tag),cam=cam,objects=objects,res=(1800,1500),file=filename,
                          title=tag+' / SISTEMA '+group,
                          subtitle='Misma planta: humedad del sustrato y temperatura de contacto en hoja',
                          rows=[group+'-T  Pinza de temperatura en hoja',group+'-H  Sonda insertada en la tierra',
                                'Dos cables continuos hacia Raspberry Pi','Sustrato cafe oscuro / no humedad del aire'],
                          colors=[red,teal,ink,ink],plant=tag))
    cam = camera('Camara_Raspberry',(4.1,-3.8,2.55),(cx,0,1.27),2.25)
    views.append(dict(name='06_Raspberry_Pi',cam=cam,objects=ground_objects|lights|hub_objects|set(connections),
                      res=(1800,1500),file='detalle_raspberry_pi.png',title='RASPBERRY PI / CENTRO DE OPERACIONES',
                      subtitle='Caja abierta para mostrar placa, interfaces y nueve entradas de sensores',
                      rows=['1 HA / 2 TA / 3 HG','4 A-T / 5 A-H / 6 B-T',
                            '7 B-H / 8 C-T / 9 C-H','Interfaces ilustrativas / no esquema electrico'],
                      colors=[blue,red,teal,ink]))

    OUT.mkdir(parents=True,exist_ok=True)
    for view in views:
        construction.render.resolution_x,construction.render.resolution_y = view['res']
        cam = view['cam']
        extras = overlay(cam,view['title'],view['subtitle'],view['rows'],label_mats[ink.name],
                         [label_mats[m.name] for m in view['colors']])
        labels = []
        if view['name'] in ('01_Invernadero','02_Distribucion'):
            for group,tag in zip(('A','B','C'),instrumented):
                p = positions[tag]+Vector((0,-.35,1.95))
                labels.append((group+' / '+tag,p,teal,.25))
            labels += [('RPI',Vector((cx,.1,2.10)),ink,.28),
                       ('HG',Vector((.75,-.20,.46)),gold,.22),
                       ('HA',Vector((2.5,-1.05,2.23)),blue,.22),
                       ('TA',Vector((2.5,1.05,2.23)),orange,.22)]
            if view['name'] == '02_Distribucion':
                for tag,p in positions.items():
                    labels.append((tag,p+Vector((.65,-.15,2.3)),ink,.18))
        elif 'plant' in view:
            for sensor in sensors:
                if sensor['plant'] == view['plant']:
                    p = sensor['source']
                    anchor = p+Vector((-.13,-.10,.27))
                    extras.append(rod('Guia_'+sensor['id'],p,anchor,.004,sensor['mat']))
                    labels.append((sensor['id'],anchor,sensor['mat'],.13))
        for body,p,mat,size in labels:
            extras.append(text('Rotulo_'+view['name']+'_'+body,body,p,size,label_mats[mat.name],cam.rotation_euler))
        scene = bpy.data.scenes.new(view['name'])
        for obj in sorted(view['objects']|set(extras)|{cam},key=lambda o:o.name):
            scene.collection.objects.link(obj)
        scene.camera,scene.world = cam,world
        scene.unit_settings.system = 'METRIC'
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 16 if PREVIEW else 48
        scene.cycles.use_denoising = True
        scene.render.resolution_x,scene.render.resolution_y = view['res']
        scene.render.resolution_percentage = 50 if PREVIEW else 100
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = str(OUT/view['file'])
        scene.view_settings.view_transform = 'AgX'
        scene['Instrumentacion'] = 'HA; TA; HG; A-T/A-H S1-P01; B-T/B-H S2-P05; C-T/C-H S3-P10'
        scene['Nota'] = '6 x 14.4 m ilustrativos. Suelo: humedad sustrato, no HR aire. Interfaces RPi esquematicas.'
        view['scene'] = scene

    bpy.context.window.scene = views[0]['scene']
    bpy.data.scenes.remove(construction)
    render_views()
    print('VERIFICADO: 30 macetas, 3 surcos x 10; 9 sensores y cables continuos a 9 entradas RPI; 6 escenas y PNG.')


if __name__ == '__main__':
    if '--render-only' in sys.argv:
        bpy.ops.wm.open_mainfile(filepath=str(HERE/'invernadero_mejorado.blend'))
        render_views()
    else:
        main()
