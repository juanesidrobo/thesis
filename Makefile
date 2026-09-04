# ============================================================
#  Makefile raíz — orquestador de compilación
#  Delega en el proyecto LaTeX de la carpeta documentacion/
# ============================================================

.PHONY: all watch clean clean-full pdf

all: pdf

pdf:
	$(MAKE) -C documentacion pdf

watch:
	$(MAKE) -C documentacion watch

clean:
	$(MAKE) -C documentacion clean

clean-full:
	$(MAKE) -C documentacion clean-full
