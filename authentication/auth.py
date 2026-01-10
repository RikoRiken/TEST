# --- Fonction d'authentification pour l'utilisateur Root ---

import string
from security import crypto
from file_io import manager

AUTH_FILENAME = "auth.crypt"

# Vérifie si l'utilisateur Root est inscrit
def est_inscrit() -> bool:
    return manager.lire_fichier_binaire(AUTH_FILENAME) is not None

# Inscrit l'utilisateur Root avec le mot de passe donné
def inscrire_root(password: str) -> bool:
    try:
        cle_derivee, sel = crypto.deriver_cle(password)
        data = sel + cle_derivee
        return manager.ecrire_fichier_binaire(AUTH_FILENAME, data)
    except Exception as e:
        print(f"Erreur inscription : {e}")
        return False

# Vérifie si le mot de passe est bien celui du Root
def verifier_root(password: str) -> bool:
    data = manager.lire_fichier_binaire(AUTH_FILENAME)
    
    if not data or len(data) < 48:
        return False

    sel_stocke = data[:16]
    hash_stocke = data[16:]

    cle_calculee, _ = crypto.deriver_cle(password, sel=sel_stocke)
    return cle_calculee == hash_stocke

# Vérifie la robustesse du mot de passe
def verifier_force_mdp(password: str) -> tuple[bool, str]:
    # 1. Longueur minimale (12 est recommandé par l'ANSSI)
    if len(password) < 12:
        return False, "Le mot de passe doit faire au moins 12 caractères."

    # 2. Au moins une majuscule
    if not any(c.isupper() for c in password):
        return False, "Le mot de passe doit contenir au moins une majuscule."

    # 3. Au moins une minuscule
    if not any(c.islower() for c in password):
        return False, "Le mot de passe doit contenir au moins une minuscule."

    # 4. Au moins un chiffre
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre."

    # 5. Au moins un caractère spécial (!@#$%^& etc.)
    if not any(c in string.punctuation for c in password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial."

    return True, "Mot de passe robuste."