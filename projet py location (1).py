import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import simpledialog
from tkcalendar import DateEntry
from ttkthemes import ThemedStyle
class gestion_reservation:
    def rechercher_reservation():
        nom_to_search = simpledialog.askstring("Recherche de réservation", "Veuillez entrer le CIN à rechercher:")

        if nom_to_search:
            found_item = None

            # Parcourir les items dans le Treeview
            for item in tree_reservations.get_children():
                values = tree_reservations.item(item, "values")
                if values and len(values) > 0 and nom_to_search == values[0]:
                    found_item = item
                    break

            if found_item:
                # Effacer la sélection actuelle dans le Treeview
                tree_reservations.selection_remove(tree_reservations.selection())
                # Sélectionner la ligne trouvée
                tree_reservations.selection_add(found_item)
                # Afficher la ligne trouvée dans le Treeview
                tree_reservations.see(found_item)

                # Afficher les détails de la réservation trouvée
                details_reservation = tree_reservations.item(found_item, "values")
                messagebox.showinfo("Réservation trouvée", f"Nom: {details_reservation[0]}\n"
                                                        f"Prénom: {details_reservation[1]}\n"
                                                        f"Téléphone: {details_reservation[2]}\n"
                                                        f"Matricule: {details_reservation[3]}\n"
                                                        f"Marque: {details_reservation[4]}\n"
                                                        f"Modèle: {details_reservation[5]}\n"
                                                        f"Date de début: {details_reservation[6]}\n"
                                                        f"Date de fin: {details_reservation[7]}\n"
                                                        f"Prix par jour (€): {details_reservation[8]}\n"
                                                        f"Nombre de jours: {details_reservation[9]}\n"
                                                        f"Montant Total: {details_reservation[10]}")
            else:
                messagebox.showinfo("Réservation non trouvée",
                                    f"Aucune réservation trouvée avec le nom {nom_to_search}")
    def afficher_reservations():
        tree_reservations.delete(*tree_reservations.get_children())  # Effacer les lignes existantes dans le tableau
        try:
            with open("client.txt", "r") as fichier:
                    for ligne in fichier:
                        elements = ligne.strip().split(";")
                        if len(elements) == 17:  # Vous avez mentionné 16 éléments, mais il y en a 17 dans votre écriture de fichier
                            selected_columns = [elements[i] for i in [0, 1,6, 10,9,8,13,14, 12,15,16]]
                            tree_reservations.insert("", "end", values=tuple(selected_columns))
        except FileNotFoundError:
            messagebox.showinfo("Aucune réservation", "Aucune réservation n'a été effectuée.")
    def supprimer_reservation():
        selected_item = tree_reservations.selection()

        if not selected_item:
            messagebox.showinfo("Suppression de réservation", "Veuillez sélectionner une réservation à supprimer.")
            return

        item_values = tree_reservations.item(selected_item, "values")

        if not item_values:
            messagebox.showinfo("Erreur", "Aucune valeur trouvée pour la réservation sélectionnée.")
            return

        nom_to_delete = item_values[0]  # Nom est dans la première colonne (index 0)

        # Supprimer la réservation du fichier client.txt
        with open("client.txt", "r") as client_file:
            lignes_client = client_file.readlines()

        with open("client.txt", "w") as client_file:
            for ligne in lignes_client:
                donnees = ligne.strip().split(";")
                if donnees and len(donnees) > 0 and donnees[0] != nom_to_delete:
                    client_file.write(ligne)

        # Supprimer la réservation du tableau
        tree_reservations.delete(selected_item)

        messagebox.showinfo("Suppression de réservation", "Réservation supprimée avec succès.")

    def modifier_reservation():
        selected_item = tree_reservations.selection()

        if not selected_item:
            messagebox.showinfo("Modification de réservation", "Veuillez sélectionner une réservation à modifier.")
            return

        # Obtenez les valeurs actuelles de la réservation
        valeurs_actuelles = tree_reservations.item(selected_item, 'values')

        # Affichez une boîte de dialogue pour permettre à l'utilisateur de modifier les valeurs
        nouvelles_valeurs = simpledialog.askstring("Modification de réservation", "Entrez les nouvelles valeurs séparées par des virgules (Nom, Prénom, Téléphone, Matricule, Marque, Modèle, Date de début, Date de fin, Prix par jour, Nombre de jours, Montant Total):", initialvalue=','.join(map(str, valeurs_actuelles)))

        if nouvelles_valeurs:
            # Mettez à jour les valeurs dans le tableau
            nouvelles_valeurs = nouvelles_valeurs.split(',')
            tree_reservations.item(selected_item, values=nouvelles_valeurs)

            # Mettez à jour les valeurs dans le fichier client.txt
            with open("client.txt", "r") as fichier_client:
                lignes_client = fichier_client.readlines()

            with open("client.txt", "w") as fichier_client:
                for ligne in lignes_client:
                    donnees = ligne.strip().split(";")
                    if donnees and len(donnees) > 0 and donnees[0] == valeurs_actuelles[0]:
                        fichier_client.write(';'.join(map(str, nouvelles_valeurs)) + '\n')
                    else:
                        fichier_client.write(ligne)

            messagebox.showinfo("Modification de réservation", "Réservation modifiée avec succès.")

