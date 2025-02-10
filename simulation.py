import random
from threading import Thread
import time
import pygame
import sys
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#import traffic_controller as controller
import matplotlib
matplotlib.use("TkAgg")

SMART_TRAFFIC = True

pygame.init()
simulationTime = 0

lane = [50, 50, 50, 50]
density = [0.25, 0.25, 0.25, 0.25]
starvation = [0, 0, 0, 0]

activeLane = 0  # Current green lane
timer = 20  # 20 Seconds default timer

defaultMinimum = 10  # Min GST
defaultMaximum = 50  # Max GST
defaultStarvation = 140  # Lane starvation

signalCoords = [(540, 250), (825, 250), (825, 580), (540, 580)]
signalTimerCoords = [(510, 270), (870, 270), (870, 610), (510, 610)]
vehicleCountCoords = [(250, 390), (730, 120), (1100, 490), (620, 750)]


selectedLane = 0  # Select lane for random vehicle input


def inputRate():
    if selectedLane == 0:
        return random.randint(1, 2)
    elif selectedLane == 1:
        return random.randint(3, 6)
    elif selectedLane == 2:
        return random.randint(1, 2)
    else:
        return random.randint(1, 4)


def calcGST(vehicleDensity):
    gst = (math.exp(vehicleDensity)*defaultMaximum)/3
    if gst < defaultMinimum:
        return defaultMinimum
    elif gst > defaultMaximum:
        return defaultMaximum
    else:
        return round(gst)


def vehiclesIn():
    global lane
    global selectedLane
    global simulationTime
    while True:
        simulationTime += 1

        for i in range(0, 4):
            if (i != activeLane):
                starvation[i] += 1

        select_lane = random.randint(0, 3)
        selectedLane = select_lane
        lane[select_lane] += inputRate()
        density[select_lane] = lane[select_lane]/sum(lane)
        time.sleep(1)


def vehiclesOut(laneIndex):
    global lane
    out = inputRate()
    if (lane[laneIndex] > out):
        lane[laneIndex] -= out
    else:
        lane[laneIndex] = 0


def animate(i):
    data = {'Lane 1': density[0], 'Lane 2': density[1], 'Lane 3': density[2],
            'Lane 4': density[3]}
    keys = list(data.keys())
    values = list(data.values())
    plt.cla()
    plt.bar(keys, values, color=['maroon'],
            width=0.6)


def plotting():
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.xlabel("Lanes")
    plt.ylabel("Density")
    plt.title("Traffic Density Graph")
    plt.tight_layout()
    plt.show()


def greenLight():
    global activeLane
    global timer

    while True:
        starvation[activeLane] = 0
        vehiclesOut(activeLane)
        #controller.activateLane(activeLane, timer, starvation)
        time.sleep(1)
        timer -= 1
        if (timer == 0):
            if (SMART_TRAFFIC):
                maxDensity = max(density)
                maxDensityIndex = density.index(maxDensity)

                maxStarvation = max(starvation)
                if (maxStarvation > defaultStarvation):
                    maxStarvationIndex = starvation.index(maxStarvation)
                    activeLane = maxStarvationIndex
                else:
                    activeLane = maxDensityIndex

                timer = calcGST(density[activeLane])
            else:
                activeLane += 1
                timer = defaultMinimum
                if (activeLane == 4):
                    activeLane = 0


class Main:
#if __name__ == "__main__":
    t1 = Thread(target=vehiclesIn)
    t2 = Thread(target=greenLight)
    t3 = Thread(target=plotting)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t1.start()
    t2.start()
    t3.start()
    background = pygame.image.load('images/field.png')
    screenSize = (background.get_width(), background.get_height())
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Traffic Simulation")

    # Loading signal images and font
    redSignal = pygame.image.load('images/red.png')
    redSignal = pygame.transform.scale(redSignal, (33, 88))
    yellowSignal = pygame.image.load('images/yellow.png')
    yellowSignal = pygame.transform.scale(yellowSignal, (33, 88))
    greenSignal = pygame.image.load('images/green.png')
    greenSignal = pygame.transform.scale(greenSignal, (33, 88))

    font = pygame.font.SysFont(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #controller.shutDownAll()
                sys.exit()
        screen.blit(background, (0, 0))

        # Traffic signal
        for i in range(0, 4):
            if (i == activeLane):
                if (timer < 4):
                    screen.blit(yellowSignal, signalCoords[i])
                else:
                    screen.blit(greenSignal, signalCoords[i])
            else:
                screen.blit(redSignal, signalCoords[i])

        # Vehicle count of each lane
        for i in range(0, 4):
            d = pygame.font.SysFont(None, 60).render(
                str(lane[i]), True, (0, 0, 0), (255, 255, 255))
            screen.blit(
                d, (vehicleCountCoords[i][0], vehicleCountCoords[i][1]))

        # GST of each lane
        signalTexts = ["", "", "", ""]
        for i in range(0, 4):
            if (i == activeLane):
                signalTexts[i] = font.render(
                    str(timer), True, (0, 255, 0))
                screen.blit(signalTexts[i], signalTimerCoords[i])

        # Starvation
        timerText = font.render("Starvation: " +
                                str(starvation), True, (255, 255, 255))
        screen.blit(timerText, (50, 50))

        # Simulation runtime
        timerText = font.render("Simulation Time: " +
                                str(simulationTime)+"s", True, (255, 255, 255))
        screen.blit(timerText, (background.get_width() -
                    250, 50))

        pygame.display.update()
