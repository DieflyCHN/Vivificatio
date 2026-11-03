from anima import Anima

import time

creatura = [Anima(1)]

uidnumber = 2
try:
    while True:
        children = []
    
        for anima in creatura:
            child = anima.reproduction(uidnumber)
            if child is not False:
                children.append(child)
                print(f"  G{anima.generation}: {anima.genome["functional"]}\t UID:{anima.uid}")
                print(f"->G{child.generation}: {child.genome["functional"]}\t UID:{child.uid}")
                uidnumber += 1
            
        print("")
        creatura += children
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped")