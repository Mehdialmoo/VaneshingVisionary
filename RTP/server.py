# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

import UdpComms as U
import socket
import time
import test
hostname = socket.gethostname()
ipaddress = socket.gethostbyname(socket.gethostname())
# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP=ipaddress, portTX=12345, portRX=12346, enableRX=True, suppressWarnings=True)


i = 0

while True:
    sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application
    i += 1

    data = sock.ReadReceivedData() # read data

    if data != None: # if NEW data has been received since last ReadReceivedData function call
        print(data) # print new received data

    time.sleep(1)