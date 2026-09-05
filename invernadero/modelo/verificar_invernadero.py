"""Comprueba el BLEND y los seis PNG sin modificarlos. Ejecutar con Blender."""
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(HERE/'invernadero_mejorado.blend'))
scene = bpy.data.scenes['01_Invernadero']
pots = [o for o in scene.objects if o.name.endswith('_Maceta')]
assert len(pots) == 30
for row in (1,2,3):
    row_pots = [p for p in pots if p['surco'] == row]
    assert sorted(p['planta'] for p in row_pots) == list(range(1,11))
    assert all(abs(p.location.x-(-1.8,0,1.8)[row-1]) < 1e-5 for p in row_pots)
    assert all(abs(p.location.y-(-5.85+(p['planta']-1)*1.3)) < 1e-5 for p in row_pots)
targets = {'S1-P01','S2-P05','S3-P10'}
assert {p.name.removesuffix('_Maceta') for p in pots if p['instrumentada']} == targets
sensors = [o for o in scene.objects if o.name.startswith('Sensor_')]
cables = [o for o in scene.objects if o.name.startswith('Conexion_')]
assert len(sensors) == len(cables) == 9
assert {o['puerto'] for o in sensors} == set(range(1,10))
for sensor in sensors:
    sid = sensor.name.removeprefix('Sensor_')
    cable = scene.objects['Conexion_'+sid]
    assert cable['sensor_id'] == sid
    assert cable['planta'] == sensor['planta']
    assert cable['puerto'] == sensor['puerto']
    points = cable.data.splines[0].bezier_points
    gland = scene.objects['RPI_Entrada_%02d' % sensor['puerto']]
    assert (points[0].co-sensor.location).length < 1e-5
    assert (points[-1].co-(gland.location-Vector((0,0,.045)))).length < 1e-5
for tag in targets:
    local = [s for s in sensors if s['planta'] == tag]
    assert {s['variable'] for s in local} == {'Temperatura hoja','Humedad suelo maceta'}
assert len(bpy.data.scenes) == 6
for view in bpy.data.scenes:
    assert view.camera is not None
    assert view.render.resolution_percentage == 100
    assert view.cycles.samples == 48
    path = Path(view.render.filepath)
    assert path.is_file(), path
    image = bpy.data.images.load(str(path),check_existing=False)
    assert tuple(image.size) == (view.render.resolution_x,view.render.resolution_y)
    bpy.data.images.remove(image)
    if view.name.startswith(('03_','04_','05_')):
        assert len([o for o in view.objects if o.name.endswith('_Maceta')]) == 1
        assert len([o for o in view.objects if o.name.startswith('Sensor_')]) == 2
assert bpy.context.scene.name == '01_Invernadero'
assert not list((HERE.parent/'renders').glob('*.rendering.png'))
print('PASS: 30 plantas / 3x10; ubicaciones A-B-C; 9 sensores y extremos de cables; 6 escenas y PNG finales.')
