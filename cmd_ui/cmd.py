#!/usr/bin/env python3

# --- Interface Utilisateur en Ligne de Commande pour l'application ---

import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box 

from file_io import manager
from security import crypto
from authentication import auth

console = Console()
MASTER_PASSWORD = None

# Afficher le header du système
def afficher_header():
    console.clear()
    console.print(Panel.fit(
        "[bold red] KEYSHELL - ROOT ACCESS[/bold red]\n[italic white]Système Mono-Utilisateur Sécurisé[/italic white]",
        border_style="red"
    ))

# Afficher l'aide des commandes disponibles
def afficher_aide():
    table = Table(title="\nCommandes du Système", box=box.ROUNDED)

    table.add_column("Commande", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("list", "Lister tous les services enregistrés")
    table.add_row("add", "Ajouter un mot de passe sécurisé")
    table.add_row("get", "Récupérer et déchiffrer un mot de passe")
    table.add_row("delete", "Supprimer un mot de passe")
    table.add_row("clear", "Nettoyer l'affichage du terminal")
    table.add_row("exit", "Verrouiller et quitter")
    
    console.print(table)

# Gestion de la connexion au système
def login_systeme():
    global MASTER_PASSWORD
    afficher_header()
    manager.init_dossier()

    # 1. Premier lancement (Installation)
    if not auth.est_inscrit():
        console.print(Panel("[bold yellow]INITIALISATION DU SYSTÈME[/bold yellow]\nVeuillez définir le mot de passe ROOT.", border_style="yellow"))
        
        # On affiche les règles à l'utilisateur
        console.print("[italic]Politique : 12 caractères minimum, 1 Maj., 1 Min., 1 Chiffre, 1 Spécial[/italic]\n")

        while True:
            pwd1 = Prompt.ask("Nouveau mot de passe Root", password=True)
            
            est_valide, message_erreur = auth.verifier_force_mdp(pwd1)
            
            if not est_valide:
                console.print(f"[bold red]❌ {message_erreur}[/bold red]")
                continue

            pwd2 = Prompt.ask("Confirmez le mot de passe", password=True)
            
            if pwd1 == pwd2:
                if auth.inscrire_root(pwd1):
                    console.print("[bold green]Compte ROOT configuré ![/bold green]")
                    MASTER_PASSWORD = pwd1
                    break
                else:
                    console.print("[red]Erreur d'écriture.[/red]")
            else:
                console.print("[red]Les mots de passe ne correspondent pas.[/red]")

    # 2. Connexion normale
    else:
        console.print("\n[red]🔒 ACCÈS RESTREINT : ROOT SEULEMENT[/red]")
        tentatives = 3
        while tentatives > 0:
            pwd = Prompt.ask(f"\nMot de passe ROOT ({tentatives} essais)", password=True)
            if auth.verifier_root(pwd):
                console.print("[bold green]Accès accordé.[/bold green] 🔓")
                MASTER_PASSWORD = pwd
                break
            else:
                tentatives -= 1
                console.print("[bold red]Accès refusé.[/bold red] 🔒")
        
        if not MASTER_PASSWORD:
            sys.exit(1)

# Sélectionner un service dans la liste
def selectionner_service(action: str):
    fichiers = manager.lister_fichiers()
    services = [f.replace('.crypt', '') for f in fichiers]

    if not services:
        console.print("[yellow]Aucun service disponible.[/yellow]")
        return None

    # Affichage du tableau de choix
    table = Table(box=box.SIMPLE)
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Service", style="magenta")

    for idx, nom in enumerate(services, 1):
        table.add_row(str(idx), nom)
    
    console.print(table)

    # L'utilisateur peut taper le nom OU le numéro
    choix = Prompt.ask("Entrez le [cyan]Numéro[/cyan] ou le [magenta]Nom[/magenta]")

    if choix.isdigit():
        index = int(choix) - 1
        if 0 <= index < len(services):
            return services[index]
        else:
            console.print("[red]Numéro invalide.[/red]")
            return None
    else:
        # On vérifie si le nom tapé existe
        if choix in services:
            return choix
        else:
            console.print(f"[red]Le service '{choix}' n'existe pas.[/red]")
            return None

# Ajouter un mot de passe sécurisé dans le coffre
def add():
    service = Prompt.ask("Nom du service")
    nom_fichier = f"{service.lower().strip()}.crypt"
    secret = Prompt.ask(f"Mot de passe pour {service}", password=True)
    
    donnees = crypto.chiffrer_message(secret, MASTER_PASSWORD)
    
    if manager.ecrire_fichier_binaire(nom_fichier, donnees):
        console.print(f"[green]✔ Mot de passe pour {service} sécurisé.[/green]")

# Récupérer et déchiffrer un mot de passe sécurisé
def get():
    service = selectionner_service(action="lire")
    if not service:
        return

    nom_fichier = f"{service.lower().strip()}.crypt"
    donnees = manager.lire_fichier_binaire(nom_fichier)

    check_pwd = Prompt.ask(f"[orange3]\n🔒 Sécurité : Confirmez votre mot de passe pour voir[/] [bold orange3]'{service}'[/]", password=True)

    if check_pwd != MASTER_PASSWORD:
        console.print("[bold red]❌ Mot de passe incorrect. Accès refusé.[/bold red]")
        return

    mdp = crypto.dechiffrer_message(donnees, MASTER_PASSWORD)
    if mdp:
        console.print(Panel(f"PASSWORD : [bold cyan]{mdp}[/bold cyan]", title=service, border_style="green"))
    else:
        console.print("[red]Erreur de déchiffrement (Fichier corrompu ?).[/red]")

# Supprimer un mot de passe sécurisé du coffre
def delete():
    service = selectionner_service(action="lire")
    if not service:
        return

    nom_fichier = f"{service.lower().strip()}.crypt"

    # 1. Vérifier si le fichier existe
    if not manager.lire_fichier_binaire(nom_fichier):
        console.print(f"[yellow]Le service '{service}' n'existe pas.[/yellow]")
        return

    # 2. Demande de confirmation sécurisée (On évite les suppressions accidentelles)
    console.print(f"[bold red]\nATTENTION : Vous allez supprimer définitivement '{service}' ![/bold red]")
    if Confirm.ask("Êtes-vous sûr de vouloir continuer ?"):
        
        # 3. Action
        if manager.supprimer_fichier_binaire(nom_fichier):
            console.print(f"[bold green]✔ Service '{service}' supprimé du coffre.[/bold green]")
        else:
            console.print("[red]Erreur lors de la suppression.[/red]")
    else:
        console.print("[italic]Suppression annulée.[/italic]")

# Lister tous les services dans le coffre
def list():
    fichiers = manager.lister_fichiers()
    clean_names = [f.replace('.crypt', '') for f in fichiers]
    
    if clean_names:
        console.print(Panel("\n".join(clean_names), title="Coffre Root"))
    else:
        console.print("[italic]Le coffre est vide.[/italic]")