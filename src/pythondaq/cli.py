import csv

import click
import matplotlib.pyplot as plt
import numpy as np

from pythondaq.arduino_device import (  # import of classes from arduino devise file
    ArduinoVISADevice,
    list_resources,
)
from pythondaq.diode_experiment_4 import (
    DiodeExperiment,  # import needed class from diode_experiment
)

# subcommando scan with range in Volt and output CSV
# start scan with range
# print current and voltage
# if output:
# create csv


@click.group()
def cmd_group():
    """a click group of functions providing list devices and scan operation"""


@cmd_group.command()

# @click.option("-d", "--diode")
def list():
    print("Work in progress, list devices")


@cmd_group.command()
@click.argument("name")
@click.option("-r", "--range_", type=float)
def scan(name, range_):
    device = ArduinoVISADevice(port="ASRL/dev/cu.usbmodem14101::INSTR")
    list_U = []
    list_I = []
    for j in np.arange(0, range_, 0.1):
        device.set_output_voltage(j)  # we are setting a certan V
    
        U_1 = device.get_input_voltage(channel=1)  # we determine U in channel 1
        U_2 = device.get_input_voltage(channel=2)  # we determine U in channel 2
    
        value_U = U_1 - U_2
        value_I = (U_2 / 220) *1000 # with resistance of 220 Ohm, and current is low, so multiply by 1000
   
        list_U.append(value_U)
        list_I.append(value_I)

    print(list_U)
    print(list_U)

    with open(f"{name}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["voltage [V]", "current [mA]"])
        for U, I in zip(list_U, list_I):
            writer.writerow([U, I])
            
    device.set_output_voltage(voltage=0)

if __name__ == "__main__":
    cmd_group()
