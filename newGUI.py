import tkinter as tk
import time
import struct
import threading
from multiprocessing import *
import socket
from tkinter import messagebox


# host = '192.168.1.107'
# port = 12571
# host = '192.168.0.101'
# port = 10004
# server_address = ('192.168.0.101', 10004)
server_address = ('149.125.118.49', 10004)
# server_address = ('10.201.10.192', 10004)
# server_address = ('192.168.1.64', 10004)
sock1 = None
# sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock1.setblocking(0)
# sock1.settimeout(10)

UDP_IP = "localhost"
UDP_PORT = 3000
MESSAGE = "Hello, World!"
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

root = tk.Tk()
root.title('Control Center')
root.geometry('2050x800')
f = open('SensorLog', 'w')

parent0_pipe, child0_pipe, = Pipe()
parent1_pipe, child1_pipe = Pipe()
parent2_pipe, child2_pipe = Pipe()
parent3_pipe, child3_pipe = Pipe()
parent4_pipe, child4_pipe = Pipe()
parent5_pipe, child5_pipe = Pipe()
parent6_pipe, child6_pipe = Pipe()
parent7_pipe, child7_pipe = Pipe()
parent8_pipe, child8_pipe = Pipe()
parent9_pipe, child9_pipe = Pipe()
parent10_pipe, child10_pipe = Pipe()
parent11_pipe, child11_pipe = Pipe()
parent12_pipe, child12_pipe = Pipe()
parent13_pipe, child13_pipe = Pipe()
parent14_pipe, child14_pipe = Pipe()
parent15_pipe, child15_pipe = Pipe()
parent16_pipe, child16_pipe = Pipe()
parent17_pipe, child17_pipe = Pipe()
parent18_pipe, child18_pipe = Pipe()
parent19_pipe, child19_pipe = Pipe()
parent20_pipe, child20_pipe = Pipe()

#temp < 60C
#Voltage(all three) 16.8V max, low 12V
#current max: 50
#actuators: still pending

MAX_AMPERAGE = 50.00                # maximum safe amperage, w
MIN_AMPERAGE = 0.00                 # minimum safe amperage, w
MIN_TEMPERATURE_AMBIENT = 10.00     # minimum safe ambient temperature reading in the pod, C
MIN_TEMPERATURE_BATTERY = 10.00     # minimum safe temperature of battery, C
MAX_TEMPERATURE_AMBIENT = 60.00     # maximum safe ambient temperature reading in the pod, C
MAX_TEMPERATURE_BATTERY = 60.00     # maximum safe temperature of battery, C
MAX_VOLTAGE = 16.80                 # maximum safe voltage, v
MIN_VOLTAGE = 12.00                 # minimum safe voltage, v


connection = False
tryConn = False
conn = None
data = None
diagram = ''
state = 1
previousState = 1
guiInput = 0
command = b'0'

unpacker = struct.Struct('1? 3I 17f')

def transferData():

    global conn, command, connection
    try:
        conn.send(command)
        command = b'0'
    except Exception as exc:
        print('The command code failed to send. Exception raised: ')
        print(exc)
        connection = False
        data.updateConnection()
        messagebox.showerror("Connection", "Connection Lost")

    try:
        packedData = conn.recv(unpacker.size)
        unpackedData = unpacker.unpack(packedData)
    except Exception as exc:
        print('The package failed to be received. Exception raised: ')
        print(exc)
        connection = False
        data.updateConnection()
        messagebox.showerror("Connection", "Connection Lost")
        # size = int(s)
        # message2 = struct.pack('i', 13)
        # conn.sendto(message2, server_address)
        # msg = str(conn.recv(size))
        # f.write(msg)
        # f.write('\n')
        # msg = conn.recv(37)
        # msg = msg.decode('utf-8')
        # msg = msg.split(',')
        # connection.sendall('0')  # transmit data from gui to spacex/
        # print('sending 0')

        # # data sent to spaceX
        # # convert data to string to be sent nicely to spacex
        # MESSAGE1 = struct.pack('BB',
        #                        69,  # team ID, given to us by space X
        #                        2)
        # MESSAGE2 = struct.pack('iiiiiiiI',
        #                        # int(dataArray[9]),
        #                        # int(dataArray[0]),
        #                        # int(dataArray[1]),
        #                        int(1),
        #                        int(2),
        #                        int(3),
        #                        0,  # zero is optional data that isn't needed
        #                        0,
        #                        0,
        #                        0,
        #                        0)
        # MESSAGE = MESSAGE1 + MESSAGE2
        # print("udp message: " + MESSAGE.decode('utf-8'))
        # # use one way udp connection to send to spacex
        # sock2.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    return unpackedData
    # else:
    #     msg = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # return msg


