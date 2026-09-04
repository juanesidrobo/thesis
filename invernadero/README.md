# invernadero/

Carpeta para el **render / modelo 3D del invernadero** donde se ejecutará y
desplegará el proyecto de la tesis.

> 🕑 **Estado: PENDIENTE.** Esta carpeta está reservada. Retomaremos el render,
> el modelado 3D y la ambientación más adelante según lo acordado.

## 📂 Estructura propuesta (cuando se desarrolle)

```
invernadero/
├── README.md               ← este archivo
├── modelo/                 ← archivos fuente del modelo 3D (.blend, .fbx, .obj, .stl)
├── texturas/               ← texturas y materiales (.png, .jpg, .hdr)
├── renders/                ← imágenes de render finales (.png, .jpg)
└── blenders/               ← scripts de Blender (setup de escena, luces, cámara)
```

## 🛠️ Herramientas sugeridas

- **Blender** (gratuito y open-source) para modelado y render del invernadero.
- **Godot / 3.js** si más adelante se quiere una visor interactivo en web.
- **MeshLab / CloudCompare** si se trabaja con nubes de puntos o escaneo.

## 📎 Notas sobre el control de versiones

Los archivos fuente del modelo 3D (`*.blend`, `*.fbx`, `*.obj`, texturas) pueden ser
muy pesados para Git. Se recomienda:

- usar **Git LFS** (`git lfs track "*.blend" "*.fbx" "*.obj"`), o
- subir **solo los renders finales** (png/jpg) y guardar los fuentes fuera del repositorio.

> ⚠️ Volveremos a esta carpeta en una fase posterior del proyecto.
