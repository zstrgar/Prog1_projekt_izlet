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


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

# Pridobitev podatkov
def download_url_to_string(url):
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


def save_page(url, ime_mape, ime_datoteke):
    ''' Pomožna funkcija, ki shrani url stran v dani 
    mapi kot niz v datoteko.'''
    besedilo = download_url_to_string(url)
    os.makedirs(ime_mape, exist_ok=True)
    path = os.path.join(ime_mape, ime_datoteke)
    with open(path, 'w', encoding='utf-8') as datoteka:
        datoteka.write(besedilo)       
    return None


# Obdelava podatkov
def read_file_to_string(ime_mape, ime_datoteke):
    ''' Vrne vsebino strani iz datoteke, kjer je shranjena, kot niz. '''
    path = os.path.join(ime_mape, ime_datoteke)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()
    return None


vzorec_izletov = re.compile(
    r'<td colspan="2"><a href="(?P<Povezava>gora\.asp\?gorovjeid=\d+?&id=(?P<id_izleta>\d+?))">'
    r'<b>(?P<Ime>.+?)&nbsp;.+?',
    flags=re.DOTALL
)


vzorec_izleta = re.compile(
    r'<title>(?P<Ime>.+?)</title>.*?'
    r'gorast\((?P<id_izleta>\d+?)\);.*?'
    r'<tr><td><b>Gorovje:</b> <a class="moder" href=.*?>(?P<Gorovje>.*?)</a></td></tr>.*?'
    r'</b> (?P<Visina>\d{1,4})&nbsp;m</td></tr>.*?'
    r'<tr><td><b>Vrsta:</b> (?P<Vrsta>.*?)</td></tr>.*?'
    r'<tr><td><b>Priljubljenost:</b> (?P<Priljubljenost>\d{1,3}%).*?'
    r'\((?P<Mesto_priljubljenosti>\d{1,4}\. mesto)\)</td></tr>.*?'
    r'href="#poti">(?P<Stevilo_poti>\d)</a></td></tr>.*?'
    r'<tr><td colspan="2"><p align="justify">(?P<Opis>.*?)</p></td></tr>.*?',
    flags=re.DOTALL
)


def page_to_izleti(stran):
    '''Vrne seznam naborov (url izleta, id izleta, ime izleta) iz strani.'''
    izleti = re.findall(vzorec_izletov, stran)
    return izleti


def podatki_izletov(izleti):
    '''Sprejme seznam parov izletov (url, id), in naloži vsebino strani url kot niz'''
    podatki_izletov = []
    for i in range(0, 3):
        url_izleta = 'http://www.hribi.net/' + izleti[i][0]
        stran_izleta = 'stran_izlet_{}.html'.format(izleti[i][1])
        stran = save_page(url_izleta, ime_mape, stran_izleta)
        niz = read_file_to_string(ime_mape, stran_izleta)
        podatki_izletov.append(re.findall(vzorec_izleta, niz)[0])
    return podatki_izletov


#TODO slovar teh poadtkov, pa pogledat, če se da da se te strani ne shranjujejo... preberi kodo od prof.


def write_csv(fieldnames, rows, directory, filename):
    '''Write a CSV file to directory/filename. The fieldnames must be a list of
    strings, the rows a list of dictionaries each mapping a fieldname to a
    cell-value.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None


def write_cat_ads_to_csv(izleti):
    ime_stolpca = izleti[0].keys()
    write_csv(ime_stolpca, izleti, ime_mape, csv)
    return None