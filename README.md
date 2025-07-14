# Simulador de Controlador Termostato - Instrucciones de Instalación y Ejecución
---

## Requisitos
- **Python 3.11** (instalado desde la Microsoft Store de Windows)
- **pip** (incluido en la instalación de Python Store)
- **Git** (opcional, para clonar el repositorio)
---

## Instalación Paso a Paso

### 1. Instalar Python 3.11
1. Abre la **Microsoft Store** en Windows.
2. Busca **Python 3.11** y haz clic en "Obtener" para instalarlo.
3. Una vez instalado, abre una terminal (CMD o PowerShell) y verifica la instalación:

> python --version

Debe mostrar `Python 3.11.x`.

### 2. Descargar el Proyecto

- Extrae el ZIP y navega a la carpeta extraída.

### 3. Instalar Dependencias
Ejecuta en la terminal dentro de la carpeta del proyecto:

> pip install -r requirements.txt

Esto instalará las librerías necesarias: `matplotlib` y `numpy`.

---

## Ejecución del Simulador
Dentro de la carpeta del proyecto, ejecuta:

> python simulacion.py


Se abrirá una ventana con la interfaz gráfica del simulador.

---

## Uso

- **Sliders**: Ajusta la temperatura ambiente, perturbación y rango de control.
- **Botones**:
  - **Defaults**: Restaura los valores por defecto.
  - **Stop/Start**: Pausa o reanuda la simulación.
  - **Reset**: Reinicia la simulación desde cero.

---

## Notas
- El simulador fue probado en Python 3.11. Otras versiones pueden no ser compatibles.

---