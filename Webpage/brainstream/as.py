import serial
serial_port = serial.Serial('COM3', baudrate=115200)
serial_port.timeout = None    
while True:
    data = serial_port.readline().decode('utf-8', errors="ignore").strip()
    ndata = [s for s in data if s != '\x00']
    ndata = ''.join(ndata)
    ndata = ndata.split('\t')
    try:
        ndata = ndata
    except ValueError:
        ndata = 0
    print(ndata)