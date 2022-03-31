#!/usr/bin/env python3

import time
import matplotlib.pyplot as plt
from collections import Counter
import random
import string
import re
import sys
from tkinter import *
from random import randint
import codecs
import socket

# Targetting ip
target_ip = "127.0.0.1"

f = codecs.open(f"{target_ip}.dat", "r", "utf8")
cont = f.read()
f.close()

Data_base = cont.replace("\n",";")
Data_base = Data_base.split(";")
theme = Data_base[0:len(Data_base):3]
question = Data_base[1:len(Data_base):3]
result = Data_base[2:len(Data_base):3]
theme.remove('')
print(theme)

cnt = Counter()
i = 0
for good in theme:
	cnt[good] += 1
	i += 1
	print(cnt)

themes = []
nbr_g_rep = []
i = 0
for k, v in sorted(cnt.items(), key=lambda item: item[1]):
	themes.append(k)
	nbr_g_rep.append(v)

plt.title("Pourcentage de bonnes réponses par matière")
plt.bar(themes, nbr_g_rep)
plt.ylabel("Profil de la personne")
plt.show()
