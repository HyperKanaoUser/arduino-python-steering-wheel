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
    1: {"x_min": 0, "x_max": 0, "y_min": 35, "y_max": 300},
    2: {"x_min": 0, "x_max": 0, "y_min": 790, "y_max": 840},
    3: {"x_min": 0, "x_max": 130, "y_min": 0, "y_max": 100},
    4: {"x_min": 0, "x_max": 105, "y_min": 905, "y_max": 990},
    5: {"x_min": 650, "x_max": 680, "y_min": 0, "y_max": 0},
    6: {"x_min": 660, "x_max": 1000, "y_min": 900, "y_max": 1023},
    -1: {"x_min": 1023, "x_max": 1023, "y_min": 840, "y_max": 1023},  # Reverse
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
    # Matikan semua tombol gigi sebelum menekan tombol baru
    for i in range(1, 7):
        j.set_button(i, 0)
    j.set_button(7, 0)  # Matikan tombol Reverse (R)

    if gear is not None:  # Jika gear valid, tekan tombol
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
                    steering, left_signal, right_signal, horn, hazard, lights, x, y = map(int, data.split(','))

                    # Tentukan gigi berdasarkan nilai X dan Y
                    gear = detect_gear(x, y)

                    # Set sumbu steering
                    set_joystick_axis(steering)

                    # Set tombol pada vJoy
                    set_button(8, left_signal)   # Tombol 1: Lampu sein kiri
                    set_button(9, right_signal)  # Tombol 2: Lampu sein kanan
                    set_button(10, horn)          # Tombol 3: Klakson
                    set_button(11, hazard)        # Tombol 4: Hazard
                    set_button(12, lights)        # Tombol 5: Lampu

                    # Set tombol gigi
                    set_gear_button(gear)

                    print(f"Steering: {steering}, Gear: {gear if gear is not None else 'None'}, X: {x}, Y: {y}, Left: {left_signal}, Right: {right_signal}, Horn: {horn}, Hazard: {hazard}, Lights: {lights}")

                except Exception as e:
                    print(f"Error: {e}")
                    ser.flushInput()

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
