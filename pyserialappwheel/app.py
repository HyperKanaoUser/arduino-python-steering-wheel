import serial
import pyvjoy

# Konfigurasi Serial
print("Enter COM Number")
port = "COM"+input("COM")  # Sesuaikan dengan port Arduino Anda
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
def set_joystick_axis(value):
    j.set_axis(pyvjoy.HID_USAGE_X, value)

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
                    steering, left_signal, right_signal, horn, hazard, lights, shift_up, shift_down = map(int, data.split(','))

                    # Set sumbu steering (X-axis)
                    set_joystick_axis(steering)

                    # Set tombol pada vJoy
                    set_button(1, left_signal)   # Tombol 1: Lampu sein kiri
                    set_button(2, right_signal)  # Tombol 2: Lampu sein kanan
                    set_button(3, horn)          # Tombol 3: Klakson
                    set_button(4, hazard)        # Tombol 4: Hazard
                    set_button(5, lights)        # Tombol 5: Lampu
                    set_button(6, shift_up)      # Tombol 6: Shift Up
                    set_button(7, shift_down)    # Tombol 7: Shift Down

                    #print(f"Steering: {steering}, Left: {left_signal}, Right: {right_signal}, Horn: {horn}, Hazard: {hazard}, Lights: {lights}, Shift Up: {shift_up}, Shift Down: {shift_down}")
                    #print(f"Steering: {steering}, Left: {left_signal}, Right: {right_signal}, Horn: {horn}, Hazard: {hazard}, Lights: {lights}, Shift Up: {shift_up}, Shift Down: {shift_down}")

                except Exception as e:
                    print(f"Error: {e}")
                    ser.flushInput()  # Flush buffer jika terjadi error

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
