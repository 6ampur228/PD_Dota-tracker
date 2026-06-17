"""
Dota 2 API klienta modulis.

Sis modulis sazinas ar publisko OpenDota API (https://www.opendota.com/),
lai iegutu Dota 2 speletaju statistiku. Tiek izmantota bibliotēka "requests".

Datu strukturas piemers: varonu saraksts tiek glabats vardnica (dict /
asociativais masivs jeb hash tabula), kur atslega ir varona id un vertiba
ir varona nosaukums. Tas lauj atrast varona vardu bez atkartotiem API
pieprasijumiem.
"""

import requests


# API bazes adrese.
API_BAZE = "https://api.opendota.com/api"

# Vardnica varonu glabasanai (id -> nosaukums). Tiek aizpildita pec pieprasijuma.
_varonu_kese = {}


def ieladet_varonus():
    """
    Ieladet visus Dota 2 varonus vardnica (hash tabula).

    Atgriez vardnicu formata {varona_id: varona_nosaukums}.
    Ja dati jau ieladeti, atgriez kesoto rezultatu.
    """

    # Ja vardnica jau aizpildita, neveicam atkartotu pieprasijumu.
    if _varonu_kese:
        return _varonu_kese

    try:
        atbilde = requests.get(API_BAZE + "/heroes", timeout=10)
        atbilde.raise_for_status()
        varoni = atbilde.json()

        # Aizpildam vardnicu: katram varonam id -> lokalizets nosaukums.
        for varonis in varoni:
            _varonu_kese[varonis["id"]] = varonis["localized_name"]

    except requests.RequestException:
        # Ja pieprasijums neizdevas, atgriezam tuksu vardnicu.
        pass

    return _varonu_kese


def iegut_speletaja_datus(dota_id):
    """
    Iegut speletaja pamatdatus pec konta id.

    Atgriez vardnicu ar speletaja datiem vai None, ja speletajs nav atrasts
    vai radas tikla kluda.
    """

    try:
        atbilde = requests.get(API_BAZE + "/players/" + str(dota_id), timeout=10)
        atbilde.raise_for_status()
        dati = atbilde.json()

        # Ja profils ir slegts vai neeksiste, "profile" lauks bus tukss.
        if dati.get("profile") is None:
            return None

        return dati

    except requests.RequestException:
        return None


def iegut_uzvaras_zaudejumus(dota_id):
    """
    Iegut speletaja uzvaru un zaudejumu skaitu.

    Atgriez vardnicu {"win": ..., "lose": ...} vai None kludas gadijuma.
    """

    try:
        atbilde = requests.get(API_BAZE + "/players/" + str(dota_id) + "/wl", timeout=10)
        atbilde.raise_for_status()

        return atbilde.json()

    except requests.RequestException:
        return None


def iegut_iecienitos_varonus(dota_id, skaits=3):
    """
    Iegut speletaja biezak sp-eletos varonus.

    Atgriez sarakstu ar varonu nosaukumiem (lidz "skaits" varoniem).
    """

    varoni = ieladet_varonus()

    try:
        atbilde = requests.get(API_BAZE + "/players/" + str(dota_id) + "/heroes", timeout=10)
        atbilde.raise_for_status()
        dati = atbilde.json()

    except requests.RequestException:
        return []

    iecienitie = []

    # Dati jau ir sakartoti pec speletu speru skaita (dilstosa seciba).
    for ieraksts in dati[:skaits]:
        varona_id = int(ieraksts["hero_id"])

        # Atrodam varona nosaukumu vardnica; ja nav, lietojam id.
        nosaukums = varoni.get(varona_id, "ID " + str(varona_id))
        iecienitie.append(nosaukums)

    return iecienitie