class voiture:
    def ajouter_voiture(matricule, cout_par_jour, marque, modele, carburant, entry_matricule, entry_cout_par_jour, entry_marque, entry_modele, entry_carburant, tree):
        global numero_voiture
        # Vérifier si tous les champs sont remplis
        if not matricule or not cout_par_jour or not marque or not modele or not carburant:
            messagebox.showwarning("Champs incomplets", "Veuillez remplir tous les champs.")
            return  # Sortir de la fonction si des champs sont manquants
            # Mettre à jour le Treeview avec les données actualisées

        with open("voiture.txt", "a") as fichier:
            fichier.write(f"{numero_voiture};{matricule};{cout_par_jour};{marque};{modele};{carburant}\n")
        numero_voiture += 1
        effacer_formulaire([entry_matricule, entry_cout_par_jour, entry_marque, entry_modele, entry_carburant])
        messagebox.showinfo("Ajout réussi", "La voiture a été ajoutée avec succès.")

        # Mettre à jour le Treeview avec les données actualisées
        update_treeview(tree)
        # Mettre à jour le Treeview avec les données actualisées


        # Sauvegarder le nouveau numéro de voiture dans le fichier
        with open("numero_voiture.txt", "w") as file:
            file.write(str(numero_voiture))
    def afficher_donnees():
        # Cette fonction mettra à jour le Treeview avec les données du fichier "voiture.txt"
        tree.delete(*tree.get_children())  # Effacer toutes les lignes actuelles du Treeview
        try:
            with open("voiture.txt", "r") as fichier:
                for ligne in fichier:
                    donnees = ligne.strip().split(";")
                    tree.insert("", "end", values=donnees)
        except FileNotFoundError:
            pass  # Ignorer si le fichier n'existe pas encore
    try:                
        with open("numero_voiture.txt", "r") as file:
            numero_voiture = int(file.read())
    except FileNotFoundError:
        numero_voiture = 1  # Par défaut, si le fichier n'existe pas encore

    def supprimer_voiture():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Suppression de voiture", "Veuillez sélectionner une voiture à supprimer.")
            return

        matricule_to_delete = tree.item(selected_item, "values")[1]  # Matricule est dans la deuxième colonne (index 1)

        # Supprimer la voiture du fichier txt
        with open("voiture.txt", "r") as fichier:
            lignes = fichier.readlines()

        with open("voiture.txt", "w") as fichier:
            for ligne in lignes:
                if matricule_to_delete not in ligne:
                    fichier.write(ligne)

        # Supprimer la voiture du tableau
        tree.delete(selected_item)

        messagebox.showinfo("Suppression de voiture", "Voiture supprimée avec succès.")
    def rechercher_voiture():
        matricule_to_search = simpledialog.askstring("Recherche de voiture",
                                                    "Veuillez entrer la matricule à rechercher:")

        if matricule_to_search:
            found_item = None

            # Parcourir les items dans le Treeview
            for item in tree.get_children():
                values = tree.item(item, "values")
                if values and len(values) > 1 and matricule_to_search == values[1]:
                    found_item = item
                    break

            if found_item:
                # Effacer la sélection actuelle dans le Treeview
                tree.selection_remove(tree.selection())
                # Sélectionner la ligne trouvée
                tree.selection_add(found_item)
                # Afficher la ligne trouvée dans le Treeview
                tree.see(found_item)

                # Afficher les détails de la voiture trouvée
                details_voiture = tree.item(found_item, "values")
                messagebox.showinfo("Voiture trouvée", f"Matricule: {details_voiture[1]}\n"
                                                    f"Coût par jour: {details_voiture[2]}\n"
                                                    f"Marque: {details_voiture[3]}\n"
                                                    f"Modèle: {details_voiture[4]}\n"
                                                    f"Carburant: {details_voiture[5]}")
            else:
                messagebox.showinfo("Voiture non trouvée",
                                    f"Aucune voiture trouvée avec la matricule {matricule_to_search}")

