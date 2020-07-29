import random
from threading import Semaphore
from threading import Thread
import time

elves_c = 0
reindeer_c = 0
santaSem = Semaphore()
reindeerSem = Semaphore()
elfTex = Semaphore()
mutex = Semaphore(1)


def prepareSleigh():
    global reindeer_c
    print("Santa Claus: preparrando trineo")


def helpElves():
    print("Santa Claus: ayudando Elfos")


def getHitched():
    print("Este es el reno  ", reindeer_c)


def getHelp():
    print("Este es el elfo", elves_c)


def santa():
    global elves_c, reindeer_c
    print("Santa Claus: Hoho, estoy aqui")
    while True:
        santaSem.acquire()
        mutex.acquire()
        if reindeer_c >= 9:
            prepareSleigh()
            for i in range(9):
                reindeerSem.release()
            print("Santa Claus: hacer feliz a todos los niños del mundo")
            reindeer_c -= 9
            time.sleep(4)
        elif elves_c == 3:
            helpElves()
        mutex.release()


def reindeer():
    global reindeer_c
    while True:
        mutex.acquire()
        reindeer_c += 1
        if reindeer_c == 9:
            santaSem.release()
        mutex.release()
        getHitched()
        print("Reno ", reindeer_c, "esta siendo enganchado")
        reindeerSem.acquire()
        time.sleep(random.randint(2, 3))


def elves():
    global elves_c
    while True:
        elfTex.acquire()
        mutex.acquire()
        elves_c += 1
        if elves_c == 3:
            santaSem.release()
        else:
            elfTex.release()
        mutex.release()
        getHelp()
        time.sleep(random.randint(2, 5))
        mutex.acquire()
        elves_c -= 1
        if elves_c == 0:
            elfTex.release()
        mutex.release()
        print("Elfo ", elves_c, " en trabajo")


elfThread = []  # hilos para elfos
reindThread = []  # hilos para renos


def main():
    thread = Thread(target=santa)  # hilo princcipal de santa claus
    thread.start()  # empezando el hilo
    for i in range(9):
        reindThread.append(Thread(target=reindeer))
    for j in range(9):
        elfThread.append(Thread(target=elves))
    for t in elfThread:
        t.start()
    for t in reindThread:
        t.start()
    for t in elfThread:
        t.join()
    for t in reindThread:
        t.join()
    thread.join()


main()