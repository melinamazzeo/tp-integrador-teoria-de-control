import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RangeSlider, Button, CheckButtons
from controlador import ThermostatSim as ctrl

# Parametros iniciales del simulador
defaults = {
    't_amb':      25.0, # De la casa en °C
    't_pert':      0.0, # Perturbacion inicial en °C
    'coef_amb':    0.002, # Influencia del entorno sobre el sistema °C / seg
    'delta_max':   0.07,  # Maximo de influencia de temp ambiente a aplicar por iteración °C / min (ajustado para demostracion)
    'vol_room':    3*3*2.9, # m³
    'actuadores_on': True, # Actuadores habilitados
    'pot_heat':    120, # W (J/s)
    'pot_cool':    2000, # W
    'eff_heat':    0.95, # Eficiencia del sistema de calefaccion
    'eff_cool':    0.75, # Eficiencia del sistema de refrigeracion
    't_low':       23.0, # Rango de control inferior en °C
    't_high':      27.0, # Rango de control superior en °C
    'dens_air':    1.2, # kg / m³
    'c_air':       1005 # J / kg.°C
}
SCALE = 60.0  # segundos en minuto

# Instanciar el simulador del controlador
sim = ctrl(defaults)

# Preparar graficos y definir limites de ejes x e y iniciales
fig, (ax_temp, ax_pert, ax_error) = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
plt.subplots_adjust(bottom=0.3)

line_theta_o, = ax_temp.plot([], [], label="\u03F4o", color="green")
line_theta_i,  = ax_temp.plot([], [], label="\u03F4i", color="orange", linestyle="--", alpha=0.8)
ax_tlow_line = ax_temp.axhline(
    defaults['t_low'],  color='blue',  linestyle='--')
ax_thigh_line = ax_temp.axhline(
    defaults['t_high'], color='red',   linestyle='--')
ax_temp.set_ylabel("°C")
ax_temp.grid()
leg_temp = ax_temp.legend(loc='upper left')

line_theta_p, = ax_pert.plot([], [], label="\u03F4p", color="magenta")
ax_pert.set_ylabel("°C")
ax_pert.grid()
leg_pert = ax_pert.legend(loc='upper left')

line_error, = ax_error.plot([], [], label="e", color="cyan")
ax_error.set_ylabel("°C")
ax_error.set_xlabel("Tiempo (min)")
ax_error.grid()
leg_error = ax_error.legend(loc='upper left')

def init_limits(ax, y0, x0=0, y_margin=1):
    ax.min_xlim = x0
    ax.max_xlim = x0
    ax.min_ylim = y0 - y_margin
    ax.max_ylim = y0 + y_margin
    ax.set_xlim(ax.min_xlim, ax.max_xlim)
    ax.set_ylim(ax.min_ylim, ax.max_ylim)

init_limits(ax_temp, defaults['t_amb'], y_margin=1)
init_limits(ax_pert, defaults['t_pert'], y_margin=0.5)
init_limits(ax_error, 0.0, y_margin=0.2)

def extend_axis(ax, low, high):
    if low < ax.min_ylim:
        ax.min_ylim = low
        ax.set_ylim(ax.min_ylim, ax.max_ylim)
    if high > ax.max_ylim:
        ax.max_ylim = high
        ax.set_ylim(ax.min_ylim, ax.max_ylim)

# Definir controles de la interfaz grafica (sliders, rango y botones)
slider_axes = [
    plt.axes([0.20, 0.14, 0.7, 0.03], facecolor='lightgoldenrodyellow'),
    plt.axes([0.20, 0.11, 0.7, 0.03], facecolor='lightgoldenrodyellow'),
    plt.axes([0.20, 0.08, 0.7, 0.03], facecolor='lightgoldenrodyellow'),
    plt.axes([0.20, 0.17, 0.7, 0.03], facecolor='lightgoldenrodyellow'),
]
sld_t_amb = Slider(slider_axes[0], "Temp. Ambiente (\u03F4i)", 0.0, 40, valinit=defaults['t_amb'], valstep=0.5)
sld_t_pert = Slider(slider_axes[1], "Perturbacion (\u03F4p)", -15.0, 15.0, valinit=defaults['t_pert'], valstep=0.5)
rsld_temp_ctrl = RangeSlider(slider_axes[2], "Rango", 0, 30, valinit=(defaults['t_low'], defaults['t_high']))
check_actu = CheckButtons(slider_axes[3], ["Actuadores activos"], actives=[defaults['actuadores_on']])

