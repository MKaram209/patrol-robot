import time
import serial

PORT = 'COM6'
BAUD = 230400

STOP_DISTANCE_MM = 300
FRONT_ANGLE_RANGE = 30
PRINT_INTERVAL = 0.2


def is_front_angle(angle_deg):
    return angle_deg <= FRONT_ANGLE_RANGE or angle_deg >= 360 - FRONT_ANGLE_RANGE


def decode_packet(packet):
    # returns a list of (angle_in_degrees, distance_in_mm)
    start_angle = (packet[4] | (packet[5] << 8)) / 100.0
    end_angle = (packet[42] | (packet[43] << 8)) / 100.0   # bytes 42-43

    span = end_angle - start_angle
    if span < 0:
        span += 360
    step = span / 11

    points = []
    for i in range(12):
        off = 6 + i * 3
        distance = packet[off] | (packet[off + 1] << 8)
        angle = (start_angle + step * i) % 360
        points.append((angle, distance))
    return points


def main():
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print("Reading lidar on", PORT)

    buffer = bytearray()
    closest = None
    packets = 0
    last_print = 0

    try:
        while True:
            buffer.extend(ser.read(ser.in_waiting or 1))

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
                del buffer[:47]
                packets += 1

                for angle, dist in decode_packet(packet):
                    if dist == 0 or not is_front_angle(angle):
                        continue
                    if closest is None or dist < closest:
                        closest = dist

            now = time.time()
            if now - last_print >= PRINT_INTERVAL:
                last_print = now
                print("packets:", packets, "| closest ahead:", closest, "mm")
                if closest is not None and closest < STOP_DISTANCE_MM:
                    print(">>> OBSTACLE TOO CLOSE, TURN AWAY <<<")
                packets = 0
                closest = None

    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
