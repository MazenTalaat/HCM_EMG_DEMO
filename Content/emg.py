import asyncio
import qtm_rt
import socket
import math


def on_packet(packet):
    global conn
    global counter
    global emg1
    global emg2
    global emg3
    global emg4
    header, signal = packet.get_analog_single()
    try:
        # print("Sending: " + str(int(signal[0][1][0][0])) + ',' + str(int(signal[0][1][0][4])) + ','
        #   + str(int(signal[0][1][0][8])) + ',' + str(int(signal[0][1][0][12])))
        if counter == 5:
            conn.sendall(bytes(
                 str(int(math.sqrt(emg1 / counter))) + ',' + str(int(math.sqrt(emg2 / counter))) + ','
                 + str(int(math.sqrt(emg3 / counter))) + ',' + str(int(math.sqrt(emg4 / counter))), "utf-8"))
            print("Sending: " + str(int(math.sqrt(emg1 / counter))) + ',' + str(int(math.sqrt(emg2 / counter))) + ','
                   + str(int(math.sqrt(emg3 / counter))) + ',' + str(int(math.sqrt(emg4 / counter))))
            counter = 0
            emg1, emg2, emg3, emg4 = 0, 0, 0, 0
        else:
            counter += 1
            emg1 += int(signal[0][1][0][0]) ** 2
            emg2 += int(signal[0][1][0][4]) ** 2
            emg3 += int(signal[0][1][0][8]) ** 2
            emg4 += int(signal[0][1][0][12]) ** 2
    except:
        exit()


async def setup():
    global conn
    global counter
    global emg1
    global emg2
    global emg3
    global emg4
    counter = 0
    emg1, emg2, emg3, emg4 = 0, 0, 0, 0
    connection = await qtm_rt.connect("127.0.0.1")
    if connection is None:
        return
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        if conn is not None:
            break
    await connection.stream_frames(components=["analogsingle"], on_packet=on_packet)


if __name__ == "__main__":
    try:
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 9999  # Port to listen on (non-privileged ports are > 1023)

        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(0)

        asyncio.ensure_future(setup())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("exit")
