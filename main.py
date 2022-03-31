#!/usr/bin/env python3
# -*- coding: utf8 -*-

from tkinter import *
from random import randint
import time
import codecs
import socket


# On lit les fichiers pour récupérer les questions/réponses

def Load_db1():
    label_titre.configure(text='\nQuestionnaire Global\n')
    f = codecs.open("data.txt", "r", "utf8")
    Data_base = f.read()
    f.close()
    Data_base = Data_base.replace("\n",";")
    Data_base = Data_base.split(";")
    Questions = Data_base[0:len(Data_base):2]
    Reponses = Data_base[1:len(Data_base):2]
    i = 0
    global Quizz
    Quizz = {}
    for i in range(len(Questions) - 1):
        Quizz[Questions[i]] = Reponses[i]
    intro()


# initiation variables, demande nombre questions, choix du questionnaire

def intro():
    global valider, deja, bonnes, Quizz, T, questions, reponses, score, SS
    champs.delete(0, END)
    deja = []
    questions = []
    reponses = []
    bonnes, score, SS = 0, 0, 0
    T = len(Quizz)
    for key, value in Quizz.items():
        questions.append(key)
        reponses.append(value)
    label.configure(text="Combien voulez vous de questions ?", fg="black")
    labelScore.configure(text='Votre score: 0 pts')
    valider = Button(root,text="ENTRER",command=nb_questions)
    valider.grid(column=1,row=2,sticky="E")
    DB1.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)


# Nombre de questions voulues

def nb_questions():
    global nb_Questions, valider
    gut = False
    while (gut == False):
        nb_Questions = int(champs.get())
        if (nb_Questions <= len(Quizz) and nb_Questions > 0):
            gut = True
        else:
            label.configure(text=f"Le nombre max de questions est de : {len(Quizz)}")
            valider.configure(state=DISABLED)
            label.update()
            time.sleep(2)
    champs.delete(0,END)
    quizz()


def countDown(a):
    tRestant=a
    Compteur.config(bg='white')
    Compteur.config(height=3, font=('times', 14, 'bold'))
    while tRestant > 0:
        if champs.get() == " ":  # on  verifie si dans l'ENTRY champs on a " " (qui est inseré après avoir validé la reponse avant que le temps pour une question finit) ca sert a metre le compteur à 0 => => il ne vérifie plus la réponse(le champs qui est effacé deja après le check() ) pour n'afficher pas le message de réponse fausse
            champs.delete(0, END)
            tRestant = 0
        Compteur["text"] = round(tRestant, 0)
        Compteur.update()
        time.sleep(0.01)
        tRestant -= 0.01
    if tRestant == 0:
        Compteur.configure(text='0')
        check()


def double():
    check()
    champs.insert(0, " ")
    


def quizz():
    global j, valider, bonnes, nb_Questions
    labelRepSaisie.configure(text="")
    if nb_Questions < bonnes + 5:
        nbQuestAffich = nb_Questions
    else:
        nbQuestAffich = bonnes + 5
    if len(deja) < nb_Questions:  # On vérifie qu'il reste des questions qu'on a pas encore posé
        j = randint(0, T - 1)
        while j in deja:  # On vérifie que la question n'est pas déjà tombée
            j = randint(0, T - 1)
        deja.append(j)
        label.configure(text=f"{questions[j]} ?", fg="black")
        valider.configure(text="Validation réponse", state=ACTIVE, command=double)  # double fait check() et insère espace dans champs(Entry) pour marquer le fait d'avoir répondu avant le temps
        countDown(25)
        
    else:
        Compteur.configure(text="")
        label.configure(text=f"Vous avez eu {bonnes} bonnes réponses sur {nbQuestAffich} questions !", fg="black")
        DB1.configure(fg='black', bg='grey', state=ACTIVE)
        valider.configure(text='ENTRER', state=DISABLED)
        

