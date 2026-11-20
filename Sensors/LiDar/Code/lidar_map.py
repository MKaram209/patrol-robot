import math
import serial
import matplotlib.pyplot as plt

PORT = 'COM6'
BAUD = 230400

MAX_RANGE_MM = 4000      # plot radius (LD06 reaches ~12000, 4000 is easier to see)
MIN_INTENSITY = 10       # drop weak, noisy points (raise if you see ghost dots)
USE_CRC = True           # set False if good packets drop to 0 (see notes)


def crc8(data):
    # CRC-8, polynomial 0x4D, init 0, no reflection
    # (written from memory of the LD06 manual, verify against your datasheet)
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


def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)

    plt.ion()
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    scatter = ax.scatter([], [], s=4, c='lime')
    ax.set_xlim(-MAX_RANGE_MM, MAX_RANGE_MM)
    ax.set_ylim(-MAX_RANGE_MM, MAX_RANGE_MM)
    ax.set_aspect('equal')
    ax.tick_params(colors='gray')
    ax.grid(color='#333333')
    ax.plot(0, 0, 'r^')   # the lidar, pointing up = 0 degrees
    ax.set_title("LD06 scan (up = straight ahead, units = mm)", color='white')

    buffer = bytearray()
    xs, ys = [], []
    last_start = 0.0

    try:
        while plt.fignum_exists(fig.number):
            chunk = ser.read(ser.in_waiting or 1)
            buffer.extend(chunk)

            while True:
                idx = buffer.find(b'\x54\x2c')
                if idx == -1:
                    # keep the last byte in case it is a split header
                    if len(buffer) > 1:
                        del buffer[:-1]
                    break
                if idx > 0:
                    del buffer[:idx]
                if len(buffer) < 47:
                    break

                packet = bytes(buffer[:47])

                if USE_CRC and crc8(packet[:46]) != packet[46]:
                    del buffer[:1]   # false header, resync
                    continue

                del buffer[:47]
                start_angle, points = decode_packet(packet)

                # angle wrapped around: one full rotation finished, draw it
                if start_angle < last_start and xs:
                    scatter.set_offsets(list(zip(xs, ys)))
                    fig.canvas.draw_idle()
                    plt.pause(0.001)
                    xs, ys = [], []
                last_start = start_angle

                for angle, dist, intensity in points:
                    if dist == 0 or dist > MAX_RANGE_MM:
                        continue
                    if intensity < MIN_INTENSITY:
                        continue
                    a = math.radians(angle)
                    xs.append(dist * math.sin(a))
                    ys.append(dist * math.cos(a))
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()


if __name__ == "__main__":
    main()
