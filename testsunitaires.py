import unittest
from datetime import datetime
from preuve import Preuve
from enqueteur import Enqueteur
from suspect import Suspect
from personne import Personne
from enquete import Enquete



class TestPreuve(unittest.TestCase):

    def test___init__(self):
        date_test = datetime.now()
        # Test avec valeurs valides
        preuve_valide = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        self.assertEqual(preuve_valide.idPreuve, 1, "__init__ : idPreuve valide")
        # Test avec une date spécifique dans le passé
        date_past = datetime(2020, 5, 17)
        preuve_past = Preuve(2, "Empreinte", "Description passée", "Lieu passé", 456, date_past)
        self.assertEqual(preuve_past.dateDecouverte, date_past, "__init__ : Date de découverte passée")
        # Test avec une date spécifique dans le futur (hypothétique)
        date_future = datetime(2025, 12, 31)
        preuve_future = Preuve(3, "Fibre", "Description future", "Lieu futur", 789, date_future)
        self.assertEqual(preuve_future.dateDecouverte, date_future, "__init__ : Date de découverte future")


        # Test avec idPreuve invalide
        self.assertRaises(ValueError, Preuve, -1, "ADN", "Description", "Lieu", 123, date_test)

        # Test avec utilisateur invalide
        self.assertRaises(ValueError, Preuve, 1, "ADN", "Description", "Lieu", -123, date_test)

        # Test avec type, description, lieu vides
        self.assertRaises(ValueError, Preuve, 1, "", "", "", 123, date_test)

        # Test avec dateDeDecouverte invalide
        self.assertRaises(TypeError, Preuve, 1, "ADN", "Description", "Lieu", 123, "non-date")

    def test_modifierPreuve(self):
        date_test = datetime.now()

        nouvelle_date = datetime(2022, 7, 14)
        # Test modification valide
        preuve = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        preuve.modifierPreuve("Empreinte", "Nouvelle description", "Nouveau lieu", 456, date_test)
        self.assertEqual(preuve.type, "Empreinte", "modifierPreuve : Type modifié")

        preuve1 = Preuve(4, "Sang", "Description initiale", "Lieu initial", 1213, date_test)
        preuve1.modifierPreuve("Cheveux", "Description modifiée", "Nouveau lieu", 1011, nouvelle_date)
        self.assertEqual(preuve1.dateDecouverte, nouvelle_date, "modifierPreuve : Date de découverte modifiée")


        # Test modification avec type, description, lieu vides
        self.assertRaises(ValueError, preuve.modifierPreuve, "", "", "", 456, date_test)

        # Test modification avec utilisateur invalide
        self.assertRaises(ValueError, preuve.modifierPreuve, "Empreinte", "Nouvelle description", "Nouveau lieu", -456,
                          date_test)

    def test_supprimerPreuve(self):
        date_test = datetime.now()
        preuve = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        preuve.supprimerPreuve()
        self.assertTrue(preuve.supprime, "supprimerPreuve : Preuve supprimée")

    def test_toDict(self):
        date_test = datetime.now()
        preuve = Preuve(1, "ADN", "Description", "Lieu", 123, date_test)
        preuve_dict = preuve.toDict()
        self.assertEqual(preuve_dict["idPreuve"], 1, "toDict : idPreuve")

