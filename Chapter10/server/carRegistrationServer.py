import socketserver


class CarRegistrationServer(socketserver.ThreadingMixIn,
                            socketserver.TCPServer): pass