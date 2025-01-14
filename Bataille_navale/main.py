import tkinter as tk 
import random

# Classe représentant un navire dans le jeu.
class Navire:
    def __init__(self, taille):
        self.taille = taille # Taille du navire (nombre de cases qu'il occupe sur le plateau).
        self.positions = [] # Liste des positions (x, y) occupées par le navire sur le plateau.
        self.touche = 0 # Compteur du nombre de fois que le navire a été touché.

    def est_coule(self):
         # Vérifie si le navire est coulé en comparant le nombre de touches avec sa taille.
        return self.touche == self.taille

class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [[None for _ in range(taille)] for _ in range(taille)]  # Création d'une grille vide (remplie de None).
        self.navires = [] # Liste pour stocker les navires placés sur le plateau.


    def placer_navire(self, navire, x, y, orientation):
        # Vérifie si le navire sort des limites du plateau selon son orientation.
        if (orientation == 'H' and y + navire.taille > self.taille) or (orientation == 'V' and x + navire.taille > self.taille):
            return False # Placement invalide si le navire dépasse les limites.
         
         # Vérifie si les cases nécessaires pour placer le navire sont libres.    
        for i in range(navire.taille):
            nx, ny = (x, y + i) if orientation == 'H' else (x + i, y) # Calcule les coordonnées pour chaque segment du navire.
            if self.grille[nx][ny] is not None: # Vérifie si la case est déjà occupée.
                return False # Retourne False si une case est déjà occupée.

        # Place le navire sur les cases si elles sont toutes libres.
        for i in range(navire.taille):
            nx, ny = (x, y + i) if orientation == 'H' else (x + i, y) # Calcule les coordonnées des segments.
            self.grille[nx][ny] = navire # Associe la case au navire.
            navire.positions.append((nx, ny)) # Enregistre la position dans le navire.
        self.navires.append(navire) # Ajoute le navire à la liste des navires du plateau.
        return True # Retourne True pour indiquer que le placement a réussi.

    def placer_navire_aleatoire(self, navire):
        # Tente de placer un navire à une position et orientation aléatoires jusqu'à ce qu'une position valide soit trouvée.
        while not self.placer_navire(navire, random.randint(0, self.taille - 1), random.randint(0, self.taille - 1), random.choice(['H', 'V'])):
            pass # Répète le processus tant que le placement échoue.

    def tirer(self, x, y):
        # Simule un tir sur une case donnée (x, y).
        case = self.grille[x][y] # Récupère le contenu de la case ciblée.
        if case is None:
            return "raté" # Retourne "raté" si la case est vide
        if isinstance(case, Navire): # Vérifie si la case contient un navire.
            case.touche += 1  # Incrémente le compteur de touches du navire.
            self.grille[x][y] = "touché" # Marque la case comme touchée.
            return "coulé" if case.est_coule() else "touché" # Retourne "coulé" si le navire est entièrement touché.

