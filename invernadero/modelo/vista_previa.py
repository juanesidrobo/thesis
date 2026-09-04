#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vista_previa.py
===============
Genera una imagen de vista previa del modelo 3D del invernadero (invernadero.glb),
renderizándolo con matplotlib de forma ordenada: primero los objetos opacos
(plantas, macetas, sensores, grava) y después los paneles translúcidos.

Guarda:
    ../../renders/vista_previa_invernadero.png
"""

import os
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# (color, alpha, orden_de_dibujo)
MAT_STYLE = {
    'aluminio':      ((0.66, 0.69, 0.73), 1.0, 0),
    'policarbonato': ((0.86, 0.91, 0.96), 0.16, 1),   # translúcido, se dibuja al final
    'terracota':     ((0.72, 0.36, 0.19), 1.0, 0),
    'suelo':         ((0.30, 0.20, 0.12), 1.0, 0),
    'tronco':        ((0.45, 0.29, 0.16), 1.0, 0),
    'hoja':          ((0.20, 0.52, 0.20), 1.0, 0),
    'grava':         ((0.84, 0.83, 0.80), 1.0, 0),
    'sensor_wh':     ((0.95, 0.96, 0.95), 1.0, 0),
    'sensor_dk':     ((0.10, 0.10, 0.11), 1.0, 0),
    'metal':         ((0.58, 0.58, 0.60), 1.0, 0),
    'conn_green':    ((0.16, 0.47, 0.27), 1.0, 0),
}


def main():
    scene = trimesh.load('invernadero.glb')

    # Reunir polígonos por material y por capa (opaco vs translúcido)
    layers = {0: [], 1: []}      # 0 = opaco, 1 = translúcido
    layercolors = {0: [], 1: []}
    layeralpha = {0: [], 1: []}
    for geom in scene.geometry.values():
        if not hasattr(geom, 'vertices') or len(geom.vertices) == 0:
            continue
        mat_name = 'gris'
        if hasattr(geom, 'visual') and geom.visual.material is not None:
            mat_name = geom.visual.material.name
        col, alpha, layer = MAT_STYLE.get(mat_name, ((0.7, 0.7, 0.7), 1.0, 0))
        tris = geom.vertices[geom.faces]
        for t in tris:
            layers[layer].append(t)
            layercolors[layer].append(col)
            layeralpha[layer].append(alpha)

    all_pts = np.array([p for t in layers[0] for p in t])
    lo, hi = all_pts.min(axis=0), all_pts.max(axis=0)
    size = hi - lo

    fig = plt.figure(figsize=(16, 11))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect(size)

    # Dibujar primero la capa opaca, luego la translúcida (para ver el interior)
    for layer in (0, 1):
        polys = layers[layer]
        if not polys:
            continue
        rgba = [[r, g, b, a] for (r, g, b), a in zip(layercolors[layer], layeralpha[layer])]
        coll = Poly3DCollection(polys, facecolors=rgba, edgecolors='none')
        ax.add_collection3d(coll)

    ax.set_xlim(lo[0], hi[0])
    ax.set_ylim(lo[1], hi[1])
    ax.set_zlim(lo[2], hi[2])
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Invernadero de cítricos con plantas madre — vista previa 3D')
    ax.view_init(elev=20, azim=-60)
    ax.grid(False)
    ax.set_axis_off()

    plt.tight_layout()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, '..', 'renders', 'vista_previa_invernadero.png')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=140, bbox_inches='tight')
    print(f"✅ Vista previa guardada: {out}")


if __name__ == '__main__':
    main()
