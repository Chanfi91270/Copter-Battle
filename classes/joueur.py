import pygame
import socket
import json

PORT = 5555


class Joueur:

    def __init__(self, nom: str, numero: int, server: bool):
        self.nom = nom
        self.numero = numero
        self.server = server

        self.helico = None

        self.score = 0
        self.parties_jouees = 0
        self.victoires = 0
        self.defaites = 0

        self.vivant = True
        self.pret = False

        self.conn = None
        self.ecouteur = None
        self.connected = False
        self._buffer = ""

        self.dernier_etat = None

        self.touches_distantes = {
            "gauche": False, "droite": False,
            "haut": False, "bas": False, "bonus": False
        }

    def set_helico(self, helico) -> None:
        self.helico = helico

    def est_server(self) -> bool:
        return self.server

    def est_vivant(self) -> bool:
        if self.helico is None:
            return False
        return self.helico.lives > 0

    def get_vies(self) -> int:
        return self.helico.lives if self.helico else 0

    def get_bonus_actif(self) -> str | None:
        if self.helico is None:
            return None
        if self.helico.bonus_bombes:
            return "bombe"
        if self.helico.bonus_rafale:
            return "rafale"
        if self.helico.bonus_shield:
            return "bouclier"
        return None


    def ajouter_score(self, points: int) -> None:
        self.score += points

    def enregistrer_victoire(self) -> None:
        self.victoires += 1
        self.parties_jouees += 1

    def enregistrer_defaite(self) -> None:
        self.defaites += 1
        self.parties_jouees += 1

    def reinitialiser_partie(self, x: int, y: int) -> None:
        self.score = 0
        self.vivant = True
        self.pret = False
        self.dernier_etat = None
        self.touches_distantes = {
            "gauche": False, "droite": False,
            "haut": False, "bas": False, "bonus": False
        }
        if self.helico is not None:
            self.helico.lives = 3
            self.helico.rect.topleft = (x, y)
            self.helico.bonus_shield = False
            self.helico.bonus_bombes = False
            self.helico.bonus_rafale = False
            self.helico.set_transparency(False)
            self.helico.transparent_until = 0
            self.helico.shield_visual_until = 0
            self.helico.pending_bonus = None
            self.helico.bonus_key_was_pressed = False


    def update(self, screen_width: int, screen_height: int) -> None:
        if self.helico is not None and self.est_vivant():
            self.helico.move(screen_width, screen_height)

    def dessiner(self, screen: pygame.Surface, img_bulle_bouclier: pygame.Surface) -> None:
        if self.helico is None:
            return
        screen.blit(self.helico.image, self.helico.rect)
        if self.helico.shield_visual_active():
            bulle_rect = img_bulle_bouclier.get_rect(center=self.helico.rect.center)
            screen.blit(img_bulle_bouclier, bulle_rect)


    def set_join(self, ip: str = "") -> None:
        if self.est_server():
            self.ecouteur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ecouteur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ecouteur.bind(("0.0.0.0", PORT))
            self.ecouteur.listen(1)
            self.ecouteur.setblocking(False)
            print(f"[{self.nom}] En attente d'un joueur sur le port {PORT}...")
        else:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.setblocking(False)
            try:
                self.conn.connect((ip, PORT))
            except BlockingIOError:
                pass

    def accepter_connexion(self) -> bool:
        if not self.est_server() or self.connected:
            return self.connected
        try:
            conn, addr = self.ecouteur.accept()
            conn.setblocking(False)
            self.conn = conn
            self.connected = True
            print(f"[{self.nom}] Joueur connecté depuis {addr}")
        except BlockingIOError:
            pass
        return self.connected

    def verifier_connexion(self) -> bool:
        if self.est_server() or self.connected:
            return self.connected
        try:
            self.conn.getpeername()
            self.connected = True
            print(f"[{self.nom}] Connecté au serveur.")
        except OSError:
            pass
        return self.connected

    def close_connection(self) -> None:
        if self.conn:
            try:
                self.conn.close()
            except OSError:
                pass
            self.conn = None
        if self.ecouteur:
            try:
                self.ecouteur.close()
            except OSError:
                pass
            self.ecouteur = None
        self.connected = False


    def envoyer(self, donnees: dict) -> None:
        if self.conn is None or not self.connected:
            return
        try:
            message = json.dumps(donnees) + "\n"
            self.conn.sendall(message.encode("utf-8"))
        except (OSError, BrokenPipeError) as e:
            print(f"[{self.nom}] Erreur envoi : {e}")
            self.connected = False

    def recevoir(self) -> list[dict]:
        messages = []
        if self.conn is None or not self.connected:
            return messages
        try:
            data = self.conn.recv(8192).decode("utf-8")
            if not data:
                self.connected = False
                return messages
            self._buffer += data
            while "\n" in self._buffer:
                ligne, self._buffer = self._buffer.split("\n", 1)
                ligne = ligne.strip()
                if ligne:
                    try:
                        messages.append(json.loads(ligne))
                    except json.JSONDecodeError as e:
                        print(f"[{self.nom}] JSON invalide : {e}")
        except BlockingIOError:
            pass
        except OSError as e:
            print(f"[{self.nom}] Erreur réception : {e}")
            self.connected = False
        return messages


    def envoyer_touches(self, touches_dict: dict) -> None:
        self.envoyer({"type": "touches", "touches": touches_dict})

    def envoyer_etat(self, helico1, helico2, obstacles) -> None:
        
        etat = {
            "type": "etat",
            "h1": {
                "x": helico1.rect.x,
                "y": helico1.rect.y,
                "vies": helico1.lives,
                "transparent": helico1.is_transparent,
                "shield_visuel": helico1.shield_visual_active(),
                "bonus": self._bonus_helico(helico1),
            },
            "h2": {
                "x": helico2.rect.x,
                "y": helico2.rect.y,
                "vies": helico2.lives,
                "transparent": helico2.is_transparent,
                "shield_visuel": helico2.shield_visual_active(),
                "bonus": self._bonus_helico(helico2),
            },
            "obstacles": [
                {
                    "x": o.hitbox.x,
                    "y": o.hitbox.y,
                    "w": o.hitbox.width,
                    "h": o.hitbox.height,
                    "armed": o.armed,
                    "projectiles": [
                        {"x": p.x, "y": p.y, "w": p.width, "h": p.height}
                        for p in o.projectiles
                    ],
                }
                for o in obstacles
            ],
        }
        self.envoyer(etat)

    def recevoir_touches(self) -> None:
        
        for msg in self.recevoir():
            if msg.get("type") == "touches":
                self.touches_distantes = msg["touches"]

    def recevoir_etat(self) -> dict | None:
        
        etat = None
        for msg in self.recevoir():
            if msg.get("type") == "etat":
                etat = msg
        if etat:
            self.dernier_etat = etat
        return etat


    @staticmethod
    def _bonus_helico(helico) -> str | None:
        if helico.bonus_bombes:
            return "bombe"
        if helico.bonus_rafale:
            return "rafale"
        if helico.bonus_shield:
            return "bouclier"
        return None


    def __repr__(self) -> str:
        role = "Serveur" if self.server else "Client"
        return (
            f"Joueur(nom={self.nom!r}, numero={self.numero}, role={role}, "
            f"vies={self.get_vies()}, score={self.score}, "
            f"V={self.victoires}/D={self.defaites})"
        )