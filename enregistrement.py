
from personne import Personne
from enqueteur import Enqueteur
from suspect import Suspect
from preuve import Preuve
from enquete import Enquete

import cmd
import json
from datetime import datetime


class Enregistrer(cmd.Cmd):
    """Permet d'ajouter et de modifier les informations"""
    intro = "Bienvenue dans le système d'enregistrement. Tapez 'help' ou '?' pour lister les commandes."

    prompt = "Gestion d'enquêtes> "

    def __init__(self):
        super().__init__()
        self.dict_personnes = {}
        self.dict_enqueteurs = {}
        self.dict_suspects = {}
        self.id_personne = 1
        self.id_enqueteur = 1
        self.id_suspect = 1
        self.dict_preuves = {}
        self.id_preuve = 1
        self.dict_enquetes = {}
        self.id_enquete = 1
        self.dict_enquetes_classees = {}
        self.charger_donnees()


    def convertir_en_json(self, obj):
        """Fonction de conversion pour les objets non sérialisables en JSON."""
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        raise TypeError(f"Type d'objet non sérialisable : {type(obj)}")

    def sauvegarder_donnees(self):
        """Permet de sauvegarder les données dans le fichier json"""
        with open('donnees.json', 'w') as fichier:
            data = {
                "personnes": {id: personne.to_dict() for id, personne in self.dict_personnes.items()},
                "enqueteurs": {id: enqueteur.to_dict() for id, enqueteur in self.dict_enqueteurs.items()},
                "suspects": {id: suspect.to_dict() for id, suspect in self.dict_suspects.items()},
                "preuves": {id: preuve.toDict() for id, preuve in self.dict_preuves.items()},
                "enquetes": {id: enquete.to_dict() for id, enquete in self.dict_enquetes.items()}
            }
            json.dump(data, fichier, default=self.convertir_en_json)

    def sauvegarder_enquetes_classees(self):
        """Permet de sauvegarder les enquêtes classées dans un fichier json"""
        with open('enquetes_classees.json', 'w') as fichier:
            data = {id: enquete.to_dict() for id, enquete in self.dict_enquetes_classees.items()}
            json.dump(data, fichier, default=self.convertir_en_json)

    def charger_enquetes_classees(self):
        """Permet de charger les enquêtes classées depuis le fichier json"""
        try:
            with open('enquetes_classees.json', 'r') as fichier:
                data = json.load(fichier)

                # Charger les enquêtes classées
                self.dict_enquetes_classees = {}
                for id_enquete, enquete_data in data.items():
                    preuve_ids = enquete_data.get("preuves", [])
                    preuves = [self.dict_preuves[preuve_id] for preuve_id in preuve_ids]
                    enquete_data["preuves"] = preuves
                    self.dict_enquetes_classees[int(id_enquete)] = Enquete(**enquete_data)

                # Ajouter une déclaration print pour vérifier le chargement
                print("Enquêtes classées chargées avec succès:", self.dict_enquetes_classees)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Afficher l'erreur et initialiser le dictionnaire si le fichier n'existe pas ou est corrompu
            print(f"Erreur lors du chargement des enquêtes classées : {e}")
            self.dict_enquetes_classees = {}
            
    def charger_donnees(self):
        """Permet de charger les données depuis le fichier json"""
        try:
            with open('donnees.json', 'r') as fichier:
                data = json.load(fichier)

                # Charger les personnes
                self.dict_personnes = {}
                for id, personne_data in data.get("personnes", {}).items():
                    filtered_data = {k: v for k, v in personne_data.items() if
                                    k in ["idPersonne", "nom", "prenom", "age", "fonction"]}
                    self.dict_personnes[int(id)] = Personne(**filtered_data)

                # Charger les enquêteurs
                self.dict_enqueteurs = {int(id): Enqueteur(**enqueteur_data) for id, enqueteur_data in
                                        data.get("enqueteurs", {}).items()}
                self.id_enqueteur = max(self.dict_enqueteurs.keys(), default=0) + 1

                # Charger les suspects
                self.dict_suspects = {int(id): Suspect(**suspect_data) for id, suspect_data in
                                    data.get("suspects", {}).items()}
                self.id_suspect = max(self.dict_suspects.keys(), default=0) + 1

                # Charger les preuves
                self.dict_preuves = {int(id): Preuve(**preuve_data) for id, preuve_data in
                                    data.get("preuves", {}).items()}

                # Charger les enquêtes avec les preuves associées
                self.dict_enquetes = {}
                for id, enquete_data in data.get("enquetes", {}).items():
                    preuve_ids = enquete_data.get("preuves", [])
                    preuves = [self.dict_preuves[preuve_id["idPreuve"]] for preuve_id in preuve_ids]
                    enquete_data["preuves"] = preuves
                    self.dict_enquetes[int(id)] = Enquete(**enquete_data)
                self.id_enquete = max(self.dict_enquetes.keys(), default=0) + 1

        except (FileNotFoundError, json.JSONDecodeError):
            # Initialiser les dictionnaires et les identifiants si le fichier n'existe pas ou est corrompu
            self.dict_personnes = {}
            self.dict_enqueteurs = {}
            self.dict_suspects = {}
            self.dict_preuves = {}
            self.dict_enquetes = {}
            self.id_personne = 1
            self.id_enqueteur = 1
            self.id_suspect = 1
            self.id_preuve = 1
            self.id_enquete = 1

    def do_ajouter_personne(self, _):
        """Ajouter une personne"""
        nom = input("Nom de la personne : ")
        prenom = input("Prenom de la personne : ")
        age = input("Âge de la personne : ")
        fonction = input("Fonction de la personne : ")

        try:
            age = int(age)
        except ValueError:
            print("Erreur : L'âge doit être un nombre valide.")
            return  # Retourne immédiatement au menu principal

            # Vérification de la fonction
        if fonction not in ['suspect', 'enquêteur']:
            print("Erreur : La fonction doit être soit 'suspect' soit 'enquêteur'.")
            return  # Retourne immédiatement au menu principal



        nouvelle_personne = Personne(self.id_personne, nom, prenom, age, fonction)
        self.dict_personnes[self.id_personne] = nouvelle_personne
        print(f"Personne ajoutée avec succès. ID de la personne : {self.id_personne}")
        self.id_personne += 1
        self.sauvegarder_donnees()

    def do_afficher_personnes(self, _):
        """Afficher la liste des personnes"""
        if not self.dict_personnes:
            print("Aucune personne enregistrée.")
        else:
            for identifiant, personne in self.dict_personnes.items():
                print("----------------------------")
                print(f"ID : {identifiant}")
                print(f"Nom : {personne.nom}")
                print(f"Prenom : {personne.prenom}")
                print(f"Âge : {personne.age}")
                print(f"Fonction : {personne.fonction}")
                print("----------------------------")

    def do_ajouter_enqueteur(self, _):
        """Ajouter un enquêteur"""
        nom = input("Nom de l'enquêteur : ")
        prenom = input("Prenom de l'enquêteur : ")
        age = input("Âge de l'enquêteur : ")
        grade = input("Grade de l'enquêteur : ")

        try:
            age = int(age)
        except ValueError:
            print("Erreur : L'âge doit être un nombre valide.")
            return

        # Création et ajout de l'enquêteur
        nouvel_enqueteur = Enqueteur(self.id_personne, nom, prenom, age, self.id_enqueteur, grade, "enquêteur")
        self.dict_enqueteurs[self.id_enqueteur] = nouvel_enqueteur

        # Ajouter également dans dict_personnes
        self.dict_personnes[self.id_personne] = nouvel_enqueteur

        print(f"Enquêteur ajouté avec succès. ID de l'enquêteur : {self.id_enqueteur}, ID de la personne : {self.id_personne}")
        self.id_enqueteur += 1
        self.id_personne += 1
        self.sauvegarder_donnees()

    def do_afficher_enqueteurs(self, _):
        """Afficher la liste des enquêteurs"""
        if not self.dict_enqueteurs:
            print("Aucun enquêteur enregistré.")
        else:
            for id_enqueteur, enqueteur in self.dict_enqueteurs.items():
                print("----------------------------")
                print(f"ID Enquêteur : {id_enqueteur}")
                print(f"Nom : {enqueteur.nom}")
                print(f"Prenom : {enqueteur.prenom}")
                print(f"Âge : {enqueteur.age}")
                print(f"Grade : {enqueteur.grade}")
                print("----------------------------")
    '''
    def do_assigner_enquete(self, _):
        """Assigner une enquête à un enquêteur"""
        id_enqueteur = input("Entrez l'ID de l'enquêteur : ")
        nom_enquete = input("Entrez le nom de l'enquête à assigner : ")

        try:
            enqueteur = self.dict_enqueteurs[int(id_enqueteur)]
            enqueteur.assignerEnquete(nom_enquete)  # Supposant que nom_enquete est suffisant pour identifier l'enquête
            print("Enquête assignée avec succès.")
        except (ValueError, KeyError):
            print("ID d'enquêteur ou nom d'enquête invalide.")
    '''

    def do_modifier_enqueteur(self, _):
        """Modifier un enquêteur"""
        id_enqueteur = input("Entrez l'ID de l'enquêteur à modifier : ")
        nouveau_nom = input("Nouveau nom : ")
        nouveau_prenom = input("Nouveau prenom : ")
        nouvel_age = input("Nouvel âge : ")
        nouveau_grade = input("Nouveau grade : ")

        try:
            enqueteur = self.dict_enqueteurs[int(id_enqueteur)]
            enqueteur.modifierEnqueteur(nouveau_nom, nouveau_prenom, int(nouvel_age), nouveau_grade)
            print("Enquêteur modifié avec succès.")
            self.sauvegarder_donnees()
        except (ValueError, KeyError):
            print("ID invalide")

    def do_supprimer_enqueteur(self, _):
        """Supprimer un enquêteur"""
        id_enqueteur = input("Entrez l'ID de l'enquêteur à supprimer : ")

        try:
            id_enqueteur = int(id_enqueteur)
            if id_enqueteur in self.dict_enqueteurs:
                # Supprimer l'enquêteur du dictionnaire
                del self.dict_enqueteurs[id_enqueteur]
                print("Enquêteur supprimé avec succès.")

                self.sauvegarder_donnees()
            else:
                print("ID d'enquêteur non trouvé.")
        except ValueError:
            print("ID invalide.")

    def do_ajouter_suspect(self, _):
        """Ajouter un suspect"""
        nom = input("Nom du suspect : ")
        prenom = input("Prenom du suspect : ")
        try:
            age = int(input("Âge du suspect : "))
        except ValueError:
            print("Erreur : L'âge doit être un nombre valide.")
            return

        date_naissance = input("Date de naissance du suspect (YYYY-MM-DD) : ")
        adresse = input("Adresse du suspect : ")
        nationalite = input("Nationalité du suspect : ")
        try:
            taille = float(input("Taille du suspect (en cm) : "))
        except ValueError:
            print("Erreur : La taille doit être un nombre valide.")
            return

        adn = input("ADN du suspect : ")
        utilisateur = input("ID de l'enquêteur qui ajoute le suspect : ")
        date_incrimination = input("Date d'incrimination du suspect (YYYY-MM-DD) : ")

        id_suspect = len(self.dict_suspects) + 1
        nouveau_suspect = Suspect(
            self.id_personne, id_suspect, nom, prenom, date_naissance, age, "suspect",
            adresse, utilisateur, nationalite, taille, date_incrimination, adn
        )
        self.dict_suspects[id_suspect] = nouveau_suspect
        self.dict_personnes[self.id_personne] = nouveau_suspect

        print(f"Suspect ajouté avec succès. ID du suspect : {id_suspect}")
        self.id_suspect += 1
        self.id_personne += 1
        self.sauvegarder_donnees()

    def do_afficher_suspects(self, _):
        """Afficher la liste des suspects"""
        if not self.dict_suspects:
            print("Aucun suspect enregistré.")
            return

        for id_suspect, suspect in self.dict_suspects.items():
            print(f"-----------------------------")
            print(f"ID du suspect : {id_suspect}")
            print(f"Nom : {suspect.nom}")
            print(f"Prénom : {suspect.prenom}")
            print(f"Âge : {suspect.age}")
            print(f"Date de naissance : {suspect.dateNaissance}")
            print(f"Adresse : {suspect.adresse}")
            print(f"Nationalité : {suspect.nationalite}")
            print(f"Taille : {suspect.taille} cm")
            print(f"ADN : {suspect.adn}")
            print(f"Date d'incrimination : {suspect.dateIncrimination}")
            print(f"Enquête associée : {suspect.enqueteAssociee}")
            #print(f"Éléments incriminants : {', '.join([str(e.idPreuve) for e in suspect.elementsIncriminants])}")
            print(f"-----------------------------")

    def do_modifier_suspect(self, _):
        """Modifier un suspect"""
        id_suspect = input("Entrez l'ID du suspect à modifier : ")

        try:
            id_suspect = int(id_suspect)
            suspect = self.dict_suspects[id_suspect]

            nouveau_nom = input("Nouveau nom du suspect : ")
            nouveau_prenom = input("Nouveau prénom du suspect : ")
            nouvel_age = int(input("Nouvel âge du suspect : "))
            nouvelle_date_naissance = input("Nouvelle date de naissance du suspect (format YYYY-MM-DD) : ")
            nouvelle_adresse = input("Nouvelle adresse du suspect : ")
            nouvelle_nationalite = input("Nouvelle nationalité du suspect : ")
            nouvelle_taille = input("Nouvelle taille du suspect (en cm) : ")
            nouvel_adn = input("Nouvel ADN du suspect : ")
            nouvel_utilisateur = int(input("Nouvel ID utilisateur : "))
            nouvelle_date_incrimination = input("Nouvelle date d'incrimination du suspect (format YYYY-MM-DD) : ")

            # Utilisation de la méthode modifier_suspect
            suspect.modifier_suspect(
                nouveau_nom, nouveau_prenom, nouvel_age, nouvelle_date_naissance, nouvelle_adresse,
                nouvelle_nationalite, nouvelle_taille, nouvel_adn, nouvel_utilisateur, nouvelle_date_incrimination
            )

            print(f"Suspect avec l'ID {id_suspect} modifié avec succès.")

        except ValueError as e:
            print(f"Erreur : {e}")
        except KeyError:
            print("ID de suspect invalide.")
        except TypeError as e:
            print(f"Erreur de type : {e}")

        self.sauvegarder_donnees()

    def do_supprimer_suspect(self, _):
        """Supprimer un suspect"""

        id_suspect = input("Entrez l'ID du suspect à supprimer : ")
        try:
            id_suspect = int(id_suspect)
            if id_suspect in self.dict_suspects:
                suspect = self.dict_suspects[id_suspect]

                # Appeler la méthode de suppression du suspect
                suspect.supprimer()

                # Supprimer le suspect du dictionnaire des suspects
                del self.dict_suspects[id_suspect]

                # Supprimer le suspect du dictionnaire des personnes
                del self.dict_personnes[id_suspect]

                print(f"Suspect avec l'ID {id_suspect} supprimé avec succès.")
                self.sauvegarder_donnees()  # Sauvegarder les modifications dans le fichier JSON
            else:
                print("ID de suspect non trouvé.")
        except ValueError:
            print("ID invalide.")

    def do_ajouter_preuve(self, _):
        """Ajouter une preuve"""

        # Demander les détails de la preuve à l'utilisateur
        id_preuve = self.id_preuve
        type_preuve = input("Type de la preuve : ")
        description = input("Description de la preuve : ")
        lieu = input("Lieu de découverte de la preuve : ")

        try:
            id_utilisateur = int(input("ID de l'enquêteur qui a découvert la preuve : "))
        except ValueError:
            print("L'ID de l'enquêteur doit être un nombre entier.")
            return

        date_str = input("Date de découverte de la preuve (format YYYY-MM-DD) : ")

        # Créer une nouvelle instance de preuve
        nouvelle_preuve = Preuve(id_preuve, type_preuve, description, lieu, id_utilisateur, date_str)

        # Ajouter la preuve dans le dictionnaire
        self.dict_preuves[id_preuve] = nouvelle_preuve
        self.id_preuve += 1

        # Associer la preuve à une enquête (si une enquête est spécifiée)
        id_enquete = input("ID de l'enquête à associer (laissez vide pour ignorer) : ")
        if id_enquete and int(id_enquete) in self.dict_enquetes:
            enquete = self.dict_enquetes[int(id_enquete)]
            enquete.ajouter_preuve(nouvelle_preuve)
            print(f"Preuve ajoutée à l'enquête '{enquete.titre}' avec succès.")
            print(f"Preuve ajoutée avec succès. ID de la preuve : {id_preuve}")

        self.sauvegarder_donnees()

    def do_afficher_preuves(self, _):
        """Afficher la liste des preuves"""
        if not self.dict_preuves:
            print("Aucune preuve enregistrée.")
            return

        for id_preuve, preuve in self.dict_preuves.items():
            print("----------------------------")
            print(f"ID Preuve : {id_preuve}")
            print(f"Type : {preuve.type}")
            print(f"Description : {preuve.description}")
            print(f"Lieu : {preuve.lieu}")
            print(f"ID Utilisateur : {preuve.utilisateur}")
            print(f"Date de Découverte : {preuve.dateDecouverte}")
            if preuve.enqueteAssociee:
                print(f"Enquête Associée : {preuve.enqueteAssociee.titre}")
            else:
                print("Enquête Associée : Aucune")
            print("----------------------------")

    def do_modifier_preuve(self, _):
        """Modifier une preuve"""

        id_preuve = input("Entrez l'ID de la preuve à modifier : ")
        try:
            id_preuve = int(id_preuve)
            preuve = self.dict_preuves[id_preuve]

            nouveau_type = input("Nouveau type : ")
            nouvelle_description = input("Nouvelle description : ")
            nouveau_lieu = input("Nouveau lieu : ")
            nouvel_utilisateur = int(input("Nouvel ID utilisateur : "))
            nouvelle_date_str = input("Nouvelle date de découverte (format YYYY-MM-DD) : ")

            preuve.modifierPreuve(nouveau_type, nouvelle_description, nouveau_lieu, nouvel_utilisateur,
                                  nouvelle_date_str)
            print("Preuve modifiée avec succès.")

        except ValueError as e:
            print(f"Erreur : {e}")
        except KeyError:
            print("ID de preuve invalide.")
        except TypeError as e:
            print(f"Erreur de type : {e}")

        self.sauvegarder_donnees()

    def do_supprimer_preuve(self, _):
        """Supprimer une preuve"""

        id_preuve = input("Entrez l'ID de la preuve à supprimer : ")
        try:
            id_preuve = int(id_preuve)
            if id_preuve in self.dict_preuves:
                del self.dict_preuves[id_preuve]
                print("Preuve supprimée avec succès.")
            else:
                print("ID de preuve non trouvé.")

        except ValueError:
            print("L'ID doit être un nombre entier.")

        self.sauvegarder_donnees()

    def do_ajouter_enquete(self, _):
        """Ajouter une enquête"""

        titre = input("Titre de l'enquête : ")
        lieu = input("Lieu de l'enquête : ")
        date_debut_str = input("Date de début de l'enquête (format YYYY-MM-DD) : ")
        priorite_str = input("Priorité de l'enquête (nombre) : ")

        try:
            priorite = int(priorite_str)
        except ValueError:
            print("Erreur de saisie. Assurez-vous d'entrer une priorité numérique.")
            return

        # Créer une nouvelle instance de Enquete
        nouvelle_enquete = Enquete(self.id_enquete, titre, date_debut_str, lieu, priorite)
        self.dict_enquetes[self.id_enquete] = nouvelle_enquete
        print(f"Enquête ajoutée avec succès. ID de l'enquête : {self.id_enquete}")

        self.id_enquete += 1
        self.sauvegarder_donnees()

    def _afficher_enquete(self, id_enquete, enquete):
        """Afficher les informations d'une enquête"""

        print(f"----------------------------")
        print(f"ID Enquête : {id_enquete}")
        print(f"Titre : {enquete.titre}")
        print(f"Date de Début : {enquete.dateDebut}")
        print(f"Lieu : {enquete.lieu}")
        print(f"Statut : {enquete.statut}")
        print(f"Priorité : {enquete.priorite}")
        print(f"Preuves associées : {', '.join([str(p.idPreuve) for p in enquete.preuves])}")
        print(f"Suspects associés : {', '.join([str(s.nom) for s in enquete.suspects])}")
        if enquete.enqueteurAssocie:
            print(f"Enquêteur associé : {enquete.enqueteurAssocie.nom}")
        else:
            print("Aucun enquêteur associé.")
        print("----------------------------")
    '''
    def do_afficher_enquetes(self, _):
        """Afficher la liste des enquêtes"""
    
        if not self.dict_enquetes:
            print("Aucune enquete enregistrée.")
            return

        for id_enquete, enquete in self.dict_enquetes.items():
            print(f"----------------------------")
            print(f"ID Enquête : {id_enquete}")
            print(f"Titre : {enquete.titre}")
            print(f"Date de Début : {enquete.dateDebut}")
            print(f"Lieu : {enquete.lieu}")
            print(f"Statut : {enquete.statut}")
            print(f"Priorité : {enquete.priorite}")
            print(f"Preuves associées : {', '.join([str(p.idPreuve) for p in enquete.preuves])}")
            print(f"Suspects associés : {', '.join([str(s.nom)  for s in enquete.suspects])}")
            if enquete.enqueteurAssocie:
                print(f"Enquêteur associé : {enquete.enqueteurAssocie.nom}")
            else:
                print("Aucun enquêteur associé.")
            print("----------------------------")
    '''
    def do_afficher_enquetes(self, _):
        """Afficher la liste des enquêtes"""

        if not self.dict_enquetes:
            print("Aucune enquête enregistrée.")
            return

        for id_enquete, enquete in self.dict_enquetes.items():
            self._afficher_enquete(id_enquete, enquete)

    def do_afficher_enquetes_classees(self, _):
        """Afficher la liste des enquêtes classées"""
        if not self.dict_enquetes_classees:
            print("Aucune enquête classée enregistrée.")
            return

        for id_enquete, enquete in self.dict_enquetes_classees.items():
            print(f"----------------------------")
            print(f"ID Enquête : {id_enquete}")
            print(f"Titre : {enquete.titre}")
            print(f"Date de Début : {enquete.dateDebut}")
            print(f"Lieu : {enquete.lieu}")
            print(f"Statut : {enquete.statut}")
            print(f"Priorité : {enquete.priorite}")
            print(f"Preuves associées : {', '.join([str(p.idPreuve) for p in enquete.preuves])}")
            print(f"Suspects associés : {', '.join([str(s.nom)  for s in enquete.suspects])}")
            if enquete.enqueteurAssocie:
                print(f"Enquêteur associé : {enquete.enqueteurAssocie.nom}")
            else:
                print("Aucun enquêteur associé.")
            print("----------------------------")

    def do_modifier_enquete(self, _):
        """Modifier une enquête"""

        id_enquete = input("Entrez l'ID de l'enquête à modifier : ")
        try:
            id_enquete = int(id_enquete)
            enquete = self.dict_enquetes[id_enquete]

            nouveau_titre = input("Nouveau titre (laisser vide pour ne pas modifier) : ")
            nouveau_lieu = input("Nouveau lieu (laisser vide pour ne pas modifier) : ")
            nouveau_statut = input("Nouveau statut (laisser vide pour ne pas modifier) : ")
            nouvelle_priorite_str = input("Nouvelle priorité (laisser vide pour ne pas modifier) : ")

            if nouveau_titre:
                enquete.titre = nouveau_titre
            if nouveau_lieu:
                enquete.lieu = nouveau_lieu
            if nouveau_statut:
                enquete.statut = nouveau_statut
            if nouvelle_priorite_str:
                enquete.priorite = int(nouvelle_priorite_str)

            print("Enquête modifiée avec succès.")

        except ValueError as e:
            print(f"Erreur : {e}")
        except KeyError:
            print("ID d'enquête invalide.")

        self.sauvegarder_donnees()

    def do_supprimer_enquete(self, _):
        """Supprimer une enquête"""

        id_enquete = input("Entrez l'ID de l'enquête à supprimer : ")
        try:
            id_enquete = int(id_enquete)
            if id_enquete in self.dict_enquetes:
                del self.dict_enquetes[id_enquete]
                print("Enquête supprimée avec succès.")
            else:
                print("ID d'enquête non trouvé.")

        except ValueError:
            print("L'ID doit être un nombre entier.")

        self.sauvegarder_donnees()

    def do_classer_enquete(self, _):
        """Classer une enquête"""

        id_enquete = input("Entrez l'ID de l'enquête à classer : ")
        try:
            id_enquete = int(id_enquete)
            if id_enquete in self.dict_enquetes:
                enquete = self.dict_enquetes[id_enquete]

                # Changer le statut de l'enquête à "Classe"
                enquete.statut = "Classe"

                # Ajouter l'enquête au dictionnaire dict_enquetes_classees
                self.dict_enquetes_classees[id_enquete] = enquete

                # Supprimer l'enquête du dictionnaire dict_enquetes
                del self.dict_enquetes[id_enquete]

                print(f"Enquête avec l'ID {id_enquete} classée avec succès.")

                # Sauvegarder les modifications dans le fichier JSON principal
                self.sauvegarder_donnees()

                # Sauvegarder les enquêtes classées dans le fichier JSON distinct
                self.sauvegarder_enquetes_classees()

            else:
                print("ID d'enquête non trouvé.")
        except ValueError:
            print("ID invalide.")


    def associer_suspect_enquete(self):
        try:
            id_enquete = int(input("ID de l'enquête : "))
            id_suspect = int(input("ID du suspect à ajouter à l'enquête : "))

            # Récupérer l'enquête et le suspect en fonction de leurs identifiants
            enquete = self.dict_enquetes.get(id_enquete)
            suspect = self.dict_suspects.get(id_suspect)

            if enquete is None or suspect is None:
                print("L'enquête ou le suspect n'existe pas.")
                return

            # Associer le suspect à l'enquête
            enquete.associerSuspect(suspect)
            print(f"Suspect ajouté à l'enquête '{enquete.titre}' avec succès.")
        except ValueError:
            print("Veuillez saisir des identifiants valides.")
    
    def do_associer_enquete_enqueteur(self, _):
        """Associer une enquête à un enquêteur"""
        id_enquete = input("Entrez l'ID de l'enquête : ")
        id_enqueteur = input("Entrez l'ID de l'enquêteur : ")

        try:
            enquete = self.dict_enquetes[int(id_enquete)]
            enqueteur = self.dict_enqueteurs[int(id_enqueteur)]

            enquete.enqueteurAssocie = enqueteur
            print(f"L'enquête {enquete.titre} a été associée à l'enquêteur {enqueteur.nom} avec succès.")
            self.sauvegarder_donnees()
        except (ValueError, KeyError):
            print("ID invalide")

    def do_associer_suspect_enquete(self, arg):
        self.associer_suspect_enquete()

    def associer_preuve_enquete(self, id_preuve, id_enquete):
        """
        Associer une preuve à une enquête.

        :param id_preuve: L'identifiant de la preuve à associer.
        :param id_enquete: L'identifiant de l'enquête à laquelle associer la preuve.
        """
        try:
            preuve = self.dict_preuves[int(id_preuve)]
            enquete = self.dict_enquetes[int(id_enquete)]

            # Ajoutez la preuve à la liste des preuves associées à l'enquête
            enquete.ajouter_preuve(preuve)

            print(f"Preuve {id_preuve} associée à l'enquête {id_enquete}.")
            self.sauvegarder_donnees()

        except (ValueError, KeyError):
            print("ID de preuve ou d'enquête invalide.")

    def do_associer_preuve_enquete(self, _):
        """Associer une preuve à une enquête"""
        id_preuve = input("Entrez l'ID de la preuve : ")
        id_enquete = input("Entrez l'ID de l'enquête : ")

        self.associer_preuve_enquete(id_preuve, id_enquete)
    """
    def do_associer_suspect_enquete(self):
        id_enquete = int(input("ID de l'enquête : "))
        id_suspect = int(input("ID du suspect à ajouter à l'enquête : "))

        if id_enquete in self.dict_enquetes and id_suspect in self.dict_suspects:
            enquete = self.dict_enquetes[id_enquete]
            suspect = self.dict_suspects[id_suspect]

            enquete.associerSuspect(suspect)

            print(f"Suspect ajouté à l'enquête '{enquete.titre}' avec succès.")
        else:
            print("L'enquête ou le suspect n'existe pas.")
    """
    
    @staticmethod
    def do_fermer(_):
        """Fermer le logiciel"""
        return True

if __name__ == "__main__":
    Enregistrer().cmdloop()
