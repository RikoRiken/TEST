import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def deriver_cle(password: str, sel: bytes = None):
    if sel is None:
        sel = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sel,
        iterations=600_000,
    )   
    cle = kdf.derive(password.encode('utf-8'))
    
    return cle, sel

def chiffrer_message(message_clair: str, password: str):
    cle, sel = deriver_cle(password, sel=None)
    aesgcm = AESGCM(cle)
    nonce = os.urandom(12)
    message_encode = message_clair.encode('utf-8')
    ciphertext_et_tag = aesgcm.encrypt(nonce, message_encode, associated_data=None)
    donnees_chiffrees = sel + nonce + ciphertext_et_tag
    
    return donnees_chiffrees

def dechiffrer_message(donnees_chiffrees: bytes, password: str):
    try:
        sel = donnees_chiffrees[:16]
        nonce = donnees_chiffrees[16:28]
        ciphertext_et_tag = donnees_chiffrees[28:]

        cle, _ = deriver_cle(password, sel=sel)
        aesgcm = AESGCM(cle)
        
        message_bytes = aesgcm.decrypt(nonce, ciphertext_et_tag, associated_data=None)
        return message_bytes.decode('utf-8')
    except Exception:
        return None