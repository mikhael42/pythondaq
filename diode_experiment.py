# connect to Arduino
# set output voltage from 0 to max
#   measure voltages
#   calculate voltage LED
#   calculate voltage resistor
#   print LED: raw_voltage_LED (voltage_LED V) Resistor: raw_voltage_resistor (voltage_resistor V)

import pyvisa
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem14101::INSTR", read_termination="\r\n", write_termination="\n"
)

#FOR VOLTAGE == 0

voltage = device.query("OUT:CH0:VOLT 0")
U_1 = device.query("MEAS:VOLT? CH1") # measure voltage at channel 1 - voltage U1 (parallel to LED+resistor)
U_2 = device.query("MEAS:VOLT? CH2") # measure voltage at channel 2 - voltage resistor (= voltage U2)

U_LED = float(U_1) - float(U_2)
print(f"LED: {U_LED} V, Resistor: {U_2} V")

#range of voltages

#list_voltages = []
#list_voltages_led =[]
#list_voltages_resistor =[]

#for i in range (0, 34, 1):
    #voltage = device.query(f"OUT:CH0:VOLT {i/10}")

    #raw_1 = device.query(f"MEAS:CH1?")
    #raw_2 = device.query(f"MEAS:CH2?")

    #raw_voltage_LED = float(raw_1) - float(raw_2)
    #raw_voltage_resistor = float(raw_2)

    #U_1 = device.query("MEAS:VOLT? CH1") # measure voltage at channel 1 - voltage u1 (parallel to LED+resistor)
    #U_2 = device.query("MEAS:VOLT? CH2") # measure voltage at channel 2 - voltage resistor 

    #U_LED = float(U_1) - float(U_2)

    #list_voltages.append(voltage)
    #list_voltages_led.append(U_LED)
    #list_voltages_resistor.append(float(U_2))

#plt.plot(list_voltages, list_voltages_led, color='red')
#plt.xlabel("Voltage (total) [V]")
#plt.ylabel("Voltage (LED) [V]")
#plt.savefig("voltage_led.png")