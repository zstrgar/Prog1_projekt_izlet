import requests
import re
import os
import csv
import time


url_izletov = 'http://www.hribi.net/goreiskanjerezultat.asp?drzavaid=1&gorovjeid=&goraime=&VisinaMIN=&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhodisceMIN=&izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zahtevnostid=&zahtevnostSmucanjeid=&IzhodisceMinOddaljenost=&IzhodisceMAXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0&mojaDolzina=0'
#mapa s podatki
ime_mape = 'Prog1_projekt_izlet/podatki_izlet'
#mapa s spletnimi stranmi
ime_mape_spl = 'Prog1_projekt_izlet/podatki_izlet/Spletne_strani'
#ime datoteke, kjer bomo shranili spletno stran
ime_datoteke = 'spletna_stran_izletov.html'
#ime CSV datoteke
ime_csv = 'podatki_izletov.csv'


vzorec_izletov = re.compile(
    r'<td colspan="2"><a href="(gora\.asp\?gorovjeid=\d+?&id=(\d+?))">'
    r'<b>(.+?)&nbsp;.+?',
    flags=re.DOTALL
)


vzorec_izleta = re.compile(
    r'<title>(?P<ime>.+?)</title>.*?'
    r'gorast\((?P<id>\d+?)\);.*?'
    r'<tr><td><b>Gorovje:</b> <a class="moder" href=.*?>(?P<gorovje>.*?)</a></td></tr>.*?'
    r'</b> (?P<visina>\d{1,4})&nbsp;m</td></tr>.*?'
    r'<tr><td><b>Vrsta:</b> (?P<vrsta>.*?)</td></tr>.*?'
    r'<tr><td><b>Priljubljenost:</b> (?P<priljubljenost>\d+?)%.*?'
    r'\((?P<mesto_priljubljenosti>\d+?)\. mesto\)</td></tr>.*?'
    r'href="#poti">(?P<stevilo_poti>\d+?)</a></td></tr>.*?'
    r'<tr><td colspan="2"><p align="justify">(?P<opis>.*?)</p></td></tr>.*?',
    flags=re.DOTALL
)


### Pridobitev podatkov


def prenesi_url(url):
    ''' Funkcija kot argument prejme url in z uporabo ukaza 
    requests poskusi prenesti vsebino strani kot niz.'''
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        print("Shranjeno!")
    except requests.exceptions.ConnectionError:
        print("Stran ne obstaja")
        return None
    return r.text


def shrani_stran(url, ime_mape_spl, ime_datoteke):
    ''' Pomožna funkcija, ki shrani prenešen url v dani
    mapi kot niz v datoteko.'''
    besedilo = prenesi_url(url)
    os.makedirs(ime_mape_spl, exist_ok=True)
    pot = os.path.join(ime_mape_spl, ime_datoteke)
    with open(pot, 'w', encoding='utf-8') as datoteka:
        datoteka.write(besedilo)       
    return None

#--> shrani_stran(url_izletov, ime_mape_spl, ime_datoteke)


### Zajem podatkov


def pretvori_v_niz(ime_mape_spl, ime_datoteke):
    ''' Vrne vsebino strani iz datoteke, kjer je shranjena, kot niz. '''
    pot = os.path.join(ime_mape_spl, ime_datoteke)
    with open(pot, 'r', encoding='utf-8') as datoteka:
        return datoteka.read()
    return None


def seznam_izletov():
    '''Vrne seznam naborov (url izleta, id izleta, ime izleta) iz strani.'''
    sez_izleti = re.findall(vzorec_izletov, pretvori_v_niz(ime_mape_spl, ime_datoteke))
    return sez_izleti
 
#--> izleti = seznam_izletov()


def podatki_izletov(izleti):
    podatki_izletov = []
    for i in range(len(izleti)):
        url_izleta = 'http://www.hribi.net/' + izleti[i][0]
        stran_izleta = 'stran_izlet_{}.html'.format(izleti[i][1])
        stran = shrani_stran(url_izleta, ime_mape_spl, stran_izleta)
        time.sleep(1)
        niz = pretvori_v_niz(ime_mape_spl, stran_izleta)
        izlet = vzorec_izleta.search(niz)
        podatki_izletov.append(izlet.groupdict())
    return podatki_izletov


### Zapis podatkov v CSV


# def zapisi_podatke_v_csv(seznam_podatkov, ime_mape, ime_csv):
#    '''Zapiše dani seznam slovarjev podatkov v 
#    ime_mape/ime_csv kot csv datoteko.'''
#    imena_stolpcev = seznam_podatkov[0].keys()
#    vrstice = seznam_podatkov
#    os.makedirs(ime_mape, exist_ok=True)
#    pot = os.path.join(ime_mape, ime_csv)
#    with open(pot, 'w', encoding= 'utf-8') as csv_dat:
#        writer = csv.DictWriter(csv_dat, fieldnames=imena_stolpcev)
#        writer.writeheader()
#        for vrstica in vrstice:
#            writer.writerow(vrstica)
#    return None

#--> zapisi_podatke_v_csv(podatki_izletov(izleti), ime_mape, ime_csv)
