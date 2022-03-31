#!/usr/bin/env python3

import os
import time
import codecs
import socket
from tkinter import *
from random import randint
# from Cryptodome.Cipher import AES
# from Cryptodome.Random import get_random_bytes


# Reading file to get questions/answers

def Load_questions():
    label_titre.configure(text='\nQuestionnaire Global\n')
    f = codecs.open("data.txt", "r", "utf8")
    Data_base = f.read()
    f.close()
    Data_base = Data_base.replace("\n",";")
    Data_base = Data_base.split(";")
    # Data logging
    global themes, questions, reponses, rep1, rep2, rep3, rep4, rep5
    themes = Data_base[0:len(Data_base):8]
    questions = Data_base[1:len(Data_base):8]
    reponses = Data_base[2:len(Data_base):8]
    rep1 = Data_base[3:len(Data_base):8]
    rep2 = Data_base[4:len(Data_base):8]
    rep3 = Data_base[5:len(Data_base):8]
    rep4 = Data_base[6:len(Data_base):8]
    rep5 = Data_base[7:len(Data_base):8]
    # Debeug section
    # print(f"themes:\n{themes}\n\nquestions:\n{questions}\n\n")
    # print(f"reponses:\n{reponses}\n\nrep1:\n{rep1}\n\n")
    # print(f"rep2:\n{rep2}\n\nrep3:\n{rep3}\n\n")
    # print(f"rep4:\n{rep4}\n\nrep5:\n{rep5}\n\n")
    work_func()


def work_func():
    global valider, bonnes, score, SS, deja
    deja = []
    bonnes = 0
    score = 0
    SS = 0
    label.configure(text="Combien voulez vous de questions ?", fg="black")
    labelScore.configure(text=f"Votre score: {score} pts")
    champs.grid(column=0, row=2)  # ,sticky="W")
    valider = Button(root,text="ENTRER",command=nb_questions)
    valider.grid(column=1,row=2,sticky="E")
    DB1.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)


# Nombre de questions à poser
def nb_questions():
    global nb_Questions, valider
    
    gut = False
    while (gut == False): # Is that loop useful ?
        nb_Questions = int(champs.get())
        if (nb_Questions <= len(questions) and nb_Questions > 0):
            gut = True
        else:
            label.configure(text=f"Le nombre max de questions est de : {len(questions)}")
            valider.configure(state=DISABLED)
            label.update()
            time.sleep(2)
            root.destroy()
    quizz()


def countDown(a):
    tRestant = a
    Compteur.config(bg='white')
    Compteur.config(height=3, font=('times', 14, 'bold'))
    # get_nbr_questions = champs.get()
    #champs.delete(0, END)
    #champs.destroy()
    while tRestant > 0:
        Compteur["text"] = round(tRestant, 0)
        Compteur.update()
        time.sleep(0.01)
        tRestant -= 0.01
    if tRestant == 0:
        Compteur.configure(text='0')
        check()


