import os
import pytest
from security import crypto
from file_io import manager

# --- TESTS DU MODULE CRYPTO : CAS DE RÉUSSITE ---

def test_chiffrement_dechiffrement_succes():
    secret_original = "MonCodeSecret123"
    password = "MasterPassword"

    # 1. On chiffre
    data_chiffree = crypto.chiffrer_message(secret_original, password)
    
    # 2. On déchiffre
    message_recupere = crypto.dechiffrer_message(data_chiffree, password)

    # 3. VERIFICATION (Assert)
    assert message_recupere == secret_original
    
# --- TESTS DU MODULE CRYPTO : CAS D'ÉCHEC ---

def test_chiffrement_mauvais_password():
    secret = "TopSecret"
    
    # On chiffre avec "Mdp1"
    data = crypto.chiffrer_message(secret, "Mdp1")
    
    # On essaie de déchiffrer avec "Mdp2"
    resultat = crypto.dechiffrer_message(data, "Mdp2")

    # On s'attend à ce que le résultat soit None (échec)
    assert resultat is None


# --- TESTS DU MODULE MANAGER ---

def test_ecriture_lecture_suppression_fichier():
    """Vérifie le cycle complet de gestion de fichier."""
    nom_test = "test_pytest.bin"
    donnees_test = b"DonneesBinairesDeTest"

    # 1. Test Écriture
    succes_ecriture = manager.ecrire_fichier_binaire(nom_test, donnees_test)
    assert succes_ecriture is True
    
    # Vérifie que le fichier existe physiquement
    chemin = manager.obtenir_chemin(nom_test)
    assert os.path.exists(chemin) is True

    # 2. Test Lecture
    contenu_lu = manager.lire_fichier_binaire(nom_test)
    assert contenu_lu == donnees_test

    # 3. Test Suppression (Nettoyage)
    succes_suppression = manager.supprimer_fichier_binaire(nom_test)
    assert succes_suppression is True
    assert os.path.exists(chemin) is False

# --- AJOUTS : TESTS DE SÉCURITÉ POUR L'INJECTION DE CHEMINS ---

def test_securite_path_traversal():
    # Tentative d'écriture dans le dossier parent
    nom_pirate = "../systeme_hack.crypt"
    donnees = b"virus"

    # Le manager DOIT refuser (renvoyer False)
    succes = manager.ecrire_fichier_binaire(nom_pirate, donnees)
    assert succes is False

    # Double vérification : le fichier ne doit pas exister physiquement
    assert os.path.exists(nom_pirate) is False

# --- AJOUTS : TESTS DE SÉCURITÉ POUR L'INJECTION DE CHEMINS ---

def test_securite_injection_chemins():
    noms_interdits = [
        "dossier/fichier.crypt",   # Slash Linux/Mac
        "dossier\\fichier.crypt",  # Backslash Windows
        "/etc/passwd",           # Racine Linux
        "C:\\Windows\\System32"  # Racine Windows
    ]

    for nom in noms_interdits:
        succes = manager.ecrire_fichier_binaire(nom, b"test")
        assert succes is False, f"La sécurité a échoué pour : {nom}"