import requests
import re
import os
import csv

url_izletov = 'http://www.hribi.net/goreiskanjerezultat.asp?drzavaid=1&gorovjeid=&goraime=&VisinaMIN=&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhodisceMIN=&izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zahtevnostid=&zahtevnostSmucanjeid=&IzhodisceMinOddaljenost=&IzhodisceMAXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0&mojaDolzina=0'
#mapa s podatki
ime_mape = 'Prog1_projekt_izlet/podatki_izlet'
#ime datoteke, kjer bomo shranili spletno stran
ime_datoteke = 'spletna_stran_izletov.html'
#ime CSV datoteke
csv_izletov = 'podatki.csv'


# Pridobitev podatkov


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


def shrani_stran(url, ime_mape, ime_datoteke):
    ''' Pomožna funkcija, ki shrani prenešen url v dani 
    mapi kot niz v datoteko.'''
    besedilo = prenesi_url(url)
    os.makedirs(ime_mape, exist_ok=True)
    pot = os.path.join(ime_mape, ime_datoteke)
    with open(pot, 'w', encoding='utf-8') as datoteka:
        datoteka.write(besedilo)       
    return None


# Obdelava podatkov


def pretvori_v_niz(ime_mape, ime_datoteke):
    ''' Vrne vsebino strani iz datoteke, kjer je shranjena, kot niz. '''
    pot = os.path.join(ime_mape, ime_datoteke)
    with open(pot, 'r', encoding='utf-8') as datoteka:
        return datoteka.read()
    return None


vzorec_izletov = re.compile(
    r'<td colspan="2"><a href="(?P<Povezava>gora\.asp\?gorovjeid=\d+?&id=(?P<Id_izleta>\d+?))">'
    r'<b>(?P<Ime>.+?)&nbsp;.+?',
    flags=re.DOTALL
)


vzorec_izleta = re.compile(
    r'<title>(?P<Ime>.+?)</title>.*?'
    r'gorast\((?P<Id_izleta>\d+?)\);.*?'
    r'<tr><td><b>Gorovje:</b> <a class="moder" href=.*?>(?P<Gorovje>.*?)</a></td></tr>.*?'
    r'</b> (?P<Visina>\d{1,4})&nbsp;m</td></tr>.*?'
    r'<tr><td><b>Vrsta:</b> (?P<Vrsta>.*?)</td></tr>.*?'
    r'<tr><td><b>Priljubljenost:</b> (?P<Priljubljenost>\d{1,3}%).*?'
    r'\((?P<Mesto_priljubljenosti>\d{1,4}\. mesto)\)</td></tr>.*?'
    r'href="#poti">(?P<Stevilo_poti>\d)</a></td></tr>.*?'
    r'<tr><td colspan="2"><p align="justify">(?P<Opis>.*?)</p></td></tr>.*?',
    flags=re.DOTALL
)


def seznam_izletov():
    '''Vrne seznam naborov (url izleta, id izleta, ime izleta) iz strani.'''
    sez_izleti = re.findall(vzorec_izletov, pretvori_v_niz(ime_mape, ime_datoteke))
    return sez_izleti


izleti = seznam_izletov()


def podatki_izletov(izleti):
    podatki_izletov = []
    for i in range(0, 3):
        url_izleta = 'http://www.hribi.net/' + izleti[i][0]
        stran_izleta = 'stran_izlet_{}.html'.format(izleti[i][1])
        stran = shrani_stran(url_izleta, ime_mape, stran_izleta)
        niz = pretvori_v_niz(ime_mape, stran_izleta)
        izlet = vzorec_izleta.search(niz)
        podatki_izletov.append(izlet.groupdict())
    return podatki_izletov

podatki_izletov = podatki_izletov(izleti)


def zapisi_csv(imena_stolpcev, vrstice, ime_mape, ime_datoteke):
    '''Zapiše datoteko v CSV file v ime_mape/ime_datoteke. 
    Imena_stolpcev je seznam nizov, vrstice seznam slovarjev, kjer
    se vsak ključ (ime_stolpca) ujema z neko vrednostjo'''
    os.makedirs(ime_mape, exist_ok=True)
    pot = os.path.join(ime_mape, ime_datoteke)
    with open(pot, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_stolpcev)
        writer.writeheader()
        for row in vrstice:
            writer.writerow(row)
    return None


def zapisi_izlete_v_csv(seznam_podatkov):
    imena_stolpcev = seznam_podatkov[0].keys()
    zapisi_csv(imena_stolpcev, seznam_podatkov, ime_mape, csv_izletov)
    return None