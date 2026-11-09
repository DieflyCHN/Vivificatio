from anima import Anima

import time
import logging
logger = logging.getLogger(__name__)

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
            status, children, uidnumber, generation = anima.do_a_tick(children, uidnumber, generation)
            if status != -1:
                survivors.append(anima)
                
                
        creatura = survivors + children

        if logger.isEnabledFor(logging.DEBUG):
            time.sleep(CFG.TIME_INTERVAL)

    return -2