def count():
    global connection
    try:
        conn.send(b'0')
    except Exception as exc:
        print('The validation code failed to send. Exception raised: ')
        print(exc)
        connection = False
        data.updateConnection()
        messagebox.showerror("Connection", "Connection Lost")

    while connection == True:

        nums = transferData()
        child0_pipe.send(nums[0])
        child1_pipe.send(nums[1])
        child2_pipe.send(nums[2])
        child3_pipe.send(nums[3])
        child4_pipe.send(nums[4])
        child5_pipe.send(nums[5])
        child19_pipe.send(nums[6])
        child20_pipe.send(nums[7])
        child6_pipe.send(nums[8])
        child7_pipe.send(nums[9])
        child8_pipe.send(nums[10])
        child9_pipe.send(nums[11])
        child10_pipe.send(nums[12])
        child11_pipe.send(nums[13])
        child12_pipe.send(nums[14])
        child13_pipe.send(nums[15])
        child14_pipe.send(nums[16])
        child15_pipe.send(nums[17])
        child16_pipe.send(nums[18])
        child17_pipe.send(nums[19])
        child18_pipe.send(nums[20])
        data.updateData()
        data.updateConnection()
        time.sleep(.5)
    sock1.close()


class UpdatingGUI(tk.Frame):
    def __init__(self, parent):
        global connect
        tk.Frame.__init__(self, parent, bg='white')
        self.parent = parent

        # Pi Connection
        self.piConnVal = tk.StringVar()
        self.piConnVal.set("False")
        self.piConn = tk.Label(self, text="Pi Connected", textvariable=self.piConnVal, fg='black', bg='white')
        self.piConnLbl = tk.Label(self, text="Pi Connected: ", fg='black', bg='white')
        self.piConnLbl.grid(row=0, column=0)
        self.piConn.grid(row=0, column=1)
        self.piConn.config(background="red")

        # Master Connection
        self.masterConnVal = tk.StringVar()
        self.masterConnVal.set("False")
        self.masterConn = tk.Label(self, text="Master Connected", textvariable=self.masterConnVal, fg='black', bg='white')
        self.masterConnLbl = tk.Label(self, text="Master Connected: ", fg='black', bg='white')
        self.masterConnLbl.grid(row=1, column=0)
        self.masterConn.grid(row=1, column=1)
        self.masterConn.config(background="red")

        # Tape Count
        self.timeInt = tk.IntVar()
        self.timeInt.set(0)
        self.time = tk.Label(self, text="Time", textvariable=self.timeInt, fg='black', bg='white')
        self.timeLbl = tk.Label(self, text="Time: ", fg='black', bg='white')
        self.timeLbl.grid(row=2, column=0)
        self.time.grid(row=2, column=1)

        # Tape Count
        self.tapeCountInt = tk.IntVar()
        self.tapeCountInt.set(0)
        self.tapeCount = tk.Label(self, text="Tape Count", textvariable=self.tapeCountInt, fg='black', bg='white')
        self.tapeCountLbl = tk.Label(self, text="Tape Count: ", fg='black', bg='white')
        self.tapeCountLbl.grid(row=3, column=0)
        self.tapeCount.grid(row=3, column=1)

        # Position
        self.posval = tk.DoubleVar()
        self.posval.set(0.0)
        self.pos = tk.Label(self, text="Position", textvariable=self.posval, fg='black', bg='white')
        self.positionLbl = tk.Label(self, text="Position: ", fg='black', bg='white')
        self.positionLbl.grid(row=4, column=0)
        self.pos.grid(row=4, column=1)

        # Acceleration X
        self.accelxval = tk.DoubleVar()
        self.accelxval.set(0.0)
        self.accelx = tk.Label(self, text="Acceleration X: ", textvariable=self.accelxval, fg='black', bg='white')
        self.accelxLbl = tk.Label(self, text="Acceleration X: ", fg='black', bg='white')
        self.accelxLbl.grid(row=5, column=0)
        self.accelx.grid(row=5, column=1)

        # Acceleration Y
        self.accelyval = tk.DoubleVar()
        self.accelyval.set(0.0)
        self.accely = tk.Label(self, text="Acceleration Y: ", textvariable=self.accelyval, fg='black', bg='white')
        self.accelyLbl = tk.Label(self, text="Acceleration Y: ", fg='black', bg='white')
        self.accelyLbl.grid(row=6, column=0)
        self.accely.grid(row=6, column=1)

        # Acceleration Z
        self.accelzval = tk.DoubleVar()
        self.accelzval.set(0.0)
        self.accelz = tk.Label(self, text="Acceleration Z: ", textvariable=self.accelzval, fg='black', bg='white')
        self.accelzLbl = tk.Label(self, text="Acceleration Z: ", fg='black', bg='white')
        self.accelzLbl.grid(row=7, column=0)
        self.accelz.grid(row=7, column=1)

        # Velocity X
        self.vxval = tk.DoubleVar()
        self.vxval.set(0.0)
        self.vx = tk.Label(self, text="Velocity X: ", textvariable=self.vxval, fg='black', bg='white')
        self.vxLbl = tk.Label(self, text="Veclocity X: ", fg='black', bg='white')
        self.vxLbl.grid(row=8, column=0)
        self.vx.grid(row=8, column=1)

        # Velocity Y
        self.vyval = tk.DoubleVar()
        self.vyval.set(0.0)
        self.vy = tk.Label(self, text="Velocity Y: ", textvariable=self.vyval, fg='black', bg='white')
        self.vyLbl = tk.Label(self, text="Veclocity Y: ", fg='black', bg='white')
        self.vyLbl.grid(row=9, column=0)
        self.vy.grid(row=9, column=1)

        # Velocity Z
        self.vzval = tk.DoubleVar()
        self.vzval.set(0.0)
        self.vz = tk.Label(self, text="Velocity Z: ", textvariable=self.vzval, fg='black', bg='white')
        self.vzLbl = tk.Label(self, text="Velocity Z: ", fg='black', bg='white')
        self.vzLbl.grid(row=10, column=0)
        self.vz.grid(row=10, column=1)

        # Roll
        self.rollval = tk.DoubleVar()
        self.rollval.set(0.0)
        self.roll = tk.Label(self, text="Roll", textvariable=self.rollval, fg='black', bg='white')
        self.rollLbl = tk.Label(self, text="Roll: ", fg='black', bg='white')
        self.rollLbl.grid(row=11, column=0)
        self.roll.grid(row=11, column=1)

        # Pitch
        self.pitchval = tk.DoubleVar()
        self.pitchval.set(0.0)
        self.pitch = tk.Label(self, text="Pitch", textvariable=self.pitchval, fg='black', bg='white')
        self.pitchLbl = tk.Label(self, text="Pitch: ", fg='black', bg='white')
        self.pitchLbl.grid(row=12, column=0)
        self.pitch.grid(row=12, column=1)

        # Yaw
        self.yawval = tk.DoubleVar()
        self.yawval.set(0.0)
        self.yaw = tk.Label(self, text="Yaw", textvariable=self.yawval, fg='black', bg='white')
        self.yawLbl = tk.Label(self, text="Yaw: ", fg='black', bg='white')
        self.yawLbl.grid(row=13, column=0)
        self.yaw.grid(row=13, column=1)

        # Amperage 1
        self.amp1val = tk.DoubleVar()
        self.amp1val.set(0.0)
        self.amp1 = tk.Label(self, text="Amperage 1", textvariable=self.amp1val, fg='black', bg='white')
        self.amp1min = tk.Label(self, text=str(MIN_AMPERAGE), fg='black', bg='light blue')
        self.amp1max = tk.Label(self, text=str(MAX_AMPERAGE), fg='black', bg='light blue')
        self.amp1Lbl = tk.Label(self, text="Amperage 1: ", fg='black', bg='white')
        self.amp1Lbl.grid(row=14, column=0)
        self.amp1min.grid(row=14, column=1)
        self.amp1.grid(row=14, column=2)
        self.amp1max.grid(row=14, column=3)

        # Amperage 2
        self.amp2val = tk.DoubleVar()
        self.amp2val.set(0.0)
        self.amp2 = tk.Label(self, text="Amperage 2 ", textvariable=self.amp2val, fg='black', bg='white')
        self.amp2min = tk.Label(self, text=str(MIN_AMPERAGE), fg='black', bg='light blue')
        self.amp2max = tk.Label(self, text=str(MAX_AMPERAGE), fg='black', bg='light blue')
        self.amp2Lbl = tk.Label(self, text="Amperage 2: ", fg='black', bg='white')
        self.amp2Lbl.grid(row=15, column=0)
        self.amp2min.grid(row=15, column=1)
        self.amp2.grid(row=15, column=2)
        self.amp2max.grid(row=15, column=3)

        # Voltage 1
        self.volt1val = tk.DoubleVar()
        self.volt1val.set(0.0)
        self.volt1 = tk.Label(self, text="Voltage 1", textvariable=self.volt1val, fg='black', bg='white')
        self.volt1min = tk.Label(self, text=str(MIN_VOLTAGE), fg='black', bg='light blue')
        self.volt1max = tk.Label(self, text=str(MAX_VOLTAGE), fg='black', bg='light blue')
        self.volt1Lbl = tk.Label(self, text="Voltage 1: ", fg='black', bg='white')
        self.volt1Lbl.grid(row=16, column=0)
        self.volt1min.grid(row=16, column=1)
        self.volt1.grid(row=16, column=2)
        self.volt1max.grid(row=16, column=3)

        # Voltage 2
        self.volt2val = tk.DoubleVar()
        self.volt2val.set(0.0)
        self.volt2 = tk.Label(self, text="Voltage 2", textvariable=self.volt2val, fg='black', bg='white')
        self.volt2min = tk.Label(self, text=str(MIN_VOLTAGE), fg='black', bg='light blue')
        self.volt2max = tk.Label(self, text=str(MAX_VOLTAGE), fg='black', bg='light blue')
        self.volt2Lbl = tk.Label(self, text="Voltage 2: ", fg='black', bg='white')
        self.volt2Lbl.grid(row=17, column=0)
        self.volt2min.grid(row=17, column=1)
        self.volt2.grid(row=17, column=2)
        self.volt2max.grid(row=17, column=3)

        # Temperature Ambient
        self.tempAmbVal = tk.DoubleVar()
        self.tempAmbVal.set(0.0)
        self.tempAmb = tk.Label(self, text="Temperature Ambient", textvariable=self.tempAmbVal, fg='black', bg='white')
        self.tempAmbMin = tk.Label(self, text=str(MIN_TEMPERATURE_AMBIENT), fg='black', bg='light blue')
        self.tempAmbMax = tk.Label(self, text=str(MAX_TEMPERATURE_AMBIENT), fg='black', bg='light blue')
        self.tempAmbLbl = tk.Label(self, text="Ambient Temperature: ", fg='black', bg='white')
        self.tempAmbLbl.grid(row=18, column=0)
        self.tempAmbMin.grid(row=18, column=1)
        self.tempAmb.grid(row=18, column=2)
        self.tempAmbMax.grid(row=18, column=3)

        # Temperature Battery 1
        self.tempBatt1Val = tk.DoubleVar()
        self.tempBatt1Val.set(0.0)
        self.tempBatt1 = tk.Label(self, text="Temperature Battery 1", textvariable=self.tempBatt1Val, fg='black', bg='white')
        self.tempBatt1Min = tk.Label(self, text=str(MIN_TEMPERATURE_BATTERY), fg='black', bg='light blue')
        self.tempBatt1Max = tk.Label(self, text=str(MAX_TEMPERATURE_BATTERY), fg='black', bg='light blue')
        self.tempBatt1Lbl = tk.Label(self, text="Battery 1 Temperature: ", fg='black', bg='white')
        self.tempBatt1Lbl.grid(row=19, column=0)
        self.tempBatt1Min.grid(row=19, column=1)
        self.tempBatt1.grid(row=19, column=2)
        self.tempBatt1Max.grid(row=19, column=3)

        # Temperature Battery 2
        self.tempBatt2Val = tk.DoubleVar()
        self.tempBatt2Val.set(0.0)
        self.tempBatt2 = tk.Label(self, text="Temperature Battery 2", textvariable=self.tempBatt2Val, fg='black', bg='white')
        self.tempBatt2Min = tk.Label(self, text=str(MIN_TEMPERATURE_BATTERY), fg='black', bg='light blue')
        self.tempBatt2Max = tk.Label(self, text=str(MAX_TEMPERATURE_BATTERY), fg='black', bg='light blue')
        self.tempBatt2Lbl = tk.Label(self, text="Battery 2 Temperature: ", fg='black', bg='white')
        self.tempBatt2Lbl.grid(row=20, column=0)
        self.tempBatt2Min.grid(row=20, column=1)
        self.tempBatt2.grid(row=20, column=2)
        self.tempBatt2Max.grid(row=20, column=3)

    def updateData(self):
        global state, previousState
        previousState = state
        state = parent1_pipe.recv()

        if(parent0_pipe.recv() == True):
            self.masterConnVal.set("True")
            self.masterConn.config(background="green")
        else:
            self.masterConnVal.set("False")
            self.masterConn.config(background="red")


        self.timeInt.set(parent2_pipe.recv())
        self.tapeCountInt.set(parent3_pipe.recv())
        self.posval.set(round(parent4_pipe.recv(), 2))
        self.accelxval.set(round(parent5_pipe.recv(), 2))
        self.accelyval.set(round(parent19_pipe.recv(), 2))
        self.accelzval.set(round(parent20_pipe.recv(), 2))
        self.vxval.set(round(parent6_pipe.recv(), 2))
        self.vyval.set(round(parent7_pipe.recv(), 2))
        self.vzval.set(round(parent8_pipe.recv(), 2))
        self.rollval.set(round(parent9_pipe.recv(), 2))
        self.pitchval.set(round(parent10_pipe.recv(), 2))
        self.yawval.set(round(parent11_pipe.recv(), 2))


        self.amp1val.set(round(parent12_pipe.recv(), 2))
        if(self.amp1val.get() >= MIN_AMPERAGE and self.amp1val.get() <= MAX_AMPERAGE):
            self.amp1.config(background="green")
        else:
            self.amp1.config(background="red")

        self.amp2val.set(round(parent13_pipe.recv(), 2))
        if (self.amp2val.get() >= MIN_AMPERAGE and self.amp2val.get() <= MAX_AMPERAGE):
            self.amp2.config(background="green")
        else:
            self.amp2.config(background="red")

        self.volt1val.set(round(parent14_pipe.recv(), 2))
        if (self.volt1val.get() >= MIN_VOLTAGE and self.volt1val.get() <= MAX_VOLTAGE):
            self.volt1.config(background="green")
        else:
            self.volt1.config(background="red")

        self.volt2val.set(round(parent15_pipe.recv(), 2))
        if (self.volt2val.get() >= MIN_VOLTAGE and self.volt2val.get() <= MAX_VOLTAGE):
            self.volt2.config(background="green")
        else:
            self.volt2.config(background="red")

        self.tempAmbVal.set(round(parent16_pipe.recv(), 2))
        if (self.tempAmbVal.get() >= MIN_TEMPERATURE_AMBIENT and self.tempAmbVal.get() <= MAX_TEMPERATURE_AMBIENT):
            self.tempAmb.config(background="green")
        else:
            self.tempAmb.config(background="red")

        self.tempBatt1Val.set(round(parent17_pipe.recv(), 2))
        if (self.tempBatt1Val.get() >= MIN_TEMPERATURE_BATTERY and self.tempBatt1Val.get() <= MAX_TEMPERATURE_BATTERY):
            self.tempBatt1.config(background="green")
        else:
            self.tempBatt1.config(background="red")

        self.tempBatt2Val.set(round(parent18_pipe.recv(), 2))
        if (self.tempBatt2Val.get() >= MIN_TEMPERATURE_BATTERY and self.tempBatt2Val.get() <= MAX_TEMPERATURE_BATTERY):
            self.tempBatt2.config(background="green")
        else:
            self.tempBatt2.config(background="red")

    def updateConnection(self):
        if(connection == True):
            self.piConnVal.set("True")
            self.piConn.config(background="green")
        else:
            self.piConnVal.set("False")
            self.piConn.config(background="red")


