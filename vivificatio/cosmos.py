from anima import Anima

import time
import logging
logger = logging.getLogger(__name__)
import random

class anima_cfg:
    # Creatura
    CREATURA_NUMBER_LIMIT = 10000000

    # Debug time interval
    TIME_INTERVAL = 0

CFG = anima_cfg
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
    
    while len(creatura) < CFG.CREATURA_NUMBER_LIMIT:
        children = []
        survivors = []

        if len(creatura) == 0:
            logger.debug("All anima are dead!")
            return generation
                    
        for anima in creatura:
            anima.do_a_tick()
            if anima.life <= 0:
                logger.debug("G%s_UID%d is now dead.", anima.generation, anima.uid)
                continue

            survivors.append(anima)

            if anima.can_reproduce() and random.random() < anima.reproduction_willing:
                if anima.can_double_reproduce():
                    uidnumber, generation = one_child(anima, children, uidnumber, generation)
                uidnumber, generation = one_child(anima, children, uidnumber, generation)
            anima.life -= 1
        
        creatura = survivors + children
        if logger.isEnabledFor(logging.DEBUG):
            time.sleep(CFG.TIME_INTERVAL)
    return -2

def one_child(anima: Anima, children: list, uidnumber: int, generation: int) -> tuple[int, int]:
    child = anima.reproduction(uidnumber)
    children.append(child)
    logger.debug("G%s_UID%d -> G%s_UID%d",
                    child.generation - 1, child.parent_uid,
                    child.generation, child.uid)
    logger.debug("%s", child.genome["functional"])
    uidnumber += 1
    generation = max(generation, child.generation)
    return uidnumber, generation