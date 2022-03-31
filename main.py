#!/usr/bin/env python3
# -*- coding: utf8 -*-

from tkinter import *
from random import randint
import time
import codecs
import requests


# On lit les fichiers pour récupérer les questions/réponses

def Load_db1():
    label_titre.configure(text='\nQuestionnaire Global\n')
    f = codecs.open("data.txt", "r", "utf8")
    Data_base = f.read()
    f.close()
    Data_base = Data_base.replace("\n",",")
    Data_base = Data_base.split(",")
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
    global valider, deja, bonnes, Quizz, T, questions, reponses, vies, score, SS
    champs.delete(0, END)
    deja = []
    questions = []
    reponses = []
    bonnes, score, SS, vies = 0, 0, 0, 5
    T = len(Quizz)
    for key, value in Quizz.items():
        questions.append(key)
        reponses.append(value)
    label.configure(text="Combien voulez vous de questions ?", fg="black")
    labelVIES.configure(text='Vous avez 5 vies')
    labelScore.configure(text='Votre score: 0 pts')
    valider = Button(root,text="ENTRER",command=nb_questions)
    valider.grid(column=1,row=2,sticky="E")
    DB1.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)


# Nombre de questions voulues

def nb_questions():
    global nb_Questions,valider
    nb_Questions = int(champs.get())
    if nb_Questions > 20:
        valider.configure(state=DISABLED)
        nb_Questions = 20
        label.configure(text="Le nombre maximale de questions est 20", fg='black')
        label.update()
        time.sleep(3)
        
    else:
        nb_Questions = nb_Questions
        
    champs.delete(0,END)
    quizz()


def countDown(a):
    tRestant=a
    Compteur.config(bg='white')
    Compteur.config(height=3, font=('times', 14, 'bold'))
    while tRestant > 0:
        if champs.get() == " ":  # on  verifie si dans l' ENTRY champs on a " " (qui est inseré après avoir validé la reponse avant que le temps pour une question finit) sa sert à metre le compteur à 0 => => il ne vérifie plus la réponse(le champs qui est effacé deja après le check() ) pour n'afficher pas le message de réponse fausse
            champs.delete(0, END)
            tRestant = 0
        Compteur["text"] = tRestant
        Compteur.update()
        time.sleep(1)
        tRestant -= 1
    if tRestant == 0:
        Compteur.configure(text='0')
        check()

# quizz() => questions aléatoires et gère fin de jeu.

def double():
    check()
    champs.insert(0, " ")
    
    
def quizz():
    global j, valider, vies, bonnes, nb_Questions
    labelRepSaisie.configure(text='')
    if nb_Questions < bonnes + 5:
        nbQuestAffich = nb_Questions
    else:
        nbQuestAffich = bonnes + 5
    if len(deja) < nb_Questions and vies > 0:  # Si il reste des questions à poser et que le nombre de vies est encore positif then...
        j = randint(0, T - 1)
        while j in deja:  # On vérifie que la question n'est pas déjà tombée
            j = randint(0, T - 1)
        deja.append(j)
        print(f"DEBEUG:\nMa question:{questions[j]}\n\n")
        label.configure(text="%s ?" % (questions[j]), fg="black")
        valider.configure(text="Validation réponse",state=ACTIVE,command = double)  # double fait check() et insère espace dans champs(Entry) pour marquer le fait d'avoir répondu avant le temps
        countDown(25)      
        
    else:
        labelVIES.configure(text='Vous avez fini la partie')
        Compteur.configure(text="")
        label.configure(text="Vous avez eu %d bonnes réponses sur %d questions !\nPour une nouvelle partie choisissez un Questionnaire\nquelconque" % (bonnes,nbQuestAffich),fg="black")
        DB1.configure(fg='black',bg='grey',state=ACTIVE)
        valider.configure(text='ENTRER',state=DISABLED)
        

# Fonction qui donne une permissivitée lors lors de la saisie des réponses

def check():
    global reponse, vies, deja, nb_Questions, score, SS, bonnes
    reponse = champs.get().encode("utf8").decode("utf8")#transforme toutes les reponses en texte unicode mais avant en string
    #on a ajouté encode pour pouvoir aplliquer decode aux réponses accentuées qui sont automatiquement unicode(mais decode transforme de string en unicode)
    champs.delete(0, END)
    ##############################################
    T1, T2 = [], []
    p, q = 0, 0
    for p in range (len(reponses[j])):
        T1.append(ord(reponses[j][p].lower()))
        p += 1  # conversion
    for q in range (len(reponse)):
        T2.append(ord(reponse[q].lower())) 
        q += 1
    ##############################################
    print(f"rep database = {T1} , {reponses[j]} , {type(reponses[j])}, \n rep= {T2} , {reponse} , {type(reponse)}")
    if len(T1) == len(T2):
        kk, kj = 0, 0
        for kk in range(len(T1)):  # si une letre a l'interieur de la réponse saisie ne correspond pas on considère la réponse bonne quand même
            if T1[kk] == T2[kk]:
                kj += 1
        if kj == len(T1) - 1:
            T2=T1
    if len(T1) == len(T2) - 1:
        kk, kj, T22 = 0, 0, T2[0:(len(T2)-1)]
        while (kk in range(len(T2)) ) and kk <= len(T1) - 1:
            if (T1[kk] != T2[kk]) and kj == 0:
                kj += 1  # cas ou on a inseré par erreur 1 lettre 
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
            labelScore.configure(text='Votre score:%d pts'% score)
        else:
            score = 0
            labelScore.configure(text='Votre score: 0 pts')
        valider.configure(text="Question Suivante",command=quizz)
    else:
        SS = 0
        if reponse == '' or reponse == ' ':
            socre = score
            labelRepSaisie.configure(text='Vous n''avez rien saisi')
        else:
            score -= 2    
            labelRepSaisie.configure(text='Vous avez saisi:"%s"'% reponse)
             
        label.configure(text="Ah non!, c'est %s" % reponses[j],fg="red")
        valider.configure(text="Question Suivante",command=quizz)
        vies=vies-1  
        labelVIES.configure(text='Vous avez encore %d vie(s)'% vies)
        if score > 0:
            labelScore.configure(text='Votre score:%d pts'% score)
        else:
            score = 0
            labelScore.configure(text='Votre score: 0 pts')
        if len(deja) == nb_Questions or vies == 0 :
            valider.configure(text = "Suivant", command = quizz)

# Affichage des règles du Quizz

def ouvrir():
    ofi = codecs.open("rules.txt", "r", "utf-8")
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


label_titre = Label(root,text="\nQuiz informatique\n",bg="grey",fg="white")
label_titre.grid(column=0,row=0,sticky="NW")
label = Label(root,bg="white")
label.grid(column=0,row=1,sticky="W")
labelVIES = Label(root,bg='white',fg='black')
labelVIES.grid(column=2,row=4,sticky="NW")
labelRepSaisie = Label(root,bg="white")
labelRepSaisie.grid(column=0,row=3,sticky="W")
labelScore = Label(root,bg="white",fg='black')
labelScore.grid(column=2,row=5,sticky="NW")

champs = Entry(root)
champs.grid(column=0,row=2,sticky="W")

bb = Button(root,text="Regles Jeu",command=ouvrir)
bb.grid(column=3,row=0,sticky="W")

DB1 = Button(root,text="START",command=Load_db1)
DB1.grid(column=0,row=6)#,sticky="W")  

Quitter = Button(root,text="Quitter",command=root.destroy)
Quitter.grid(column=3,row=6)  # ,sticky="E")

Compteur = Label(root)
Compteur.grid(column=1,row=1)

root.mainloop()