class SoftwareStateDiagram(tk.Label):
    def __init__(self, parent):
        tk.Label.__init__(self, parent, bg='black', width=1000, height=600, borderwidth=3, )
        self.parent = parent
        # Row 1

        self.states = []

        self.insertion = tk.Label(self, width=10, height=5, text="Pod Insertion", bg='grey', fg='white')
        self.insertion.place(x=0, y=0)
        self.states.append(self.insertion)

        # self.insertion.grid(row=1, column=1)
        self.idle = tk.Label(self, width=10, height=5, text="Idle", background='gray', fg='white')
        self.idle.place(x=160, y=0)
        self.states.append(self.idle)

        self.sysCheck = tk.Label(self, width=10, height=5, text="System Check", background='gray', fg='white')
        self.sysCheck.place(x=320, y=0)
        self.states.append(self.sysCheck)

        self.ready = tk.Label(self, width=10, height=5, text="Ready", background='gray', fg='white')
        self.ready.place(x=480, y=0)
        self.states.append(self.ready)

        self.pushing = tk.Label(self, width=10, height=5, text="Pushing", background='gray', fg='white')
        self.pushing.place(x=640, y=0)
        self.states.append(self.pushing)

        # Row 2
        self.reconnect = tk.Label(self, width=10, height=5, text="Reconnect\nAttempt", background='gray', fg='white')
        self.reconnect.place(x=0, y=160)
        self.states.append(self.reconnect)

        self.faultBreaks = tk.Label(self, width=10, height=5, text="Fault\n(Brakes)", background='gray', fg='white')
        self.faultBreaks.place(x=320, y=160)
        self.states.append(self.faultBreaks)

        self.faultNoBreaks = tk.Label(self, width=10, height=5, text="Fault\n(No Brakes)", background='gray', fg='white')
        self.faultNoBreaks.place(x=480, y=160)
        self.states.append(self.faultNoBreaks)

        self.coasting = tk.Label(self, width=10, height=5, text="Coasting", background='gray', fg='white')
        self.coasting.place(x=640, y=160)
        self.states.append(self.coasting)

        # Row 3
        self.diagnostic = tk.Label(self, width=10, height=5, text="Diagnostic", background='red', fg='white')
        self.diagnostic.place(x=0, y=320)
        self.states.append(self.diagnostic)

        self.brakeOverride = tk.Label(self, width=10, height=5, text="Manual\nBrake\nOverride", background='blue', fg='white')
        self.brakeOverride.place(x=160, y=320)
        self.states.append(self.brakeOverride)

        self.powerOff = tk.Label(self, width=10, height=5, text="Power Off", background='gray',fg='white')
        self.powerOff.place(x=320, y=320)
        self.states.append(self.powerOff)

        self.disengage = tk.Label(self, width=10, height=5, text="Disengage\nBrakes", background='gray', fg='white')
        self.disengage.place(x=480, y=320)
        self.states.append(self.disengage)

        self.braking = tk.Label(self, width=10, height=5, text="Braking", background='gray', fg='white')
        self.braking.place(x=640, y=320)
        self.states.append(self.braking)

        self.flash()

    def flash(self):
        current_color = self.states[state].cget("background")
        if(previousState != state):
            if previousState != 9 and previousState != 10:
                next_color = "grey"
                next_text = "white"
            elif previousState == 9:
                next_color = "red"
                next_text = "white"
            else:
                next_color = "blue"
                next_text = "white"
            self.states[previousState].config(background=next_color, fg=next_text)
        if state != 9 and state != 10:
            if current_color == "grey":
                next_color = "yellow"
                next_text = "black"
            else:
                next_color = "grey"
                next_text = "white"
        elif state == 9:
            if current_color == "red":
                next_color = "yellow"
                next_text = "black"
            else:
                next_color = "red"
                next_text = "white"
        else:
            if current_color == "blue":
                next_color = "yellow"
                next_text = "black"
            else:
                next_color = "blue"
                next_text = "white"
        self.states[state].config(background=next_color, fg=next_text)
        root.after(500, self.flash)