class fair_reservation:
    
    def __init__(self, cin, permis, nom, prenom, sex, adresse, telephone, email, marque, model, matricule, couleur,cout_par_jour, date_debut, date_fin, nombre_joure):
        self.cin = cin
        self.permis = permis
        self.nom = nom
        self.prenom = prenom
        self.sex = sex
        self.adresse = adresse
        self.telephone = telephone
        self.email = email
        self.model = model
        self.marque = marque
        self.matricule = matricule
        self.couleur = couleur
        self.cout_par_jour = cout_par_jour
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_joure=nombre_joure
    def write_to_file(self):
        with open('client.txt', 'a') as file:
            file.write(f"{self.cin};")
            file.write(f"{self.permis};")
            file.write(f"{self.nom};")
            file.write(f"{self.prenom};")
            file.write(f"{self.sex};")
            file.write(f"{self.adresse};")
            file.write(f"{self.telephone};")
            file.write(f"{self.email};")
            file.write(f"{self.model};")
            file.write(f"{self.marque};")
            file.write(f"{self.matricule};")
            file.write(f"{self.couleur};")
            file.write(f"{self.cout_par_jour};")
            file.write(f"{self.date_debut};")
            file.write(f"{self.date_fin};")
            file.write(f"{self.nombre_joure};")
            file.write(f"{float(self.nombre_joure)*float(self.cout_par_jour)}\n")
    def read_from_file(tree_tous_clients):
         with open("client.txt", "r") as fichier:
                for ligne in fichier:
                    elements = ligne.strip().split(";")
                    if len(elements) == 17:  # Vous avez mentionné 16 éléments, mais il y en a 17 dans votre écriture de fichier
                        selected_columns = [elements[i] for i in [0, 1,6, 10,9,8,13,14, 12,15,16]]
                        tree_tous_clients.insert("", "end", values=tuple(selected_columns))   

def enter_data(marque_entry, model_entry, matricule_entry, couleur_entry,
               cin_entry, permis_entry, nom_entry, prenom_entry,
               sex_combobox, adresse_entry, telephone_entry, email_entry,
               cout_par_jour_entry, date_debut_entry, date_fin_entry, nombre_joure_entry):

    # Vérifier si tous les champs sont remplis
    if not (marque_entry.get() and model_entry.get() and matricule_entry.get() and couleur_entry.get() and
            cin_entry.get() and permis_entry.get() and nom_entry.get() and prenom_entry.get() and
            sex_combobox.get() and adresse_entry.get() and telephone_entry.get() and email_entry.get() and
            cout_par_jour_entry.get() and date_debut_entry.get() and date_fin_entry.get() and nombre_joure_entry.get()):

        # Afficher un message d'erreur si tous les champs ne sont pas remplis
        messagebox.showerror("Erreur de saisie", "Veuillez remplir tous les champs du formulaire.")
        return

    user_info = fair_reservation(
        cin_entry.get(),
        permis_entry.get(),
        nom_entry.get(),
        prenom_entry.get(),
        sex_combobox.get(),
        adresse_entry.get(),
        telephone_entry.get(),
        email_entry.get(),
        marque_entry.get(),
        model_entry.get(),
        matricule_entry.get(),
        couleur_entry.get(),
        cout_par_jour_entry.get(),
        date_debut_entry.get(),
        date_fin_entry.get(),
        nombre_joure_entry.get()
    )

    # Écrire les données dans le fichier
    user_info.write_to_file()

    # Effacer le formulaire
    effacer_formulaire([cin_entry, permis_entry, nom_entry, prenom_entry,
                        sex_combobox, adresse_entry, telephone_entry, email_entry,
                        marque_entry, model_entry, matricule_entry, couleur_entry,
                        cout_par_jour_entry, date_debut_entry, date_fin_entry, nombre_joure_entry])



def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_label_entry(parent, label_text, row, column):
    label = tk.Label(parent, text=label_text)
    entry = tk.Entry(parent)
    label.grid(row=row, column=column, padx=25, pady=25, sticky=tk.W)
    entry.grid(row=row, column=column + 1, padx=25, pady=25)
    return entry

def create_combobox(parent, label_text, values, row, column):
    label = tk.Label(parent, text=label_text)
    combobox = ttk.Combobox(parent, values=values)
    label.grid(row=row, column=column, padx=25, pady=25, sticky=tk.W)
    combobox.grid(row=row, column=column + 1, padx=25, pady=25)
    return combobox

def effacer_formulaire(entries):
    for entry in entries:
        entry.delete(0, tk.END)




def update_treeview(tree):
    # Effacer toutes les lignes existantes dans le Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Lire le fichier et ajouter chaque voiture au Treeview
    with open("voiture.txt", "r") as fichier:
        for ligne in fichier:
            donnees_voiture = ligne.strip().split(";")
            tree.insert("", "end", values=donnees_voiture)














