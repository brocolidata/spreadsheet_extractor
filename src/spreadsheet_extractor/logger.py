import logging

logger = logging.getLogger('annuaire_statistique_logs')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(level=logging.DEBUG)
formatter =  logging.Formatter('%(levelname)s | %(asctime)s : %(message)s', '%d/%m/%Y %H:%M:%S')
console.setFormatter(formatter)
logger.addHandler(console)