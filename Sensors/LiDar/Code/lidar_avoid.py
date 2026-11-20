import time
import serial

PORT = 'COM6'
BAUD = 230400

STOP_DISTANCE_MM = 300     # closer than this = obstacle
MIN_INTENSITY = 10         # ignore weak, noisy points
CONFIRM_SCANS = 2          # obstacle must be seen in this many scans in a row
STALE_SECONDS = 0.5        # no fresh scan for this long = lidar fault, stop
USE_CRC = True             # set False if good packets drop to 0

# Zones, in degrees. 0 = straight ahead, angles increase clockwise.
# If left and right are swapped on your robot, swap LEFT_ZONE and RIGHT_ZONE.
FRONT_RANGE = 30           # front = 330..360 and 0..30
RIGHT_ZONE = (30, 90)
LEFT_ZONE = (270, 330)


def crc8(data):
    # CRC-8, polynomial 0x4D, init 0 (from memory of the LD06 manual)
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x4D) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc


def decode_packet(packet):
    # returns (start_angle, [(angle, distance_mm, intensity), ...])
    start_angle = (packet[4] | (packet[5] << 8)) / 100.0
    end_angle = (packet[42] | (packet[43] << 8)) / 100.0   # bytes 42-43

    span = end_angle - start_angle
    if span < 0:
        span += 360
    step = span / 11

    points = []
    for i in range(12):
        off = 6 + i * 3
        dist = packet[off] | (packet[off + 1] << 8)
        intensity = packet[off + 2]
        angle = (start_angle + step * i) % 360
        points.append((angle, dist, intensity))
    return start_angle, points


def zone_of(angle):
    if angle <= FRONT_RANGE or angle >= 360 - FRONT_RANGE:
        return "front"
    if RIGHT_ZONE[0] < angle <= RIGHT_ZONE[1]:
        return "right"
    if LEFT_ZONE[0] <= angle < LEFT_ZONE[1]:
        return "left"
    return None


def decide(scan):
    # scan = {"front": mm or None, "left": ..., "right": ...}
    # returns a command string. Replace the print/return with motor control.
    front = scan["front"]
    if front is None or front >= STOP_DISTANCE_MM:
        return "FORWARD"

    left = scan["left"]
    right = scan["right"]
    # None means nothing seen in that zone, so treat it as wide open
    left_space = left if left is not None else 99999
    right_space = right if right is not None else 99999

    if left_space < STOP_DISTANCE_MM and right_space < STOP_DISTANCE_MM:
        return "STOP"
    return "TURN_LEFT" if left_space > right_space else "TURN_RIGHT"


def send_to_motors(command):
    # TODO: hook up your motors here (GPIO, or ser_arduino.write(...))
    print(command)


def new_scan():
    return {"front": None, "left": None, "right": None}


def main():
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print("Reading lidar on", PORT)

    buffer = bytearray()
    current = new_scan()
    last_start = 0.0
    last_scan_time = None
    close_count = 0
    last_command = None

    try:
        while True:
            chunk = ser.read(ser.in_waiting or 1)
            buffer.extend(chunk)

            while True:
                idx = buffer.find(b'\x54\x2c')
                if idx == -1:
                    if len(buffer) > 1:
                        del buffer[:-1]
                    break
                if idx > 0:
                    del buffer[:idx]
                if len(buffer) < 47:
                    break

                packet = bytes(buffer[:47])
                if USE_CRC and crc8(packet[:46]) != packet[46]:
                    del buffer[:1]
                    continue
                del buffer[:47]

                start_angle, points = decode_packet(packet)

                # a full rotation finished: decide based on it
                if start_angle < last_start:
                    last_scan_time = time.time()
                    if current["front"] is not None and current["front"] < STOP_DISTANCE_MM:
                        close_count += 1
                    else:
                        close_count = 0

                    if close_count >= CONFIRM_SCANS:
                        command = decide(current)
                    else:
                        command = "FORWARD"

                    if command != last_command:
                        send_to_motors(command)
                        last_command = command
                    print("scan:", current)
                    current = new_scan()
                last_start = start_angle

                for angle, dist, intensity in points:
                    if dist == 0 or intensity < MIN_INTENSITY:
                        continue
                    zone = zone_of(angle)
                    if zone is None:
                        continue
                    if current[zone] is None or dist < current[zone]:
                        current[zone] = dist

            # safety: no fresh scan lately means the lidar is not working
            if last_scan_time is not None and time.time() - last_scan_time > STALE_SECONDS:
                if last_command != "STOP":
                    print("LIDAR DATA STALE, STOPPING")
                    send_to_motors("STOP")
                    last_command = "STOP"

    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        send_to_motors("STOP")
        ser.close()


if __name__ == "__main__":
    main()
