import os

DOSSIER_DATA = "passwords"

def init_dossier():
    """Crée le dossier de stockage s'il n'existe pas."""
    if not os.path.exists(DOSSIER_DATA):
        os.makedirs(DOSSIER_DATA)

def obtenir_chemin(nom_fichier: str) -> str:
    return os.path.join(DOSSIER_DATA, nom_fichier)

def lire_fichier_binaire(nom_fichier: str):
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