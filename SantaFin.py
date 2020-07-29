import threading
import time
import random

SantaSem = threading.Semaphore(0)
ReindeerSem = threading.Semaphore(0)
ElfSemH = threading.Semaphore(3)
ElfSem = threading.Semaphore(0)

ReindeerCount = 0
ren = 0
ElvesCount = 0
elfs = 0
turn = 1

Reindeer = 9
Elves = 9
ElvesHelped = 3
TO_WAKE_UP = 7
TO_HELP = 2

ReindeerNames = ["RODOLFO", "BLITZEN", "DONDER", "CUPIDO", "COMETA", "VIXEN", "PRANCER", "DANCER", "DASHER"]
ElfNames = ["Tanos", "Aladin", "Halafarin", "Adamar", "Galateo","Estelar", "Elvis", "Alex","Jhon"]

def santa():
    global ReindeerCount
    global elfs
    global turn
    print("-----> SANTA DICE: ESTOY CANSADO")
    print("-----> SANTA DICE: VOY A DORMIR")
    for i in range(TO_WAKE_UP):
        SantaSem.acquire()
        print("-----> SANTA DICE: DESPERTE HO HO HO")
        if elfs == ElvesHelped:
            elfs = 0
            print("-----> SANTA DICE: ¿CUAL ES EL PROBLEMA?")
            for i in range(ElvesHelped):
                print("-----> SANTA AYUDA AL ELFO {} DE 3".format(i + 1))
                ElfSemH.release()
            print("-----> SANTA TERMINA SU TURNO {}".format(turn))
            turn += 1
            for i in range(ElvesHelped):
                ElfSem.release()
        elif ReindeerCount == Reindeer:
            ReindeerCount = 0
            preparesleigh()
            for i in range(Reindeer):
                ReindeerSem.release()

def reindeer():
    global ReindeerCount
    global ren

    num = ReindeerCount
    ReindeerCount += 1
    print("       {} aki!".format(ReindeerNames[num]))
    time.sleep(random.randint(5, 7))

    ren +=1
    if ren == 9:
        print("      Reno {} Soy el {}".format(ReindeerNames[num], ren))
        SantaSem.release()
    else:
        print("      Reno {} llego de vacaiones".format(ReindeerNames[num]))
    
    ReindeerSem.acquire()
    print("      {} listo y atado".format(ReindeerNames[num]))
    print("      Reno {} termino".format(ReindeerNames[num]))

def elf():
    global ElvesCount
    global elfs

    num = ElvesCount
    ElvesCount += 1
    print("Hola Soy el elfo {}".format(ElfNames[num]))

    for i in range(TO_HELP):
        time.sleep(random.randint(1,5))
        ElfSemH.acquire()
        elf = elfs + 1
        elfs += 1
        if elf < 3:
            print("Elfo {} dice: Tengo un proplema Soy el {} esperando".format(ElfNames[num], elf))
        elif elf == ElvesHelped:
            print("Elfo {} dice: Tengo un problema Soy el {} SANTAAA!".format(ElfNames[num], elf))
        ElfSem.acquire()
        print("Elfo {} esta siendo ayudado".format(ElfNames[num]))
    print("Elfo {} termino!".format(ElfNames[num]))


def preparesleigh():
    print("-----> SANTA DICE: JUEGUETES ESTAN LISTOS")
    print("-----> SANTA CARGA LOS JUGUETES")
    print("-----> SANTA DICE: HASTA LA PROXIMA NAVIDAD HO HO HO")
    print("-----> SANTA DICE: VOY A DORMIR")

def main():
    threads = []

    s = threading.Thread(target=santa)
    threads.append(s)

    for i in range(Elves):
        e = threading.Thread(target=elf)
        threads.append(e)


    for i in range(Reindeer):
        r = threading.Thread(target=reindeer)
        threads.append(r)

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

    print("LA NAVIDAD TERMINO!")

if __name__=="__main__":
    main()