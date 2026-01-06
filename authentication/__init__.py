import os
from file_io import manager
from security import crypto

AUTH_FILE = "auth.bin"

def est_inscrit() -> bool:
    """Vérifie si un utilisateur est déjà enregistré (si le fichier existe)."""
    return os.path.exists(AUTH_FILE)

def inscrire_utilisateur(password: str) -> bool:
    """
    Crée le compte maître.
    On dérive le mot de passe (hash) et on stocke le résultat + le sel.
    """
    try:
        # On utilise ta fonction crypto pour obtenir un hash sécurisé
        # deriver_cle renvoie (cle, sel)
        cle_derivee, sel = crypto.deriver_cle(password)
        
        # On stocke le sel (16 bytes) + la clé dérivée (32 bytes)
        data = sel + cle_derivee
        
        return manager.ecrire_fichier_binaire(AUTH_FILE, data)
    except Exception as e:
        print(f"Erreur inscription : {e}")
        return False

def verifier_login(password: str) -> bool:
    """
    Vérifie si le mot de passe correspond à celui enregistré.
    """
    data = manager.lire_fichier_binaire(AUTH_FILE)
    if not data or len(data) < 48: # 16 (sel) + 32 (cle)
        return False

    # On récupère le sel qui a été utilisé lors de l'inscription
    sel_stocke = data[:16]
    hash_stocke = data[16:]

    # On re-calcule le hash du mot de passe tapé avec CE sel
    cle_calculee, _ = crypto.deriver_cle(password, sel=sel_stocke)

    # Si les deux sont identiques, c'est le bon mot de passe
    return cle_calculee == hash_stocke