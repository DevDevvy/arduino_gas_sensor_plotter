# Gas Sensor Interface For Arduino Project

## Description

This Python script interfaces with an Arduino board (I used the Due) equipped with 5 gas sensors, namely MQ8, MQ4, MQ9, MQ7, and MQ135. It reads sensor data from the Arduino via serial communication, writes the data to a CSV file, and provides live plotting of the data using matplotlib. The script employs threading to ensure smooth operation, with one thread dedicated to reading serial data and another thread handling CSV writing. Live plotting is done in the main thread, while periodically clearing plot data to prevent excessive memory usage.

## Getting Started

To use this project, follow these steps:

1. **Arduino Setup:**

   - Obtain the [Arduino code](https://github.com/DevDevvy/arduino_gas_sensor_code) for interfacing with the gas sensors.
   - Load the Arduino code into the Arduino board.
   - Set up the gas sensors with the Arduino board.

2. **Python Setup:**

   - Clone this repository to your local machine.

3. **Dependencies:**

   - Install the required Python libraries using pip:
     ```
     pip install pandas matplotlib
     ```

4. **Run the Script:**
   - Update the serial port in the script to match your Arduino's configuration.
   - Run virtual environment:
     ```
     python3 -m venv venv
     ```
     ```
     source venv/bin/activate
     ```
   - Run the Python script `read_sensors.py`.
5. **Viewing Data:**
   - The script will generate a CSV file named `sensor_data_<timestamp>.csv`, containing sensor readings.
   - Live plotting of the data will be displayed in a matplotlib window.
   - The live chart will update every 2 seconds, and data will be written to the CSV file every 60 seconds.

## License

This project is licensed under the [MIT License](LICENSE).