class TestSuspect(unittest.TestCase):

    def test___init__(self):
        date_test = datetime.now()
        # Test avec valeurs valides
        suspect_valide = Suspect(1, 1, "Devroye", "Lilian", date_test, 30, "suspect", "Rue de coquerie", 123, "Belge", 180, date_test, "ADN 1")
        self.assertEqual(suspect_valide.idSuspect, 1, "__init__ : idSuspect valide")
        self.assertEqual(suspect_valide.nom, "Devroye", "__init__ : Nom valide")
        self.assertEqual(suspect_valide.prenom, "Lilian", "__init__ : Prénom valide")


        # Test avec age invalide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, -30, "suspect", "Adresse", 123, "Nationalité", 180, date_test, "ADN")

        # Test avec adresse vide
        with self.assertRaises(ValueError):
            Suspect(1, 3, "Nom", "Prénom", date_test, 30, "suspect", "", 123, "Nationalité", 180, date_test, "ADN")

        # Test avec dateNaissance invalide
        with self.assertRaises(TypeError):
            Suspect(1, 4, "Nom", "Prénom", "date invalide", 30, "suspect", "Adresse", 123, "Nationalité", 180, date_test, "ADN")

        # Test avec idPersonne invalide
        with self.assertRaises(ValueError):
            Suspect(-1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", 180,
                    date_test, "ADN")

            # Test avec idSuspect invalide
        with self.assertRaises(ValueError):
            Suspect(1, -1, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", 180,
                    date_test, "ADN")

            # Test avec nom vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", 180, date_test,
                    "ADN")

            # Test avec prénom vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "", date_test, 30, "suspect", "Adresse", 123, "Nationalité", 180, date_test,
                    "ADN")

        # Test avec utilisateur invalide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", -123, "Nationalité", 180,
                    date_test, "ADN")

        # Test avec nationalité vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "", 180, date_test, "ADN")

        # Test avec taille vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", "", date_test,
                    "ADN")

            # Test avec adn vide
        with self.assertRaises(ValueError):
            Suspect(1, 2, "Nom", "Prénom", date_test, 30, "suspect", "Adresse", 123, "Nationalité", 180,
                     date_test, "")


    def test_to_dict(self):
        # Conversion de l'instance en dictionnaire
        self.date_naissance = datetime(1980, 1, 1)
        self.date_incrimination = datetime.now()
        self.suspect = Suspect(1, 1, "Nom", "Prénom", self.date_naissance, 40, "suspect", "Adresse", 123,
                               "Nationalité", 180, self.date_incrimination, "ADN")
        suspect_dict = self.suspect.to_dict()

        # Vérification de la présence des clés et de la correspondance des valeurs
        self.assertEqual(suspect_dict["idSuspect"], self.suspect.idSuspect, "to_dict : idSuspect")
        self.assertEqual(suspect_dict["nom"], self.suspect.nom, "to_dict : nom")
        self.assertEqual(suspect_dict["prenom"], self.suspect.prenom, "to_dict : prenom")
        self.assertEqual(suspect_dict["dateNaissance"], self.suspect.dateNaissance, "to_dict : dateNaissance")
        self.assertEqual(suspect_dict["adresse"], self.suspect.adresse, "to_dict : adresse")
        self.assertEqual(suspect_dict["utilisateur"], self.suspect.utilisateur, "to_dict : utilisateur")
        self.assertEqual(suspect_dict["nationalite"], self.suspect.nationalite, "to_dict : nationalite")
        self.assertEqual(suspect_dict["taille"], self.suspect.taille, "to_dict : taille")
        self.assertEqual(suspect_dict["dateIncrimination"], self.suspect.dateIncrimination,
                         "to_dict : dateIncrimination")
        self.assertEqual(suspect_dict["adn"], self.suspect.adn, "to_dict : adn")

    def test_modifier_suspect(self):
        # Création d'un suspect pour le test
        date_naissance = datetime(1980, 1, 1)
        date_incrimination = datetime.now()
        suspect = Suspect(1, 1, "Nom", "Prénom", date_naissance, 40, "suspect", "Adresse", 123, "Nationalité", 180,
                          date_incrimination, "ADN")

        # Test modification valide
        nouvelle_date_naissance = "1981-02-02"
        nouvelle_date_incrimination = "2022-07-14"
        suspect.modifier_suspect("Nouveau Nom", "Nouveau Prénom", 41, nouvelle_date_naissance, "Nouvelle Adresse",
                                 "Nouvelle Nationalité", 185, "Nouvel ADN", 456, nouvelle_date_incrimination)
        self.assertEqual(suspect.nom, "Nouveau Nom", "modifier_suspect : Nom modifié")
        self.assertEqual(suspect.prenom, "Nouveau Prénom", "modifier_suspect : Prénom modifié")
        self.assertEqual(suspect.age, 41, "modifier_suspect : Age modifié")
        self.assertEqual(suspect.dateNaissance, datetime.strptime(nouvelle_date_naissance, "%Y-%m-%d"),
                         "modifier_suspect : Date de naissance modifiée")
        self.assertEqual(suspect.adresse, "Nouvelle Adresse", "modifier_suspect : Adresse modifiée")
        self.assertEqual(suspect.nationalite, "Nouvelle Nationalité", "modifier_suspect : Nationalité modifiée")
        self.assertEqual(suspect.taille, 185, "modifier_suspect : Taille modifiée")
        self.assertEqual(suspect.adn, "Nouvel ADN", "modifier_suspect : ADN modifié")
        self.assertEqual(suspect.utilisateur, 456, "modifier_suspect : Utilisateur modifié")
        self.assertEqual(suspect.dateIncrimination, datetime.strptime(nouvelle_date_incrimination, "%Y-%m-%d"),
                         "modifier_suspect : Date d'incrimination modifiée")

        # Test modification avec valeurs invalides
        with self.assertRaises(ValueError):
            suspect.modifier_suspect("", "", 0, "date invalide", "", "", "", "", -1, "date invalide")

    def test_supprimer(self):
        # Création d'un suspect pour le test
        suspect = Suspect(1, 1, "Nom", "Prénom", datetime.now(), 40, "suspect", "Adresse", 123, "Nationalité", 180,
                          datetime.now(), "ADN")

        # Test de la suppression
        suspect.supprimer()
        self.assertTrue(suspect.supprimer, "supprimer : Suspect correctement supprimé")

class TestEnqueteur(unittest.TestCase):

    def test___init__(self):
        # Test avec valeurs valides
        enqueteur_valide = Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "enquêteur")
        self.assertEqual(enqueteur_valide.idPersonne, 1, "__init__ : idPersonne valide")
        self.assertEqual(enqueteur_valide.nom, "NomEnqueteur", "__init__ : Nom valide")
        self.assertEqual(enqueteur_valide.prenom, "PrénomEnqueteur", "__init__ : Prénom valide")
        self.assertEqual(enqueteur_valide.age, 40, "__init__ : Age valide")
        self.assertEqual(enqueteur_valide.idEnqueteur, 100, "__init__ : idEnqueteur valide")
        self.assertEqual(enqueteur_valide.grade, "GradeEnqueteur", "__init__ : Grade valide")
        self.assertEqual(enqueteur_valide.fonction, "enquêteur", "__init__ : Fonction valide")

        # Test avec idPersonne invalide
        with self.assertRaises(ValueError):
            Enqueteur(-1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "enquêteur")

        # Test avec idEnqueteur invalide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, -100, "GradeEnqueteur", "enquêteur")

        # Test avec nom vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "enquêteur")

        # Test avec prénom vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "", 40, 100, "GradeEnqueteur", "enquêteur")

        # Test avec age invalide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", -1, 100, "GradeEnqueteur", "enquêteur")

        # Test avec grade vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "", "enquêteur")

        # Test avec fonction vide
        with self.assertRaises(ValueError):
            Enqueteur(1, "NomEnqueteur", "PrénomEnqueteur", 40, 100, "GradeEnqueteur", "")


    def test_to_dict(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        result = enqueteur.to_dict()
        expected_keys = ['idPersonne', 'nom', 'prenom', 'age', 'fonction', 'idEnqueteur', 'grade']
        self.assertTrue(all(key in result for key in expected_keys),
                        "Les clés attendues sont toutes présentes dans le dictionnaire")

    def test_assignerEnquete(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        enquete = Enquete(1, 'Enquête Test', datetime.now(), 'Paris', 1)
        enqueteur.assignerEnquete(enquete)
        self.assertIn(enquete, enqueteur.enquetesAssignees, "L'enquête a été correctement assignée")

    def test_modifierEnqueteur(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        enqueteur.modifierEnqueteur('Martin', 'Paul', 45, 'Capitaine')
        self.assertEqual(enqueteur.nom, 'Martin')
        self.assertEqual(enqueteur.prenom, 'Paul')
        self.assertEqual(enqueteur.age, 45)
        self.assertEqual(enqueteur.grade, 'Capitaine')
        self.assertEqual(enqueteur.fonction, 'enquêteur')

    def test_supprimerEnqueteur(self):
        enqueteur = Enqueteur(1, 'Dupont', 'Jean', 40, 100, 'Lieutenant',"enquêteur")
        enqueteur.supprimerEnqueteur()
        self.assertTrue(enqueteur.estSupprime, "Enquêteur correctement supprimé")

class TestPersonne (unittest.TestCase):
    def test__init__(self):
        personne = Personne(1, "Dupont", "Jean", 30, "suspect")
        self.assertEqual(personne.idPersonne, 1)
        self.assertEqual(personne.nom, "Dupont")
        self.assertEqual(personne.prenom, "Jean")
        self.assertEqual(personne.age, 30)
        self.assertEqual(personne.fonction, "suspect")
        self.assertIsInstance(personne.idPersonne, int)
        self.assertIsInstance(personne.nom, str)
        self.assertIsInstance(personne.prenom, str)
        self.assertIsInstance(personne.age, int)
        self.assertIsInstance(personne.fonction, str)

        # limites 
        personne = Personne(1000000, "Dupont", "Jean", 30, "enquêteur")
        self.assertEqual(personne.idPersonne, 1000000)
        personne2 = Personne(2, "Dupont", "Jean", 120, "enquêteur")
        self.assertEqual(personne2.age, 120)
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", 0, "enquêteur")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", -1, "suspect")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", 30, "ishfdsjhkgjd")
        with self.assertRaises(ValueError):
            Personne(-1, "Dupont", "Jean", 30, "suspect")
        with self.assertRaises(ValueError):
            Personne(1, "", "Jean", 30, "suspect")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "", 30, "suspect")
        with self.assertRaises(ValueError):
            Personne(-1, "Dupont", "Jean", 30, "enquêteur")
        with self.assertRaises(ValueError):
            Personne(0, "Dupont", "Jean", 30, "enquêteur")
        with self.assertRaises(ValueError):
            Personne(1, "Dupont", "Jean", 30, "autreFonction")

    def testToDict(self):
        personnne = Personne(1, "Dupont", "Jean", 30, "suspect")
        dictionnaireAttendu = {
            "idPersonne": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "age": 30,
            "fonction": "suspect"
        }
        self.assertEqual(personnne.to_dict(), dictionnaireAttendu)
        self.assertIsInstance(personnne.to_dict(), dict)

class TestEnquete (unittest.TestCase):
    def setUp(self):
        self.date_Debut = datetime.now()
        self.enquete = Enquete(1, "Enquête Test", self.date_Debut, "Lieu Fictif", 5)

    def testInit(self):
        self.assertEqual(self.enquete.idEnquete, 1)
        self.assertEqual(self.enquete.titre, "Enquête Test")
        self.assertEqual(self.enquete.dateDebut, self.date_Debut)
        self.assertEqual(self.enquete.lieu, "Lieu Fictif")
        self.assertEqual(self.enquete.priorite, 5)
        self.assertEqual(self.enquete.preuves, [])
        self.assertEqual(self.enquete.suspects, [])
        self.assertEqual(self.enquete.enqueteurAssocie, None)
        self.assertEqual(self.enquete.enqueteurs, [])
        self.assertEqual(self.enquete.statut, "En cours")
        self.assertIsInstance(self.enquete.idEnquete, int)
        self.assertIsInstance(self.enquete.titre, str)
        self.assertIsInstance(self.enquete.dateDebut, datetime)
        self.assertIsInstance(self.enquete.lieu, str)
        self.assertIsInstance(self.enquete.priorite, int)
        self.assertIsInstance(self.enquete.preuves, list)
        self.assertIsInstance(self.enquete.suspects, list)
        self.assertIsInstance(self.enquete.enqueteurs, list)
        self.assertIsInstance(self.enquete.statut, str)

    def testErreurs(self):
        with self.assertRaises(ValueError):
            Enquete(0, "Enquête Test", datetime.now(), "Lieu Fictif", 5)
        with self.assertRaises(ValueError):
            Enquete(-1, "Enquête Test", datetime.now(), "Lieu Fictif", 5)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "Lieu Fictif", 0)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "Lieu Fictif", -4)
        with self.assertRaises(ValueError):
            Enquete(1, "", datetime.now(), "Lieu Fictif", 5)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "", 5)
        with self.assertRaises(ValueError):
            Enquete(1, "Enquête Test", datetime.now(), "Lieu Fictif", 5, statut="")
        with self.assertRaises(TypeError):
            Enquete(1, "Enquête Test", "1998/20/12", "Lieu Fictif", 5)

    def test_to_dict(self):
        enqueteDict = self.enquete.to_dict()
        self.assertEqual(enqueteDict['idEnquete'], 1)
        self.assertEqual(enqueteDict['titre'], "Enquête Test")
        self.assertEqual(enqueteDict['dateDebut'], self.date_Debut)
        self.assertEqual(enqueteDict['lieu'], "Lieu Fictif")
        self.assertEqual(enqueteDict['statut'], "En cours")
        self.assertEqual(enqueteDict['priorite'], 5)
        self.assertEqual(enqueteDict['preuves'], [])
        self.assertEqual(enqueteDict['suspects'], [])
        self.assertEqual(enqueteDict['enqueteurs'], [])

    def test_ajouter_preuve(self):
        preuve = Preuve(1, "Type", "Sang", "Lieu", 4, datetime.now())
        self.enquete.ajouter_preuve(preuve)
        self.assertIn(preuve, self.enquete.preuves)



    def test_modifer_informations(self):
        self.enquete.modifierInformations()
        self.assertEqual(self.enquete.titre, "Enquête Test")
        nouvelle_date = datetime.now()
        self.enquete.modifierInformations(titre="nOUVEAu Titre", dateDebut=nouvelle_date, statut="Résolu", lieu="Nouveau Lieu", priorite=10)
        self.assertEqual(self.enquete.titre, "nOUVEAu Titre")
        self.assertEqual(self.enquete.dateDebut, nouvelle_date)
        self.assertEqual(self.enquete.statut, "Résolu")
        self.assertEqual(self.enquete.lieu, "Nouveau Lieu")
        self.assertEqual(self.enquete.priorite, 10)

    def test_supprimer_informations(self):
        self.enquete.supprimerInformations()
        self.assertIsNone(self.enquete.idEnquete)
        self.assertIsNone(self.enquete.titre)
        self.assertIsNone(self.enquete.dateDebut)
        self.assertIsNone(self.enquete.statut)
        self.assertIsNone(self.enquete.lieu)
        self.assertIsNone(self.enquete.priorite)
        self.assertEqual(self.enquete.preuves, [])
        self.assertEqual(self.enquete.suspects, [])

    def test_classer_enquete(self):
        self.enquete.classer_enquete()
        self.assertEqual(self.enquete.statut, "Classé")

    def test_enquete_resolue(self):
        self.enquete.classer_enquete()
        self.assertEqual(self.enquete.statut, "Classé")
        self.assertEqual(self.enquete.priorite, 5)


    def test_associerSuspect(self):
        # Créez une instance de la classe Enquete pour effectuer les tests
        enquete = Enquete(idEnquete=1, titre="Enquête Test", dateDebut=datetime.now(), lieu="Lieu Test", priorite=1)

        # Créez une instance de la classe Suspect pour tester l'association
        suspect = Suspect(idPersonne=1, idSuspect=1, nom="Nom Test", prenom="Prenom Test", dateNaissance=datetime.now(),
                  age=30, fonction="suspect", adresse="Adresse Test", utilisateur=123, nationalite="France",
                  taille=180, dateIncrimination=datetime.now(), adn="ADN Test")

        # Appelez la méthode à tester
        enquete.associerSuspect(suspect)

        # Assurez-vous que le suspect a été ajouté à la liste des suspects de l'enquête
        self.assertIn(suspect, enquete.suspects)

        # Assurez-vous que l'enquête associée au suspect est correcte
        self.assertEqual(suspect.enqueteAssociee, enquete.idEnquete)

        # Testez le cas où un suspect déjà associé est ajouté
        with self.assertRaises(ValueError):
            enquete.associerSuspect(suspect)

        # Testez le cas où un suspect non valide est ajouté
        with self.assertRaises(TypeError):
            enquete.associerSuspect("Suspect non valide")



if __name__ == '__main__':
    unittest.main()
