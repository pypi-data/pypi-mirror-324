import importlib
import os
import sys
import time
from multiprocessing import Event, Process, Queue
from threading import Lock

import serial

LOW_LEVEL_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(
    LOW_LEVEL_FOLDER_PATH,
)
import mimic_hand_pb2

# ------------------------------ Define Variables ------------------------------
DEFAULT_BAUDRATE = 3000000

# Set Protobuf Commands
NOP = 0
GET_UART_ID = 1
SET_UART_ID = 2
INIT_MOTORS = 3
SET_MOTOR_MODE = 4
GET_MOTOR_POS = 5
SET_MOTOR_POS = 6
GET_MOTOR_CURRENT = 7
INIT_SPOOL_SENSORS = 8
GET_SPOOL_ANGLES = 9
GET_MOTOR_DATA = 10
SET_PID_VALUES = 11
SET_CURRENT_LIMIT = 12
GET_HAND_ID = 13
SET_HAND_ID = 14

# Motor Modes
MOTOR_OFF = 0
MOTOR_CALIBRATE = 1
MOTOR_POS_CTRL = 2
MOTOR_CUR_LIM_POS_CTRL = 3

motor_mode_str = {
    0: 'OFF',
    1: 'CALIBRATE',
    2: 'POSITION CONTROL',
    3: 'CURRENT-LIMITED POSITION CONTROL',
}
# ------------------------------------------------------------------------------


# ------------------------- CRC Functions & Variables --------------------------

# CRC lookup table
crcTable = [
    0x0000,
    0x8005,
    0x800F,
    0x000A,
    0x801B,
    0x001E,
    0x0014,
    0x8011,
    0x8033,
    0x0036,
    0x003C,
    0x8039,
    0x0028,
    0x802D,
    0x8027,
    0x0022,
    0x8063,
    0x0066,
    0x006C,
    0x8069,
    0x0078,
    0x807D,
    0x8077,
    0x0072,
    0x0050,
    0x8055,
    0x805F,
    0x005A,
    0x804B,
    0x004E,
    0x0044,
    0x8041,
    0x80C3,
    0x00C6,
    0x00CC,
    0x80C9,
    0x00D8,
    0x80DD,
    0x80D7,
    0x00D2,
    0x00F0,
    0x80F5,
    0x80FF,
    0x00FA,
    0x80EB,
    0x00EE,
    0x00E4,
    0x80E1,
    0x00A0,
    0x80A5,
    0x80AF,
    0x00AA,
    0x80BB,
    0x00BE,
    0x00B4,
    0x80B1,
    0x8093,
    0x0096,
    0x009C,
    0x8099,
    0x0088,
    0x808D,
    0x8087,
    0x0082,
    0x8183,
    0x0186,
    0x018C,
    0x8189,
    0x0198,
    0x819D,
    0x8197,
    0x0192,
    0x01B0,
    0x81B5,
    0x81BF,
    0x01BA,
    0x81AB,
    0x01AE,
    0x01A4,
    0x81A1,
    0x01E0,
    0x81E5,
    0x81EF,
    0x01EA,
    0x81FB,
    0x01FE,
    0x01F4,
    0x81F1,
    0x81D3,
    0x01D6,
    0x01DC,
    0x81D9,
    0x01C8,
    0x81CD,
    0x81C7,
    0x01C2,
    0x0140,
    0x8145,
    0x814F,
    0x014A,
    0x815B,
    0x015E,
    0x0154,
    0x8151,
    0x8173,
    0x0176,
    0x017C,
    0x8179,
    0x0168,
    0x816D,
    0x8167,
    0x0162,
    0x8123,
    0x0126,
    0x012C,
    0x8129,
    0x0138,
    0x813D,
    0x8137,
    0x0132,
    0x0110,
    0x8115,
    0x811F,
    0x011A,
    0x810B,
    0x010E,
    0x0104,
    0x8101,
    0x8303,
    0x0306,
    0x030C,
    0x8309,
    0x0318,
    0x831D,
    0x8317,
    0x0312,
    0x0330,
    0x8335,
    0x833F,
    0x033A,
    0x832B,
    0x032E,
    0x0324,
    0x8321,
    0x0360,
    0x8365,
    0x836F,
    0x036A,
    0x837B,
    0x037E,
    0x0374,
    0x8371,
    0x8353,
    0x0356,
    0x035C,
    0x8359,
    0x0348,
    0x834D,
    0x8347,
    0x0342,
    0x03C0,
    0x83C5,
    0x83CF,
    0x03CA,
    0x83DB,
    0x03DE,
    0x03D4,
    0x83D1,
    0x83F3,
    0x03F6,
    0x03FC,
    0x83F9,
    0x03E8,
    0x83ED,
    0x83E7,
    0x03E2,
    0x83A3,
    0x03A6,
    0x03AC,
    0x83A9,
    0x03B8,
    0x83BD,
    0x83B7,
    0x03B2,
    0x0390,
    0x8395,
    0x839F,
    0x039A,
    0x838B,
    0x038E,
    0x0384,
    0x8381,
    0x0280,
    0x8285,
    0x828F,
    0x028A,
    0x829B,
    0x029E,
    0x0294,
    0x8291,
    0x82B3,
    0x02B6,
    0x02BC,
    0x82B9,
    0x02A8,
    0x82AD,
    0x82A7,
    0x02A2,
    0x82E3,
    0x02E6,
    0x02EC,
    0x82E9,
    0x02F8,
    0x82FD,
    0x82F7,
    0x02F2,
    0x02D0,
    0x82D5,
    0x82DF,
    0x02DA,
    0x82CB,
    0x02CE,
    0x02C4,
    0x82C1,
    0x8243,
    0x0246,
    0x024C,
    0x8249,
    0x0258,
    0x825D,
    0x8257,
    0x0252,
    0x0270,
    0x8275,
    0x827F,
    0x027A,
    0x826B,
    0x026E,
    0x0264,
    0x8261,
    0x0220,
    0x8225,
    0x822F,
    0x022A,
    0x823B,
    0x023E,
    0x0234,
    0x8231,
    0x8213,
    0x0216,
    0x021C,
    0x8219,
    0x0208,
    0x820D,
    0x8207,
    0x0202,
]


