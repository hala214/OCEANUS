import random
from time import sleep

ships = ["Container Ships", "Bulk Carrier", "Passenger Ships", "Naval Ships"]
captured = []
def check_ships():
    return random.choice(ships)