def AdminPage():
    global menu_window, numero_voiture, tree ,tree_reservations # Déclarer la fenêtre, la variable et le Treeview comme globaux
    numero_voiture = 1

    global menu_window, tree  # Déclarer la fenêtre et le Treeview comme variables globales
    # Détruire la fenêtre actuelle (si elle existe)
    try:
        menu_window.destroy()
    except tk.TclError:
        pass  # Ignorer l'erreur si la fenêtre n'existe pas encore

    # Créer une nouvelle fenêtre pour la page d'administration
    admin_window = tk.Tk()
    admin_window.title("Page d'administration")

    # Activer le mode plein écran
    admin_window.attributes("-fullscreen", True)

    # Ajout du formulaire pour ajouter une voiture


    # Ligne bleue sous le titre Gestion de voiture
    canvas_gestion_voiture = tk.Canvas(admin_window, height=2, bg="blue")
    canvas_gestion_voiture.grid(row=1, column=0, columnspan=12, sticky="ew")
    label_gestion_voiture = tk.Label(admin_window, text="Gestion de voiture", font=("Arial", 16, "bold"))
    label_gestion_voiture.grid(row=1, column=6, columnspan=12, pady=10)
    canvas = tk.Canvas(admin_window, height=2, bg="blue")
    canvas.grid(row=11, column=0, columnspan=12, sticky="ew")


    # Matricule
    label_matricule = tk.Label(admin_window, text="Matricule:")
    entry_matricule = tk.Entry(admin_window)
    label_matricule.grid(row=2, column=2, padx=10, pady=10)
    entry_matricule.grid(row=2, column=3, padx=10, pady=10)

    # Coût par jour
    label_cout_par_jour = tk.Label(admin_window, text="Coût par jour:")
    entry_cout_par_jour = tk.Entry(admin_window)
    label_cout_par_jour.grid(row=3, column=2, padx=10, pady=10)
    entry_cout_par_jour.grid(row=3, column=3, padx=10, pady=10)

    # Marque
    label_marque = tk.Label(admin_window, text="Marque:")
    entry_marque = tk.Entry(admin_window)
    label_marque.grid(row=4, column=2, padx=10, pady=10)
    entry_marque.grid(row=4, column=3, padx=10, pady=10)

    # Modèle
    label_modele = tk.Label(admin_window, text="Modèle:")
    entry_modele = tk.Entry(admin_window)
    label_modele.grid(row=5, column=2, padx=10, pady=10)
    entry_modele.grid(row=5, column=3, padx=10, pady=10)

    # Carburant
    label_carburant = tk.Label(admin_window, text="Carburant:")
    combobox_carburant = ttk.Combobox(admin_window, values=["Diesel", "Essence", "Électrique"])
    label_carburant.grid(row=6, column=2, padx=10, pady=10)
    combobox_carburant.grid(row=6, column=3, padx=10, pady=10)

    # Bouton Ajouter Voiture
    btn_ajouter_voiture = tk.Button(admin_window, text="Ajouter Voiture", command=lambda: voiture.ajouter_voiture(
        entry_matricule.get(),
        entry_cout_par_jour.get(),
        entry_marque.get(),
        entry_modele.get(),
        combobox_carburant.get(),  # Obtenez la valeur sélectionnée du Combobox pour le carburant
        entry_matricule,
        entry_cout_par_jour,
        entry_marque,
        entry_modele,
        combobox_carburant,
        tree  # Passez le Treeview en tant qu'argument
    ),bg="blue", fg="white")

    btn_ajouter_voiture.grid(row=7, column=2, pady=9)

    # Ajouter le Treeview à côté du formulaire
    tree = ttk.Treeview(admin_window, columns=("Numéro", "Matricule", "Coût par jour", "Marque", "Modèle", "Carburant"),
                        show="headings")
    tree.heading("Numéro", text="Numéro")
    tree.heading("Matricule", text="Matricule")
    tree.heading("Coût par jour", text="Coût par jour")
    tree.heading("Marque", text="Marque")
    tree.heading("Modèle", text="Modèle")
    tree.heading("Carburant", text="Carburant")
    tree.grid(row=2, column=8, rowspan=6, padx=10, pady=10)

    btn_afficher_donnees = tk.Button(admin_window, text="Liste de voiture", command=voiture.afficher_donnees,bg="blue", fg="white")
    btn_afficher_donnees.grid(row=7, column=3, pady=10, padx=9)  # Placez-le à la colonne suivante

    btn_supprimer_voiture = tk.Button(admin_window, text="Supprimer Voiture", command=voiture.supprimer_voiture,bg="blue", fg="white")
    btn_supprimer_voiture.grid(row=9, column=2, pady=9)


    btn_rechercher_voiture = tk.Button(admin_window, text="Rechercher Voiture", command=voiture.rechercher_voiture,bg="blue", fg="white")
    btn_rechercher_voiture.grid(row=9, column=3, pady=10)
    canvas = tk.Canvas(admin_window, height=2, bg="blue")
    canvas.grid(row=11, column=0, columnspan=12, sticky="ew")

    def retour():
        admin_window.destroy()  # Détruire la fenêtre actuelle
        Menu()  # Revenir à la page précédente (Menu)

    # Ajout du bouton "Retour" sans arrière-plan
    retour_button = tk.Button(admin_window, text="Retour", bg="#FF3399", fg="#FFFFFF", height=2, width=10,
                              command=retour)
    retour_button.place(x=admin_window.winfo_screenwidth() - 10 - retour_button.winfo_reqwidth(),
                        y=10)  # Placement en haut à droite

    center_window(admin_window, admin_window.winfo_screenwidth(), admin_window.winfo_screenheight())  # Remplir l'écran
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12))
    style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))

    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12))
    style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))

    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

    reservation_columns = ("cin", "Prénom", "Téléphone", "Matricule", "Marque", "Modèle",
                           "Date de début", "Date de fin", "Prix par jour (€)", "Nombre de jours", "Montant Total")

    tree_reservations = ttk.Treeview(admin_window, columns=reservation_columns, show="headings", style="Treeview")

    for col in reservation_columns:
        tree_reservations.heading(col, text=col, anchor="w")
        tree_reservations.column(col, anchor="w", width=100)  # Ajustez la largeur selon vos besoins

    # Ajustez la colonne pour que le tableau s'étende de gauche à droite
    tree_reservations.grid(row=12, column=0, columnspan=12, padx=10, pady=10, sticky="nsew")

    # Configurer les poids des colonnes pour l'expansion
    for i in range(12):
        admin_window.grid_columnconfigure(i, weight=1)

    # Ajouter un titre au-dessus du tableau
    label_tableau_reservations = tk.Label(admin_window, text="Gestion de réservations", font=("Arial", 16, "bold"))
    label_tableau_reservations.grid(row=11, column=0, columnspan=12, pady=10)

    # Bouton pour afficher toutes les réservations
    btn_afficher_reservations = tk.Button(admin_window, text="Liste réservations", command=gestion_reservation.afficher_reservations,
                                          bg="blue", fg="white")
    btn_afficher_reservations.grid(row=13, column=0, columnspan=13, pady=10)
    # Bouton Supprimer Réservation
    btn_supprimer_reservation = tk.Button(admin_window, text="Supprimer Réservation", command=gestion_reservation.supprimer_reservation,
                                          bg="blue", fg="white", padx=10)
    btn_supprimer_reservation.grid(row=13, column=8, pady=10, columnspan=3)
    # Bouton Rechercher Réservation
    btn_rechercher_reservation = tk.Button(admin_window, text="Rechercher Réservation", command=gestion_reservation.rechercher_reservation,
                                           bg="blue", fg="white")
    btn_rechercher_reservation.grid(row=14, column=8, pady=10)
    btn_modifier_reservation = tk.Button(admin_window, text="Modifier Réservation", command=gestion_reservation.modifier_reservation,
                                         bg="blue", fg="white")
    btn_modifier_reservation.grid(row=14, column=0, columnspan=13, pady=10)

    admin_window.mainloop()

