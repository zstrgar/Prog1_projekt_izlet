import requests
import re
import os
import csv

url = 'http://www.hribi.net/goreiskanjerezultat.asp?drzavaid=1&gorovjeid=&goraime=&VisinaMIN=&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhodisceMIN=&izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zahtevnostid=&zahtevnostSmucanjeid=&IzhodisceMinOddaljenost=&IzhodisceMAXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0&mojaDolzina=0'
#mapa s podatki
directory = 'Prog1_pariski_hoteli/data'
#ime datoteke, kjer bomo shranili spletno stran
filename = 'spletna_stran.html'
#ime CSV datoteke
csv = 'podatki.csv'

### Pridobitev podatkov
def download_url_to_string(url):
    '''This function takes a URL as argument and tries to download it
    using requests. Upon success, it returns the page contents as string.'''
    try:      
        r = requests.get(url)
        print("download successful")
    except requests.exceptions.ConnectionError:
        print("Stran ne obstaja")
        return None
    return r.text

def save_page():
    besedilo = download_url_to_string(url)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as datoteka:
        datoteka.write(besedilo)        
    return None

####Obdelava podatkov
