# connect to Arduino
# set output voltage from 0 to max
#   measure voltages
#   calculate voltage LED
#   calculate voltage resistor
#   print LED: raw_voltage_LED (voltage_LED V) Resistor: raw_voltage_resistor (voltage_resistor V)

import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem14101::INSTR", read_termination="\r\n", write_termination="\n"
)

for i in range (0, 34, 1):
    voltage = device.query(f"OUT:CH0:VOLT {i/10}")

    raw_1 = device.query(f"MEAS:CH1?")
    raw_2 = device.query(f"MEAS:CH2?")

    raw_voltage_LED = float(raw_1) - float(raw_2)
    raw_voltage_resistor = float(raw_2)

    U_1 = device.query("MEAS:VOLT? CH1") # measure voltage at channel 1 - voltage u1 (parallel to LED+resistor)
    U_2 = device.query("MEAS:VOLT? CH2") # measure voltage at channel 2 - voltage resistor 

    U_LED = float(U_1) - float(U_2)

    print(f"LED: {U_LED} V, Resistor: {U_2} V")
    print(f"Raw LED: {raw_voltage_LED}, Resistor: {raw_voltage_resistor}")