def check():
    global reponse, deja, nb_Questions, score, SS, bonnes
    reponse = champs.get().encode("utf8").decode("utf8")  # transforme toutes les reponses en texte unicode mais avant en string
    # on a ajouté encode pour pouvoir aplliquer decode aux réponses accentuées qui sont automatiquement unicode(mais decode transforme de string en unicode)
    champs.delete(0, END)
    ##############################################
    T1, T2 = [], []
    p, q = 0, 0
    for p in range (len(reponses[j])):  # On passe les réponses en minuscules pour les comparer
        T1.append(ord(reponses[j][p].lower()))
        p += 1
    for q in range (len(reponse)):
        T2.append(ord(reponse[q].lower()))
        q += 1
    ##############################################
    registration(questions[j], reponse)
    print(f"Question: {questions[j]}\nrep true = {T1} , {reponses[j]} , {type(reponses[j])}\nrep user = {T2} , {reponse} , {type(reponse)}")
    if (len(T1) == len(T2)):
        kk, kj = 0, 0
        for kk in range(len(T1)):  # si une lettre a l'interieur de la réponse saisie ne correspond pas on considère la réponse bonne quand même
            if T1[kk] == T2[kk]:
                kj += 1
        if kj == len(T1) - 1:
            T2=T1
    if (len(T1) == len(T2) - 1):
        kk, kj, T22 = 0, 0, T2[0:(len(T2)-1)]
        while (kk in range(len(T2))) and kk <= len(T1) - 1:
            if (T1[kk] != T2[kk]) and kj == 0:
                kj += 1  # cas ou on a inseré par erreur 1 lettre (CA MARCHE PAS)
                T2.remove(T2[kk])
            kk += 1
        if T1 == T22:
            T2 = T1
    if  T1 == T2:
        if SS == 1:
            bonnes, score = bonnes + 1, score + 3
        else:
            bonnes, score = bonnes + 1, score + 5
        SS=0
        label.configure(text="BRAVO!", fg="green")
        if score > 0:
            labelScore.configure(text=f"Votre score: {score} pts")
        else:
            score = 0
            labelScore.configure(text='Votre score: 0 pts')
        valider.configure(text="Question Suivante", command=quizz)
    else:
        SS = 0
        if reponse == "" or reponse == " ":
            socre = score
            labelRepSaisie.configure(text="Vous n'avez rien saisi")
        else:
            score -= 2    
            labelRepSaisie.configure(text=f"Vous avez saisi: {reponse}")
             
        label.configure(text=f"Mauvaise réponse !,\nLa bonne réponse était <{reponses[j]}>", fg="red")
        valider.configure(text="Question Suivante",command=quizz)
        if score > 0:
            labelScore.configure(text=f"Votre score: {score} pts")
        else:
            score = 0
            labelScore.configure(text='Votre score: 0 pts')
        if len(deja) == nb_Questions:
            valider.configure(text = "Suivant", command = quizz)


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
    reg.mainloop()
    
    
# Travail sur Tkinter (GUI)

root=Tk()
root.title("Projet Python !")
root.geometry("900x275")
root.configure(bg="white")


label_titre = Label(root, text="\nQuiz informatique\n", bg="grey", fg="white")
label_titre.grid(column=0, row=0, sticky="NW")
label = Label(root, bg="white")
label.grid(column=0, row=1, sticky="W")
labelRepSaisie = Label(root, bg="white")
labelRepSaisie.grid(column=0, row=3, sticky="W")
labelScore = Label(root, bg="white", fg='black')
labelScore.grid(column=2, row=5, sticky="NW")

champs = Entry(root)
champs.grid(column=0, row=2)  # ,sticky="W")

bb = Button(root, text="Regles Jeu", command=read_rules)
bb.grid(column=3, row=0)  # , sticky="W")

DB1 = Button(root, text="START", command=Load_db1)
DB1.grid(column=0, row=4)  # ,sticky="W")  

Quitter = Button(root, text="Quitter",command=root.destroy)
Quitter.grid(column=3, row=4, sticky="E")

Compteur = Label(root)
Compteur.grid(column=1, row=1, sticky="NE")

root.mainloop()

hote = "10.0.55.1"
port = 55555
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print(f"[+] Connexion sur le port {port}")
readfile = codecs.open("registry.dat", "r", "utf8")
message = readfile.read()
print(f"Le message a envoyer est le suivant\n{message}")
socket.send(message.encode())
print("[-] Fin de connexion")
socket.close()

# Nettoyage du fichier temporaire
file = open("registry.dat","w")
file.close()