def sendtoConnect():

    # global connection, tryConn, conn, sock1
    global connection, tryConn, conn, sock1
    while(True):
        # while (tryConn == False):
        #     pass
        # tryConn = False
        if connection == False:
            try:
                print('connection attempt')
                sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock1.settimeout(2)
                sock1.bind(server_address)
                sock1.listen(1)
                conn, addr = sock1.accept()
                msg = conn.recv(1)
                msg = msg.decode("utf-8")
                if msg == '0':
                    messagebox.showinfo("Connection!", "Connection Successful")
                    connection = True
                    count()
                else:
                    messagebox.showerror("Connection!", 'Wrong connection message obtained.')
                    connection = False
                    data.updateConnection()
            except Exception as exc:
                print('Failed to connect to Pi. Exception raised:')
                print(exc)
                connection = False
                data.updateConnection()


# def Check():
#     global connection
#     if(connection == True):
#         messagebox.showinfo("Connection!", "Connection is good!")
#     else:
#         messagebox.showinfo("Connection!", "There is currently no connection.")


def endConnect():
    global connection, conn
    if connection == True:
        sock1.close()
        connection = False
        messagebox.showinfo("Connection!", "The conneciton has been disabled.")
        data.updateConnection()
    else:
        connection = False
        messagebox.showinfo("Connection!", "There was no connection.")
        data.updateConnection()


