# helmet-model-system

Tämä repository sisältää Helmet-liikenne-ennustejärjestelmän python-ohjelmia. Lähdekieliset ohjelmat ovat kansiossa Scripts.

## Käyttö
Tässä kappaleessa neuvotaan, miten Helmet 4.0 asennetaan toimimaan INROn Emme-ohjelmiston kanssa. Kaikki tarvittava löytyy repositoreista helmet-model-system ja helmet-ui. Niiden lisäksi käyttäjän ei tarvitse asentaa muita ohjelmistoja.
Jos sinulla ei ole Emme-lisenssiä tai jos haluat kehittää Helmet 4.0 -järjestelmää edelleen, siirry lukuun Development.

## Asennus
Järjestelmä käyttää Python-versiota 2.7, joka toimitetaan ja asennetaan INROn Emme-ohjelmiston yhteydessä.

Järjestelmä käyttää pythonin riippuvuuksia, jotka tulevat asennettaessa INROn Emme-ohjelmistoa. Jotta näitä riippuvuuksia voitaisiin käyttää, sinun on lisättävä ne omaan PATH-määrittelyysi.
1.	Avaa Windows-järjestelmän Ohjauspaneeli
2.	Valitse Käyttäjätilit ja vielä uudelleen Käyttäjätilit. Valitse sen jälkeen vasemmalla olevasta valikosta ”Muuta ympäristömuuttujia”.
3.	Etsi ylhäällä olevasta laatikosta ”käyttäjän [oma_käyttäjätunnuksesi] muuttujat”, valitse Path-muuttuja ja ”muokkaa ympäristömuuttujia”.
4.	Valitse Uusi ja kirjoita %EMMEPATH%\Programs
5.	Paina OK ikkunassa ”Muokkaa ympäristömuuttujia” ja vielä uudelleen OK ikkunassa ”ympäristömuuttujat”.

Seuraavaksi sinun on määriteltävä Emme-projekti:
1.	Käynnistä Emme-ohjelmisto.
2.	Perusta uusi projekti, jonka nimi on helmet-model-system. Määrittele, mihin kansioon haluat sen asentaa. Emme muodostaa tiedoston helmet-model-system.emp kansioon .\helmet-model-system ja sen alikansioon.\helmet-model-system\database suuren binaaritiedoston emmebank sekä muitakin alikansioita ja tiedostoja.
3.	Erillisessä ohjeessa kerrotaan mm. sopivista dimensioista (solmujen, linkkien ym. maksimimäärät), jotka vaikuttavat em. emmebank-tiedoston kokoon.
4.	Kopioi tästä repositorystä kansion Scripts sisältö. Helpoin tapa on valita painike Clone or download ja Download Zip, joka muodostaa käyttäjän haluamaan paikkaan tiedostopaketin helmet-model-system-master.zip. Siitä saa purkamalla haluamansa tiedostot.

## Ajo
Helmet 4.0 -ajon voi käynnistää Komentokehote-ikkunasta tai käyttöliittymästä helmet-ui. Ennen kuin käynnistät ajon Komentokehote-ikkunasta, määrittele kansiopolku tiedostoon dev-config.json. Siirry sen jälkeen Emme-projektisi kansioon helmet-model-system ja kirjoita:
cd Scripts
python helmet.py
Emme assignment can be tested without further configuration:
Emme-sijoittelua voi testata ilman muita määrityksiä:
cd Scripts
python test_assignment.py

## Kehitystyö
Käytämme Python-versiota 2.7, koska sitä INRO Emme-ohjelmisto tukee.
1.	Asenna Python 2.7. (2020-04-16: valitse versio Python 2.7.16, koska versio 2.7.17 ei toimi kunnolla ennen kuin tämä on ratkaistu)
2.	Lisää Ohjauspaneelin ympäristömuuttujissa omaan PATH-muuttujaasi C:\Python27 ja C:\Python27\Scripts.
3.	Avaa uusi Komentokehote-ikkuna ja kirjoita kehotteen perään 
python --version
(siis kaksi tavuviivaa peräkkäin). Vastaukseksi pitäisi tulla Python 2.7.16 tai jokin muu Python 2.7 -versio.

