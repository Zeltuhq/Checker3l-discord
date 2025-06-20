import os
import time
import requests
from pystyle import Colors, Colorate
import socket

# Bannière ASCII
banner = r"""
███╗░░░███╗██╗░░░██╗██╗░░░██╗███╗░░██╗███████╗██████╗░  ██╗░█████╗░
████╗░████║██║░░░██║██║░░░██║████╗░██║██╔════╝██╔══██╗  ██║██╔══██╗
██╔████╔██║██║░░░██║██║░░░██║██╔██╗██║█████╗░░██████╦╝  ██║██║░░╚═╝
██║╚██╔╝██║██║░░░██║██║░░░██║██║╚████║██╔══╝░░██╔══██╗  ██║██║░░██╗
██║░╚═╝░██║╚██████╔╝╚██████╔╝██║░╚███║███████╗██████╦╝  ██║╚█████╔╝
╚═╝░░░░░╚═╝░╚═════╝░░╚═════╝░╚═╝░░╚══╝╚══════╝╚═════╝░  ╚═╝░╚════╝░
"""

os.system("cls" if os.name == "nt" else "clear")
print(Colorate.Vertical(Colors.red_to_white, banner))
print(Colorate.Horizontal(Colors.red_to_white, " " * 45 + "by zelt\n"))

def stylized_msg(type, msg):
    colors = {
        "info": Colors.cyan,
        "success": Colors.green,
        "error": Colors.red,
        "warn": Colors.yellow
    }
    prefix = f"{Colorate.Horizontal(Colors.red_to_white, '[*]')} "
    return f"{prefix}{Colorate.Color(colors.get(type, Colors.white), msg)}"

def load_pseudos():
    if not os.path.exists("pseudo à tester.txt"):
        print(stylized_msg("error", "Le fichier 'pseudo à tester.txt' est manquant."))
        return []
    with open("pseudo à tester.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_valid_pseudo(pseudo):
    with open("valide.txt", "a", encoding="utf-8") as f:
        f.write(pseudo + "\n")

def save_used_token(token):
    with open("token use.txt", "a", encoding="utf-8") as f:
        f.write(token + "\n")

def is_valid_token(token):
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    return r.status_code == 200

def change_username(token, password, new_username):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "username": new_username,
        "password": password
    }
    r = requests.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
    return r.status_code == 200

def main():
    pc_name = socket.gethostname()
    print(stylized_msg("info", f"Machine: {pc_name}"))
    print(stylized_msg("info", "Le token Discord est requis pour effectuer des changements."))

    token = input(f"\n{Colorate.Color(Colors.red, '[>]')} Entrez votre token utilisateur Discord: ").strip()
    if not is_valid_token(token):
        print(stylized_msg("error", "Token invalide ou expiré."))
        return

    password = input(f"{Colorate.Color(Colors.red, '[>]')} Entrez votre mot de passe Discord: ").strip()

    pseudos = load_pseudos()
    if not pseudos:
        return

    save_used_token(token)

    for pseudo in pseudos:
        print(stylized_msg("info", f"Vérification de '{pseudo}'..."))
        success = change_username(token, password, pseudo)
        if success:
            print(stylized_msg("success", f"Pseudo modifié avec succès : {pseudo}"))
            save_valid_pseudo(pseudo)
            break
        else:
            print(stylized_msg("warn", f"'{pseudo}' invalide ou déjà utilisé."))
        time.sleep(1.5)

    print(stylized_msg("info", "Vérification terminée."))

if __name__ == "__main__":
    main()
