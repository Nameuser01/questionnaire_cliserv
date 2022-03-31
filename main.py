#!/usr/bin/env python3
# -*- coding: utf8 -*-

from tkinter import *
from random import randint
import time
import codecs
import requests

# Chargements des questions données avec les fichiers liés
def Load_db1():
    label_titre.configure(text='\nQuestionnaire Réseau\n')
    Data_base = "".join(open("Berenger.txt","r"))
    Data_base = Data_base.replace("\n",",")
    Data_base = Data_base.split(",")

    Questions = Data_base[0:len(Data_base):2]
    Reponses = Data_base[1:len(Data_base):2]
    i=0
    global Quizz
    Quizz={}
    # print(Questions)
    for i in range(len(Questions)-1):
        # Questions[i] = Questions[i].decode("utf8")
        # Reponses[i] = Reponses[i].decode("utf8")
        Quizz[Questions[i]]= Reponses[i]
    intro()
    
def Load_db2():
    label_titre.configure(text='\nQuestionnaire Culture générale\n')
    Data_base = "".join(open("Sandu.txt","r"))
    Data_base = Data_base.replace("\n",",")
    Data_base = Data_base.split(",")

    Questions = Data_base[0:len(Data_base):2]
    Reponses = Data_base[1:len(Data_base):2]
    i=0
    global Quizz
    Quizz={}
    for i in range(len(Questions)-1):
        # Questions[i] = Questions[i].decode("utf8")
        # # Reponses[i] = Reponses[i].decode("utf8")
        Quizz[Questions[i]]= Reponses[i]
    intro()
    
def Load_db3():
    label_titre.configure(text='\nQuestionnaire Géographie\n')
    Data_base = "".join(open("Christophe.txt","r"))
    Data_base = Data_base.replace("\n",",")
    Data_base = Data_base.split(",")

    Questions = Data_base[0:len(Data_base):2]
    Reponses = Data_base[1:len(Data_base):2]
    i=0
    global Quizz
    Quizz={}
    #print Questions
    for i in range(len(Questions)-1):
        # Questions[i] = Questions[i].decode("utf8")
        # Reponses[i] = Reponses[i].decode("utf8")
        Quizz[Questions[i]]= Reponses[i]
    intro()
    
def Load_db4():
    label_titre.configure(text='\nQuestionnaire Anglais\n')
    Data_base = "".join(open("ying.txt","r"))
    Data_base = Data_base.replace("\n",",")
    Data_base = Data_base.split(",")

    Questions = Data_base[0:len(Data_base):2]
    Reponses = Data_base[1:len(Data_base):2]
    i=0
    global Quizz
    Quizz={}
    for i in range(len(Questions)-1):
        # Questions[i] = Questions[i].decode("utf8")
        # # Reponses[i] = Reponses[i].decode("utf8")
        Quizz[Questions[i]]= Reponses[i]
    intro()
    
def Load_db5():
    label_titre.configure(text='\nQuestionnaire Géographie\n')
    Data_base = "".join(open("Viet.txt","r"))
    Data_base = Data_base.replace("\n",",")
    Data_base = Data_base.split(",")

    Questions = Data_base[0:len(Data_base):2]
    Reponses = Data_base[1:len(Data_base):2]
    i=0
    global Quizz
    Quizz={}
    for i in range(len(Questions)-1):
        # Questions[i] = Questions[i].decode("utf8")
        # Reponses[i] = Reponses[i].decode("utf8")
        Quizz[Questions[i]]= Reponses[i]
    intro()
    
def Load_db6():
    label_titre.configure(text='\nQuestionnaire Global\n')
    Data_base = "".join(open("data.txt","r"))
    Data_base = Data_base.replace("\n",",")
    Data_base = Data_base.split(",")

    Questions = Data_base[0:len(Data_base):2]
    Reponses = Data_base[1:len(Data_base):2]
    i=0
    global Quizz
    Quizz={}
    for i in range(len(Questions)-1):
        # Questions[i] = Questions[i].decode("utf8")
        # # Reponses[i] = Reponses[i].decode("utf8")
        Quizz[Questions[i]]= Reponses[i]
    intro()


