from anima import Anima

import time

creatura = [Anima(1)]

uidnumber = 2
print(f"G1: {creatura[0].genome["functional"]}")
try:
    while True:
        children = []

        if len(creatura) == 0:
            print("All anima are dead!")
            break
    
        for anima in creatura[:]:
            child = anima.reproduction(uidnumber)
            if anima.life <= 0:
                print(f"G{anima.generation}_UID{anima.uid} is now dead.")
                creatura.remove(anima)
            else:
                if child is not False:
                    children.append(child)
                    print(f"G{child.generation - 1}_UID{child.parrent_uid} -> G{child.generation}_UID{child.uid}")
                    print(f"{child.genome["functional"]}")
                    uidnumber += 1
                anima.life -= 1
            
        print("")
        creatura += children
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped")