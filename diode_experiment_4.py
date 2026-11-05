
import math

from arduino_device import ArduinoVISADevice


class DiodeExperiment: 
    def __init__(self):
        self.device = ArduinoVISADevice(port="ASRL/dev/cu.usbmodem14101::INSTR")

    def statistics(self, list):
        N = len(list)
        x_oud = 0

        for x in list:
            total = x + x_oud
            x_oud = total

        mean_x = total / N

        _oud = 0
        # numpy std
        for y in list:
            _ = (y - mean_x) ** 2
            total_ = _ + _oud
            _oud = total_

        rho = math.sqrt(total_ / (N - 1))

        return mean_x, rho


    def U_I_determination(self, i):

        self.device.set_output_voltage(i / 10)  # we are setting a certan V

        U_1 = self.device.get_input_voltage(channel=1)  # we determine U in channel 1
        U_2 = self.device.get_input_voltage(channel=2)  # we determine U in channel 2

        U_LED = U_1 - U_2
        I_LED = (
            U_2 / 220
        ) * 1000  # with resistance of 220 Ohm, and current is low, so multiply by 1000

        return U_LED, I_LED

    # Now lets find the mean values and errors

    def errors(self, N_repeat):
        list_all_U_ = []
        list_all_I_ = []
        
        for j in range(0, 34, 1):  # voltage changes from 0 to maximum value
            results_U = []
            results_I = []

            for m in range(N_repeat):  # each step will be repeated -N_repeat- times
                U_LED_, I_LED_ = self.U_I_determination(j)
                results_U.append(U_LED_)
                results_I.append(I_LED_)

            list_all_U_.append(results_U)  # list with all results of voltage LED for each step
            list_all_I_.append(results_I)

        f_U = []
        f_I = []

        list_mean_U = []
        list_mean_I = []

        for n in range(0, 34, 1):
            U_mean, U_f = self.statistics(list_all_U_[n])
            list_mean_U.append(U_mean)
            f_U.append(U_f)

            I_mean, I_f = self.statistics(list_all_I_[n])
            list_mean_I.append(I_mean)
            f_I.append(I_f)


        error_U = []
        error_I = []

        for k, l in zip(f_U, f_I):
            div_s_U = k / (math.sqrt(N_repeat))
            div_s_I = l / (math.sqrt(N_repeat))

            error_U.append(div_s_U)
            error_I.append(div_s_I)

        return list_mean_U, list_mean_I, error_U, error_I