#################################################################################################################
#Cette fonction initie les variables, et demande le nombre de questions voulues,permet le choix du questionnaire#
#################################################################################################################

def intro():   
    global valider,deja,bonnes,Quizz,T,questions,reponses,vies,score,SS
    champs.delete(0,END)
    deja = []
    bonnes,score,SS,vies = 0,0,0,5
    T = len(Quizz)
    questions = Quizz.keys()
    print(questions)
    reponses = Quizz.values()
    label.configure(text="Combien voulez vous de questions ?",fg="black")
    labelVIES.configure(text='Vous avez 5 vies')
    labelScore.configure(text='Votre score:0 pts')
    valider= Button(root,text="ENTRER",command=nb_questions)
    valider.grid(column=1,row=2,sticky="E")
    DB1.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)
    DB2.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)
    DB3.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)
    DB4.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)
    DB5.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)
    DB6.configure(fg='white',bg='white',relief=RAISED,state=DISABLED)
    Indice.configure(state=DISABLED)

# Ici on récupère le nombre de réponses voulues#

def nb_questions():
    global nb_Questions,valider
    nb_Questions = int(champs.get())
    if nb_Questions > 20 :
        valider.configure(state=DISABLED)
        nb_Questions = 20
        label.configure(text="Le nombre maximale de questions est 20",fg='black')
        label.update()
        time.sleep(3)
        
    else :
        nb_Questions = nb_Questions
        
    champs.delete(0,END)
    quizz()


def countDown(a):
    tRestant=a
    Compteur.config(bg='white')
    Compteur.config(height=3, font=('times', 14, 'bold'))
    while tRestant > 0:
        if champs.get() == " ": #on  verifie si dans l' ENTRY champs on a " " 
#(qui est inseré après avoir validé la reponse avant que le temps pour une question finit) sa sert à metre le compteur à 0 =>
# => il ne vérifie plus la réponse(le champs qui est effacé deja après le check() ) pour n'afficher pas le message de réponse fausse
            champs.delete(0,END)
            tRestant = 0                
        Compteur["text"] = tRestant    
        Compteur.update()
        time.sleep(1)
        tRestant -=1        
    if tRestant == 0:
        Compteur.configure(text='0')
        check()



#############################################################################################################
# La fonction quizz sert à tourner le jeu(donner des questions aléatoires...) et aussi gère le fin du jeu.  #
#Les reponses aux questions sont vérifiées à l'aide de la fonction check() décrite plus bas                 #
#############################################################################################################
def double():
    check()
    champs.insert(0, " " )
    
    
def quizz():
    global j,valider,vies,bonnes,nb_Questions
    labelRepSaisie.configure(text='')
    if nb_Questions<bonnes+5:
        nbQuestAffich = nb_Questions
    else:
        nbQuestAffich = bonnes + 5
    Indice1.configure(text="",bg="white")
    Indice2.configure(text="",bg="white")
    Indice3.configure(text="",bg="white")
    Indice4.configure(text="",bg="white")
    print("DEBEUG: ON EST Là !!!!!!")
    if len(deja)< nb_Questions and vies>0:
        j = randint(0,T-1)
        while j in deja :
            j = randint(0,T-1)
        deja.append(j)    
        label.configure(text="%s ?" % (questions[j]),fg="black")
        Indice.configure(state=ACTIVE)
        valider.configure(text="Validation réponse",state=ACTIVE,command = double)  # double fait check() et insère espace dans champs(Entry) pour marquer le fait d'avoir répondu avant le temps
        countDown(25)      
        
    else:
        labelVIES.configure(text='Vous avez fini la partie')
        Compteur.configure(text="")
        label.configure(text="Vous avez eu %d bonnes réponses sur %d questions !\nPour une nouvelle partie choisissez un Questionnaire\nquelconque" % (bonnes,nbQuestAffich),fg="black")
        DB1.configure(fg='black',bg='grey',state=ACTIVE)
        DB2.configure(fg='black',bg='grey',state=ACTIVE)
        DB3.configure(fg='black',bg='grey',state=ACTIVE)
        DB4.configure(fg='black',bg='grey',state=ACTIVE)
        DB5.configure(fg='black',bg='grey',state=ACTIVE)
        DB6.configure(fg='black',bg='grey',state=ACTIVE)
        valider.configure(text='ENTRER',state=DISABLED)
        Indice.configure(state=DISABLED)
        