Python-pakettien suositeltava asennusohjelma on pip. Pythonin normaali asennusrutiini asentaa pip-ohjelman kansioon C:\Python27\Scripts. Kirjoita Komentokehote-ikkunaan
pip --version 
nähdäksesi, onko pip asennettu ja liitetty PATH-määrittelyysi. Komennon pitäisi tulostaa
pip 20.0.2 from c:\python27\lib\site-packages\pip (python 2.7) (pip version voi vaihdella).

pipenv-ohjelmalla haetaan INROn Emme-ohjelmiston käyttämät avoimen lähdekoodin kirjastot. pipenv eristää meidän ympäristömme muista globaaleista Python-moduuleista ja varmistaa, että meidän järjestelmämme ei vahingoita niitä. Johdatus pipenv-ohjelman käyttöön löytyy seuraavilla linkeillä Python docs tai Jonathan Cutrer's blog.
1.	Avaa Komentokehote-ikkuna.
2.	Asenna pipenv komennolla
python -m pip install --user pipenv
Sen pitäisi tulla kansioon %APPDATA%\Python\Scripts (esim. C:\Users\USERNAME\AppData\Roaming\Python\Scripts).
3.	Lisää omaan PATH-määrittelyysi %APPDATA%\Python\Scripts.
4.	Sulje Komentokehote-ikkuna ja avaa se jälleen. Tarkista, että pipenv tunnistetaan kirjoittamalla 
pipenv –version
Tuloksena pitäisi tulla pipenv, version 2018.11.26.
5.	Lataa itsellesi repository helmet-model-system ja avaa Komentokehote-ikkunassa sen alikansio Scripts.
6.	Asenna riippuvuudet tiedostosta Pipfile kirjoittamalla
o	Ensimmäisellä kerralla: pipenv --python 2.7 install --dev
o	Synkronointi, jos uusi paketteja on lisätty: pipenv --python 2.7 sync --dev
7.	Riippuen käyttöjärjestelmästäsi muuta tiedoston tyypin .env-win (Windows) tai .env-nix (Linux) tilalle .env. Windows-ympäristössä tämän voi tehdä Komentokehote-ikkunassa kirjoittamalla 
copy .env-win .env.

Nyt sinulla pitäisi olla virtuaaliympäristö kansiossa C:\Users\USERNAME\.virtualenvs\Scripts-xxxxxxxx\Lib\site-packages.
Kun suoritat skriptejä, kirjoita komennon alkuun pipenv, esimerkiksi:

cd Scripts
pipenv run python test_assignment.py

## Visual Studio Code
Kun käytät Visual Studio Code’a kehitystyössä, seuraavien laajennusten käyttö on suositeltavaa:
•	Python
•	Test Explorer UI
•	Python Test Explorer for Visual Studio Code

Muutama vinkki, joilla saat kaiken toimimaan:
•	Muista ensin määritellä kehitysympäristösi. Avaa sen jälkeen Visual Studio Code’ssa kansio Scripts ja valitse virtuaaliympäristösi vasemman alakulman Python-tulkkien luettelosta.
•	Testien konfigurointia varten paina Ctrl-Shift-P, kirjoita Python: Configure tests, valitse pytest ja kansio, jossa testit ovat.  Testien pitäisi ilmestyä ikkunaan Test Explorer (paina vasemmalla olevaa pullonkuvaa)

## OMX
Emmen käyttää matriisien siirtoon OpenMatrix-kirjastoa.
•	Lisätietoja: https://github.com/osPlanning/omx/wiki/EMME
•	Python-lähdekoodi: https://github.com/osPlanning/omx-python
•	Hyödyllinen työkalu, kun matriiseja siirretään komentoriviä käyttäen: https://github.com/bstabler/EMXtoOMX
