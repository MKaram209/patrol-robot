# OKdo LiDAR HAT (LD19) for Raspberry Pi 4B

Quick-reference notes for setting up and running the OKdo LiDAR HAT.

- **Driver & scripts (OKdo GitHub):** https://github.com/LetsOKdo/ld19
- **Pi 4 basic kit setup guide:** https://www.okdo.com/gettingstarted/get-started-with-okdo-pi-4-basic-kit/

The LiDAR uses a low-power infrared laser (Class 1 certified), a serial interface, and PWM motor control. It depends on ROS (Robot Operating System), installed via the scripts below.

## 1. Prepare the Pi

- Set up Raspberry Pi OS (full desktop version recommended) with internet access (Ethernet or Wi-Fi). OS updates can be skipped during setup.
- Do this **before** fitting the HAT.

## 2. Install ROS (~2h 15m)

```bash
cd
curl https://raw.githubusercontent.com/LetsOKdo/ld19/master/lidar_ros_setup.sh | bash
```

Build progress is shown in the Terminal title (e.g. `[179 of 187]`). When finished, reboot and test:

```bash
roscore      # Ctrl+C to exit
```

## 3. Enable serial

*Preferences > Raspberry Pi Configuration > Interfaces*

- Serial Port: **Enabled**
- Serial Console: **Disabled**

Reboot when prompted, then shut down and disconnect power.

## 4. Attach the LiDAR

With the Pi **powered off**, fit the module to the bracket, place the unit with the cutout over the GPIO header, and secure it. Connect the cable as below (note: the colours are **not** conventional):

| LiDAR Pin  | Raspberry Pi Pin | Colour | Min | Typical | Max  |
|------------|------------------|--------|-----|---------|------|
| 1 (TX)     | Pin 10 (RXD)     | White  | 0V  | 3.3V    | 3.5V |
| 2 (PWM)    | Pin 12 (PWM0)    | Yellow | –   | –       | 3.3V |
| 3 (GND)    | Pin 6 (GND)      | Red    | 0V  | 0V      | –    |
| 4 (P5V)    | Pin 4 (5V)       | Blue   | 5V  | 5V      | 5.5V |

Double-check the connector alignment before powering on.

## 5. Install the driver

Power on the Pi. The LiDAR head should spin up with a rotating blue LED.

```bash
cd
curl https://raw.githubusercontent.com/LetsOKdo/ld19/master/lidar_driver_setup.sh | bash
```

Reboot, then launch the driver:

```bash
cd ~/ld06
source devel/setup.bash
roslaunch ldlidar ld19.launch
```

Leave this Terminal running.

> **Driver errors?** Check that the Serial Console is disabled in Raspberry Pi Configuration.

## 6. Visualise with RViz

In a **new** Terminal:

```bash
rosrun rviz rviz
```

Then *File > Open Config* and select `ldlidar.rviz` from `~/ld06/rviz`. The room should appear on the 2D grid in real time (topic: `/LIDAR/LD19`).

## 7. Shutting down

1. Close RViz.
2. `Ctrl+C` in the driver Terminal.
3. Safely shut down the Pi.
4. Disconnect power to stop the LiDAR.
