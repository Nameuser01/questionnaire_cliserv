#!/usr/bin/env python3
import os
import time
import codecs
import socket
from tkinter import *
from random import randint
from simplecrypt import encrypt

# Informations client / serveur :
hote = "127.0.0.1"
port = 55555

# Temps de réponse par question :
tmps_rep = 10


# Reading file to get questions/answers
def Load_questions():
    label_titre.configure(text='\nQuestionnaire Global\n')
    f = codecs.open("data.txt", "r", "utf8")
    Data_base = f.read()
    f.close()
    Data_base = Data_base.replace("\n",";")
    Data_base = Data_base.split(";")
    global themes, questions, reponses, rep1, rep2, rep3, rep4, rep5
    themes = Data_base[0:len(Data_base):8]
    questions = Data_base[1:len(Data_base):8]
    reponses = Data_base[2:len(Data_base):8]
    rep1 = Data_base[3:len(Data_base):8]
    rep2 = Data_base[4:len(Data_base):8]
    rep3 = Data_base[5:len(Data_base):8]
    rep4 = Data_base[6:len(Data_base):8]
    rep5 = Data_base[7:len(Data_base):8]
    work_func()


def work_func():
    global valider, bonnes, score, deja
    deja = []
    bonnes = 0
    score = 0
    label.configure(text="Combien voulez vous de questions ?", fg="#d0d3d4")
    labelScore.configure(text=f"Votre score: {score} pts")
    champs.grid(column=0, row=2, sticky="W")  # On affiche le champs d'entrée du nombre de questions
    valider = Button(root, text="ENTRER", command=nb_questions)
    valider.grid(column=1, row=2, sticky="E")
    DB1.configure(fg='white', bg='white', relief=RAISED, state=DISABLED)
    DB1.destroy()


# Nombre de questions à poser
def nb_questions():
    global nb_Questions, valider
    nb_Questions = int(champs.get())
    if (nb_Questions <= len(questions) and nb_Questions > 0):
        quizz()
    else:
        label.configure(text=f"Le nombre max de questions est de : {len(questions)}")
        valider.configure(state=DISABLED)
        label.update()
        time.sleep(2)
        root.destroy()


# Compteur pour chaque question
def countDown(a):
    tRestant = a
    Compteur.config(bg='#2f3640', fg="white")
    Compteur.config(height=3, font=('times', 14, 'bold'))
    champs.destroy()
    while tRestant > 0:
        Compteur["text"] = round(tRestant, 0)
        Compteur.update()
        time.sleep(0.01)
        tRestant -= 0.01
    
    check()  # Cas ou le temps de réponse est dépassé
    

# Quizz running
def quizz():
    global q_selector, cb1, cb2, cb3, cb4, cb5, qa, qb, qc, qd, qe
    # Définition et globalisation des 5 variables qui vont contenir les réponses (booléens)
    cb1 = IntVar()
    cb2 = IntVar()
    cb3 = IntVar()
    cb4 = IntVar()
    cb5 = IntVar()
    if nb_Questions < bonnes + 5:
        nbQuestAffich = nb_Questions
    else:
        nbQuestAffich = bonnes + 5

    if(len(deja) < nb_Questions):  # On vérifie qu'il reste des questions qu'on a pas encore posé
        q_selector = randint(0, len(questions) - 1)
        while q_selector in deja:  # On vérifie que la question n'est pas déjà tombée
            q_selector = randint(0, len(questions) - 1)
        deja.append(q_selector)
        qa = Checkbutton(root, text=f"{rep1[q_selector]}", onvalue=1, offvalue=0, variable=cb1)
        qb = Checkbutton(root, text=f"{rep2[q_selector]}", onvalue=1, offvalue=0, variable=cb2)
        qc = Checkbutton(root, text=f"{rep3[q_selector]}", onvalue=1, offvalue=0, variable=cb3)
        qd = Checkbutton(root, text=f"{rep4[q_selector]}", onvalue=1, offvalue=0, variable=cb4)
        qe = Checkbutton(root, text=f"{rep5[q_selector]}", onvalue=1, offvalue=0, variable=cb5)
        label.configure(text=f"{questions[q_selector]}", fg="#d0d3d4")
        if (rep1[q_selector]):
            qa.grid()
        else:
            pass
        if(rep2[q_selector]):
            qb.grid()
        else:
            pass
        if(rep3[q_selector]):
            qc.grid()
        else:
            pass
        if(rep4[q_selector]):
            qd.grid()
        else:
            pass
        if(rep5[q_selector]):
            qe.grid()
        else:
            pass
        valider.configure(text="Validation réponse", state=ACTIVE, command=check)
        countDown(tmps_rep)
    else:
        Compteur.configure(text="")
        label.configure(text=f"Vous avez eu {bonnes} bonnes réponses sur {nbQuestAffich} questions !", fg="#d0d3d4")
        valider.configure(text='ENTRER', state=DISABLED)
        

