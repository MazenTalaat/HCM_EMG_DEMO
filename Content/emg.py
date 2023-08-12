import asyncio
import qtm_rt
import socket
import math
import numpy as np

def on_packet(packet):
    global conn
    global counter
    global emg1
    global emg2
    global emg3
    global emg4
    header, signal = packet.get_analog_single()
    try:
        # conn.sendall(bytes(str(int(signal[0][1][0][0])) + ',' + str(int(signal[0][1][0][4])) + ','
        #                    + str(int(signal[0][1][0][8])) + ',' + str(int(signal[0][1][0][12])), "utf-8"))
        # print("Sending: " + str(int(signal[0][1][0][0])) + ',' + str(int(signal[0][1][0][4])) + ','
        #   + str(int(signal[0][1][0][8])) + ',' + str(int(signal[0][1][0][12])))
        if counter == 20:
            conn.sendall(bytes(
                 str(int(np.sqrt(np.mean(np.array(emg1)**2)))) + ',' + str(int(np.sqrt(np.mean(np.array(emg2)**2)))) + ','
                 + str(int(np.sqrt(np.mean(np.array(emg3)**2)))) + ',' + str(int(np.sqrt(np.mean(np.array(emg4)**2)))), "utf-8"))
            print("Sending: " + str(int(np.sqrt(np.mean(np.array(emg1)**2)))) + ',' + str(int(np.sqrt(np.mean(np.array(emg2)**2)))) + ','
                 + str(int(np.sqrt(np.mean(np.array(emg3)**2)))) + ',' + str(int(np.sqrt(np.mean(np.array(emg4)**2)))))
            emg1.append(int(signal[0][1][0][0]))
            emg2.append(int(signal[0][1][0][4]))
            emg3.append(int(signal[0][1][0][8]))
            emg4.append(int(signal[0][1][0][12]))
            emg1.pop(0)
            emg2.pop(0)
            emg3.pop(0)
            emg4.pop(0)
        else:
            counter += 1
            emg1.append(int(signal[0][1][0][0]))
            emg2.append(int(signal[0][1][0][4]))
            emg3.append(int(signal[0][1][0][8]))
            emg4.append(int(signal[0][1][0][12]))

    except:
        counter = 0
        emg1, emg2, emg3, emg4 = [], [], [], []
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            if conn is not None:
                break


async def setup():
    global conn
    global counter
    global emg1
    global emg2
    global emg3
    global emg4
    counter = 0
    emg1, emg2, emg3, emg4 = [], [], [], []
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
        s.listen()

        asyncio.ensure_future(setup())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("exit")