ax_actu = plt.axes([0.20, 0.01, 0.15, 0.04])
ax_actu.set_axis_off()
text_actu = ax_actu.text(0.5, 0.5, 'Estado: ', horizontalalignment='center', verticalalignment='center',
                   fontsize=8, color='blue')

ax_default = plt.axes([0.48, 0.01, 0.1, 0.04])
ax_toggle = plt.axes([0.7, 0.01, 0.1, 0.04])
ax_reset = plt.axes([0.59, 0.01, 0.1, 0.04])

btn_defaults = Button(ax_default, 'Defaults')
btn_toggle = Button(ax_toggle, 'Stop')
btn_reset = Button(ax_reset, 'Reset')

# Funcion de actualizacion de animacion (graficos)
def update(frame):
    # ejecutar un paso de la simulacion
    t, temp, amb, pert, error, state = sim.step()

    # calcular escala y eje de tiempo una sola vez
    minutes = t / SCALE
    minutes_axis = np.arange(int(t)) / SCALE

    # re setear los datos a los graficos con los resultados de la nueva iteracion
    line_theta_o.set_data(minutes_axis, sim.temps)
    line_theta_i.set_data(minutes_axis, sim.ambs)
    line_theta_p.set_data(minutes_axis, sim.perts)
    line_error.set_data(minutes_axis, sim.errors)

    # actualizar las lineas horizontales de control con el valor actual del rango (interfaz grafica)
    ax_thigh_line.set_ydata([sim.params['t_high'], sim.params['t_high']])
    ax_tlow_line.set_ydata([sim.params['t_low'], sim.params['t_low']])

    # extender ejes y en cada grafico si fuese necesario
    low_t  = min(temp, amb, sim.params['t_low'],  sim.params['t_high']) - 1
    high_t = max(temp, amb, sim.params['t_low'],  sim.params['t_high']) + 1
    extend_axis(ax_temp, low_t, high_t)

    low_p  = pert - 0.5
    high_p = pert + 0.5
    extend_axis(ax_pert, low_p, high_p)

    low_e  = error - 0.2
    high_e = error + 0.2
    extend_axis(ax_error, low_e, high_e)

    # extender eje x de tiempo
    ax_temp.set_xlim(0, minutes)
    ax_error.set_xlim(0, minutes)
    ax_pert.set_xlim(0, minutes)

    # actualizar textos de leyendas con valores actuales
    texts_temp = leg_temp.get_texts()
    texts_temp[0].set_text(f"\u03F4o: {temp:.2f} °C")
    texts_temp[1].set_text(f"\u03F4i: {amb:.2f} °C")

    texts_pert = leg_pert.get_texts()
    texts_pert[0].set_text(f"\u03F4p: {pert:.2f} °C")

    texts_error = leg_error.get_texts()
    texts_error[0].set_text(f"e: {error:.3f} °C")

    text_actu.set_text(f"Estado: {state}")

    return line_theta_o, line_theta_i, line_theta_p, line_error

is_running = [True] # permite que se pueda modificar este valor dentro de las funciones de eventos de interfaz grafica
ani = FuncAnimation(fig, update, interval=33.33, blit=False, cache_frame_data=False)

# Eventos de interfaz grafica
def on_t_amb(event):
    sim.params['t_amb'] = sld_t_amb.val
sld_t_amb.on_changed(on_t_amb)

def on_t_pert(event):
    sim.params['t_pert'] = sld_t_pert.val
sld_t_pert.on_changed(on_t_pert)

def on_t_ctrl(event):
    sim.params['t_low'] = rsld_temp_ctrl.val[0]
    sim.params['t_high'] = rsld_temp_ctrl.val[1]
rsld_temp_ctrl.on_changed(on_t_ctrl)

def on_check_actu(event):
    sim.params['actuadores_on'] = check_actu.get_status()[0]
check_actu.on_clicked(on_check_actu)

def on_defaults(event):
    sld_t_amb.reset()
    sld_t_pert.reset()
    rsld_temp_ctrl.reset()
    check_actu.set_active(0, True)
    sim.reset()
    btn_toggle.label.set_text('Start')
    ani.event_source.stop()
    is_running[0] = False
btn_defaults.on_clicked(on_defaults)

def event_toggle(event):
    if is_running[0]:
        ani.event_source.stop()
        btn_toggle.label.set_text('Start')
    else:
        ani.event_source.start()
        btn_toggle.label.set_text('Stop')
    is_running[0] = not is_running[0]
def on_reset(event):
    ani.event_source.stop()
    sim.reset()
    btn_toggle.label.set_text('Start')
    is_running[0] = False
btn_toggle.on_clicked(event_toggle)
btn_reset.on_clicked(on_reset)

plt.show()
