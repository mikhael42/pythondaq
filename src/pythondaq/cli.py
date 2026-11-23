import csv

import click
import numpy as np

from pythondaq.arduino_device import (  # import of classes from arduino devise file
    ArduinoVISADevice,
    list_resources,
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
    list_ind = list_resources() 
    return list_ind

@cmd_group.command()

@click.argument("port_")

def info(port_):
    device = ArduinoVISADevice(port=port_)
    print(device.get_identification())

@cmd_group.command()
@click.argument("port__")
@click.option("-o", "--output")
@click.option("-ra", "--range_", type=float)
@click.option("-re", "--repeat", type=int, default=1)
@click.option("-st","--steps",type=float, default=0.1)


def scan(port__, output, range_, repeat, steps):
    device = ArduinoVISADevice(port=port__)

    list_mean_U=[]
    list_mean_I=[]
    list_std_U=[]
    list_std_I=[]

    for j in np.arange(0, range_, steps):
        device.set_output_voltage(j)  # we are setting a certan V
        list_U = []
        list_I = []

        for n in range(repeat): 
            U_1 = device.get_input_voltage(channel=1)  # we determine U in channel 1
            U_2 = device.get_input_voltage(channel=2)  # we determine U in channel 2
    
            value_U = U_1 - U_2
            value_I = (U_2 / 220) *1000 # with resistance of 220 Ohm, and current is low, so multiply by 1000
   
            list_U.append(value_U)
            list_I.append(value_I)

        mean_U = np.mean(list_U)
        mean_I = np.mean(list_I)
        std_U = np.std(list_U)
        std_I =np.std(list_I)

        list_mean_U.append(mean_U)
        list_mean_I.append(mean_I)
        list_std_U.append(std_U)
        list_std_I.append(std_I)
    
    error_U = []
    error_I = []

    for std_U_, std_I_ in zip(list_std_U, list_std_I):

        div_s_U = std_U_ / (np.sqrt(repeat))
        div_s_I = std_I_ / (np.sqrt(repeat))

        error_U.append(div_s_U)
        error_I.append(div_s_I)
        
    with open(f"{output}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["voltage [V]", "error voltage [V]", "current [mA]", "error cirrent [mA]"])
        for U_mean, err_U, I_mean, err_I in zip(list_mean_U, error_U, list_mean_I, error_I):
            writer.writerow([U_mean, err_U, I_mean, err_I])

    device.set_output_voltage(voltage=0)

if __name__ == "__main__":
    cmd_group()
