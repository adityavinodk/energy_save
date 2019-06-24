import os

class Config(object):
    DEBUG = True
    TESTING = False

class DevConfig(Config):
    ROOT_DIRECTORY_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    DATASET_PATH = os.path.join(ROOT_DIRECTORY_PATH, 'datasets')
    SECRET_KEY = 'energyiseverythingtoeveryoneforsurvival'
    PRODUCT_CATEGORIES = ['Poor: The appliance seems to be using up a lot of energy. ',
                  'OK: The appliance seems to be operating just fine. ', 'Good: The appliance is in good condition. ']
    APPLIANCES = ['dryer', 'monitor', 'washing_machine']