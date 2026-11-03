from anima import Anima

import time
import logging
logger = logging.getLogger(__name__)

def cosmos() -> int:
    """
    return: max generation of this cosmos.\n
    -1: G1 can't reproduct. Please check can_reproduce() and settings.\n
    -2: Interrupted because the number of creatura > 100000.
    """
    creatura = [Anima()]
    generation = 1
    uidnumber = 2

    logger.info("Fiat vita!")
    logger.debug("G1: %s", creatura[0].genome["functional"])

    if not creatura[0].can_reproduce():
        logger.warning("G1 can't reproduct. Please check can_reproduce() and settings.")
        return -1
    
    while len(creatura) < 100000:   # Can be a config
        children = []
        survivors = []

        if len(creatura) == 0:
            logger.debug("All anima are dead!")
            return generation
                    
        for anima in creatura:
            if anima.life <= 0:
                logger.debug("G%s_UID%d is now dead.", anima.generation, anima.uid)
                continue

            survivors.append(anima)

            if anima.can_reproduce():
                child = anima.reproduction(uidnumber)
                children.append(child)
                logger.debug("G%s_UID%d -> G%s_UID%d",
                              child.generation - 1, child.parent_uid,
                              child.generation, child.uid)
                logger.debug("%s", child.genome["functional"])
                uidnumber += 1
                generation = max(generation, child.generation)
            anima.life -= 1
        
        creatura = survivors + children
        if logger.isEnabledFor(logging.DEBUG):
            time.sleep(0.5)
    return -2