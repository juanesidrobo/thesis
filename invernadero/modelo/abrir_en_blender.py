#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
abrir_en_blender.py
====================
ABRE EL MODELO DEL INVERNADERO DENTRO DE BLENDER.

Blender NO "abre" archivos .glb con File > Open (eso solo abre .blend).
Para ver un .glb en Blender debes IMPORTARLO:  File > Import > glTF 2.0 (.glb/.gltf).
Este script automatiza ese proceso para que no tengas que buscar el menú.

CÓMO USARLO (elige UNA opción):

  OPCIÓN A) Desde la interfaz de Blender (lo más fácil):
     1. Abre Blender.
     2. En el menú superior:  Scripting  (pestaña junto a Layout / Modeling).
     3. Abre este archivo con  Text > Open...  y selecciona abrir_en_blender.py.
     4. Pulsa el botón  ▶ Run Script  (o Alt+P).

  OPCIÓN B) Desde la línea de comandos (sin abrir la interfaz antes):
     blender --background --python abrir_en_blender.py

  OPCIÓN C) Arrastrando:
     Arrastra el .glb a la ventana de Blender y confirma con "Import glTF".

El modelo importado quedará en la colección 'Invernadero' de la escena.
"""

import os
import bpy

# Ruta al modelo GLB (relativa a este script)
HERE = os.path.dirname(os.path.abspath(__file__))
GLB = os.path.join(HERE, 'invernadero.glb')


def ensure_path():
    if not os.path.exists(GLB):
        # Fallback: buscar en el directorio de trabajo o un nivel arriba
        candidates = [
            GLB,
            os.path.join(os.getcwd(), 'invernadero.glb'),
            os.path.join(os.getcwd(), '..', 'invernadero.glb'),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        raise FileNotFoundError(
            f"No se encontró invernadero.glb. Buscado en: {candidates}"
        )
    return GLB


def main():
    glb = ensure_path()
    print(f"▶ Importando: {glb}")

    # Limpiar la escena actual (opcional; quita la cámara/luz por defecto)
    # Se deja comentado para no perder la escena por defecto si lo prefieres.
    # bpy.ops.object.select_all(action='SELECT')
    # bpy.ops.object.delete()

    # Importar el GLB
    bpy.ops.import_scene.gltf(filepath=glb)

    # Reunir todos los objetos importados
    imported = [o for o in bpy.context.selected_objects]
    if not imported:
        imported = [o for o in bpy.data.objects if o.type == 'MESH']
    print(f"✅ Objetos importados: {len(imported)}")

    # Crear/asegurar una colección para el invernadero
    col = bpy.data.collections.get('Invernadero')
    if col is None:
        col = bpy.data.collections.new('Invernadero')
        bpy.context.scene.collection.children.link(col)

    # Mover los objetos importados a la colección 'Invernadero'
    for obj in imported:
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        col.objects.link(obj)

    # Ajustar la cámara para encuadrar el modelo
    try:
        bpy.ops.view3d.camera_to_view_selected()
    except Exception:
        print("  (no se pudo encuadrar automáticamente la cámara)")

    print("✅ Listo. Cambia a la pestaña 'Layout' o 'Modeling' para ver el invernadero.")
    print("   Consejo: pon el Viewport en 'Material Preview' o 'Rendered' para ver los colores.")


if __name__ == "__main__":
    main()
