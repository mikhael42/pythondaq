import csv

import click
import matplotlib.pyplot as plt

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
    """a click group of functions providing list devices and scan operation 
    """
@cmd_group.command()
# @click.argument("list")
# @click.option("-d", "--diode")
def list():
    print("Work in progress, list devices")

@cmd_group.command()
# @click.argument("scan")
# @click.option("-d", "--diode")
def scan():
    print("print Work in progress, scan LED")

if __name__ == "__main__":
    cmd_group()
