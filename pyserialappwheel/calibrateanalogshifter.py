import serial
import pyvjoy

# Konfigurasi Serial
print("Enter COM Number")
port = "COM" + input("COM")  # Input manual COM port
baudrate = 115200

# Inisialisasi vJoy
j = pyvjoy.VJoyDevice(1)

# Inisialisasi Serial
try:
    ser = serial.Serial(port, baudrate, timeout=0.01)
    print(f"Terhubung ke {port} dengan baudrate {baudrate}")
    ser.flushInput()
except Exception as e:
    print(f"Error: {e}")
    exit()

# Threshold X dan Y dari data kalibrasi
gear_thresholds = {
    1: {"x_min": 0, "x_max": 130, "y_min": 0, "y_max": 130},
    2: {"x_min": 0, "x_max": 130, "y_min": 600, "y_max": 700},
    3: {"x_min": 100, "x_max": 250, "y_min": 0, "y_max": 130},
    4: {"x_min": 110, "x_max": 240, "y_min": 800, "y_max": 900},
    5: {"x_min": 660, "x_max": 770, "y_min": 0, "y_max": 140},
    6: {"x_min": 680, "x_max": 1010, "y_min": 700, "y_max": 1000},
    -1: {"x_min": 1023, "x_max": 1023, "y_min": 580, "y_max": 750},  # Reverse
}

# Fungsi untuk mendeteksi gigi berdasarkan X dan Y
def detect_gear(x, y):
    for gear, t in gear_thresholds.items():
        if t["x_min"] <= x <= t["x_max"] and t["y_min"] <= y <= t["y_max"]:
            return gear
    return None  # Jika tidak sesuai threshold, tidak ada tombol yang ditekan

# Fungsi untuk mengubah nilai input (0 - 32767) ke sumbu vJoy
def set_joystick_axis(value):
    j.set_axis(pyvjoy.HID_USAGE_X, value)

# Fungsi untuk mengatur tombol pada vJoy
def set_button(index, state):
    j.set_button(index, 1 if state else 0)

# Fungsi untuk mengatur tombol gigi pada vJoy
def set_gear_button(gear):
    for i in range(1, 7):
        j.set_button(i, 0)
    j.set_button(7, 0)  # Matikan tombol Reverse (R)

    if gear is not None:
        if gear > 0:
            j.set_button(gear, 1)  # Aktifkan tombol gigi 1-6
        elif gear == -1:
            j.set_button(7, 1)  # Aktifkan tombol Reverse (R)

def main():
    try:
        while True:
            if ser.in_waiting > 0:
                try:
                    # Baca data dari serial
                    data = ser.readline().decode('utf-8').strip()
                    steering, left_signal, right_signal, horn, brake, gas, x, y, gear_mode = map(int, data.split(','))

                    # Tentukan gigi berdasarkan nilai X dan Y
                    gear = detect_gear(x, y)

                    # Set sumbu steering
                    set_joystick_axis(steering)

                    # Set tombol pada vJoy
                    set_button(8, left_signal)   # Tombol 8: Lampu sein kiri
                    set_button(9, right_signal)  # Tombol 9: Lampu sein kanan
                    set_button(10, horn)         # Tombol 10: Klakson
                    set_button(11, brake)       # Tombol 11: brake
                    set_button(12, gas)       # Tombol 12: Lampu
                    set_button(13, gear_mode)    # Tombol 13: Mode gigi

                    # Set tombol gigi
                    set_gear_button(gear)

                    #print(f"Steering: {steering}, Gear: {gear if gear is not None else 'None'}, X: {x}, Y: {y}, Mode: {gear_mode}, Left: {left_signal}, Right: {right_signal}, Horn: {horn}, brake: {brake}, gas: {gas}")

                except Exception as e:
                    print(f"Error: {e}")
                    ser.flushInput()

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
