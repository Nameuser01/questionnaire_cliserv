#!/usr/bin/env python3

import matplotlib.pyplot as plt
from collections import Counter
import codecs

# Targetting ip
target_ip = "127.0.0.1"

f = codecs.open(f"{target_ip}.dat", "r", "utf8")
cont = f.read()
f.close()

Data_base = cont.replace("\n",";")
Data_base = Data_base.split(";")
theme = Data_base[0:len(Data_base):2]
result = Data_base[1:len(Data_base):2]
if (theme[len(theme) - 1] == ''):  # Supprimer la dernière valeur si besoin
	theme.remove('')
else:
	pass

cnt = Counter()
cnt_tot = Counter()
i = 0
for good in theme:
	if (result[i] == "correct"):
		cnt[good] += 1
	else:
		pass
	i += 1

m = 0
for good in theme:
	cnt_tot[good] += 1
	m += 1

themes_0 = []
nbr_g_rep = []
themes_1 = []
nbr_tot_rep = []

i = 0
for k, v in sorted(cnt_tot.items(), key=lambda item: item[1]):
	themes_0.append(k)
	nbr_tot_rep.append(v)

i = 0
for j, x in sorted(cnt.items(), key=lambda item: item[1]):
	themes_1.append(j)
	nbr_g_rep.append(x)

themes_0.reverse()
nbr_g_rep.reverse()
themes_1.reverse()
nbr_tot_rep.reverse()

diff = len(themes_0) - len(themes_1)
if (diff >= 1):
	for i in range(diff):
		nbr_g_rep.append(0)

pourcentage = []
compteur = -1
for i in range(len(themes_0)):
	compteur += 1
	temp = (100 * nbr_g_rep[compteur] / nbr_tot_rep[compteur])
	pourcentage.append(temp)

plt.title(f"Profil de l'utilisateur {target_ip}")
plt.bar(themes_0, pourcentage, width=0.2, align='center')
plt.grid(True)
plt.ylabel("Pourcentage de bonne réponses")
plt.show()
