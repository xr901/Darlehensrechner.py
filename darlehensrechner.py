#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Darlehensrechner
#	Laufzeit
#	Gesamtzinsen nach x Jahren
#	Annuität bestehend aus Tilgung und Zinsen

import locale


kredit = 150					# Darlehen in Tausend €
kredit *= 1000				
sollzins = 2.00					# Sollzins in % pro Jahr
zahlung = 7500					# Zahlungsrate bzw. Annuität (Tilgung und Zins) pro Jahr
sondertilgung = 7500				# jährliche Sondertilgung, gezahlt im Januar eines Jahres, oft 5 % vom kredit
zperiode = 12					# Zahlungsperiode, x mal im Jahr
skip = 2					# alle skip Jahre Werte ausgeben
graphZeigen = False				# Graph ausgeben (True oder False)

if graphZeigen:
	import matplotlib.pyplot as plot
schulden = kredit				# restliche Schulden, Anfangswert ist der Kredit Faktor Tausend
ezins = (1 + sollzins/zperiode) ** zperiode -1	# effektiver Jahreszins bei monatlicher Zahlung
tilgung = 0					# berechneter Tilgungsanteil je Monat
jahre = 0					# berechnete Gesamtlaufzeit
zsum = 0					# Zinszahlungen gesamt
zlist = []					# Liste mit Zinsen
tlist = []					# Liste mit Tilgungen
jlist = []					# Liste mit Jahren

locale.setlocale(locale.LC_ALL, '')		# regionale Eigenschaften des Systems auslesen
def euro(value):				# Hilfsfunktion Beträge in Euro formatieren
	return locale.currency(value, grouping=True)

print("┌────────────────── Darlehensrechner ──────────────────┐")
print("\tKredit:\t\t\t" + euro(kredit))
print("\tAnnuität:\t\t" + euro(zahlung) + "/a")
print("\t\t\t\t" + euro(zahlung/12) + "/Monat")
if sondertilgung > 0:
	print("\tSondertilgung:\t\t" + euro(sondertilgung) + "/a")
print("\tNominalzins:\t\t" + str(sollzins) + " %/a")
print("\tEff. Jahreszins:\t" + str(round(ezins, 2)) + " %/a")
print("├──────────────────────────────────────────────────────┤")

while schulden > 0:				# while-Schleife bis es keine Schulden mehr gibt
	jahre += 1				# Jahre um eins hochzählen
	if schulden < sondertilgung:		# letztes Jahr Resttilgung durch Sondertilgung
		sondertilgung -= schulden
		schulden = 0
		zins = 0
		tilgung = 0
	else:
		schulden -= sondertilgung		# jährliche Sondertilgung, am Anfang vom Jahr
		zins = schulden * sollzins/100		# Zins für Jahr berechnen
		zsum += zins				# Zins aufsummieren
		tilgung = zahlung - zins		# Tilgung für Jahr berechnen
		if tilgung < 0:				# Sonderfall zu geringe Zahlungsrate
			print("[!] Zahlungsrate zu gering: Zins übersteigt Zahlungsrate.")
			exit(1)

	if schulden < tilgung:			# Sonderfall letztes Jahr, komplette Tilgung
		tilgung = schulden		# letztes Jahr wird nicht monategenau berechnet (Zins)
		schulden = 0
	else:
		schulden -= tilgung		# Restkredit für nächstes Jahr berechnen
	
	# Werte ausgeben alle $skip Jahre und immer das erste und letzte Jahr
	if jahre % skip == 1 or skip == 1 or schulden == 0:
		zlist.append(zins)
		tlist.append(tilgung)
		jlist.append("Jahr " + str(jahre))
		print("Jahr " + str(jahre))
		print("\tZins:\t\t" + euro(zins) + ("\t\t" if zins<100 else "\t") + euro(zins/12) + "/Monat")
		print("\tTilgung:\t" + euro(tilgung) + ("\t\t" if tilgung<100 else "\t") + euro(tilgung/12) + "/Monat")
		if sondertilgung > 0:
			print("\tSondertilgung:\t" + euro(sondertilgung) + ("\t\t" if tilgung<100 else "\t"))
		print("\tRestkredit\t" + euro(schulden))

print("├──────────────────────────────────────────────────────┤")
print("\tLaufzeit:\t\t< " + str(jahre) + " Jahre")
print("\tZinszahlungen:\t\t" + euro(zsum) + " (" + str(round(100/kredit*zsum, 2)) + " %)")
print("└──────────────────────────────────────────────────────┘")

if graphZeigen:
	fig, ax = plot.subplots()
	ax.bar(jlist, tlist, 0.6, label='Tilgung')
	ax.bar(jlist, zlist, 0.6, bottom=tlist, label='Zins')
	ax.set_ylabel("Zahlungsrate in €/a")
	ax.set_title("Annuität über Laufzeit")
	ax.legend()
	plot.show()
