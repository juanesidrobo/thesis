"""Blender 4.2+: escena nativa y dos renders reproducibles, sin dependencias.

blender --background --python invernadero/modelo/renderizar_invernadero.py
Anadir -- --preview para reducir resolucion y muestras.
La escena actual se reemplaza; ejecutar en un archivo nuevo.
"""
import math
import random
import sys
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
        p.handle_left_type = p.handle_right_type = 'AUTO'
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


def main():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    metal = material('Aluminio satinado', (.49, .55, .58), .28, .8)
    clay = material('Terracota porosa', (.48, .19, .08), .85, noise=True)
    soil = material('Sustrato', (.055, .032, .014), 1, noise=True)
    bark = material('Corteza', (.16, .085, .027), .9, noise=True)
    greens = [material('Hoja citrico %s' % i, c, .36) for i, c in enumerate(
        [(.09, .23, .018), (.17, .32, .025), (.24, .39, .038), (.055, .16, .012)])]
    gravel = material('Grava caliza', (.42, .43, .38), .95, noise=True)
    white = material('Carcasa blanca', (.87, .9, .87), .3)
    dark = material('Cable y juntas', (.014, .024, .026), .62)
    ink = material('Texto grafito', (.025, .065, .068), .7)
    colors = [material(n, c, .4) for n, c in [
        ('01 HR ambiente azul', (.025, .30, .64)),
        ('02 T ambiente naranja', (.85, .24, .025)),
        ('03 T hoja rojo', (.7, .055, .035)),
        ('04 HR planta turquesa', (.015, .43, .32))]]
    label_colors = []
    for mat in [ink, *colors]:
        label = bpy.data.materials.new('Rotulo ' + mat.name)
        label.use_nodes = True
        label.node_tree.nodes.clear()
        emission = label.node_tree.nodes.new('ShaderNodeEmission')
        emission.inputs[0].default_value = mat.diffuse_color
        output = label.node_tree.nodes.new('ShaderNodeOutputMaterial')
        label.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])
        label_colors.append(label)
    film = material('Cubierta translucida', (.81, .87, .83), .5)
    nodes = film.node_tree.nodes
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    mix = nodes.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = .17
    film.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
    film.node_tree.links.new(next(n for n in nodes if n.type == 'BSDF_PRINCIPLED').outputs[0], mix.inputs[2])
    film.node_tree.links.new(mix.outputs[0], next(n for n in nodes if n.type == 'OUTPUT_MATERIAL').inputs['Surface'])

    box('Entorno', (0, 0, -.15), (200, 200, .12), material('Fondo piedra', (.72, .74, .69), 1))
    box('Lecho de grava', (0, 0, -.025), (6.1, 4.3, .18), gravel)
    # Shared pebble mesh keeps the editable scene small.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1)
    pebble = finish(bpy.context.object, 'Grava_0000', gravel)
    for i in range(2500):
        obj = pebble if i == 0 else bpy.data.objects.new('Grava_%04d' % i, pebble.data)
        if i:
            bpy.context.collection.objects.link(obj)
        obj.location = (random.uniform(-2.97, 2.97), random.uniform(-2.07, 2.07), .07)
        r = random.uniform(.022, .055)
        obj.scale = (r, r*.8, r*.65)
        obj.rotation_euler = (random.random(), random.random(), random.random()*6)

    structure = []
    for x in (-3, 3):
        for y in (-2.1, 0, 2.1):
            structure.append(rod('Estructura_poste', (x,y,.05), (x,y,2.65), .04, metal))
            box('Placa anclaje', (x,y,.1), (.17,.17,.055), metal)
        for z in (.14, 2.65):
            structure.append(rod('Estructura_larguero', (x,-2.1,z), (x,2.1,z), .035, metal))
    for y in (-2.1, 0, 2.1):
        structure.append(rod('Estructura_cabio', (-3,y,2.65), (0,y,3.35), .04, metal))
        structure.append(rod('Estructura_cabio', (0,y,3.35), (3,y,2.65), .04, metal))
    structure.append(rod('Estructura_cumbrera', (0,-2.1,3.35), (0,2.1,3.35), .04, metal))
    for y in (-2.1, 2.1):
        structure.append(rod('Estructura_base', (-3,y,.14), (3,y,.14), .035, metal))
    panels = [box('Cubierta_posterior', (0,2.1,1.39), (6,.012,2.5), film, 0),
              box('Cubierta_izquierda', (-3,0,1.39), (.012,4.2,2.5), film, 0)]
    for x in (-1.5, 1.5):
        panel = box('Cubierta_techo', (x,0,3), (math.hypot(3,.7),4.2,.012), film, 0)
        panel.rotation_euler.y = math.copysign(math.atan2(.7,3), x)
        if x > 0:
            panel.hide_render = True
        panels.append(panel)
    # Removable front/right panels preserve a complete editable greenhouse.
    for name, loc, size in [('Frontal', (0,-2.1,1.39), (6,.012,2.5)),
                            ('Derecho', (3,0,1.39), (.012,4.2,2.5))]:
        obj = box('Panel_desmontado_' + name, loc, size, film, 0)
        obj.hide_render = True
        obj.hide_set(True)

    pots = []
    other_plants = []
    for row, y in enumerate((-1.25, 0, 1.25)):
        for col, x in enumerate((-1.8, 0, 1.8)):
            number = row*3+col+1
            tag = 'P%02d' % number
            before = set(bpy.data.objects)
            pots.append(rod(tag+'_Maceta', (x,y,.09), (x,y,.58), .24, clay, .34))
            bpy.ops.mesh.primitive_torus_add(major_radius=.328, minor_radius=.027,
                                            major_segments=48, minor_segments=12, location=(x,y,.57))
            finish(bpy.context.object, tag+'_Borde', clay)
            rod(tag+'_Tierra', (x,y,.571), (x,y,.58), .305, soil)
            box(tag+'_Placa', (x,y-.315,.43), (.19,.018,.095), white, .008)
            text(tag, tag, (x-.065,y-.329,.402), .065, ink, (math.pi/2,0,0))
            h = random.uniform(1.45, 1.72)
            rod(tag+'_Tronco', (x,y,.57), (x+.025,y,h), .033, bark, .012)
            specs = []
            for j in range(18):
                angle = j*2.399 + random.uniform(-.2,.2)
                z = .86 + (j/18)*.71
                reach = random.uniform(.29,.47) * (1 if j < 10 else .65)
                a = Vector((x,y,z))
                b = a + Vector((math.cos(angle)*reach, math.sin(angle)*reach, random.uniform(.18,.35)))
                rod(tag+'_Rama', a, b, .009, bark, .003)
                for k in range(11):
                    t = .18 + k*.075
                    p = a.lerp(b, t)
                    theta = angle + (1 if k % 2 else -1)*random.uniform(.5,1.25)
                    specs.append((p, (math.cos(theta),math.sin(theta),random.uniform(-.25,.6)),
                                  random.uniform(.16,.26), random.uniform(.038,.062)))
            leaves(tag+'_Follaje', specs, greens)
            if number != 2:
                other_plants.extend(set(bpy.data.objects)-before)

    sensor_points = []
    for i, x in enumerate((-2.63,-1.95)):
        y, z = -1.84, 1.6
        rod('S0%d_Soporte' % (i+1), (x,y,.1), (x,y,z), .019, metal)
        rod('S0%d_Nucleo' % (i+1), (x,y,z-.1), (x,y,z+.12), .06, dark)
        for j in range(6):
            rod('S0%d_Abrigo_radiacion' % (i+1), (x,y,z-.09+j*.048),
                (x,y,z-.065+j*.048), .14, white, .10)
        rod('S0%d_Identificador' % (i+1), (x,y,z-.145), (x,y,z-.1), .079, colors[i])
        cable('S0%d_Cable' % (i+1), [(x,y,z-.15),(x+.035,y,.7),(x+.05,y,.15),(-.3,-1.55,.15)], dark)
        sensor_points.append(Vector((x,y,z+.18)))

    # Both plant sensors belong to P02; HR measures air beside the leaf, not soil.
    leaf_origin = Vector((.12,-1.57,1.39))
    leaf_tip = Vector((.46,-1.86,1.48))
    rod('P02_Rama_instrumentada', (0,-1.25,1.08), leaf_origin, .009, bark, .004)
    leaves('P02_Hoja_instrumentada', [(leaf_origin, leaf_tip-leaf_origin, .46, .10)], [greens[2]])
    clip = Vector((.32,-1.74,1.46))
    for dz in (-.022,.022):
        box('S03_Pinza_temperatura_hoja', clip+Vector((0,0,dz)), (.13,.055,.026), white, .01)
    box('S03_Identificador_rojo', clip+Vector((.02,-.033,.023)), (.06,.012,.02), colors[2], .004)
    rod('S03_Contacto_termico', clip-Vector((0,0,.018)), clip+Vector((0,0,.012)), .008, metal)
    cable('S03_Cable', [clip,(.52,-1.8,1.2),(.3,-1.55,.65),(.13,-1.58,.57)], dark, .006)
    sensor_points.append(clip)
    hr = Vector((-.30,-1.67,1.24))
    rod('S04_Soporte_P02', (-.23,-1.39,.59), (-.23,-1.39,1.32), .012, metal)
    rod('S04_Brazo', (-.23,-1.39,1.27), hr, .012, metal)
    box('S04_Humedad_relativa_follaje', hr, (.13,.09,.22), white, .022)
    box('S04_Identificador_verde', hr+Vector((0,-.051,.065)), (.105,.014,.04), colors[3], .004)
    for j in range(5):
        box('S04_Ranura_aire', hr+Vector((0,-.047,-.06+j*.022)), (.085,.008,.008), dark, .003)
    cable('S04_Cable', [hr,(-.35,-1.57,.99),(-.26,-1.58,.65),(-.13,-1.58,.55)], dark, .006)
    sensor_points.append(hr)
    box('P02_Adquisicion_datos', (0,-1.59,.72), (.24,.10,.20), dark)
    box('P02_Panel_registrador', (0,-1.645,.73), (.19,.012,.12), colors[3], .008)

    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 16 if PREVIEW else 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 1800, 1500
    scene.render.resolution_percentage = 55 if PREVIEW else 100
    scene.render.image_settings.file_format = 'PNG'
    scene.world.color = (.55,.55,.55)
    scene.view_settings.view_transform = 'AgX'
    for name, loc, power, size in [('Luz principal', (0,-4,8), 1700, 7),
                                    ('Relleno', (-5,-1,4), 850, 5)]:
        bpy.ops.object.light_add(type='AREA', location=loc)
        light = bpy.context.object
        light.name, light.data.energy, light.data.shape, light.data.size = name, power, 'DISK', size
        light.rotation_euler = (Vector((0,0,0))-light.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.light_add(type='SUN', location=(0,0,8))
    bpy.context.object.data.energy = 1.3
    bpy.context.object.data.angle = .15
    bpy.context.object.rotation_euler = (.4,-.5,-.4)
    general = camera('01_Vista_general', (7,-11,8.7), (0,0,1.35), 9.9)
    detail = camera('02_Planta_instrumentada', (2.7,-6,3.1), (0,-1.4,1.05), 2.95)
    rows = ['01  Humedad relativa ambiente', '02  Temperatura ambiente',
            '03  Temperatura de hoja / P02', '04  Humedad relativa junto a hoja / P02']
    general_labels = overlay(general, 'INVERNADERO / CITRICOS',
                            '9 plantas madre  /  4 sensores  /  vista de corte ilustrativa', rows, label_colors[0], label_colors[1:])
    detail_labels = overlay(detail, 'P02 / MICROCLIMA FOLIAR',
                           '03 contacto en hoja  /  04 humedad relativa del aire junto al follaje',
                           ['03  Pinza de contacto sobre la hoja', '04  Sonda ventilada: HR del aire'], label_colors[0], label_colors[3:])
    badges = []
    for i, p in enumerate(sensor_points):
        anchor = p + Vector((-.10,0,.25 if i != 3 else .30))
        rod('Guia_S%02d' % (i+1), p, anchor, .005, colors[i])
        obj = text('Identificador_S%02d' % (i+1), '%02d' % (i+1), anchor, .14, label_colors[i+1])
        badges.append(obj)

    assert len(pots) == 9
    assert len(sensor_points) == 4
    OUT.mkdir(parents=True, exist_ok=True)
    detail_hidden = other_plants + structure + panels + [
        obj for obj in bpy.data.objects if obj.name.startswith(('S01_', 'S02_', 'Guia_S01', 'Guia_S02', 'Placa anclaje'))] + badges[:2]
    original_visibility = {obj: obj.hide_render for obj in detail_hidden}
    for cam, filename in [(general,'render_invernadero_mejorado.png'),
                           (detail,'detalle_sensores_planta.png')]:
        scene.camera = cam
        for obj in general_labels:
            obj.hide_render = cam != general
        for obj in detail_labels:
            obj.hide_render = cam != detail
        for obj in badges:
            obj.rotation_euler = cam.rotation_euler
        for obj in detail_hidden:
            obj.hide_render = True if cam == detail else original_visibility[obj]
        # Isolate the same P02 geometry for a readable instrumentation detail.
        scene.render.filepath = str(OUT / filename)
        bpy.ops.render.render(write_still=True)
    scene.camera = general
    for obj, hidden in original_visibility.items():
        obj.hide_render = hidden
    for obj in general_labels:
        obj.hide_render = False
    for obj in detail_labels:
        obj.hide_render = True
    for obj in badges:
        obj.rotation_euler = general.rotation_euler
    scene.render.filepath = str(OUT / 'render_invernadero_mejorado.png')
    scene['Instrumentacion'] = 'S01 HR ambiente; S02 T ambiente; S03 T hoja P02; S04 HR aire follaje P02'
    scene['Nota'] = 'Diseno ilustrativo, no dimensiones ni carcasas de equipos comerciales. Frente y lateral derecho desmontados para visualizacion.'
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(HERE / 'invernadero_mejorado.blend'))
    print('VERIFICADO: 9 macetas; 4 sensores; S03 y S04 en P02. Dos PNG y escena BLEND guardados.')


if __name__ == '__main__':
    main()
