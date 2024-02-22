import serial
import csv
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import time
from threading import Thread

# Open serial connection to Arduino
ser = serial.Serial('/dev/tty.usbmodem143101', 9600)  # Update the port as per your Raspberry Pi's configuration

# Initialize dictionary to store sensor readings
sensor_data = defaultdict(list)

# Generate unique filename based on current date and time
current_datetime = time.strftime('%Y-%m-%d_%H-%M-%S')
csv_filename = f'sensor_data_{current_datetime}.csv'

# Create CSV file to store data
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Time", "MQ8", "MQ4", "MQ9", "MQ7", "MQ135"])

# Initialize time for downsampling and live plotting
start_time = time.time()
plot_interval = 2  # Update plot every 6 seconds
plot_data = defaultdict(list)

# Function to read serial data
def read_serial():
    while True:
        line = ser.readline().decode().strip()
        readings = line.split(",")
        for reading in readings:
            sensor, value = reading.split(":")
            value = int(value)
            plot_data[sensor].append((time.time(), value))
            sensor_data[sensor].append(value)

# Function to write data to CSV
def write_csv():
    while True:
        time.sleep(60)  # Wait for one minute
        avg_values = [sum(sensor_data[sensor]) / len(sensor_data[sensor]) for sensor in sensor_data.keys()]
        csv_writer.writerow([start_time, *avg_values])
        csv_file.flush()

# Start threads for reading serial data and writing to CSV
serial_thread = Thread(target=read_serial)
csv_thread = Thread(target=write_csv)
serial_thread.daemon = True  # Daemonize threads so they exit when the main program exits
csv_thread.daemon = True
serial_thread.start()
csv_thread.start()

# Main loop for plotting data
try:
    while True:
        time_now = time.time()
        if time_now - start_time >= plot_interval:
            plt.clf()
            for sensor, data in plot_data.items():
                times, values = zip(*data)
                plt.plot(times, values, label=sensor)
            plt.xlabel('Time')
            plt.ylabel('Sensor Value')
            plt.legend()
            plt.pause(0.05)
            start_time = time_now

        # Check if 24 hours have passed and clear plot_data
        if time_now - start_time >= 24*3600:
            plot_data.clear()
            start_time = time_now

except KeyboardInterrupt:
    ser.close()
    csv_file.close()
    print("Serial connection closed.")