def NouvelleReservationPage():
    global menu_window  # Déclarer la fenêtre comme variable globale
    # Détruire la fenêtre actuelle (si elle existe)
    try:
        menu_window.destroy()
    except tk.TclError:
        pass  # Ignorer l'erreur si la fenêtre n'existe pas encore

    # Créer une nouvelle fenêtre pour la page de nouvelle réservation
    reservation_window = tk.Tk()
    reservation_window.title("Nouvelle Réservation")

    # Appliquer le thème bleu
    style = ThemedStyle(reservation_window)
    style.set_theme("aquativo")


    # Activer le mode plein écran
    reservation_window.attributes("-fullscreen", True)
    titre_label = ttk.Label(reservation_window, text="Nouvelle Réservation", font=("Helvetica", 20, "bold"), background="#3498db", foreground="white")
    titre_label.pack(fill=tk.X)
    def retour():
        reservation_window.destroy()  # Détruire la fenêtre actuelle
        Menu()  # Revenir à la page précédente

    # Ajout du bouton "Retour" sans arrière-plan
    retour_button = tk.Button(reservation_window, text="Retour", bg="#FF3399", fg="#FFFFFF", height=2, width=10,
                              command=retour)
    retour_button.place(x=reservation_window.winfo_screenwidth() - 10 - retour_button.winfo_reqwidth(),
                        y=10)  # Placement en haut à droite

    center_window(reservation_window, reservation_window.winfo_screenwidth(), reservation_window.winfo_screenheight())  # Remplir l'écran
    frame_user = tk.Frame(reservation_window)
    frame_user.pack()
    TT_user = tk.LabelFrame(frame_user, text="User Information")
    TT_user.grid(row=0, column=0)

    cin_entry = tk.Entry(TT_user)
    cin_entry.grid(row=1, column=0)
    permis_entry = tk.Entry(TT_user)
    permis_entry.grid(row=1, column=2)
    nom_entry = tk.Entry(TT_user)
    nom_entry.grid(row=1, column=1)

    prenom_entry = tk.Entry(TT_user)
    prenom_entry.grid(row=1, column=3)

    # Use ttk.Combobox for sex_combobox
    sex_combobox = ttk.Combobox(TT_user, values=["Male", "Female"])
    sex_combobox.grid(row=3, column=0)

    adresse_entry = tk.Entry(TT_user)
    adresse_entry.grid(row=3, column=1)
    telephone_entry = tk.Entry(TT_user)
    telephone_entry.grid(row=3, column=2)

    email_entry = tk.Entry(TT_user)
    email_entry.grid(row=3, column=3)

    cin_lable = tk.Label(TT_user, text="CIN")
    cin_lable.grid(row=0, column=0)
    permis_lable = tk.Label(TT_user, text="permis")
    permis_lable.grid(row=0, column=3)
    nom_lable = tk.Label(TT_user, text="nom")
    nom_lable.grid(row=0, column=1)
    prenom_lable = tk.Label(TT_user, text="prenom")
    prenom_lable.grid(row=0, column=2)
    sex_lable = tk.Label(TT_user, text="sex")
    sex_lable.grid(row=2, column=0)
    adresse_lable = tk.Label(TT_user, text="adresse")
    adresse_lable.grid(row=2, column=1)
    telephone_lable = tk.Label(TT_user, text="telephone")
    telephone_lable.grid(row=2, column=2)
    email_lable = tk.Label(TT_user, text="email")
    email_lable.grid(row=2, column=3)

    frame_car = tk.Frame(reservation_window)
    frame_car.pack(side=tk.LEFT, padx=10)

    TT_car = tk.LabelFrame(frame_user, text="Voiture Information")
    TT_car.grid(row=2, column=0)
    marque_lable = tk.Label(TT_car, text='marque')
    marque_lable.grid(row=0, column=0)
    marque_entry = tk.Entry(TT_car)
    marque_entry.grid(row=1, column=0)
    model_lable = tk.Label(TT_car, text='model')
    model_lable.grid(row=0, column=1)
    model_entry = tk.Entry(TT_car)
    model_entry.grid(row=1, column=1)
    matricule_lable = tk.Label(TT_car, text='matricule')
    matricule_lable.grid(row=0, column=2)
    matricule_entry = tk.Entry(TT_car)
    matricule_entry.grid(row=1, column=2)
    couleur_lable = tk.Label(TT_car, text='couleur')
    couleur_lable.grid(row=0, column=3)
    couleur_entry = tk.Entry(TT_car)
    couleur_entry.grid(row=1, column=3)
    frame_location = tk.Frame(reservation_window)
    frame_location.pack(side=tk.LEFT, padx=10)

    TT_location = tk.LabelFrame(frame_user, text="Location Information")
    TT_location.grid(row=3, column=0)
    cout_par_jour_lable = tk.Label(TT_location, text="cout par jour")
    cout_par_jour_lable.grid(row=0, column=0)
    cout_par_jour_entry = tk.Entry(TT_location)
    cout_par_jour_entry.grid(row=1, column=0)
    date_debut_label = tk.Label(TT_location, text="Date de début")
    date_debut_label.grid(row=0, column=2)

    date_debut_entry = DateEntry(TT_location)
    date_debut_entry.grid(row=1, column=2)

    # Ajouter une étiquette et un champ de saisie pour la date de fin
    date_fin_label = tk.Label(TT_location, text="Date de fin")
    date_fin_label.grid(row=0, column=3)

    date_fin_entry = DateEntry(TT_location)
    date_fin_entry.grid(row=1, column=3)
    nombre_joure_lable=tk.Label(TT_location,text='nombre des jour')
    nombre_joure_lable.grid(row=0,column=1)
    nombre_joure_entry=tk.Entry(TT_location)
    nombre_joure_entry.grid(row=1,column=1)
    button_save = tk.Button(frame_user, text="Confirmer le reservation ", command=lambda: [enter_data(
    marque_entry, model_entry, matricule_entry, couleur_entry,
    cin_entry, permis_entry, nom_entry, prenom_entry,
    sex_combobox, adresse_entry, telephone_entry, email_entry,
    cout_par_jour_entry, date_debut_entry, date_fin_entry, nombre_joure_entry),
    effacer_formulaire([cin_entry, permis_entry, nom_entry, prenom_entry,
                        sex_combobox, adresse_entry, telephone_entry, email_entry,
                        marque_entry, model_entry, matricule_entry, couleur_entry,
                        cout_par_jour_entry, date_debut_entry, date_fin_entry, nombre_joure_entry])])

    button_save.grid(row=4, column=0, sticky="news", padx=20, pady=20)

    button_afiche = tk.Button(frame_user, text="Liste des reservation", command=lambda:afficher_tous_clients())
    button_afiche.grid(row=5, column=0, sticky="news", padx=20, pady=20)
    for frame in [frame_user, frame_car, frame_location]:
        frame.configure(borderwidth=2, relief="solid", padx=10, pady=10, background="#ecf0f1")

    # Styliser les labels avec une couleur de fond
    for label in [TT_user, TT_car, TT_location]:
        label.configure(background="#3498db", foreground="white")
    def afficher_tous_clients():
        TT_car = tk.LabelFrame(frame_user, text="Affichage des informations", bg="#3498db", fg="white")
        TT_car.grid(row=6, column=0, pady=10, padx=10, sticky="nsew")

        # Définir les colonnes à afficher
        ID = ("CIN", "Prénom", "Téléphone", "Matricule", "Marque", "Modèle",
            "Date de début", "Date de fin", "Prix par jour (€)", "Nombre de jours", "Montant Total")

        tree_tous_clients = ttk.Treeview(TT_car, columns=ID, show="headings", style="Treeview")

        for col in ID:
            tree_tous_clients.heading(col, text=col)

        tree_tous_clients.grid(row=0, column=0, sticky="nsew")

        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(TT_car, orient="vertical", command=tree_tous_clients.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree_tous_clients.configure(yscrollcommand=scrollbar.set)

        # Ajuster la largeur des colonnes
        for col in ID:
            tree_tous_clients.column(col, width=105)  # Vous pouvez ajuster cette valeur en fonction de la longueur du texte

        # Lire toutes les lignes du fichier et afficher les clients
        try:
            fair_reservation.read_from_file(tree_tous_clients)
        except FileNotFoundError:
            messagebox.showinfo("Fichier introuvable", "Le fichier client.txt n'a pas été trouvé.")

    # Ajouter un style pour le Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#3498db", foreground="white", fieldbackground="#3498db")
    style.map("Treeview", background=[('selected', '#3498db')])

# Appeler la fonction afficher_tous_clients() après la création de l'interface graphique
# afficher_tous_clients()

def fermer_application():
    menu_window.destroy()
def compter_reservations():
    try:
        with open("client.txt", "r") as fichier:
            nombre_reservations = sum(1 for _ in fichier)
        return nombre_reservations
    except FileNotFoundError:
        return 0
def compter_voitures():
    try:
        with open("voiture.txt", "r") as fichier:
            nombre_voitures = sum(1 for _ in fichier)
        return nombre_voitures
    except FileNotFoundError:
        return 0  # Retourne 0 si le fichier n'existe pas
def calculer_chiffre_affaires():
    try:
        with open("client.txt", "r") as fichier:
            chiffre_affaires = sum(float(ligne.strip().split(";")[-1]) for ligne in fichier)
        return chiffre_affaires
    except (FileNotFoundError, ValueError):
        return 0.0



def Menu():
    global menu_window  # Déclarer la fenêtre comme variable globale
    # Détruire la fenêtre actuelle (si elle existe)
    try:
        window.destroy()
    except tk.TclError:
        pass  # Ignorer l'erreur si la fenêtre n'existe pas encore

    # Créer une nouvelle fenêtre
    menu_window = tk.Tk()
    menu_window.title(" le Tableau de bord ")  # Titre du tableau de bord
    background_image = Image.open("background2.jpg")
    background_photo = ImageTk.PhotoImage(background_image)

# Créer une étiquette pour contenir l'image d'arrière-plan
    background_label = tk.Label(menu_window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # Activer le mode plein écran
    menu_window.attributes("-fullscreen", True)

    # Configurer le fond d'écran
    menu_window.config(background="#000000")

    # Définir le thème "clam" avec des couleurs personnalisées
    style = ttk.Style(menu_window)
    style.theme_use("clam")
    style.configure('TButton',  background='#0000FF', font=('Arial', 16))

    # Bouton "Deconnexion" en haut à droite de l'écran
    deconnexion_button = tk.Button(menu_window, text="Deconnexion", bg="#FF0000", fg="#FFFFFF", height=2, width=15,
                                   command=fermer_application)
    deconnexion_button.place(x=menu_window.winfo_screenwidth() - 150, y=10)  # Placement en haut à droite

    # Cadre principal pour le tableau de bord
    dashboard_frame = tk.Frame(menu_window, bg='#000000')

    # Titre du tableau de bord avec un fond bleu à la taille de l'écran
    title_label = tk.Label(dashboard_frame, text="Bienvenue sur votre Tableau de bord", font=("Arial", 24, "bold"), bg='#0000FF', fg='#ffffff', pady=5)
    title_label.pack(fill='x')

    # Bloc pour afficher le nombre de réservations
    reservations_frame = tk.Frame(dashboard_frame, bg='#87CEEB', bd=5, relief="groove")  # Couleur de fond bleu clair
    reservations_frame.pack(side='left', padx=8)

    # Titre pour le bloc des réservations avec un fond bleu
    reservations_title = tk.Label(reservations_frame, text="Nombre de réservations", font=("Arial", 18, "bold"),
                                  bg='#0000FF', fg='#ffffff')  # Couleur de fond bleu
    reservations_title.pack(pady=(10, 20))  # Ajouter de l'espace vertical après le titre

    # Donnée pour le nombre de réservations
    label_nombre_reservations = tk.Label(reservations_frame, text=f"{compter_reservations()}",
                                         font=("Arial", 18),
                                         bg='#87CEEB')  # Couleur de fond bleu clair
    label_nombre_reservations.pack(pady=10)

    # Espace entre les blocs
    tk.Label(dashboard_frame, text="", bg='#ffffff').pack(side='left', padx=20)

    # Bloc pour afficher le nombre de voitures
    voitures_frame = tk.Frame(dashboard_frame, bg='#87CEEB', bd=5, relief="groove")  # Couleur de fond bleu clair
    voitures_frame.pack(side='left', padx=20)

    # Titre pour le bloc des voitures avec un fond bleu
    voitures_title = tk.Label(voitures_frame, text="Nombre de voitures", font=("Arial", 18, "bold"),
                               bg='#0000FF', fg='#ffffff')  # Couleur de fond bleu
    voitures_title.pack(pady=(10, 20))  # Ajouter de l'espace vertical après le titre

    # Donnée pour le nombre de voitures
    label_nombre_voitures = tk.Label(voitures_frame, text=f"{compter_voitures()}", font=("Arial", 18),
                                     bg='#87CEEB')  # Couleur de fond bleu clair
    label_nombre_voitures.pack(pady=10)

    # Espace entre les blocs
    tk.Label(dashboard_frame, text="", bg='#ffffff').pack(side='left', padx=20)

    # Bloc pour afficher le chiffre d'affaires
    chiffre_affaires_frame = tk.Frame(dashboard_frame, bg='#87CEEB', bd=5, relief="groove")  # Couleur de fond bleu clair
    chiffre_affaires_frame.pack(side='left', padx=15)

    # Titre pour le bloc du chiffre d'affaires avec un fond bleu
    chiffre_affaires_title = tk.Label(chiffre_affaires_frame, text="Chiffre d'affaires total", font=("Arial", 18, "bold"),
                                      bg='#0000FF', fg='#ffffff')  # Couleur de fond bleu
    chiffre_affaires_title.pack(pady=(10, 20))  # Ajouter de l'espace vertical après le titre

    # Donnée pour le chiffre d'affaires
    label_chiffre_affaires = tk.Label(chiffre_affaires_frame, text=f"{calculer_chiffre_affaires()} €",
                                      font=("Arial", 18),
                                      bg='#87CEEB')  # Couleur de fond bleu clair
    label_chiffre_affaires.pack(pady=10)

    dashboard_frame.pack()

    # Boutons "Admin" et "Nouvelle réservation" avec un style personnalisé
    admin_button = ttk.Button(menu_window, text="Administrateur", command=AdminPage)
    reservation_button = ttk.Button(menu_window, text="Nouvelle réservation", command=NouvelleReservationPage)

    # Configuration du style personnalisé pour les boutons
    button_style = ttk.Style()

    # Pour le bouton "Admin"
    button_style.configure(
        "Admin.TButton",  # Nom du style
        foreground="white",  # Couleur du texte
        font=("Helvetica", 14, "bold")  # Police et taille du texte
    )

    # Appliquer le style au bouton "Admin"
    admin_button.configure(style="Admin.TButton")

    # Pour le bouton "Nouvelle réservation"
    button_style.configure(
        "Reservation.TButton",  # Nom du style
        foreground="white",  # Couleur du texte
        font=("Helvetica", 14, "bold")  # Police et taille du texte
    )

    # Appliquer le style au bouton "Nouvelle réservation"
    reservation_button.configure(style="Reservation.TButton")

    # Utiliser pack pour placer les boutons en bas et au centre de l'écran
    admin_button.pack(side='bottom', pady=20, ipadx=20, ipady=10, anchor='s')
    reservation_button.pack(side='bottom', pady=20, ipadx=20, ipady=10, anchor='s')

    # Utiliser grid pour centrer les boutons horizontalement
    menu_window.grid_columnconfigure(0, weight=1)
    menu_window.grid_columnconfigure(0, weight=1)
    menu_window.mainloop()



window = tk.Tk()
window.title("Login Form")

# Activer le mode plein écran pour la fenêtre de login
window.attributes("-fullscreen", True)

# Charger l'image d'arrière-plan
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Créer une étiquette pour contenir l'image d'arrière-plan
background_label = tk.Label(window, image=background_photo)
background_label.place(relwidth=1, relheight=1)

def login():
    username = 'tariq'
    password = 'tariq'
    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="Login Success", message="Hello Mr.Mazen")
        Menu()
    else:
        messagebox.showinfo(title="Login not Success", message="You have 3 more tries")

# Utiliser une couleur transparente pour le cadre
login_label = tk.Label(window, text="Login", fg="#FFFFFF", font=("Arial", 30), bg='#333333')
username_label = tk.Label(window, text="Username", fg="#FFFFFF", font=("Arial", 16), bg='#333333')
username_entry = tk.Entry(window, font=("Arial", 16))
password_entry = tk.Entry(window, show="*", font=("Arial", 16))
password_label = tk.Label(window, text="Password", fg="#FFFFFF", font=("Arial", 16), bg='#333333')
login_button = tk.Button(window, text="Login", bg="#FF3399", fg="#FFFFFF", command=login)

login_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
username_label.grid(row=1, column=0, pady=20)
username_entry.grid(row=1, column=1, pady=20, padx=10, sticky="w")
password_label.grid(row=2, column=0, pady=20)
password_entry.grid(row=2, column=1, pady=20, padx=10, sticky="w")
login_button.grid(row=3, column=0, columnspan=2, pady=30)

window.mainloop()