def quizz():
    global q_selector, cb1, cb2, cb3, cb4, cb5, qa, qb, qc, qd, qe
    # Définition et globalisation des 5 variables qui vont contenir les réponses (booléens)
    cb1 = IntVar()
    cb2 = IntVar()
    cb3 = IntVar()
    cb4 = IntVar()
    cb5 = IntVar()
    # labelRepSaisie.configure(text="test")
    if nb_Questions < bonnes + 5:
        nbQuestAffich = nb_Questions
    else:
        nbQuestAffich = bonnes + 5

    if(len(deja) < len(questions)):  # On vérifie qu'il reste des questions qu'on a pas encore posé
        q_selector = randint(0, len(questions) - 1)
        while q_selector in deja:  # On vérifie que la question n'est pas déjà tombée
            q_selector = randint(0, len(questions) - 1)
        deja.append(q_selector)
        qa = Checkbutton(root, text=f"{rep1[q_selector]}", onvalue=1, offvalue=0, variable=cb1)
        qb = Checkbutton(root, text=f"{rep2[q_selector]}", onvalue=1, offvalue=0, variable=cb2)
        qc = Checkbutton(root, text=f"{rep3[q_selector]}", onvalue=1, offvalue=0, variable=cb3)
        qd = Checkbutton(root, text=f"{rep4[q_selector]}", onvalue=1, offvalue=0, variable=cb4)
        qe = Checkbutton(root, text=f"{rep5[q_selector]}", onvalue=1, offvalue=0, variable=cb5)
        label.configure(text=f"{questions[q_selector]} ?", fg="black")
        qa.grid()
        qb.grid()
        qc.grid()
        qd.grid()
        qe.grid()
        valider.configure(text="Validation réponse", state=ACTIVE, command=check)
        countDown(25)
    else:
        Compteur.configure(text="")
        label.configure(text=f"Vous avez eu {bonnes} bonnes réponses sur {nbQuestAffich} questions !", fg="black")
        DB1.configure(fg='black', bg='grey', state=ACTIVE)
        valider.configure(text='ENTRER', state=DISABLED)
        

def check():
    global reponse, deja, nb_Questions, score, SS, bonnes
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
    print(f"Comparing:\n\ngood = {good_rep_cmp}\nuser = {user_rep_cmp}")
    # Comparaison toute simple des deux listes
    if (user_rep_cmp == good_rep_cmp):
        score += 5
        label.configure(text="BRAVO!", fg="green")
    else:
        score -= 2
        label.configure(text="Mauvaise réponse!", fg="red")
    if (score < 0):
        score = 0
    else:
        pass
    labelScore.configure(text=f"Votre score: {score} pts")
    valider.configure(text="Question Suivante", command=quizz)

# Enregistrement des réponses questions de la sessions dans un fichier
def registration(question, user_answer):
    fichier = open("registry.dat", "a")
    fichier.write(f"{question},{user_answer}\n")
    fichier.close()
    

# Affichage des règles du Quizz

def read_rules():
    ofi = codecs.open("rules.txt", "r", "utf8")
    t = ofi.read()
    reg = Tk()
    reg.title("Regles du Quizz")
    lab = Label(reg, text = t, bg = "white", fg = "black")
    lab.pack()
    close = Button(reg, text="Fermer", command=reg.destroy)
    close.pack(side=BOTTOM)
    reg.mainloop()
    
    
# Travail sur Tkinter (GUI)

root=Tk()
root.title("Projet Python !")
root.geometry("900x480")
root.configure(bg="white")


label_titre = Label(root, text="\nQuiz informatique\n", bg="white", fg="black")
label_titre.grid(column=0, row=0, sticky="NW")
label = Label(root, bg="white")
label.grid(column=0, row=1, sticky="W")
labelRepSaisie = Label(root, bg="white")
labelRepSaisie.grid(column=0, row=3, sticky="W")
labelScore = Label(root, bg="white", fg='black')
labelScore.grid(column=2, row=5, sticky="NW")

champs = Entry(root)

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
    # key = get_random_bytes(16)
    # cipher = AES.new(key, AES.MODE_EAX)
    # ciphertext, tag = cipher.encrypt_and_digest(message)
    
    # # enregistrement dans un fichier du chiffre
    # file_out = open("encryptfile.bin", "wb")
    # [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    # file_out.close()
    return message


hote = "127.0.0.1"
port = 55555
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print(f"[+] Connexion sur le port {port}")
readfile = codecs.open("registry.dat", "r", "utf8")
message = readfile.read()
cyphered_message = do_encrypt(message)
print(f"Le message a envoyer est le suivant\n{cyphered_message}")
print(f"Cyphered message:\n{cyphered_message}")
socket.send(cyphered_message.encode())
print("[-] Fin de connexion")
socket.close()

# Nettoyage du fichier temporaire
os.remove("registry.dat")
