
#   set number of repeated measurements
#  -     measure voltages 
#   -    calculate voltage LED
#     -  calculate current LED
# -  calculate average voltage LED and uncertainty
#  - calculate average current LED and uncertainty
#   print average voltage: average_voltage_LED +/- err_average_voltage_LED V  average current: average_current_LED +/- err_average_current_LED A
#
# -turn LED off
# -create csv-file
# -plot average_current_LED vs average_voltage_LED

import pyvisa
import matplotlib.pyplot as plt
import math 
import csv

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource("ASRL/dev/cu.usbmodem14101::INSTR", read_termination="\r\n", write_termination="\n")

list_voltages = []
list_voltages_led =[]
list_I_led = [] 
list_voltages_resistor =[]
list_raw_led = []
list_raw_resistor = []

#mean determination 
def statistics(list): 
    N = len(list) 
    x_oud =0 

    for x in list:
        total = x + x_oud
        x_oud = total 

    mean_x = (1/N) * total 

    _oud = 0 

    for y in list: 
        _ = (y - mean_x)**2
        total_ = _ + _oud 
        _oud = total_

    rho = math.sqrt(total_/N)

    return mean_x, rho

def U_I_determination(i): 

    voltage = device.query(f"OUT:CH0:VOLT {i/10}")

    raw_1 = device.query(f"MEAS:CH1?")
    raw_2 = device.query(f"MEAS:CH2?")

    raw_voltage_LED = float(raw_1) - float(raw_2)
    raw_voltage_resistor = float(raw_2)

    U_1 = float(device.query("MEAS:CH1?")) * (3.3/1024)# measure voltage at channel 1 = voltage u1 (parallel to LED+resistor)
    U_2 = float(device.query("MEAS:CH2?")) * (3.3/1024) # measure voltage at channel 2 = voltage resistor 

    U_LED = U_1 - U_2
    I_LED = (U_2/220) * 1000  #with resistance of 220 Ohm 

        #print(f"U LED = {U_LED} V")
        #print(f"I LED = {I_LED} mA")
    return voltage, U_LED, I_LED, U_2


for i in range (0, 34, 1):

    voltage_, U_LED, I_LED, U_2 = U_I_determination(i)
    
    list_voltages.append(float(voltage_)) #add voltage to list
    list_voltages_led.append(U_LED) #add voltage LED to list
    list_I_led.append(I_LED)
    list_voltages_resistor.append(U_2) #add voltage resistor to list

list_all_U_ = []
list_all_I_ = [] 

#Now lets find the mean values and errors

N_repeat = 2


for j in range (0, 34, 1): #voltage changes from 0 to maximum value 
    results_U =[]
    results_I=[] 

    for m in range (N_repeat): #each step will be repeated -N_repeat- times 
        _voltage, _U, _I, _U_2 = U_I_determination(j)
        results_U.append(_U)
        results_I.append(_I)

    list_all_U_.append(results_U)
    list_all_I_.append(results_I) 

f_U =[]
f_I = []

list_mean_U = []
list_mean_I = [] 

for n in range (0, 34, 1):

    U_mean, U_f = statistics(list_all_U_[n])
    list_mean_U.append(U_mean)
    f_U.append(U_f)

    I_mean, I_f = statistics(list_all_I_[n])
    list_mean_I.append(I_mean)
    f_I.append(I_f)


#afwijking van gem

def flags(list_f_U, list_f_I):

    error_U =[]
    error_I = []
    for k, l in zip(list_f_U, list_f_I):

        div_s_U = k / (math.sqrt(N_repeat))
        div_s_I = l / (math.sqrt(N_repeat))

        
        error_U.append(div_s_U)
        error_I.append(div_s_I)

    return error_U, error_I

err_U, err_I = flags(f_U, f_I)


with open("U_I_LED_with_errors.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)
    writer.writerow(["voltage [V]", "current[A]"])

    for U_mean_csv, I_mean_csv, err_U_csv, err_I_csv in zip(list_mean_U, list_mean_I, err_U, err_I):
        print(f"Avarage voltage = {U_mean_csv} +/- {err_U_csv}, Avarage current {I_mean_csv} +/- {err_I_csv}")
    
        writer.writerow([U_mean_csv, err_U_csv, I_mean_csv, err_I_csv])
...
    # na dit blok sluit Python automatisch het bestand

#plt.errorbar(list_voltages_led, list_I_led, xerr=f_U, yerr=f_I, fmt='o', color='red')
plt.errorbar(list_mean_U, list_mean_I, xerr=err_U, yerr=err_I, fmt='o', color='red', markersize = 4)

plt.xlabel("avarage U (LED) [V]")
plt.ylabel("avarage I (LED) [mA]")

plt.savefig("IU-LED_avarage.png")

device.query("OUT:CH0:VOLT 0") #set voltage back to 0