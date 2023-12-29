from personne import Personne
from datetime import datetime
class Suspect(Personne):
    def __init__(self, idPersonne: int, idSuspect: int, nom: str, prenom: str, dateNaissance: datetime, age: int, fonction: str,
                 adresse: str, utilisateur: int, nationalite: str, taille: int, dateIncrimination: datetime, adn: str, enqueteAssociee=None, PreuvesIncriminants: list = None):
        if not isinstance(idPersonne, int) or idPersonne <= 0:
            raise ValueError("idPersonne doit être un entier positif.")
        if not isinstance(idSuspect, int) or idSuspect <= 0:
            raise ValueError("idSuspect doit être un entier positif.")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("age doit être un entier positif.")
        if not isinstance(utilisateur, int) or utilisateur <= 0:
            raise ValueError("utilisateur doit être un entier positif.")
        if not isinstance(taille, int) or taille <= 0:
            raise ValueError("taille doit être un entier positif.")
        if not all(isinstance(arg, str) and arg for arg in (nom, prenom, fonction, adresse, nationalite, adn)):
            raise ValueError(
                "nom, prenom, fonction, adresse, nationalite, et adn ne doivent pas être des chaînes vides.")
        if not isinstance(dateNaissance, datetime):
            raise TypeError("dateNaissance doit être une instance de datetime.")
        super().__init__(idPersonne, nom, prenom, age, fonction)
        self.idSuspect = idSuspect
        self.dateNaissance = dateNaissance
        self.adresse = adresse
        self.utilisateur = utilisateur
        self.nationalite = nationalite
        self.taille = taille
        self.dateIncrimination = dateIncrimination
        self.adn = adn
        #self.elementsIncriminants = [] if PreuvesIncriminants is None else PreuvesIncriminants
        self.enqueteAssociee = enqueteAssociee

    def get_nom(self):
        return self.nom

    def get_prenom(self):
        return self.prenom

    def to_dict(self) -> dict:
        """
        Convertit l'instance de Suspect en un dictionnaire.
        """
        personne_dict = super().to_dict()
        suspect_dict = {
            "idSuspect": self.idSuspect,
            "dateNaissance": self.dateNaissance,
            "adresse": self.adresse,
            "utilisateur": self.utilisateur,
            "nationalite": self.nationalite,
            "taille": self.taille,
            "dateIncrimination": self.dateIncrimination,
            "adn": self.adn,
            #"PreuvesIncriminants": [element.idPreuve for element in self.elementsIncriminants],  # Supposant que chaque élément a un attribut idPreuve
            "enqueteAssociee": self.enqueteAssociee.idEnquete if self.enqueteAssociee else None
        }
        return {**personne_dict, **suspect_dict}


    def modifier_suspect(self, nouveau_nom: str, nouveau_prenom: str, nouvel_age: int, nouvelle_date_naissance: str,    
                         nouvelle_adresse: str, nouvelle_nationalite: str, nouvelle_taille: int, nouvel_adn: str,
                         nouvel_utilisateur: int, nouvelle_date_incrimination: str):
        """
        Modifie les attributs du suspect.
        """
        self.nom = nouveau_nom
        self.prenom = nouveau_prenom
        self.age = nouvel_age
        self.dateNaissance = datetime.strptime(nouvelle_date_naissance, "%Y-%m-%d")
        self.adresse = nouvelle_adresse
        self.nationalite = nouvelle_nationalite
        self.taille = nouvelle_taille
        self.adn = nouvel_adn
        self.utilisateur = nouvel_utilisateur
        self.dateIncrimination = datetime.strptime(nouvelle_date_incrimination, "%Y-%m-%d")

    def supprimer(self):
        """Supprimer un suspect"""
        self.supprimer = True