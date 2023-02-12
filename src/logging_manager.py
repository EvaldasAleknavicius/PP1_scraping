import logging
import yaml

with open('config/config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

logging.basicConfig(
    filename=config['logging']['filename'],
    level=config['logging']['level'],
    format=config['logging']['format'],
    datefmt=config['logging']['datefmt'],
)

def o_info(msg):
    logging.info(msg)