def connections(connectionsFrame):
    Connections = tk.Label(connectionsFrame, width=20, height=10, background='black')
    Connections.place(x=100, y=100)

    # connect = tk.Button(Connections, text='Connect', command=tryConnection)
    # connect.place(x=20,y=0)
    #
    # check = tk.Button(Connections, text='Check Connection', command=Check)
    # check.place(x=0, y=30)

    close = tk.Button(Connections, text='Close Connection', command=endConnect)
    close.place(x=2,y=60)


# def tryConnection():
#     global tryConn
#     tryConn = True


def getSensorData(root):
    global data
    data = UpdatingGUI(root)
    data.place(x=100, y=360)


def getStateDiagram(root):
    global diagram
    diagram = SoftwareStateDiagram(root)
    diagram.place(x=400, y=200)


def commands(canvas):
    commands= tk.Label(canvas, width=200, height=800, background="black")
    commands.place(x=1300, y=100)

    insert = tk.Button(commands, text='Insert Pod', command=lambda: sendCommand(b'1'), width=15, height=7)
    insert.place(x=0, y=0)

    start = tk.Button(commands, text='Start', command=lambda: sendCommand(b'2'), width=15, height=7)
    start.place(x=0, y=140)

    power = tk.Button(commands, text='Power Off', command=lambda: sendCommand(b'3'), width=15, height=7)
    power.place(x=0, y=280)

    engage = tk.Button(commands, text='Engage Brakes', command=lambda: sendCommand(b'4'), width=15, height=7)
    engage.place(x=0, y=420)

    disengage = tk.Button(commands, text='Disengage Brakes', command=lambda: sendCommand(b'5'), width=15, height=7)
    disengage.place(x=0, y=560)


