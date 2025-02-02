from Spline import Spline

class PulseGenerator():
    @micropython.native
    def __init__(self, time_resolution:int = 10, vhigh:float = 1.0, factor:float = 1.0):
        """
        TODO
        """
        # all units in [ns] and [V]
        if time_resolution < 6:
            raise Exception("Error: time_resolution too small.")
        self.time_resolution = time_resolution
        self.frequency = 1_000_000_000 / self.time_resolution
        self.max_points = 4096
        self.points_per_ns = 1 / self.time_resolution
        self.set_calibration(output_voltage_at_minimal_gain=vhigh, calibration_factor=factor)
        self.set_offset(offset=3.3)
        # caching
        self.pulse_constant = []
        self.total_pulse_duration = 0
        self.pulse = []
        # coefficients for spline interpolation
        self.coefficients = None
        self.grid_hat = None

    @micropython.native
    def get_points_per_ns(self):
        return self.points_per_ns

    @micropython.native
    def calculate_pulse_number_of_points(self, total_pulse_duration:int) -> int:
        """
        TODO
        """
        pulse_number_of_points = int(total_pulse_duration / self.time_resolution)
        if pulse_number_of_points > self.max_points:
            return self.max_points
        return pulse_number_of_points

    @micropython.native
    def calibration_pulse(self) -> list[int]:
        high = int((0) * self.points_per_volt)
        low = int((0 - self.offset) * self.points_per_volt)
        pulse = [high] * 1000 + [low] * 1000
        return pulse

    @micropython.native
    def set_offset(self, offset:float):
        """
        TODO
        """
        self.offset = offset
        self.gain = self.offset / self.output_voltage_at_minimal_gain
        voltage_resolution = 4096
        self.points_per_volt = int(self.calibration_factor * voltage_resolution / self.gain)

    @micropython.native
    def set_calibration(self, output_voltage_at_minimal_gain:float, calibration_factor:float):
        self.output_voltage_at_minimal_gain = output_voltage_at_minimal_gain
        self.calibration_factor = calibration_factor

    @micropython.native
    def get_frequency(self):
        """
        TODO
        """
        return self.frequency

    @micropython.native
    def get_max_points(self):
        """
        TODO
        """
        return self.max_points

    @micropython.native
    def pulse_from_config(self, ps_config:list[list[float]], padding:bool = False) -> list[int]:
        """
        TODO
        """
        pulse = []
        for point in ps_config:
            t = point[0]
            v = point[1] - self.offset
            n = int(t * self.points_per_ns)
            value = int(v * self.points_per_volt)
            pulse += [value] * n
        # padding with last value
        if padding:
            length = len(pulse)
            if length < self.max_points:
                last_value = pulse[-1]
                pulse += [last_value] * (self.max_points - length)
        # sanity check
        if len(pulse) > self.max_points:
            raise Exception("Erroneous pulse config: pulse too large.")
        return pulse

    @micropython.native
    def pulse_from_spline(self, xpoints:list[int], ypoints:list[float], padding:bool = False) -> list[int]:
        if len(xpoints) != len(ypoints):
            raise Exception("xpoints and ypoints have different lengths.")
        tpoints = [0] * len(xpoints)
        vpoints = [0] * len(xpoints)
        for i in range(len(xpoints)):
            tpoints[i] = int(xpoints[i] * self.points_per_ns)
            vpoints[i] = int((ypoints[i] - self.offset) * self.points_per_volt)
        a = tpoints[0]
        b = tpoints[-1]
        if a == b:
            return vpoints
        #print(f"frequency = {self.frequency}")
        #print(f"tpoints = {tpoints}")
        #print(f"vpoints = {vpoints}")
        #print(f"a = {a}")
        #print(f"b = {b}")
        #self.coefficients = Spline.cal_coefs(a, b, vpoints)
        self.grid_hat = Spline.calc_grid(a, b, b - a) # grid with step size one
        #self.pulse = list([int(Spline.interpolate(x, a, b, self.coefficients)) for x in self.grid_hat])
        self.pulse = Spline.pchip_interpolate(tpoints, vpoints, self.grid_hat)
        self.pulse = list(map(int, self.pulse))
        #print(f"offset = {self.offset}")
        #print(f"points_per_volt = {self.points_per_volt}")
        #print(f"points_per_ns = {self.points_per_ns}")
        return self.pulse

    @micropython.native
    def pulse_from_lambda(self, ps_lambda, total_pulse_duration:int, padding:bool = False) -> list[int]:
        """
        TODO
        """
        if self.total_pulse_duration != total_pulse_duration:
            pulse_number_of_points = self.calculate_pulse_number_of_points(total_pulse_duration)
            self.pulse = [0] * pulse_number_of_points
        t = 0
        dt = self.time_resolution
        for i in range(pulse_number_of_points):
            self.pulse[i] = int((ps_lambda(t) - self.offset) * self.points_per_volt)
            t += dt
        # padding with last value
        if padding:
            if pulse_number_of_points < self.max_points:
                last_value = self.pulse[-1]
                self.pulse += [last_value] * (self.max_points - pulse_number_of_points)
        return self.pulse

    @micropython.native
    def pulse_from_list(self, pulse:list[int], padding:bool = False) -> list[int]:
        """
        Puls is generated from raw list without offset or gain correction applied.
        """
        # padding with last value
        if padding:
            length = len(pulse)
            if length < self.max_points:
                last_value = pulse[-1]
                pulse += [last_value] * (self.max_points - length)
        # sanity check
        if len(pulse) > self.max_points:
            raise Exception("Fatal error: pulse too large.")
        return pulse

    @micropython.native
    def predefined_pulse1_constant(self, vstart:float, tramp:int, vstep:float, tstep:int):
        """
        TODO
        """
        # this part of the pulse must be calculated only once and can be stored
        pulse_constant = []
        if tramp > 0:
            # trunk-ignore(ruff/E731)
            ramp_lambda = lambda t: (vstep - vstart) / tramp * t + vstart
            nramp = self.calculate_pulse_number_of_points(tramp)
            ramp = [0] * nramp
            t = 0
            dt = self.time_resolution
            for i in range(nramp):
                ramp[i] = int((ramp_lambda(t) - self.offset) * self.points_per_volt)
                t += dt
            pulse_constant += ramp
        nstep = int(tstep * self.points_per_ns)
        value = int((vstep - self.offset) * self.points_per_volt)
        pulse_constant += [value] * nstep
        self.pulse_constant = pulse_constant

    @micropython.native
    def predefined_pulse1(self, vstart:float, tramp:int, vstep:float, tstep:int, length:int, vend:float, recalc_constant:bool = False, padding:bool = False) -> list[int]:
        """
        TODO
        """
        if self.pulse_constant == [] or recalc_constant:
            self.predefined_pulse1_constant(vstart, tramp, vstep, tstep)
        pulse = self.pulse_constant.copy()
        nlength = int(length * self.points_per_ns)
        pulse += [int((0 - self.offset) * self.points_per_volt)] * nlength
        pulse += [(int((vend - self.offset) * self.points_per_volt))]
        # padding with last value
        if padding:
            length = len(pulse)
            if length < self.max_points:
                last_value = pulse[-1]
                pulse += [last_value] * (self.max_points - length)
        # sanity check
        if len(pulse) > self.max_points:
            raise Exception("Error: pulse too large.")
        return pulse

    @micropython.native
    def pulse_from_predefined(self, ps_config:dict, recalc_const:bool = False, padding:bool = False) -> list[int]:
        """
        TODO
        """
        pulse = []
        if ps_config["psid"] == 1:
            if self.pulse_constant == [] or recalc_const:
                pulse = self.predefined_pulse1(ps_config["vstart"], ps_config["tramp"], ps_config["vstep"], ps_config["tstep"], ps_config["length"], ps_config["vend"], True, padding)
            else:
                pulse = self.predefined_pulse1(0.0, 0, 0.0, 0, ps_config["length"], ps_config["vend"], False, padding)
        return pulse