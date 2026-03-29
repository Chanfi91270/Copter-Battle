import pygame
import socket

PORT = 5555

class Joueur:
    def __init__(self, nom: str, server : bool):
        self.nom = nom
        self.server = server

        self.conn = None
        self.ecouteur = None
        self.connected = False

    def est_server(self):
        return self.server

    def set_join(self,ip: str=""):
        if self.est_server():
            self.ecouteur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ecouteur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ecouteur.bind(("0.0.0.0", PORT))  # écoute sur le port 5555
            self.ecouteur.listen(1)
            self.ecouteur.setblocking(False)
            print("En attente d'un joueur...")

        else:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.setblocking(False)
            try:
                self.conn.connect((ip, PORT))
            except BlockingIOError:
                pass
              

    def close_connection(self):
        if self.conn:
            self.conn.close()
        if self.ecouteur:
            self.ecouteur.close()  
