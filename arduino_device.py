import pyvisa


def list_resources():
    """This function is used to identify connected arduino and provides informations about his ports 

    Returns:
        list: returns a list with all avalable output ports
    """
    rm = pyvisa.ResourceManager("@py")
    list_of_available_ports = rm.list_resources()
    return list_of_available_ports


class ArduinoVISADevice:
    """_summary_ class which contains different functions
    """
    def __init__(self, port):
        """_summary_ Device indentification. 

        Args:
            port (int): we provide information which port gives us the values we want to use in our research
        """
        self.rm = pyvisa.ResourceManager("@py")

        self.device = self.rm.open_resource(
            port,
            read_termination="\r\n",
            write_termination="\n",
        )

    def get_identification(self):
        """_summary_ this function returns a list of channels from which we can determine voltage

        Returns:
            _type_: returns a overview at it's channels 
        """
        return self.device
        # return identification string of connected device

    def set_output_value(self, value):
        """_summary_ This function returns a ADC value 

        Args:
            value (int): a certain ADS value we set on our arduino

        Returns:
            _int_: returns a ADC value at channel 0
        """
        self.raw = self.device.query(f"OUT:CH0 {value}")
        return self.raw

    #        set a value on the output channel
    #
    def set_output_voltage(self, voltage):
        """_summary_ in this function we set a certain voltage on our arduino 

        Args:
            voltage (float): voltage value we set on channel 0 

        Returns:
            float: returns a voltage we set 
        """
        self.voltage = self.device.query(f"OUT:CH0:VOLT {voltage}")
        return self.voltage

    #        set a voltage on the output channel (in Volt)
    #
    def get_output_value(self):
        """_summary_ returns ADC value at channel 0 

        Returns:
            int: ADC value at channel 0 
        """
        return self.raw

    #        return the value of the output channel
    #
    def get_output_voltage(self):
        """_summary_ returns voltage at channel 0

        Returns:
            int: voltage at channel 0 
        """
        return self.voltage

    #        return the voltage of the output channel (in Volt)
    #
    def get_input_value(self, channel):
        """_summary_ this function determines the ADC value at certain channel 

        Args:
            channel (int): the number of channel we are interested in 

        Returns:
            int: ADC value at a certain channel 
        """
        raw = self.device.query(f"MEAS:CH{channel}?")
        return raw

    #        return the value of the input channel
    #
    def get_input_voltage(self, channel):
        """_summary_ this function determines a voltage at a certain channel 

        Args:
            channel (int): channel number we want to investigate  

        Returns:
            voltage (float): voltage at this certain channel 
        """
        raw_ = self.device.query(f"MEAS:CH{channel}?")
        voltage = float(raw_) * (3.3 / 1024)
        return voltage


#        return the voltage of the input channel (in Volt)


# test code

# get available ports
print(list_resources())

# create an instance for the Arduino on port "ASRL28::INSTR"
# device = ArduinoVISADevice(port="ASRL28::INSTR")
device = ArduinoVISADevice(
    port="ASRL/dev/cu.usbmodem14101::INSTR"
)  # I use thisone because I/m using mac


# print identification string
identification = device.get_identification()
print(identification)

# set OUTPUT voltage on channel 0 in Volt (0 - 3.3 V)
response = device.set_output_voltage(voltage=3.3)
print(f"{response=}")

# set OUTPUT voltage on channel 0 in ADC values (0 - 1023)
device.set_output_value(value=828)

# measure the voltage on INPUT channel 2 in ADC values (0 - 1023)
ch2_value = device.get_input_value(channel=2)
print(f"{ch2_value=}")

# measure the voltage on INPUT channel 2 in Volt (0 - 3.3 V)
ch2_voltage = device.get_input_voltage(channel=2)
print(f"{ch2_voltage=}")

# get the previously set OUTPUT voltage on channel 0 in ADC values (0 - 1023)
ch0_value = device.get_output_value()
print(f"{ch0_value=}")

# turn of the LED
device.set_output_voltage(voltage=0)