# Checking for score update
def check():
    global reponse, deja, nb_Questions, score, bonnes
    # stop = " "
    Compteur.configure(text='0')
    qa.destroy()
    qb.destroy()
    qc.destroy()
    qd.destroy()
    qe.destroy()
    # Vérification des bonnes réponses
    good_rep_cmp = []  # Liste des bonnes réponses
    user_rep_cmp = []  # Liste des réponses de l'utilisateur
    for i in range(len(reponses[q_selector])):
        good_rep_cmp.append(reponses[q_selector][i])
    if (cb1.get() == 1):
        user_rep_cmp.append("1")
    else:
        pass
    if (cb2.get() == 1):
        user_rep_cmp.append("2")
    else:
        pass
    if (cb3.get() == 1):
        user_rep_cmp.append("3")
    else:
        pass
    if (cb4.get() == 1):
        user_rep_cmp.append("4")
    else:
        pass
    if (cb5.get() == 1):
        user_rep_cmp.append("5")
    else:
        pass
    # Comparaison toute simple des deux listes
    if (user_rep_cmp == good_rep_cmp):
        score += 5
        bonnes += 1
        label.configure(text="BRAVO!", fg="green")
        registration(themes[q_selector], questions[q_selector], "correct")
    else:
        score -= 2
        label.configure(text="Mauvaise réponse!", fg="red")
        registration(themes[q_selector], questions[q_selector], "erreur")
    if (score < 0):
        score = 0
    else:
        pass
    labelScore.configure(text=f"Votre score: {score} pts")
    valider.configure(text="Question Suivante", command=quizz)


# Enregistrement des réponses questions de la sessions dans un fichier
def registration(theme, question, result):
    fichier = open("registry.dat", "a")
    fichier.write(f"{theme};{result}\n")
    fichier.close()
    

# Affichage des règles du Quizz
def read_rules():
    ofi = codecs.open("rules.txt", "r", "utf8")
    t = ofi.read()
    ofi.close()
    reg = Tk()
    reg.title("Regles du Quizz")
    lab = Label(reg, text=t, bg="#2e4053", fg="#d0d3d4")
    lab.pack()
    close = Button(reg, text="Quitter", command=reg.destroy)
    close.pack(side=BOTTOM)
    reg.mainloop()
    
    
# Travail sur Tkinter (GUI)
root=Tk()
root.title("Projet Python !")
root.geometry("900x480")
root.configure(bg="#2f3640")

label_titre = Label(root, text="\nProjet Python\n", bg="#2f3640", fg="#d0d3d4")
label_titre.grid(column=0, row=0, sticky="NW")
label = Label(root, bg="#2f3640", fg="#d0d3d4")
label.grid(column=0, row=1, sticky="W")
labelRepSaisie = Label(root, bg="#2f3640", fg="#d0d3d4")
labelRepSaisie.grid(column=0, row=3, sticky="W")
labelScore = Label(root, bg="#2f3640", fg="#d0d3d4")
labelScore.grid(column=2, row=5, sticky="NW")

champs = Entry(root)
# champs.grid(column=0, row=2, sticky="W")

bb = Button(root, text="Règles Jeu", command=read_rules)
bb.grid(column=3, row=0)  # , sticky="W")

DB1 = Button(root, text="Démarrer", command=Load_questions)
DB1.grid(column=0, row=4)  # ,sticky="W")  

Quitter = Button(root, text="Quitter",command=root.destroy)
Quitter.grid(column=3, row=4, sticky="E")

Compteur = Label(root)
Compteur.grid(column=1, row=1, sticky="NE")

root.mainloop()


def do_encrypt(message):
    keypass = "secretpassword"
    message = encrypt(keypass, message)
    return message

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
os.system("clear")
print(f"[+] Connexion sur le port {port}")
readfile = codecs.open("registry.dat", "r", "utf8")
message = readfile.read()
cyphered_message = do_encrypt(message)
socket.send(cyphered_message)
print("[-] Fin de connexion")
socket.close()

# Nettoyage du fichier temporaire
os.remove("registry.dat")