# calculate 16-bit CRC
def calculateCRC16(message):
    remainder = 0

    for i in range(len(message)):
        data = reflect(message[i], 8) ^ (remainder >> 8)
        remainder = crcTable[data] ^ ((remainder << 8) & 0xFFFF)

    return reflect(remainder, 16)


# function to reflect the binary data
def reflect(data, len):
    reflection = 0
    for i in range(len):
        if data & 0x01:
            reflection |= 1 << (len - 1 - i)
        data = data >> 1
    return reflection


# ------------------------------------------------------------------------------


# ------------------------------- RP2040 Client --------------------------------
class RP2040Client:
    def __init__(self, portName):
        self.__port = portName
        self.__isOpen = False
        self.__ser = None
        self.__serialLock = None
        self.__baudrate = DEFAULT_BAUDRATE

        self.__uartIDs = []

        self.__process = None
        self.__stopProcess = Event()
        self.__flag_getData = Event()
        self.__flag_setData = Event()
        self.__motorDataQueue = Queue()
        self.__desiredPositionQueue = Queue()

        self.__flag_getData.set()
        self.__flag_setData.set()

        self.__setupPort()

        self.nAttempts = [0, 0, 0, 0, 0]
        self.nErrors = [0, 0, 0, 0, 0]

    def setBaudRate(self, baudrate):
        if baudrate in [
            9600,
            19200,
            38400,
            57600,
            115200,
            230400,
            460800,
            500000,
            576000,
            921600,
            1000000,
            1152000,
            2000000,
            2500000,
            3000000,
            3500000,
            4000000,
        ]:
            self.__baudrate = baudrate
        else:
            print(
                '\n\033[93mWarning:\033[0m Invalid Baudrate. Default baudrate',
                ' was set.',
            )
            self.__baudrate = DEFAULT_BAUDRATE
        self.__setupPort()

    def __setupPort(self):
        if self.__isOpen:
            self.closePort()

        self.__ser = serial.Serial(
            port=self.__port,
            baudrate=self.__baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.02,
        )
        self.__serialLock = Lock()
        self.__isOpen = True

        with self.__serialLock:
            self.__ser.reset_input_buffer()

        self.tx_time_per_byte = (1000.0 / self.__baudrate) * 10.0

    def openPort(self):
        if not self.__isOpen:
            self.__setupPort()

    def closePort(self):
        if self.__isOpen:
            self.__isOpen = False
            with self.__serialLock:
                self.__ser.close()

    def __write(self, data):
        msg = data.SerializeToString()
        send = bytearray(b':')
        send.extend(msg)
        send.extend(calculateCRC16(msg).to_bytes(2, 'big'))
        send.extend(b'\r\n')

        ack = False

        with self.__serialLock:
            self.__ser.write(send)

        ack = self.__waitForAck()

        return ack

    def __read(self):
        with self.__serialLock:
            line = self.__ser.read_until(expected=b'\r\n')
            self.__ser.reset_input_buffer()
        if line and len(line) > 5:
            rx_CRC = line[-3] | (line[-4] << 8)
            CRC = calculateCRC16(line[:-4])
            if CRC == rx_CRC:
                return line[:-4]

        return False

    def __waitForAck(self):
        with self.__serialLock:
            serial_data = self.__ser.read_until(expected=b'\r\n')

        if serial_data == b'\x06\r\n':
            return True

        return False

    def setUartID(self, newID):
        oldID = self.getUartID()

        if oldID is False:
            return False

        message = mimic_hand_pb2.Message()
        message.address = oldID
        message.command = SET_UART_ID
        message.metaData = newID

        if self.__write(message):
            return True

        return False

    def getUartID(self):
        message = mimic_hand_pb2.Message()
        message.address = 0
        message.command = GET_UART_ID

        if self.__write(message):
            reply = mimic_hand_pb2.Message()
            raw_reply = self.__read()
            if raw_reply:
                reply.ParseFromString(raw_reply)
                return reply.metaData

        return False
    
    def getHandID(self, uartID):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = GET_HAND_ID
        
        if self.__write(message):
            reply = mimic_hand_pb2.Message()
            raw_reply = self.__read()
            if raw_reply:
                reply.ParseFromString(raw_reply)
                return reply.hand_id.id

        return False

    def setHandID(self, uartID, handID):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = SET_HAND_ID
        
        # last byte is null termination
        fixed_len_hand_id = ""
        if len(handID) < 31:
            fixed_len_hand_id = handID.ljust(31, ' ')
        else:
            fixed_len_hand_id = handID[:31]

        message.hand_id.id = fixed_len_hand_id
        
        if self.__write(message):
            return True

        return False


    def setPID(self, uartID, Kp, Ki, Kd, Kb):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = SET_PID_VALUES
        message.pid.Kp = Kp
        message.pid.Ki = Ki
        message.pid.Kd = Kd
        message.pid.Kb = Kb

        if self.__write(message):
            return True

        return False

    def initMotors(self, uartID, motorIDs):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = INIT_MOTORS

        for i in range(len(motorIDs)):
            message.motors.add()
            message.motors[i].motorid = motorIDs[i]

        if self.__write(message):
            if uartID not in self.__uartIDs:
                self.__uartIDs.append(uartID)
            return True

        return False

    def setMotorMode(self, uartID, mode):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = SET_MOTOR_MODE
        message.metaData = mode

        if self.__write(message):
            return True

        return False

    def setCurrentLimit(self, uartID, limit):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = SET_CURRENT_LIMIT
        message.metaData = limit

        if self.__write(message):
            return True

        return False

    def __getMotorPos(self, uartID):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = GET_MOTOR_POS

        if self.__write(message):
            reply = mimic_hand_pb2.Message()
            positions = {}
            raw_reply = self.__read()
            if raw_reply:
                reply.ParseFromString(raw_reply)
                for i in range(len(reply.motors)):
                    positions[reply.motors[i].motorid] = reply.motors[i].position
                return positions

        return False

    def __setMotorPos(self, uartID, positions):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = SET_MOTOR_POS

        ind = 0
        for motorID, position in positions.items():
            message.motors.add()
            message.motors[ind].motorid = motorID
            message.motors[ind].position = position
            ind += 1

        if self.__write(message):
            return True

        return False

    def __getMotorCurr(self, uartID):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = GET_MOTOR_CURRENT

        if self.__write(message):
            reply = mimic_hand_pb2.Message()
            currents = {}
            raw_reply = self.__read()
            if raw_reply:
                reply.ParseFromString(raw_reply)
                for i in range(len(reply.motors)):
                    currents[reply.motors[i].motorid] = reply.motors[i].current
                return currents

        return False

    def __getSpoolAngles(self, uartID):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = GET_SPOOL_ANGLES

        if self.__write(message):
            reply = mimic_hand_pb2.Message()
            spoolData = {}
            raw_reply = self.__read()
            if raw_reply:
                reply.ParseFromString(raw_reply)
                for i in range(len(reply.motors)):
                    spoolData[reply.motors[i].motorid] = reply.motors[i].spool
                return spoolData

        return False

    def __getMotorData(self, uartID):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = GET_MOTOR_DATA

        if self.__write(message):
            reply = mimic_hand_pb2.Message()
            raw_reply = self.__read()
            if raw_reply:
                reply.ParseFromString(raw_reply)
                return reply
            else:
                return False

        return False

    def process(self, mode):
        self.stopProcess()

        if mode == MOTOR_OFF:
            self.__process = None
        elif mode == MOTOR_CALIBRATE:
            self.__stopProcess.clear()
            self.__process = Process(
                target=self.__calibrationProcess,
                args=(
                    self.__stopProcess,
                    self.__uartIDs,
                    self.__flag_getData,
                    self.__motorDataQueue,
                ),
            )
            self.__process.start()
        elif mode == MOTOR_POS_CTRL:
            self.__stopProcess.clear()
            self.__process = Process(
                target=self.__positionControlProcess,
                args=(
                    self.__stopProcess,
                    self.__uartIDs,
                    self.__flag_getData,
                    self.__flag_setData,
                    self.__motorDataQueue,
                    self.__desiredPositionQueue,
                ),
            )
            self.__process.start()
        elif mode == MOTOR_CUR_LIM_POS_CTRL:
            self.__stopProcess.clear()
            self.__process = Process(
                target=self.__positionControlProcess,
                args=(
                    self.__stopProcess,
                    self.__uartIDs,
                    self.__flag_getData,
                    self.__flag_setData,
                    self.__motorDataQueue,
                    self.__desiredPositionQueue,
                ),
            )
            self.__process.start()

    def stopProcess(self):
        if self.__process:
            self.__stopProcess.set()
            self.__process.join()

    def __calibrationProcess(self, stopProcess, uartIDs, flag_getData, motorDataQueue):
        motorData = {}

        while not stopProcess.is_set():
            for uartID in uartIDs:
                data = self.__getMotorData(uartID)

                if data:
                    motorData[uartID] = data

                time.sleep(0.01)

            if not flag_getData.is_set():
                motorDataQueue.put(motorData)
                flag_getData.set()

    def __positionControlProcess(
        self,
        stopProcess,
        uartIDs,
        flag_getData,
        flag_setData,
        motorDataQueue,
        desiredPositionQueue,
    ):
        motorData = {}
        desiredMotorPos = {uartID: {} for uartID in uartIDs}

        while not stopProcess.is_set():
            for uartID in uartIDs:
                data = self.__getMotorData(uartID)
                if data:
                    motorData[uartID] = data

                if uartID in desiredMotorPos and desiredMotorPos[uartID]:
                    status = self.__setMotorPos(uartID, desiredMotorPos[uartID])

            if not flag_getData.is_set():
                motorDataQueue.put(motorData)
                flag_getData.set()

            if not flag_setData.is_set():
                updated_positions = desiredPositionQueue.get()
                for uartID, positions in updated_positions.items():
                    desiredMotorPos[uartID] = positions
                flag_setData.set()

            time.sleep(0.001)

    def getMotorPositions(self):
        motorData = self.getMotorData()

        positions = {}
        if motorData:
            for uartID in self.__uartIDs:
                positions[uartID] = {}
                data = motorData[uartID]
                for i in range(len(data.motors)):
                    ind = data.motors[i].motorid
                    positions[uartID][ind] = data.motors[i].position
        return positions

    def getMotorCurrents(self):
        motorData = self.getMotorData()

        currents = {}
        if motorData:
            for uartID in self.__uartIDs:
                currents[uartID] = {}
                data = motorData[uartID]
                for i in range(len(data.motors)):
                    ind = data.motors[i].motorid
                    currents[uartID][ind] = data.motors[i].current
        return currents

    def getSpoolPositions(self):
        motorData = self.getMotorData()

        spoolPos = {}
        if motorData:
            for uartID in self.__uartIDs:
                spoolPos[uartID] = {}
                data = motorData[uartID]
                for i in range(len(data.motors)):
                    ind = data.motors[i].motorid
                    spoolPos[uartID][ind] = (
                        data.motors[i].spool.angle,
                        data.motors[i].spool.status,
                    )
        return spoolPos

    def getMotorData(self):
        self.__flag_getData.clear()
        self.__flag_getData.wait()
        motorData = self.__motorDataQueue.get()
        return motorData

    def setMotorPositions(self, positions):
        self.__desiredPositionQueue.put(positions)
        self.__flag_setData.clear()
        self.__flag_setData.wait()

    def initSpoolSensing(self, uartID, nSensors):
        message = mimic_hand_pb2.Message()
        message.address = uartID
        message.command = INIT_SPOOL_SENSORS
        message.metaData = nSensors

        if self.__write(message):
            return True

        return False


# ------------------------------------------------------------------------------
