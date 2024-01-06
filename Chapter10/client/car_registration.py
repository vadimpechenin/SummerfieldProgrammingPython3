"""
Программа-клиент для регистрации данных об автомобиле
"""
import collections
import pickle
import socket
import struct
import sys

from client.socketManager import SocketManager
from common_utils import Console

Address = ["localhost", 9653]
CarTuple = collections.namedtuple("CarTuple", "seats mileage owner")



def main():
    if len(sys.argv) > 1:
        Address[0] = sys.argv[1]
    call = dict(c=get_car_details, m=change_mileage, o=change_owner,
                n=new_registration, s=stop_server, q=quit)
    menu = ("(C)ar  Edit (M)ileage  Edit (O)wner  (N)ew car  "
            "(S)top server  (Q)uit")
    valid = frozenset("cmonsq")
    previous_license = None
    while True:
        action = Console.get_menu_choice(menu, valid, "c", True)
        previous_license = call[action](previous_license)


def retrieve_car_details(previous_license):
    #извлечь данные по автомобилю по номеру лицензии (подфункция обращения к серверу)
    license = Console.get_string("License", "license",
                                 previous_license)
    if not license:
        return previous_license, None
    license = license.upper()
    ok, *data = handle_request("GET_CAR_DETAILS", license)
    if not ok:
        print(data[0])
        return previous_license, None
    return license, CarTuple(*data)


def get_car_details(previous_license):
    # извлечь данные по автомобилю по номеру лицензии
    license, car = retrieve_car_details(previous_license)
    if car is not None:
        print("License: {0}\nSeats:   {seats}\nMileage: {mileage}\n"
              "Owner:   {owner}".format(license, **car._asdict()))
    return license


def change_mileage(previous_license):
    # изменить пробег
    license, car = retrieve_car_details(previous_license)
    if car is None:
        return previous_license
    mileage = Console.get_integer("Mileage", "mileage",
                                  car.mileage, 0)
    if mileage == 0:
        return license
    ok, *data = handle_request("CHANGE_MILEAGE", license, mileage)
    if not ok:
        print(data[0])
    else:
        print("Mileage successfully changed")
    return license


def change_owner(previous_license):
    # изменить владельца
    license, car = retrieve_car_details(previous_license)
    if car is None:
        return previous_license
    owner = Console.get_string("Owner", "owner", car.owner)
    if not owner:
        return license
    ok, *data = handle_request("CHANGE_OWNER", license, owner)
    if not ok:
        print(data[0])
    else:
        print("Owner successfully changed")
    return license


def new_registration(previous_license):
    # Новая запись (регистрация)
    license = Console.get_string("License", "license")
    if not license:
        return previous_license
    license = license.upper()
    seats = Console.get_integer("Seats", "seats", 4, 0)
    if not (1 < seats < 10):
        return previous_license
    mileage = Console.get_integer("Mileage", "mileage", 0, 0)
    owner = Console.get_string("Owner", "owner")
    if not owner:
        return previous_license
    ok, *data = handle_request("NEW_REGISTRATION", license, seats,
                               mileage, owner)
    if not ok:
        print(data[0])
    else:
        print("Car {0} successfully registered".format(license))
    return license


def quit(*ignore):
    sys.exit()


def stop_server(*ignore):
    handle_request("SHUTDOWN", wait_for_reply=False)
    sys.exit()


def handle_request(*items, wait_for_reply=True):
    #Функция для всех сетевых взаимодействий
    SizeStruct = struct.Struct("!I")
    data = pickle.dumps(items, 3) # 3 - протокол консервирования

    try:
        with SocketManager(tuple(Address)) as sock:
            #Отправка всех переданных данных, за кулисами много вызовов socket.socket.send()
            sock.sendall(SizeStruct.pack(len(data)))
            sock.sendall(data)
            #Если wait_for_reply имеет значение False, функция не ждет получения ответа от сервера и немедленно возвращает управление
            if not wait_for_reply:
                return
            #Метод для приема ответа, блокирует выполнение программы, пока не примет данные
            size_data = sock.recv(SizeStruct.size)
            #Распаковывание первых данных - количества принятых байт
            size = SizeStruct.unpack(size_data)[0]
            result = bytearray()
            while True:
                #Получение данных блоками по 4000 байт
                data = sock.recv(4000)
                if not data:
                    break
                result.extend(data)
                if len(result) >= size:
                    #По достижению размера конец распаковки
                    break
        #Распаковывание данных
        return pickle.loads(result)
    except socket.error as err:
        print("{0}: is the server running?".format(err))
        sys.exit(1)


main()