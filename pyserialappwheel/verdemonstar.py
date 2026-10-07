import serial
import pyvjoy

# Konfigurasi Serial
port = 'COM7'  # Sesuaikan dengan port Arduino Anda
baudrate = 115200

# Inisialisasi vJoy
j = pyvjoy.VJoyDevice(1)

# Inisialisasi Serial
try:
    ser = serial.Serial(port, baudrate, timeout=0.01)
    print(f"Terhubung ke {port} dengan baudrate {baudrate}")
    ser.flushInput()  # Membersihkan input buffer saat memulai
except Exception as e:
    print(f"Error: {e}")
    exit()

# Fungsi untuk mengubah nilai input (0 - 32767) ke sumbu vJoy
def set_joystick_axis(x_value, y_value):
    j.set_axis(pyvjoy.HID_USAGE_X, x_value)
    j.set_axis(pyvjoy.HID_USAGE_Y, y_value)

# Fungsi untuk mengatur tombol pada vJoy
def set_button(index, state):
    j.set_button(index, 1 if state else 0)

def main():
    try:
        while True:
            if ser.in_waiting > 0:
                try:
                    # Membaca data dari serial
                    data = ser.readline().decode('utf-8').strip()
                    steering, left_signal, right_signal, horn, hazard, lights = map(int, data.split(','))

                    # Set sumbu steering (X-axis)
                    set_joystick_axis(steering, 16383)  # Nilai default untuk Y-axis

                    # Mengatur sumbu Y berdasarkan tombol hazard dan lampu
                    if hazard == 1 and lights == 0:
                        y_axis_value = 0  # Arah negatif (bawah)
                    elif hazard == 0 and lights == 1:
                        y_axis_value = 32767  # Arah positif (atas)
                    elif hazard == 1 and lights == 1:
                        y_axis_value = 16383  # Tengah jika keduanya ditekan
                    else:
                        y_axis_value = 16383  # Tengah jika tidak ada yang ditekan

                    # Mengatur Axis Y pada vJoy
                    set_joystick_axis(steering, y_axis_value)

                    # Set tombol pada vJoy
                    set_button(1, left_signal)   # Tombol 1: Lampu sein kiri
                    set_button(2, right_signal)  # Tombol 2: Lampu sein kanan
                    set_button(3, horn)          # Tombol 3: Klakson

                    # Debugging untuk memantau input
                    #print(f"Steering: {steering}, Y-Axis: {y_axis_value}, Left: {left_signal}, Right: {right_signal}, Horn: {horn}")

                except Exception as e:
                    print(f"Error: {e}")
                    ser.flushInput()  # Flush buffer jika terjadi error

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