# Classe représentant l'application principale du jeu.
class BatailleNavaleApp:
    def __init__(self):
        self.root = tk.Tk() # Crée la fenêtre principale de l'application.
        self.root.title("Bataille Navale") # Définit le titre de la fenêtre.

        self.joueur_plateau = Plateau() # Initialise le plateau du joueur
        self.ordi_plateau = Plateau() # Initialise le plateau de l'ordinateur.
        self.navires = [Navire(t) for t in [5, 4, 3, 3, 2, 2]] # Crée une flotte de navires de différentes tailles.
        self.orientation = 'H' # Définit l'orientation initiale des navires à "Horizontale".
        self.tour_joueur = True # Indique si c'est le tour du joueur.
        self.fin_partie = False  # Indique si la partie est terminée.

        self.creer_interface()
        self.root.mainloop() # Lance la boucle principale de l'application.

    def creer_interface(self):
        self.joueur_frame = tk.LabelFrame(self.root, text="Grille Joueur") # Cadre pour la grille du joueur.
        self.joueur_frame.grid(row=0, column=0, padx=10, pady=10)
        self.ordi_frame = tk.LabelFrame(self.root, text="Grille Ordinateur")  # Cadre pour la grille de l'ordinateur.
        self.ordi_frame.grid(row=0, column=1, padx=10, pady=10)

        self.controls_frame = tk.Frame(self.root) # Cadre pour les contrôles du jeu.
        self.controls_frame.grid(row=1, column=0, columnspan=2) # Positionne le cadre en bas des grilles.

        tk.Button(self.controls_frame, text="Nouvelle Partie", command=self.nouvelle_partie).pack()  # Bouton pour démarrer une nouvelle partie.
        self.message_label = tk.Label(self.controls_frame, text="Cliquez sur 'Nouvelle Partie' pour commencer")
        self.message_label.pack() # Positionne le message dans le cadre.

        self.orientation_button = tk.Button(self.controls_frame, text="Orientation: Horizontale", command=self.changer_orientation) # Bouton pour changer l'orientation des navires.
        self.orientation_button.pack()

        self.tour_label = tk.Label(self.controls_frame, text="Tour : Joueur") # Label indiquant le tour actuel.
        self.tour_label.pack()

        self.joueur_buttons = self.creer_plateau_buttons(self.joueur_frame, self.placer_navire) # Boutons pour le plateau du joueur.
        self.ordi_buttons = self.creer_plateau_buttons(self.ordi_frame, self.tirer, state="disabled") # Boutons pour le plateau de l'ordinateur.
        
        #  affiche le statut des navires coulés.
        self.joueur_navires_coules = tk.Label(self.root, text="Navires coulés Joueur: Aucun", anchor="w")
        self.joueur_navires_coules.grid(row=2, column=0, sticky="w", padx=10)

        self.ordi_navires_coules = tk.Label(self.root, text="Navires coulés Ordinateur: Aucun", anchor="w")
        self.ordi_navires_coules.grid(row=2, column=1, sticky="w", padx=10)

    def creer_plateau_buttons(self, frame, command, state="normal"):
        buttons = []
        for x in range(10):
            row = []
            for y in range(10):
                btn = tk.Button(frame, width=2, height=1, state=state, command=lambda x=x, y=y: command(x, y))
                btn.grid(row=x, column=y)
                row.append(btn)
            buttons.append(row)
        return buttons

    def nouvelle_partie(self):
        self.navires = [Navire(t) for t in [5, 4, 3, 3, 2, 2]]
        self.message_label.config(text="Placez vos navires")
        self.tour_label.config(text="Tour : Joueur")
        self.tour_joueur = True
        self.joueur_plateau = Plateau()
        self.ordi_plateau = Plateau()
        self.fin_partie = False  # Réinitialiser l'état de la partie

        for btn_row in self.joueur_buttons:
            for btn in btn_row:
                btn.config(bg="SystemButtonFace", text="", state="normal")

        for btn_row in self.ordi_buttons:
            for btn in btn_row:
                btn.config(bg="SystemButtonFace", text="", state="disabled")

        self.joueur_navires_coules.config(text="Navires coulés Joueur: Aucun")
        self.ordi_navires_coules.config(text="Navires coulés Ordinateur: Aucun")

    def placer_navire(self, x, y):
        if self.navires:
            navire = self.navires[0]
            if self.joueur_plateau.placer_navire(navire, x, y, self.orientation):
                for nx, ny in navire.positions:
                    self.joueur_buttons[nx][ny].config(bg="gray")
                self.navires.pop(0)
                if not self.navires:
                    self.placer_navires_ordinateur()
                    self.message_label.config(text="Navires placés. À vous de tirer !")
                    self.activer_tirs()

    def placer_navires_ordinateur(self):
        for navire in [Navire(t) for t in [5, 4, 3, 3, 2, 2]]:
            self.ordi_plateau.placer_navire_aleatoire(navire)

    def changer_orientation(self):
        self.orientation = 'V' if self.orientation == 'H' else 'H'
        self.orientation_button.config(text=f"Orientation: {'Verticale' if self.orientation == 'V' else 'Horizontale'}")

    def activer_tirs(self):
        for btn_row in self.ordi_buttons:
            for btn in btn_row:
                btn.config(state="normal")

    def tirer(self, x, y):
        resultat = self.ordi_plateau.tirer(x, y)
        btn = self.ordi_buttons[x][y]
        if resultat == "raté":
            btn.config(text="O", fg="blue", state="disabled")  # Rond bleu pour un tir raté
        elif resultat == "touché":
            btn.config(text="X", fg="red", state="disabled")  # Croix rouge pour un tir touché
        elif resultat == "coulé":
            btn.config(text="X", fg="red", bg="black", state="disabled")  # Croix rouge sur fond noir pour un navire coulé
            self.mettre_a_jour_navires_coules()
        self.verifier_fin_partie()
        self.changer_tour()

    def changer_tour(self):
        self.tour_joueur = not self.tour_joueur
        if not self.tour_joueur:
            self.tour_label.config(text="Tour : Ordinateur")
            self.root.after(1000, self.tour_ordinateur)  # Attendre 1 seconde avant que l'ordinateur joue 
        else:
            self.tour_label.config(text="Tour : Joueur")

    def tour_ordinateur(self):
        cases_disponibles = [(x, y) for x in range(10) for y in range(10) if self.joueur_plateau.grille[x][y] != "touché"]
        if cases_disponibles:
            x, y = random.choice(cases_disponibles)
            resultat = self.joueur_plateau.tirer(x, y)
            btn = self.joueur_buttons[x][y]
            if resultat == "raté":
                btn.config(text="O", fg="blue", state="disabled")  # Rond bleu pour un tir raté 
            elif resultat == "touché":
                btn.config(text="X", fg="red", state="disabled")  # Croix rouge pour un tir touché
            elif resultat == "coulé":
                btn.config(text="X", fg="red", bg="black", state="disabled")  # Croix rouge sur fond noir pour un navire coulé
                self.mettre_a_jour_navires_coules()
            self.verifier_fin_partie()
            self.changer_tour()

    def mettre_a_jour_navires_coules(self):
        joueur_coules = [n.taille for n in self.ordi_plateau.navires if n.est_coule()]
        ordi_coules = [n.taille for n in self.joueur_plateau.navires if n.est_coule()]

        self.joueur_navires_coules.config(text=f"Navires coulés Joueur: {', '.join(map(str, joueur_coules)) if joueur_coules else 'Aucun'}")
        self.ordi_navires_coules.config(text=f"Navires coulés Ordinateur: {', '.join(map(str, ordi_coules)) if ordi_coules else 'Aucun'}")

    def verifier_fin_partie(self):
        if self.fin_partie:
            return  # Éviter les appels multiples 

        if all(navire.est_coule() for navire in self.ordi_plateau.navires):
            self.fin_partie = True
            self.afficher_ecran_fin("Félicitations ! Vous avez gagné !")
        elif all(navire.est_coule() for navire in self.joueur_plateau.navires):
            self.fin_partie = True
            self.afficher_ecran_fin("Dommage ! Vous avez perdu.")

    def afficher_ecran_fin(self, message):
        fin_fenetre = tk.Toplevel(self.root)
        fin_fenetre.title("Fin de Partie")
        tk.Label(fin_fenetre, text=message, font=("Arial", 16)).pack(pady=20)
        tk.Button(fin_fenetre, text="Nouvelle Partie", command=lambda: [fin_fenetre.destroy(), self.nouvelle_partie()]).pack(pady=10)

if __name__ == "__main__":
    BatailleNavaleApp()
