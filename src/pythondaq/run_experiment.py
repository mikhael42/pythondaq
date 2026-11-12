import csv

import matplotlib.pyplot as plt

from pythondaq.arduino_device import (  # import of classes from arduino devise file
    ArduinoVISADevice,
    list_resources,
)
from pythondaq.diode_experiment_4 import (
    DiodeExperiment,  # import needed class from diode_experiment
)

# diode_experiment_4 is a version of the original diode_experiment, but updated to fit new exercise
device = ArduinoVISADevice(port="ASRL/dev/cu.usbmodem14101::INSTR")
experiment = DiodeExperiment()

list_mean_U, list_mean_I, err_U, err_I = experiment.errors(3)

with open("final_U_I_LED_with_errors.csv", "w", newline="") as csvfile:
    """this section of the code makes a csv file and adds all the mean values of current and voltage together with uncertainties in one csv file
    """

    writer = csv.writer(csvfile)
    writer.writerow(["voltage [V]", "error voltage [V]", "current [mA]", "error current [mA]"])
    for U_mean_csv, I_mean_csv, err_U_csv, err_I_csv in zip(list_mean_U, list_mean_I, err_U, err_I):
        writer.writerow([U_mean_csv, err_U_csv, I_mean_csv, err_I_csv])

    # na dit blok sluit Python automatisch het bestand
# print identification string
print(list_resources())
identification = device.get_identification()
print(identification)

# after that it's time to plot our data
plt.errorbar(list_mean_U, list_mean_I, xerr=err_U, yerr=err_I, fmt="o", color="red", markersize=2)

plt.xlabel("avarage U (LED) [V]")
plt.ylabel("avarage I (LED) [mA]")
# plt.show()
plt.savefig("IU-LED_final_run_experiment_result.png")
# turn off the LED

device.set_output_voltage(voltage=0)
