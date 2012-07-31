## encoding: utf-8
from django import template
from django.utils.safestring import mark_safe
import urllib
import re


register = template.Library()

@register.simple_tag
def filter_checkbox(filters, filtername, filterentry):
    if filterentry in filters.get(filtername, []):
        return u' checked="1" '
    return u''

@register.filter(name='exp_afk')
def exp_afk(value):
    if value is None:
        return u''
    codes = dict(line.split('|') for line in '''A0|zelfstandig naamwoord
A1|eigennaam
A2|telwoord
A3|eigennaam (acroniem)
A4|eigennaam (backroniem)
B0|bijvoeglijk naamwoord
C0|werkwoord
D0|voornaamwoord
E0|bijwoord
F0|voorzetsel
G1|lidwoord
H0|voegwoord
I0|tussenwerpsel
J0|afkorting
X0|niet van toepassing / niet zeker
KO|woordgroep
AM|Amerikaans
AR|Arabisch
AT|Atjehs
BI|Bahasa Indonesia
BJ|Bataviaas/Jakartaas
BL|Balinees
BN|Bandanees
BT|Bataks
BU|Boeginees
CH|Chinees-Maleis
EN|Engels
FR|Frans
IN|Indisch
JM|Japans-Maleis
JP|Japans
JQ|Javaans kromo
JR|Javaans kromo-inggil
JS|Javaans kromo-ngoko
JT|Javaans ngoko
JU|Javaans boekentaal
JV|Javaans
KT|kamptaal
LT|Latijn
MA|Maleis-Indisch
MI|Minangkabaus
MJ|Maleis + Javaans
MK|Makassaars
ML|Maleis
MO|Moluks
NE|Nederlands
NI|Nias
OM|ouder Maleis
PO|Portugees
PP|populair, spreektaal
SK|Sanskriet
SM|Soembaas
SO|Soendaas
TO|Torajaas
VM|verbasterd Maleis
XX|onbekend
A|Wetenschap, kunst, onderwijs en journalistiek
AA|Wetenschap
AAA|Algemeen wetenschappelijk
AAB|Aardrijkskunde, topografie
AABA|Geologie
AABB|Landschap, provincie, residentie
AABC|Stad, plaats, desa, kampong
AABD|Straat, plein, wijk
AABE|Rivier, meer
AABF|Berg, vulkaan
AABG|Eiland
AABH|Zee, oceaan
AABI|Tijd, seizoen
AAC|Biologie
AACA|Flora, landschap
AACB|Boom, bos, hout
AACC|Plant, struik, heester
AACD|Vrucht, noot, bloem, blad
AACE|Fauna
AACF|Zoogdier
AACG|Vogel
AACH|Reptiel
AACI|Amfibie
AACJ|Vis
AACK|Ongewerveld dier
AACL|Extract, olie, hars, lak
AAD|Geneeskunde en Gezondheidszorg
AAE|Geschiedenis
AAF|Astronomie
AB|Kunst
ABA|Bouwkunst en architectuur
ABAA|Gebouw
ABB|Beeldende kunsten
ABC|Letteren, epiek, toneel, mythologie
ABD|Muziek
ABDA|Muziekinstrument
ABF|Dans
ABG|Toneel
AC|Onderwijs
AD|Journalistiek
B|De mens in zijn openbaar leven
BA|Openbaar leven (als staatsburger)
BAA|Staatsbestuur (incl. kampong)
BAB|Oorlog, leger, stammentwist, etc.
BABA|Wapen
BABB|Kleding (uniform)
BABC|Titel
BAC|Rechtspraak (incl. adat)
BAD|Godsdienst
BADA|God
BADB|Tempel
BADC|Goena-goena
BAE|Hof- en paleisleven
BAF|Kampperiode
BAG|Politiek
BB|De mens als lid van de maatschappij
BBA|Algemeen maatschappelijk
BBB|Werk, industrie, beroep
BBC|Handel
BBCA|Geld
BBCB|Gewicht, maat
BBD|Stadsleven
BBE|Landleven
BBF|Reizen (verlof, repatriering)
BBG|Vervoer
BBGA|Scheepvaart
C|De mens in zijn particulier leven
CA|Sociaal leven (privé)
CAA|Huis, huishouden en interieur
CAB|Kleding
CABA|Hoofddeksel, schoeisel
CABB|Stof
CABC|Sieraad
CAC|Voeding, voedsel
CACA|Groente
CACB|Gerecht
CACC|Kruid, specerij
CACD|Snoep, nagerecht, gebak, koek
CACE|Drank
CAD|Hygiëne, toilet maken
CB|Sociaal leven (naar anderen toe)
CBA|Sociaal gedrag
CBAA|Familie
CBB|Sport en spel
CBC|Feest, plechtigheid, vermaak
CBD|Afkomst, verhouding
CBE|Communicatie
CBEA|Volk
CBEB|Taal
CC|Zintuiglijkheid
CCA|Kleur
CCB|Geur
CCC|Geluid
CCD|Smaak
CCE|Gevoel
CCF|Genotmiddel, verslaving, verslaafde
CCG|Voorkomen, uiterlijk
CCH|Eigenschap (karakter)
D|Algemeen woord'''.split('\n'))
    return codes.get(value.upper(), value)


@register.filter(name='betekenislinks')
def betekenislinks(value):
    if value is None:
        return u''
    value = value.strip()
    # first fix the bronnen
    for nc in ['BEEWOO', 'BROTRO', 'BRUIND', 'BRUNED', 'BRUTUI', 'CATGRO', 
               'COOSOE', 'CREPET', 'DELDIE', 'DIESTE', 'ERISOE', 'GEEVAN', 
               'GONGE\xc3\x8f', 'GRATRO', 'GRUJAV', 'HEYNUT', 'IWANEW', 
               'JONKON', 'KONATL', 'KRAKAM', 'KRUVAN', 'LOEPET', 'LUBGES', 
               'L\xc3\x96TELS', 'MALVAN', 'MAYMAL', 'MERPLA', 'MIKGES', 
               'PIGJAV', 'RAHLEX', 'ROEIND', 'SALWOO', 'STESTA', 'SUCJAN', 
               'TEEIND', 'VEEVAN', 'VELJAP', 'WITIND']:
        nc = nc.decode('utf8')
        if value.find(nc) > -1:
            value = value.replace(nc, u'<a href="/search/?q=%s">%s</a>' % (urllib.quote_plus(nc.encode('utf8')), nc))

    value = value.replace('\r\n', '\n')
    
    # And now do the "zie:""
    value = re.sub(r'zie: (.*)', r'zie: <a href="/search/?q=%22\1%22">\1</a>', value)

    value = re.sub(r'zie ook: (.*)', r'zie ook: <a href="/search/?q=%22\1%22">\1</a>', value)
    return mark_safe(value)
