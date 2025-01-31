
## Cursos disponibles:

- Introducción a Linux [15 horas]
- Personalización de Linux [3 horas]
- Introducción al Hacking [53 horas]

## Instalación

Instala el paquete usando `pip3`:

```python3
pip3 install paquete
```

## Uso básico

### Listar todos los cursos

```python
from courses import listar

for x in listar():
    print(x)
```

### Obtener un curso por nombre

```python
from courses import buscar

course = buscar("Introduccion a Linux")
print(course)
```

### Calcular duración total de los cursos

```python3
from courses.utils import duracion

print(f"Duración total: {duracion()} horas")
```

