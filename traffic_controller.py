import time
from pyfirmata import Arduino, util, STRING_DATA

PORT = 'COM5'
board = Arduino(PORT)


class TrafficLight:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green


# TL For each lanes
TL_lane_1 = TrafficLight(13, 12, 11)
TL_lane_2 = TrafficLight(10, 9, 8)
TL_lane_3 = TrafficLight(7, 6, 5)
TL_lane_4 = TrafficLight(4, 3, 2)

TL = [TL_lane_1, TL_lane_2, TL_lane_3, TL_lane_4]

##### Functions #####


def ledCheck():
    for i in range(13, 1, -1):
        board.digital[i].write(1)
        time.sleep(0.025)
        board.digital[i].write(0)
    for i in range(2, 14):
        board.digital[i].write(1)
        time.sleep(0.025)
        board.digital[i].write(0)


def shutDownAll():
    for i in range(2, 14):
        board.digital[i].write(0)


def lcd(text):
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(text))


def activateLane(laneIndex, gst, starvation):
    lcd("Lane: "+str(laneIndex)+" ("+str(gst)+")s")
    lcd(str(starvation[0])+" "+str(starvation[1]
                                   )+" "+str(starvation[2])+" "+str(starvation[3]))
    for i in range(0, 4):
        if (i != laneIndex):
            board.digital[TL[i].yellow].write(0)
            board.digital[TL[i].green].write(0)
            board.digital[TL[i].red].write(1)
        else:
            if (gst < 4):
                board.digital[TL[i].red].write(0)
                board.digital[TL[i].green].write(0)
                board.digital[TL[i].yellow].write(1)
            else:
                board.digital[TL[i].red].write(0)
                board.digital[TL[i].yellow].write(0)
                board.digital[TL[i].green].write(1)


ledCheck()
