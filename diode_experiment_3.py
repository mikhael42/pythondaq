import csv
import math

import matplotlib.pyplot as plt

from arduino_device import ArduinoVISADevice, list_resources


# mean determination
def statistics(list):
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


device = ArduinoVISADevice(port="ASRL/dev/cu.usbmodem14101::INSTR")


def U_I_determination(i):

    device.set_output_voltage(i / 10)  # we are setting a certan V

    U_1 = device.get_input_voltage(channel=1)  # we determine U in channel 1
    U_2 = device.get_input_voltage(channel=2)  # we determine U in channel 2

    U_LED = U_1 - U_2
    I_LED = (
        U_2 / 220
    ) * 1000  # with resistance of 220 Ohm, and current is low, so multiply by 1000

    return U_LED, I_LED


list_all_U_ = []
list_all_I_ = []

# Now lets find the mean values and errors

N_repeat = 3  # we repeat measurments N_repeat times

for j in range(0, 34, 1):  # voltage changes from 0 to maximum value
    results_U = []
    results_I = []

    for m in range(N_repeat):  # each step will be repeated -N_repeat- times
        _U, _I = U_I_determination(j)
        results_U.append(_U)
        results_I.append(_I)

    list_all_U_.append(results_U)  # list with all results of voltage LED for each step
    list_all_I_.append(results_I)

f_U = []
f_I = []

list_mean_U = []
list_mean_I = []

for n in range(0, 34, 1):
    U_mean, U_f = statistics(list_all_U_[n])
    list_mean_U.append(U_mean)
    f_U.append(U_f)

    I_mean, I_f = statistics(list_all_I_[n])
    list_mean_I.append(I_mean)
    f_I.append(I_f)


# afwijking van gem
def flags(list_f_U, list_f_I):

    error_U = []
    error_I = []

    for k, l in zip(list_f_U, list_f_I):
        div_s_U = k / (math.sqrt(N_repeat))
        div_s_I = l / (math.sqrt(N_repeat))

        error_U.append(div_s_U)
        error_I.append(div_s_I)

    return error_U, error_I


err_U, err_I = flags(f_U, f_I)


with open("003_U_I_LED_with_errors.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ["voltage [V]", "error voltage [V]", "current [mA]", "error current [mA]"]
    )
    for U_mean_csv, I_mean_csv, err_U_csv, err_I_csv in zip(
        list_mean_U, list_mean_I, err_U, err_I
    ):
        writer.writerow([U_mean_csv, err_U_csv, I_mean_csv, err_I_csv])

    # na dit blok sluit Python automatisch het bestand
# print identification string

print(list_resources())

identification = device.get_identification()

print(identification)

plt.errorbar(
    list_mean_U, list_mean_I, xerr=err_U, yerr=err_I, fmt="o", color="red", markersize=2
)

plt.xlabel("avarage U (LED) [V]")
plt.ylabel("avarage I (LED) [mA]")
plt.show()
plt.savefig("IU-LED_advanced_class_version.png")
# turn of the LED

device.set_output_voltage(voltage=0)
