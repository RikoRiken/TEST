import os

DOSSIER_DATA = "passwords"

def init_dossier():
    """Crée le dossier de stockage s'il n'existe pas."""
    if not os.path.exists(DOSSIER_DATA):
        os.makedirs(DOSSIER_DATA)

def verifier_securite_nom(nom_fichier: str) -> bool:
    """
    Vérifie que le nom de fichier ne contient pas de tentative d'intrusion.
    Empêche les '..' (Path Traversal) et les séparateurs de dossiers.
    """
    if not nom_fichier or nom_fichier.strip() == "":
        return False
        
    # On interdit de remonter dans les dossiers ou de changer de dossier
    if ".." in nom_fichier or "/" in nom_fichier or "\\" in nom_fichier:
        print(f"[ALERTE SÉCURITÉ] Tentative de Path Traversal bloquée : {nom_fichier}")
        return False
        
    return True

def obtenir_chemin(nom_fichier: str) -> str:
    return os.path.join(DOSSIER_DATA, nom_fichier)

def lire_fichier_binaire(nom_fichier: str):

    if not verifier_securite_nom(nom_fichier):
        return False
    
    """Lit un fichier dans le dossier passwords/"""
    chemin = obtenir_chemin(nom_fichier)
    if not os.path.exists(chemin):
        return None
    try:
        with open(chemin, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Erreur lecture : {e}")
        return None

def ecrire_fichier_binaire(nom_fichier: str, donnees: bytes):

    if not verifier_securite_nom(nom_fichier):
        return False
    

    """Écrit un fichier dans le dossier passwords/"""
    init_dossier() # On s'assure que le dossier existe
    chemin = obtenir_chemin(nom_fichier)
    try:
        with open(chemin, 'wb') as f:
            f.write(donnees)
        return True
    except Exception as e:
        print(f"Erreur écriture : {e}")
        return False
    
def supprimer_fichier_binaire(nom_fichier: str) -> bool:

    if not verifier_securite_nom(nom_fichier):
        return False
    
    # Supprime définitivement un fichier du coffre.
    chemin = obtenir_chemin(nom_fichier)
    
    if os.path.exists(chemin):
        try:
            os.remove(chemin)
            return True
        except Exception as e:
            print(f"Erreur suppression : {e}")
            return False
    return False

def lister_fichiers():
    """Liste tous les services enregistrés."""
    if not os.path.exists(DOSSIER_DATA):
        return []
    return [f for f in os.listdir(DOSSIER_DATA) if f.endswith('.crypt') and f != 'auth.crypt']