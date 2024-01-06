"""
Класс для реализации методов обработки запросов клиента +
обязательный метод handle, который вызывается классом сервера
"""
import copy
import pickle

from server.car import Car
from server.finish import Finish
import threading
import socketserver
import struct


class RequestHandler(socketserver.StreamRequestHandler):
    #Блокировки для словарей Cars и Call
    CarsLock = threading.Lock()
    CallLock = threading.Lock()
    #Главный словарь, который используется для выполнения работы и формирования ответов на запросы клиентов
    #Методы непосредственно мы использовать не можем, потому еще есть атрибут self
    Call = dict(
        GET_CAR_DETAILS=(
            lambda self, *args: self.get_car_details(*args)),
        CHANGE_MILEAGE=(
            lambda self, *args: self.change_mileage(*args)),
        CHANGE_OWNER=(
            lambda self, *args: self.change_owner(*args)),
        NEW_REGISTRATION=(
            lambda self, *args: self.new_registration(*args)),
        SHUTDOWN=lambda self, *args: self.shutdown(*args))

    def handle(self):
        #Метод для обработки запросов
        #Всякий раз, когда клиент выполняет запрос, создается новый поток
        #с новым экземпляром класса RequestHandler, после чего вызывается данных метод.
        #Внутри данного метода данные, полученные от клиента, читаются с помощью объекта файла self.rfile,
        # а отправка данных выполнена с помощью объекта файла self.wfile, предоставленных socketserver
        SizeStruct = struct.Struct("!I") #Целочисленный счетчик байтов, необходимый для чтения формата "длина + данные"
        size_data = self.rfile.read(SizeStruct.size)
        size = SizeStruct.unpack(size_data)[0]
        data = pickle.loads(self.rfile.read(size))

        try:
            with RequestHandler.CallLock:
                function = self.Call[data[0]]
            reply = function(self, *data[1:])
        except Finish:
            return
        data = pickle.dumps(reply, 3)
        self.wfile.write(SizeStruct.pack(len(data)))
        self.wfile.write(data)

    def get_car_details(self, license):
        with RequestHandler.CarsLock:
            car = copy.copy(self.Cars.get(license, None))
        if car is not None:
            return (True, car.seats, car.mileage, car.owner)
        return (False, "This license is not registered")

    def change_mileage(self, license, mileage):
        if mileage < 0:
            return (False, "Cannot set a negative mileage")
        with RequestHandler.CarsLock:
            car = self.Cars.get(license, None)
            if car is not None:
                if car.mileage < mileage:
                    car.mileage = mileage
                    return (True, None)
                return (False, "Cannot wind the odometer back")
        return (False, "This license is not registered")

    def change_owner(self, license, owner):
        if not owner:
            return (False, "Cannot set an empty owner")
        with RequestHandler.CarsLock:
            car = self.Cars.get(license, None)
            if car is not None:
                car.owner = owner
                return (True, None)
        return (False, "This license is not registered")

    def new_registration(self, license, seats, mileage, owner):
        if not license:
            return (False, "Cannot set an empty license")
        if seats not in {2, 4, 5, 6, 7, 8, 9}:
            return (False, "Cannot register car with invalid seats")
        if mileage < 0:
            return (False, "Cannot set a negative mileage")
        if not owner:
            return (False, "Cannot set an empty owner")
        with RequestHandler.CarsLock:
            if license not in self.Cars:
                self.Cars[license] = Car(seats, mileage, owner)
                return (True, None)
        return (False, "Cannot register duplicate license")

    def shutdown(self, *ignore):
        self.server.shutdown()
        raise Finish()