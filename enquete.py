from datetime import datetime
from suspect import Suspect
from preuve import Preuve

class Enquete:
    """
    Classe représentant une enquête.

    Auteurs : 2TL2 - 2
    Date : Decembre 2023

    Attributs:
    - idEnquete (int) = L'identifiant de l'enquête.
    - titre (str) = Le titre de l'enquête
    - dateDebut (date) : La date de l'enquête
    - statut (str) : Le statut de l'enquête
    - lieu (str) = Le lieu du crime
    - priorite (int) = La priorité de l'enquête
    - preuves (list) = la liste des preuves associées à cette enquête
    - suspects (list) = la liste des suspects associées à cette enquête

    """

    dictionnaireEnquetesResolues = {}

    def __init__(self, idEnquete: int, titre: str, dateDebut: datetime, lieu: str, priorite: int,
                 statut: str = 'En cours', preuves=None, suspects=None, enqueteurs=None) -> None:
        """
        Auteur : Thibault 
        Initialise une instance de la classe Enquete.

        PRE : idEnquete et priorité doivent être des entiers
              titre,statut et lieu doivent être des chaînes de caractères
        POST : Une Enquête a été crée avec ses attributs idEnquete, titre, dateDebut, lieu, priorite qui prendront la valeur de ce qui a été passé en paramètre
        RAISE : ValueError si idEnquete ou priorite ne sont pas des entiers positifs
                ValueError si titre,statut ou lieu sont des chaînes vides
                TypeError si date n'est pas une instance de datetime.date
        """
        if not isinstance(idEnquete, int) or idEnquete <= 0:
            raise ValueError("idEnquete doit être un entier positif.")
        if not isinstance(priorite, int) or priorite <= 0:
            raise ValueError("priorite doit être un entier positif.")
        if not isinstance(titre, str) or not titre.strip():
            raise ValueError("titre ne doit pas être une chaîne vide.")
        if not isinstance(lieu, str) or not lieu.strip():
            raise ValueError("lieu ne doit pas être une chaîne vide.")
        if not isinstance(statut, str) or not statut.strip():
            raise ValueError("statut ne doit pas être une chaîne vide.")
        if not isinstance(dateDebut, datetime):
            raise TypeError("dateDebut doit être une instance de datetime.")



        self.idEnquete = idEnquete
        self.titre = titre
        self.dateDebut = dateDebut
        self.statut = statut
        self.lieu = lieu
        self.priorite = priorite
        self.preuves = preuves or []
        self.suspects = suspects or[]
        self.enqueteurAssocie = None
        self.preuves = preuves or []
        self.enqueteurs = enqueteurs or []
        self.statut = statut

    def to_dict(self) -> dict:
        """
        Convertit l'instance de Enquete en un dictionnaire pour la sérialisation JSON.

        PRE : /
        POST : Retourne un dictionnaire contenant les informations de l'enquête.
        """
        enquete_dict = {
            "idEnquete": self.idEnquete,
            "titre": self.titre,
            "dateDebut": self.dateDebut,
            "lieu": self.lieu,
            "statut": self.statut,
            "priorite": self.priorite,
            "preuves": [preuve.toDict() for preuve in self.preuves],
            "suspects": [suspect.to_dict() for suspect in self.suspects],
            "enqueteurs": [enqueteur.to_dict() for enqueteur in self.enqueteurs]
        }

        return {**enquete_dict}

    def ajouter_preuve(self, preuve) -> None:
        """
        Auteur : Léon 
        Ajoute des Preuves liées à l'enquête.
        Modifie l'attribut enqueteAssociee pour être l'idEnquete

        PRE : /
        POST : La preuve a été ajoutée à la liste des preuves de l'enquête et la valeur de 
               l'attribut enqueteAssociee prend la valeur de l'idEnquete
        RAISE : TypeError Si la preuve n'est pas une instance de Preuve
        """
        self.preuves.append(preuve)

    def associerSuspect(self, suspect) -> None:
        """
        Auteur : Léon
        Ajoute des Suspects liées à l'enquête.
        Modifie l'attribut enqueteAssociee pour être l'idEnquete

        PRE : /
        POST : Le suspect a été ajoutée à la liste des suspects de l'enquête
        RAISE : TypeError Si le suspect n'est pas une instance de Suspect
        """

        if not isinstance(suspect, Suspect):
            raise TypeError("Le suspect qui est ajouté doit être une instance de Suspect")

        if suspect.enqueteAssociee is not None:
            raise ValueError("Le suspect est déjà associé à une enquête.")

        suspect.enqueteAssociee = self.idEnquete
        self.suspects.append(suspect)

    def modifierInformations(self, titre: str = None, dateDebut: datetime = None,
                             statut: str = None, lieu: str = None, priorite: int = None) -> None:
      
        if titre is not None:
            self.titre = titre
        if dateDebut is not None:
            self.dateDebut = dateDebut
        if statut is not None:
            self.statut = statut
        if lieu is not None:
            self.lieu = lieu
        if priorite is not None:
            self.priorite = priorite

    def supprimerInformations(self) -> None:
    
        self.idEnquete = None
        self.titre = None
        self.dateDebut = None
        self.statut = None
        self.lieu = None
        self.priorite = None
        self.preuves.clear()
        self.suspects.clear()

    def classer_enquete(self):
        """Classer l'enquête"""
        self.statut = "Classé"