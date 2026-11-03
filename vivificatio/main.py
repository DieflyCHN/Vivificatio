from anima import Anima

import time

def cosmos():
    creatura = [Anima(1)]
    generation = 0

    uidnumber = 2
    #print(f"G1: {creatura[0].genome["functional"]}")
    while True:
        children = []

        if len(creatura) == 0:
            #print("All anima are dead!")
            return generation
                    
        for anima in creatura[:]:
            if anima.life <= 0:
                #print(f"G{anima.generation}_UID{anima.uid} is now dead.")
                creatura.remove(anima)
                continue

            child = anima.reproduction(uidnumber)

            if child is not False:
                children.append(child)
                #print(f"G{child.generation - 1}_UID{child.parrent_uid} -> G{child.generation}_UID{child.uid}")
                #print(f"{child.genome["functional"]}")
                uidnumber += 1
                generation = max(generation, child.generation)
            anima.life -= 1
        
        #print("")
        creatura += children
        #time.sleep(0.5)

cosmos_rounds = 0
max_rounds = 100000
stat = []
try:
    for _ in range(max_rounds):
        stat.append(cosmos())
except KeyboardInterrupt:
    print("Interrupted.")

if stat:
    print(
        f"Rounds: {len(stat)}\t"
        f"Max Gen. Observed: {max(stat)}\t"
        f"Mean Max Gen.: {sum(stat) / len(stat)}"
    )