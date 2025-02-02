"""calibrate_iinput.py
This example can be used to calibrate an Interface IInput channel for voltage and/or pressure."""
import asmu

def calibrate_iinput_cV():
    interface = asmu.Interface(device = "ASIO Fireface USB",
                               analog_input_channels=[10],
                               blocksize=8192)
    calcV = asmu.analyzer.CalIInput(interface, 0.1, "V", gain = 30, averages=100)
    interface.iinput(ch = 10).connect(calcV.input())

    stream = interface.start()
    while not calcV.finished():
        pass
    stream.stop()
    print(calcV.evaluate())
    print(f"cV = {interface.iinput(ch = 10).cV}")
    print(f"fV = {interface.iinput(ch = 10).fV}")

def calibrate_iinput_cPa():
    interface = asmu.Interface(device = "ASIO Fireface USB",
                               analog_input_channels=[10],
                               blocksize=8192)
    calcV = asmu.analyzer.CalIInput(interface, 104, "SPL", gain = 30, averages=100)
    interface.iinput(ch = 10).connect(calcV.input())

    stream = interface.start()
    while not calcV.finished():
        pass
    stream.stop()
    print(calcV.evaluate())
    print(f"cPa = {interface.iinput(ch = 10).cPa}")
    print(f"fPa = {interface.iinput(ch = 10).fPa}")

if __name__ == "__main__":
    calibrate_iinput_cV()
    #calibrate_iinput_cPa()
