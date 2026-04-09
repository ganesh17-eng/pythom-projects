import serial
import csv
import time

PORT = "COM3"
BAUD = 9600

def main():
    arduino = connect()
    if not arduino:
        return
    
    setup()

    try:
        current_state = None
        while True:
            row = arduino.readline()
            line = row.decode("utf-8").strip()

            if line:
                value = parse(line)
                if value is not None:
                    print("...")
                    csv_save(value)
                    if value <= 8:
                        new_state = b'1'        #sends 1 in bytes
                    else:
                        new_state = b'0'
                    
                    if new_state != current_state:
                        arduino.write(new_state)
                        current_state = new_state

    except KeyboardInterrupt:
        arduino.close()



def connect():
    try:
        arduino = serial.Serial(PORT, BAUD, timeout=2)
        time.sleep(2)
        print(f"Connected to Arduino on {PORT}")
        return arduino
    except serial.SerialException:
        print("Cannot connect to Arduino")
        return None


def setup():
    with open("sound.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Distance"])

def csv_save(value):
    with open("sound.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([value])

def parse(line):
    try:
        value = float(line)
        if value <= 0:
            return None
        
        return value
    except:
        return None

main()
