import csv

import matplotlib.pyplot as plt

from arduino_device import ArduinoVISADevice, list_resources
from diode_experiment_4 import errors

device = ArduinoVISADevice(port="ASRL/dev/cu.usbmodem14101::INSTR")

list_mean_U, list_mean_I, err_U, err_I = errors(3)

with open("004_U_I_LED_with_errors.csv", "w", newline="") as csvfile:
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
plt.savefig("IU-LED_genious_version.png")
# turn of the LED

device.set_output_voltage(voltage=0)
