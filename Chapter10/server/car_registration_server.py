"""
Серверная часть. Главный файл запуска
"""
import contextlib
import gzip
import os
import pickle
import random
import sys

from server.car import Car
from server.carRegistrationServer import CarRegistrationServer
from server.requestHandler import RequestHandler


def save(filename, cars):
    try:
        with contextlib.closing(gzip.open(filename, "wb")) as fh:
            pickle.dump(cars, fh, 3)
    except (EnvironmentError, pickle.UnpicklingError) as err:
        print("server failed to save data: {0}".format(err))
        sys.exit(1)


def load(filename):
    if not os.path.exists(filename):
        # Генерация начальных данных для сервера
        cars = {}
        owners = []
        for forename, surname in zip(("Warisha", "Elysha", "Liona",
                                      "Kassandra", "Simone", "Halima", "Liona", "Zack",
                                      "Josiah", "Sam", "Braedon", "Eleni"),
                                     ("Chandler", "Drennan", "Stead", "Doole", "Reneau",
                                      "Dent", "Sheckles", "Dent", "Reddihough", "Dodwell",
                                      "Conner", "Abson")):
            owners.append(forename + " " + surname)
        for license in ("1H1890C", "FHV449", "ABK3035", "215 MZN",
                        "6DQX521", "174-WWA", "999991", "DA 4020", "303 LNM",
                        "BEQ 0549", "1A US923", "A37 4791", "393 TUT", "458 ARW",
                        "024 HYR", "SKM 648", "1253 QA", "4EB S80", "BYC 6654",
                        "SRK-423", "3DB 09J", "3C-5772F", "PYJ 996", "768-VHN",
                        "262 2636", "WYZ-94L", "326-PKF", "EJB-3105", "XXN-5911",
                        "HVP 283", "EKW 6345", "069 DSM", "GZB-6052", "HGD-498",
                        "833-132", "1XG 831", "831-THB", "HMR-299", "A04 4HE",
                        "ERG 827", "XVT-2416", "306-XXL", "530-NBE", "2-4JHJ"):
            mileage = random.randint(0, 100000)
            seats = random.choice((2, 4, 5, 6, 7))
            owner = random.choice(owners)
            cars[license] = Car(seats, mileage, owner)
        return cars
        # return {}
    try:
        with contextlib.closing(gzip.open(filename, "rb")) as fh:
            return pickle.load(fh)
    except (EnvironmentError, pickle.UnpicklingError) as err:
        print("server cannot load data: {0}".format(err))
        sys.exit(1)


def main():
    filename = os.path.join(os.path.dirname(__file__),
                            "car_registrations.dat")
    cars = load(filename)
    print("Loaded {0} car registrations".format(len(cars)))
    RequestHandler.Cars = cars
    server = None
    try:
        server = CarRegistrationServer(("", 9653), RequestHandler)
        server.serve_forever()
    except Exception as err:
        print("ERROR", err)
    finally:
        if server is not None:
            server.shutdown()
            save(filename, cars)
            print("Saved {0} car registrations".format(len(cars)))


main()