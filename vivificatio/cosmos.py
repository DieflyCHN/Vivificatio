from anima import Anima

import time
import logging
logger = logging.getLogger(__name__)

def cosmos():
    creatura = [Anima()]
    generation = 0
    uidnumber = 2

    logger.info("Fiat vita!")
    logger.debug("G1: %s", creatura[0].genome["functional"])
    
    while True:
        children = []

        if len(creatura) == 0:
            logger.debug("All anima are dead!")
            return generation
                    
        for anima in creatura[:]:
            if anima.life <= 0:
                logger.debug("G%s_UID%d is now dead.", anima.generation, anima.uid)
                creatura.remove(anima)
                continue

            child = anima.reproduction(uidnumber)

            if anima.can_reproduce():
                children.append(child)
                logger.debug("G%s_UID%d -> G%s_UID%d",
                              child.generation - 1, child.parent_uid,
                              child.generation, child.uid)
                logger.debug("%s", child.genome["functional"])
                uidnumber += 1
                generation = max(generation, child.generation)
            anima.life -= 1
        
        creatura += children
        if logger.isEnabledFor(logging.DEBUG):
            time.sleep(0.5)