################################################################################################################
#c'est une fonction qui vérifie si la réponse saisie correspond à celle attendue. On considère que les réponses #
# avec une lettre fausse sont bonnes et celles avec une lettre saisie comme erreur de frappe sont aussi bonnes #
################################################################################################################

def check():
    global reponse,vies,deja,nb_Questions,score,SS,bonnes
    reponse = champs.get().encode("utf8").decode("utf8")#transforme toutes les reponses en texte unicode mais avant en string
    #on a ajouté encode pour pouvoir aplliquer decode aux réponses accentuées qui sont automatiquement unicode(mais decode transforme de string en unicode)
    champs.delete(0,END)
    ##############################################
    T1,T2=[],[]
    p,q=0,0
    for p in range (len(reponses[j])):
        T1.append(ord(reponses[j][p].lower()))
        p +=1                                        #conversion
    for q in range (len(reponse)):
        T2.append(ord(reponse[q].lower())) 
        q +=1
    ##############################################
    print("rep database=",T1,reponses[j],type(reponses[j]),"\n rep=",T2,reponse ,type(reponse))
    if len(T1)==len(T2):          #
        kk,kj=0,0                 #
        for kk in range(len(T1)): #si une letre a l'interieur de la réponse saisie ne correspond pas on considère la réponse bonne quand même
            if T1[kk]==T2[kk]:    #
                kj +=1            #
        if kj == len(T1)-1:       #
            T2=T1                 #
    if len(T1) == len(T2)-1 :                                     # 
        kk,kj,T22=0,0,T2[0:(len(T2)-1)]                           #
        while (kk in range(len(T2)) )   and   kk <= len(T1) -1 :  #
            if (T1[kk] != T2[kk]) and kj==0 :                     #
                kj +=1                                            #cas ou on a inseré par erreur 1 lettre 
                T2.remove(T2[kk])                                 #
            kk +=1                                                #
        if T1 == T22:                                             #
            T2=T1                                                  #
    if  T1 == T2 :
        if SS == 1:
            bonnes,score = bonnes + 1,score + 3
        else:
            bonnes,score = bonnes + 1,score + 5
        SS=0
        label.configure(text="BRAVO!",fg="green")
        if score > 0:
            labelScore.configure(text='Votre score:%d pts'% score)
        else:
            score=0
            labelScore.configure(text='Votre score: 0 pts')
        valider.configure(text="Question Suivante",command=quizz)
    else :
        SS=0 
        if reponse == '' or reponse == ' ':
            socre =score
            labelRepSaisie.configure(text='Vous n''avez rien saisi')
        else:
            score -=2    
            labelRepSaisie.configure(text='Vous avez saisi:"%s"'% reponse)
             
        label.configure(text="Ah non!, c'est %s" % reponses[j],fg="red")
        valider.configure(text="Question Suivante",command=quizz)
        vies=vies-1  
        labelVIES.configure(text='Vous avez encore %d vie(s)'% vies)
        if score > 0:
            labelScore.configure(text='Votre score:%d pts'% score)
        else:
            score =0
            labelScore.configure(text='Votre score: 0 pts')
        if len(deja) == nb_Questions or vies == 0 :
            valider.configure(text="Suivant",command=quizz)
