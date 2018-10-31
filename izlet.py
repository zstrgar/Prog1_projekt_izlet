import requests
import re
import os
import csv

url_izletov = 'http://www.hribi.net/goreiskanjerezultat.asp?drzavaid=1&gorovjeid=&goraime=&VisinaMIN=&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhodisceMIN=&izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zahtevnostid=&zahtevnostSmucanjeid=&IzhodisceMinOddaljenost=&IzhodisceMAXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0&mojaDolzina=0'
#mapa s podatki
directory = 'Prog1_pariski_hoteli/podatki_izlet'
#ime datoteke, kjer bomo shranili spletno stran
filename = 'spletna_stran_izletov.html'
#ime CSV datoteke
csv = 'podatki.csv'

# Pridobitev podatkov
def download_url_to_string(url):
    ''' Funkcija kot argument prejme url in z uporabo ukaza 
    requests poskusi prenesti vsebino strani kot niz.'''
    try:
        r = requests.get(url)
        print("Shranjeno!")
    except requests.exceptions.ConnectionError:
        print("Stran ne obstaja")
        return None
    return r.text


def save_page(url):
    ''' Pomožna funkcija, ki shrani url stran
    kot niz v datoteko v neki mapi.'''
    besedilo = download_url_to_string(url)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as datoteka:
        datoteka.write(besedilo)       
    return None

# Obdelava podatkov
def read_file_to_string(directory, filename):
    ''' Vrne vsebino strani iz datoteke, kjer je shranjena, kot niz. '''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()
    return None


vzorec = re.compile(
    r'<td colspan="2"><a href="(?P<Povezava>.+?)"><b>(?P<Ime>.+?)&nbsp;.+?',
    flags=re.DOTALL
)


def page_to_izleti(page):
    izleti = re.findall(vzorec, page)
    return izleti


vzorec_izleta = re.compile(
    r'<tr><td><b>Gorovje:</b> <a class="moder" href=.*?>(?P<Gorovje>.*?)</a></td></tr>.*?'
    r'</b> (?P<Nadmorska_visina>\d{1,4})&nbsp;m</td></tr>.*?'
    r'<tr><td><b>Vrsta:</b> (?P<vrsta>.*?)</td></tr>.*?'
    r'<tr><td><b>Priljubljenost:</b> (?P<Priljubljenost>\d{1,3}%).*?'
    r'\((?P<mesto>\d{3}\. mesto)\)</td></tr>.*?'
    #r'.(?P<Mesto_priljubljenosti>\d{1,4}\.mesto).</td></tr>.*?',
    r'href="#poti">(?P<St_poti>\d)</a></td></tr>.*?',
    flags=re.DOTALL
)