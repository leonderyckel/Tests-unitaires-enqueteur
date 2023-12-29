class Personne:
    """
    Classe représentant une Personne soit un enquêteur soit un suspect.

    Attributs :
    - idPersonne (int) : l'identifiant de la personne.
    - nom (string) : le nom de la personne.
    - age (int) : l'âge de la personne.
    - fonction (string): si la personne est un enquêteur ou un suspect.
    """

    def __init__(self, idPersonne: int, nom: str, prenom: str, age: int, fonction: str):
        """
        Auteur : Thibault
        Crée une instance de la classe Personne.

        PRE : idPersonne doit être un entier, une personne doit être soit un suspect soit un enquêteur.
        POST : Une Personne est créée avec ses attributs idPersonne, nom, age, fonction qui prendront la valeur de ce qui a été passé en paramètre.
        RAISES : ValueError si idPersonne est négatif ou si fonction n'est pas 'suspect' ou 'enquêteur'.
        """
        if not isinstance(idPersonne, int) or idPersonne <= 0:
            raise ValueError("L'identifiant de la personne doit être un entier positif.")
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom ne doit pas être une chaîne vide.")
        if not isinstance(prenom, str) or not prenom.strip():
            raise ValueError("Le prénom ne doit pas être une chaîne vide.")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("L'âge doit être un entier positif.")
        if not isinstance(fonction, str) or fonction not in ['suspect', 'enquêteur']:
            raise ValueError("La fonction doit être soit 'suspect' soit 'enquêteur'.")

        if idPersonne <= 0:
            raise ValueError("L'identifiant de la personne doit être positif.")
        if fonction not in ['suspect', 'enquêteur']:
            raise ValueError("La fonction doit être soit 'suspect' soit 'enquêteur'.")
        self.idPersonne = idPersonne
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.fonction = fonction

    def to_dict(self) -> dict:
        return {
            "idPersonne": self.idPersonne,
            "nom": self.nom,
            "prenom": self.prenom,
            "age": self.age,
            "fonction": self.fonction
        }