##############################################################################################################
#La fonction indice sert a afficher 4 variantes de réponses possibles.Elle initialise une variable pour      #
#compter le score final en ajoutant moins de points pour une réponse correcte avec l'utilisation des indices #
##############################################################################################################
def indice():
    global SS,j,reponses
    SS,deja1,deja2=1,[],[]
    T3=[0,1,2,3]    
    d=randint(0,3)
    deja1.append(d)
    T3[d] = reponses[j]
    w,w1,w2=randint(0,19),randint(0,19),randint(0,19)
    if w==j:
        while w==j:
            w=randint(0,19)    
    if (w1==w) or (w1==j) :
        while (w1==w) or (w1==j):
            w1=randint(0,19)
    if (w2==w) or (w2==w1) or (w2==j):
        while (w2==w) or (w2==w1) or (w2==j):
            w2=randint(0,19)
    ################################
    
    if T3[0] == reponses[j] :
        T3[1]=reponses[w]
        T3[2]=reponses[w1]
        T3[3]=reponses[w2]    
    else:
        T3[0]=reponses[w]
        if T3[1] == reponses[j]:
            T3[2]=reponses[w1]
            T3[3]=reponses[w2]
        else:
            T3[1] = reponses[w1]
            if     T3[2] == reponses[j]:
                    T3[3]=reponses[w2]
            else:
                T3[2]=reponses[w2]
    Indice.configure(state=DISABLED)
    Indice1.configure(text=" %s " % T3[0],bg='white',fg="black")
    Indice2.configure(text=" %s " % T3[1],bg='white',fg="black")
    Indice3.configure(text=" %s " % T3[2],bg='white',fg="black")
    Indice4.configure(text=" %s " % T3[3],bg='white',fg="black")
##################################################################
#       Cette fonction sert à ouvrir les regles du jeu           #
##################################################################
def ouvrir():
    ofi = codecs.open("reglesJeu.txt", "r", "utf-8")
    t= ofi.read()
    reg=Tk()
    reg.title('Regles du jeu')
    lab=Label(reg,text=t,bg='white',fg='black')
    lab.pack()
    reg.mainloop()
    
    
#################################################################
#            Là on construit l'interface graphique du jeu       #
#################################################################

root=Tk()
root.title("Projet Python !")
root.geometry("900x275")
root.configure(bg="white")


label_titre = Label(root,text="\nQuiz informatique\n",bg="blue",fg="white")
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

DB1 = Button(root,text="Questionnaire Réseau",command=Load_db1)
DB2 = Button(root,text="Questionnaire Culture Générale",command=Load_db2)
DB2 = Button(root,text="Questionnaire Culture Générale",command=Load_db2)
DB3 = Button(root,text="Questionnaire Géopolitique",command=Load_db3)
DB4 = Button(root,text="Questionnaire Anglais",command=Load_db4)
DB5 = Button(root,text="Questionnaire Geographie",command=Load_db5)   
DB6 = Button(root,text="Commencer le questionnaire",command=Load_db6) 
DB1.grid(column=1,row=6)#,sticky="W")  
DB2.grid(column=0,row=6)#,sticky="W")
DB3.grid(column=0,row=5)#,sticky="W") 
DB4.grid(column=1,row=5)#,sticky="W")
DB5.grid(column=1,row=4)#,sticky="W")
DB6.grid(column=0,row=4)#,sticky="W")

Quitter = Button(root,text="Quitter",command=root.destroy)
Quitter.grid(column=3,row=6)#,sticky="E")
Indice = Button(root,text="Indice",state=DISABLED,command=indice)
Indice.grid(column=2,row=6)#,sticky="E")

Indice1 = Label(root)
Indice1.grid(column=2,row=1)
Indice2 = Label(root)
Indice2.grid(column=2,row=2)
Indice3 = Label(root)
Indice3.grid(column=3,row=1)
Indice4 = Label(root)
Indice4.grid(column=3,row=2)

Compteur = Label(root)
Compteur.grid(column=1,row=1)

root.mainloop()
