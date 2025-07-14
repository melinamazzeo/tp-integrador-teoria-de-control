import numpy as np

class ThermostatSim:
    def __init__(self, params):
        self.params = params
        self.reset()

    def reset(self):
        # unpack parameters
        self.t = 0
        self.temps = []
        self.errors = []
        self.ambs  = []
        self.perts = []
        self.states = []
        # initial system temperature equals input param
        self.current_temp = self.params['t_amb']
        self.heater_on   = False
        self.cooler_on   = False

    def step(self):
        """Advance simulation by one second, update internals, return new data."""
        p = self.params
        amb = p['t_amb'] + p['t_pert']

        # passive exchange
        error = amb - self.current_temp
        infl = (amb - self.current_temp) * p['coef_amb']
        infl = np.clip(infl, -p['delta_max'], p['delta_max'])
        self.current_temp += infl

        # active control
        if p['actuadores_on']:
            if self.heater_on:
                self.current_temp += self._deltaT(p['pot_heat'] * p['eff_heat'])
            if self.cooler_on:
                self.current_temp -= self._deltaT(p['pot_cool'] * p['eff_cool'])

        # decide next state
        state = self._interpret(self.current_temp)
        self.heater_on, self.cooler_on = state[1], state[2]

        if not p['actuadores_on']:
            state = ("OFF", state[1], state[2])

        # record
        self.ambs.append(amb)
        self.perts.append(p['t_pert'])
        self.errors.append(error)
        self.temps.append(self.current_temp)
        self.states.append(state[0])
        self.t += 1
        return self.t, self.current_temp, amb, p['t_pert'], error, state[0]

    def _deltaT(self, power):
        mass = self.params['vol_room'] * self.params['dens_air']
        return power / (mass * self.params['c_air'])

    def _interpret(self, temp):
        if temp < self.params['t_low']:
            return ("CALENTADOR", True, False)
        if temp > self.params['t_high']:
            return ("REFRIGERADOR", False, True)
        return ("OFF", False, False)