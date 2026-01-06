#!/usr/bin/env python3
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

def afficher_header():
    console.clear()
    console.print(Panel.fit(
        "[bold red]GUARDIA BOX - ROOT ACCESS[/bold red]\n[italic white]Système Mono-Utilisateur Sécurisé[/italic white]",
        border_style="red"
    ))

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

def login_systeme():
    global MASTER_PASSWORD
    afficher_header()
    manager.init_dossier()

    # CAS 1 : Premier lancement (Installation)
    if not auth.est_inscrit():
        console.print(Panel("[bold yellow]INITIALISATION DU SYSTÈME[/bold yellow]\nVeuillez définir le mot de passe ROOT.", border_style="yellow"))
        
        while True:
            pwd1 = Prompt.ask("Nouveau mot de passe Root", password=True)
            pwd2 = Prompt.ask("Confirmez le mot de passe", password=True)
            
            if pwd1 == pwd2 and len(pwd1) > 0:
                if auth.inscrire_root(pwd1):
                    console.print("[bold green]Compte ROOT configuré ![/bold green]")
                    MASTER_PASSWORD = pwd1
                    break
                else:
                    console.print("[red]Erreur d'écriture.[/red]")
            else:
                console.print("[red]Les mots de passe ne correspondent pas.[/red]")

    # CAS 2 : Connexion normale
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

def selectionner_service(action: str):
    """Affiche une liste et renvoie le nom du service choisi."""
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
            return services[index] # On renvoie le nom correspondant au numéro
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

def add():
    service = Prompt.ask("Nom du service")
    nom_fichier = f"{service.lower().strip()}.crypt"
    secret = Prompt.ask(f"Mot de passe pour {service}", password=True)
    
    donnees = crypto.chiffrer_message(secret, MASTER_PASSWORD)
    
    if manager.ecrire_fichier_binaire(nom_fichier, donnees):
        console.print(f"[green]✔ Mot de passe pour {service} sécurisé.[/green]")

def get():
    service = selectionner_service(action="lire")
    if not service:
        return

    nom_fichier = f"{service.lower().strip()}.crypt"
    donnees = manager.lire_fichier_binaire(nom_fichier)

    # 2. DOUBLE VÉRIFICATION DE SÉCURITÉ
    check_pwd = Prompt.ask(f"[bold orange3]\n🔒 Sécurité : Confirmez votre mot de passe pour voir '{service}'[/]", password=True)

    if check_pwd != MASTER_PASSWORD:
        console.print("[bold red]❌ Mot de passe incorrect. Accès refusé.[/bold red]")
        return

    # 3. Si c'est bon, on déchiffre
    mdp = crypto.dechiffrer_message(donnees, MASTER_PASSWORD)
    if mdp:
        console.print(Panel(f"PASSWORD : [bold cyan]{mdp}[/bold cyan]", title=service, border_style="green"))
    else:
        console.print("[red]Erreur de déchiffrement (Fichier corrompu ?).[/red]")

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

def list():
    fichiers = manager.lister_fichiers()
    clean_names = [f.replace('.crypt', '') for f in fichiers]
    
    if clean_names:
        console.print(Panel("\n".join(clean_names), title="Coffre Root"))
    else:
        console.print("[italic]Le coffre est vide.[/italic]")