#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_invernadero.py
======================
Genera el modelo 3D (GLB) del invernadero de cítricos con plantas madre,
según la referencia fotográfica aportada, y lo exporta a:

    invernadero/modelo/invernadero.glb

Contenido del modelo:
  - Estructura metálica (aluminio): postes, vigas y cabios del techo.
  - Paredes y techo en material blanco translúcido (policarbonato).
  - Suelo de grava (lecho).
  - Macetas de barro (terracota) con plantas madre de cítricos (tronco + hojas).
  - Sensores:
        * sensor de temperatura/humedad ambiente (carcasa blanca de láminas).
        * sensor de humedad en el suelo (sonda en el lecho de grava).
    En ALGUNAS plantas (instrumentadas):
        * sensor de humedad en la maceta.
        * sensor de temperatura en las hojas (pinza con cable).
  - Se añaden MÁS plantas SIN sensores; solo algunas portan instrumentación.

Ejecutar:
    python3 generar_invernadero.py
"""

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals

# ----------------------------------------------------------------------------
#  MATERIALES (PBR)
# ----------------------------------------------------------------------------
def make_mat(name, base, metallic=0.0, rough=0.8, alpha=None, double=False):
    """Crea un material PBR. Si alpha no es None, se usa modo BLEND."""
    m = PBRMaterial(name=name,
                    baseColorFactor=[*base, 1.0],
                    metallicFactor=metallic,
                    roughnessFactor=rough)
    if alpha is not None:
        m.baseColorFactor = [*base, alpha]
        m.alphaMode = 'BLEND'
        m.doubleSided = True
    return m


MATS = {
    'aluminio':   make_mat('aluminio',   [0.72, 0.74, 0.78], metallic=0.9, rough=0.35),
    'vidrio':     make_mat('policarbonato', [0.94, 0.97, 1.00], metallic=0.1, rough=0.12, alpha=0.33, double=True),
    'terracota':  make_mat('terracota',  [0.70, 0.36, 0.20], metallic=0.0, rough=0.9),
    'suelo':      make_mat('suelo',      [0.20, 0.13, 0.08], metallic=0.0, rough=1.0),
    'tronco':     make_mat('tronco',     [0.40, 0.26, 0.15], metallic=0.0, rough=0.9),
    'hoja':       make_mat('hoja',       [0.22, 0.50, 0.20], metallic=0.0, rough=0.45),
    'grava':      make_mat('grava',      [0.78, 0.77, 0.74], metallic=0.0, rough=1.0),
    'sensor_wh':  make_mat('sensor_wh',  [0.92, 0.93, 0.92], metallic=0.1, rough=0.4),
    'sensor_dk':  make_mat('sensor_dk',  [0.12, 0.12, 0.13], metallic=0.2, rough=0.5),
    'metal':      make_mat('metal',      [0.55, 0.55, 0.57], metallic=0.85, rough=0.4),
    'conn_green': make_mat('conn_green', [0.16, 0.46, 0.26], metallic=0.0, rough=0.5),
}


# ----------------------------------------------------------------------------
#  UTILIDADES GEOMÉTRICAS
# ----------------------------------------------------------------------------
GEOM_COUNTER = [0]

def _set_mat(mesh, mat):
    mesh.visual = TextureVisuals(material=mat)
    return mesh


def _name(prefix):
    GEOM_COUNTER[0] += 1
    return f"{prefix}_{GEOM_COUNTER[0]:04d}"


def rotation_from_to(a, b):
    """Matriz de rotación 3x3 que alinea el vector a con el b."""
    a = np.asarray(a, float) / np.linalg.norm(a)
    b = np.asarray(b, float) / np.linalg.norm(b)
    v = np.cross(a, b)
    c = float(np.dot(a, b))
    s = float(np.linalg.norm(v))
    if s < 1e-8:
        return np.eye(3) if c > 0 else -np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - c) / (s * s))


def beam(p1, p2, t, mat, prefix='viga'):
    """Caja (prisma) entre dos puntos, con sección cuadrada de lado t."""
    p1 = np.asarray(p1, float)
    p2 = np.asarray(p2, float)
    d = p2 - p1
    L = float(np.linalg.norm(d))
    if L < 1e-9:
        return None
    mesh = trimesh.creation.box(extents=[L, t, t])
    R = rotation_from_to([1, 0, 0], d)
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = (p1 + p2) / 2.0
    mesh.apply_transform(T)
    return _set_mat(mesh, mat)


def box(size, loc, mat, prefix='caja', rot=None):
    mesh = trimesh.creation.box(extents=size)
    T = np.eye(4)
    if rot is not None:
        T[:3, :3] = rot
    T[:3, 3] = loc
    mesh.apply_transform(T)
    return _set_mat(mesh, mat)


def cylinder(radius, height, loc, mat, prefix='cil', segments=20, axis=(0, 1, 0), r2=None):
    """Cilindro. Si r2 se da, se genera un cilindro cónico (frustum)."""
    if r2 is None:
        mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=segments)
    else:
        # frustum: dos círculos de distinto radio
        mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=segments)
        top = mesh.vertices[:, 1] > 0
        mesh.vertices[top, :2] *= (r2 / radius)
    mesh.apply_translation([0, height / 2.0, 0])   # base en el origen
    R = rotation_from_to([0, 1, 0], axis)
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = loc
    mesh.apply_transform(T)
    return _set_mat(mesh, mat)


def torus(major, minor, loc, mat, prefix='toro', rot=None):
    mesh = trimesh.creation.torus(major_radius=major, minor_radius=minor, major_segments=24, minor_segments=10)
    T = np.eye(4)
    if rot is not None:
        T[:3, :3] = rot
    T[:3, 3] = loc
    mesh.apply_transform(T)
    return _set_mat(mesh, mat)


def icosphere(radius, loc, mat, prefix='esfera', scale=None, rot=None):
    mesh = trimesh.creation.icosphere(subdivisions=1, radius=radius)
    if scale is not None:
        mesh.apply_scale(scale)
    T = np.eye(4)
    if rot is not None:
        T[:3, :3] = rot
    T[:3, 3] = loc
    mesh.apply_transform(T)
    return _set_mat(mesh, mat)


# ----------------------------------------------------------------------------
#  CONSTRUCTORES DE PARTES
# ----------------------------------------------------------------------------
def build_frame():
    """Estructura metálica del invernadero."""
    g = []
    X = 3.0        # semiancho
    Z = 2.0        # semiprofundidad
    H = 2.2        # altura de los muros (alero)
    RIDGE = 3.2    # altura de la cumbrera
    t = 0.06       # grosor de perfiles

    # Postes verticales en las 4 esquinas y en puntos medios
    for z in (-Z, Z):
        for x in (-X, -X/2, 0, X/2, X):
            g.append(cylinder(t, H, (x, 0, z), MATS['aluminio'], 'poste', segments=8))
    # Postes en los laterales (muros largos)
    for x in (-X, X):
        for z in (-Z/2, Z/2):
            g.append(cylinder(t, H, (x, 0, z), MATS['aluminio'], 'poste', segments=8))

    # Vigas superiores (alero): un rectángulo perimetral
    y_e = H
    for x in (-X, X):
        g.append(beam((x, y_e, -Z), (x, y_e, Z), t, MATS['aluminio'], 'viga'))
    for z in (-Z, Z):
        g.append(beam((-X, y_e, z), (X, y_e, z), t, MATS['aluminio'], 'viga'))

    # Cabios del techo (gable a dos aguas) en cada extremo y en puntos intermedios
    for z in (-Z, -Z/2, 0, Z/2, Z):
        g.append(beam((-X, y_e, z), (0, RIDGE, z), t, MATS['aluminio'], 'cabio'))
        g.append(beam((0, RIDGE, z), (X, y_e, z), t, MATS['aluminio'], 'cabio'))

    # Cumbrera
    g.append(beam((0, RIDGE, -Z), (0, RIDGE, Z), t, MATS['aluminio'], 'cumbrera'))

    # Refuerzos horizontales en muros (a media altura)
    for z in (-Z, Z):
        for x in (-X, X):
            g.append(beam((x, H/2, z), (x, H/2, z), 0.001, MATS['aluminio'], 'dummy') if False else None)
    for z in (-Z, Z):
        g.append(beam((-X, H*0.55, z), (X, H*0.55, z), 0.04, MATS['aluminio'], 'refuerzo'))
    for x in (-X, X):
        g.append(beam((x, H*0.55, -Z), (x, H*0.55, Z), 0.04, MATS['aluminio'], 'refuerzo'))

    g = [m for m in g if m is not None]
    return g


def build_walls():
    """Paneles translúcidos de paredes y techo."""
    g = []
    X, Z, H, RIDGE = 3.0, 2.0, 2.2, 3.2
    th = 0.02  # grosor del panel

    # Muros frontales y traseros
    for z in (-Z, Z):
        g.append(box([2*X, H-0.1, th], (0, H/2, z), MATS['vidrio'], 'muro'))
    # Muros laterales
    for x in (-X, X):
        g.append(box([th, H-0.1, 2*Z], (x, H/2, 0), MATS['vidrio'], 'muro'))

    # Paneles del techo (dos aguas)
    def roof_panel(x1, x2):
        p1 = np.array([x1, H, 0.0])
        p2 = np.array([x2, RIDGE, 0.0])
        d = p2 - p1
        L = float(np.linalg.norm(d))
        mid = (p1 + p2) / 2.0
        mesh = trimesh.creation.box(extents=[L, 0.02, 2*Z-0.05])
        R = rotation_from_to([1, 0, 0], d)
        T = np.eye(4); T[:3, :3] = R; T[:3, 3] = mid
        mesh.apply_transform(T)
        return _set_mat(mesh, MATS['vidrio'])
    g.append(roof_panel(-X, 0.0))
    g.append(roof_panel(0.0, X))
    return g


def build_gravel():
    """Lecho de grava: base + piedrecillas dispersas."""
    g = []
    X, Z = 2.75, 1.75
    # Base del lecho
    g.append(box([2*X, 0.06, 2*Z], (0, 0.03, 0), MATS['grava'], 'cama_grava'))
    # Piedrecillas
    rng = np.random.default_rng(7)
    n = 140
    for _ in range(n):
        x = rng.uniform(-X+0.1, X-0.1)
        z = rng.uniform(-Z+0.1, Z-0.1)
        r = rng.uniform(0.02, 0.045)
        g.append(icosphere(r, (x, 0.06 + r*0.4, z), MATS['grava'], 'piedra', scale=[1, 0.7, 1]))
    return g


def build_plant(base, instrumented=False, seed=0):
    """Planta madre de cítricos en maceta de barro. Devuelve lista de mallas."""
    g = []
    rng = np.random.default_rng(seed)
    x0, z0 = base
    H_PLANT = 1.15           # altura total aprox.
    pot_h = 0.34
    pot_r_top = 0.24
    pot_r_bot = 0.17

    # --- Maceta (frustum de terracota) ---
    pot = cylinder(pot_r_bot, pot_h, (x0, 0.06, z0), MATS['terracota'], 'maceta', segments=24, r2=pot_r_top)
    g.append(pot)
    # Borde de la maceta
    g.append(torus(pot_r_top*0.98, 0.025, (x0, 0.06+pot_h, z0), MATS['terracota'],
                   'borde_maceta', rot=rotation_from_to([0, 0, 1], [0, 1, 0])))
    # --- Tierra ---
    soil_top_y = 0.06 + pot_h - 0.02
    g.append(cylinder(pot_r_top*0.94, 0.04, (x0, soil_top_y-0.04, z0), MATS['suelo'], 'tierra', segments=24))

    # --- Tronco ---
    trunk_h = H_PLANT * 0.55
    trunk = cylinder(0.028, trunk_h, (x0, soil_top_y, z0), MATS['tronco'], 'tronco', segments=10, r2=0.018)
    g.append(trunk)
    top_base = np.array([x0, soil_top_y, z0])

    # --- Ramas y hojas ---
    n_branch = 3
    leaf_clusters = []
    for b in range(n_branch):
        ang = rng.uniform(0, 2*np.pi)
        tilt = rng.uniform(0.35, 0.7)
        length = rng.uniform(0.28, 0.42)
        d = np.array([np.cos(ang)*np.sin(tilt), np.cos(tilt), np.sin(ang)*np.sin(tilt)])
        p_end = top_base + np.array([0, trunk_h*0.55, 0]) + d * length
        g.append(beam(top_base + np.array([0, trunk_h*0.35, 0]), p_end, 0.016, MATS['tronco'], 'rama'))
        leaf_clusters.append(p_end)

    # Copas densas de hojas alrededor de los extremos de ramas
    for i, c in enumerate(leaf_clusters):
        for _ in range(6):
            off = rng.normal(0, 0.16, 3)
            off[1] *= 0.7
            r = rng.uniform(0.05, 0.10)
            g.append(icosphere(r, c + off, MATS['hoja'], 'hoja', scale=[1.0, 0.6, 1.0]))
    # Copa central
    top_center = top_base + np.array([0, trunk_h*0.8, 0])
    for _ in range(8):
        off = rng.normal(0, 0.20, 3); off[1] *= 0.6
        g.append(icosphere(rng.uniform(0.05, 0.11), top_center + off, MATS['hoja'], 'hoja', scale=[1.0, 0.62, 1.0]))

    if instrumented:
        # --- Sensor de humedad en la maceta ---
        probe_y = soil_top_y
        g.append(cylinder(0.012, 0.16, (x0+pot_r_top*0.55, probe_y-0.10, z0+0.02), MATS['sensor_dk'], 'sonda_hm', segments=10, axis=(0, 1, 0)))
        # conector verde en el borde
        g.append(cylinder(0.018, 0.05, (x0+pot_r_top*0.55, probe_y, z0+0.02), MATS['conn_green'], 'conector', segments=10))
        # --- Sensor de temperatura en hoja: pinza + cable ---
        leaf_pt = leaf_clusters[0] + np.array([0.08, -0.04, 0.02])
        g.append(box([0.035, 0.02, 0.02], leaf_pt, MATS['sensor_dk'], 'pinza_hoja'))
        # cable fino desde la pinza hasta la maceta
        g.append(beam(leaf_pt, (x0+pot_r_top*0.4, soil_top_y+0.05, z0-0.04), 0.006, MATS['sensor_dk'], 'cable'))

    return g


def build_ambient_sensor(loc):
    """Sensor de temperatura/humedad ambiente (carcasa blanca de láminas)."""
    g = []
    x, z = loc
    # Poste
    g.append(cylinder(0.018, 0.9, (x, 0.06, z), MATS['metal'], 'poste_sensor', segments=10))
    # Carcasa de láminas (discos blancos apilados)
    y0 = 0.72
    for i in range(5):
        y = y0 + i*0.035
        g.append(cylinder(0.085, 0.022, (x, y, z), MATS['sensor_wh'], 'lamina', segments=20))
    return g


def build_ground_moisture(loc):
    """Sensor de humedad en el suelo, clavado en el lecho de grava."""
    g = []
    x, z = loc
    g.append(cylinder(0.012, 0.22, (x, 0.06, z), MATS['sensor_dk'], 'sonda_suelo', segments=10, axis=(0, 1, 0)))
    g.append(cylinder(0.02, 0.05, (x, 0.26, z), MATS['sensor_dk'], 'captor_suelo', segments=10))
    g.append(cylinder(0.03, 0.04, (x+0.05, 0.05, z), MATS['sensor_dk'], 'caja_suelo', segments=10))
    g.append(beam((x, 0.26, z), (x+0.05, 0.05, z), 0.008, MATS['sensor_dk'], 'cable_suelo'))
    return g


# ----------------------------------------------------------------------------
#  COMPOSICIÓN DE LA ESCENA
# ----------------------------------------------------------------------------
def build_scene():
    parts = []

    parts += build_frame()
    parts += build_walls()
    parts += build_gravel()

    # Plantas madre de cítricos: rejilla de 3x3 = 9 plantas.
    # Solo ALGUNAS están instrumentadas (3 de 9).
    plants = []
    for r, z in enumerate([-1.05, 0.0, 1.05]):
        for c, x in enumerate([-1.7, 0.0, 1.7]):
            plants.append({'base': (x, z), 'seed': r*10 + c})

    # Índices instrumentados: 0, 4, 8 (esquina, centro, esquina)
    inst_flags = {0: True, 4: True, 8: True}
    for i, p in enumerate(plants):
        parts += build_plant(p['base'], instrumented=inst_flags.get(i, False), seed=p['seed'])

    # Sensor ambiental y de suelo (ubicados fuera del eje de las plantas)
    parts += build_ambient_sensor((2.55, 1.55))
    parts += build_ground_moisture((0.85, 0.6))

    # --- Construir escena trimesh ---
    scene = trimesh.Scene()
    for m in parts:
        if m is not None:
            scene.add_geometry(m, node_name=_name('obj'), geom_name=_name('geo'))
    return scene


if __name__ == '__main__':
    scene = build_scene()
    out = 'invernadero.glb'
    scene.export(out)
    print(f"✅ Modelo exportado: {out}")
    print(f"   Geometrías: {len(scene.geometry)}")
    print(f"   Materiales: {len([g.visual.material.name for g in scene.geometry.values() if hasattr(g.visual, 'material') and g.visual.material is not None])}")
    b = scene.bounds
    print(f"   Extensión (m): x=[{b[0][0]:.2f},{b[1][0]:.2f}]  y=[{b[0][1]:.2f},{b[1][1]:.2f}]  z=[{b[0][2]:.2f},{b[1][2]:.2f}]")