def sendCommand(cmd):
    global command
    command = cmd
    print(command)


def Stop(stopFrame):
    stopper = tk.Label(stopFrame, width=20, height=10, background='black')
    stopper.place(x=100, y=200)

    def check():
        passw = E.get()
        if passw == "laur":
            message = struct.pack('i', 14)
            sock1.sendto(message, server_address)
            msg = sock1.recv(2)
            if msg == "sc":
                messagebox.showinfo("Emergency Stop", "The Testbed has Landed")
                endConnect()
            else:
                messagebox.showerror("Emergency Stop", "There was an Error Stopping a Testbed. Error: " + msg)
        else:
            messagebox.showerror("Emergency Stop", "Incorrect Password")

    question = tk.Label(text='Please Enter 4 Digit Code')
    E = tk.Entry(stopper, bd=5)
    E.place(x=0, y=0)
    B = tk.Button(stopper, text='Stop', command=check)
    B.place(x=30, y=0)
    B.place(x=0, y=30)

def main():
    global root, connection, tryConn
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))
    canvas = tk.Canvas(width=width, height=height, bg='black')
    canvas.pack(expand='yes', fill='both')

    getSensorData(canvas)
    getStateDiagram(canvas)
    connections(canvas)
    Stop(canvas)
    commands(canvas)

    title = tk.PhotoImage(file='Title.gif')
    titleLbl = tk.Label(root, image=title, background='black')
    titleLbl.place(x=500, y=2)

    threading.Thread(target=sendtoConnect).start()
    threading.Thread(target=root.mainloop()).start()

    # endConnect()


main()
f.close()
