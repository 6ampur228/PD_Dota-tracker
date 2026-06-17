"""
Autentifikacijas modulis.

Sis modulis nodrosina lietotaja piekluves aizsardzibu: registraciju un
pieslegsanos. Paroles netiek glabatas atklata teksta, bet gan saglabatas
ka jaucejvertiba (hash), izmantojot SHA-256 algoritmu un nejausu "salu".
"""

import hashlib
import os

import datubaze


def izveidot_paroles_hash(parole, sals=None):
    """
    Izveido paroles jaucejvertibu (hash).

    Ja sals nav padota, tiek generets jauns nejauss sals. Sals tiek pievienota
    rezultatam, lai velak varetu parbaudit paroli. Rezultata formats: sals$hash.
    """

    # Ja sals nav padota, generejam jaunu nejausu sals (16 baiti).
    if sals is None:
        sals = os.urandom(16).hex()

    # Apvienojam paroli ar sals un aprekinam SHA-256 jaucejvertibu.
    kombinacija = (sals + parole).encode("utf-8")
    hash_vertiba = hashlib.sha256(kombinacija).hexdigest()

    return sals + "$" + hash_vertiba


def parbaudit_paroli(parole, saglabata_vertiba):
    """Parbauda, vai ievaditа parole atbilst saglabatajai jaucejvertibai."""

    # Atdalam sals no jaucejvertibas.
    sals, _ = saglabata_vertiba.split("$")

    # Aprekinam jaucejvertibu ievaditajai parolei ar to pasu sals.
    parbaudes_vertiba = izveidot_paroles_hash(parole, sals)

    return parbaudes_vertiba == saglabata_vertiba


def registrēt(lietotajvards, parole):
    """
    Registre jaunu lietotaju.

    Atgriez (True, zinojums), ja izdevas, vai (False, zinojums), ja ne.
    """

    # Parbaudam, vai ievaddati ir derigi.
    if len(lietotajvards) < 3:
        return False, "Lietotajvardam jabut vismaz 3 simbolus garam."

    if len(parole) < 4:
        return False, "Parolei jabut vismaz 4 simbolus garai."

    # Izveidojam paroles jaucejvertibu un meginam saglabat lietotaju.
    paroles_hash = izveidot_paroles_hash(parole)
    izdevas = datubaze.pievienot_lietotaju(lietotajvards, paroles_hash)

    if izdevas:
        return True, "Registracija veiksmiga!"
    else:
        return False, "Sads lietotajvards jau eksiste."


def pieslēgties(lietotajvards, parole):
    """
    Parbauda lietotaja pieslegsanas datus.

    Atgriez lietotaja id, ja dati pareizi, vai None, ja nepareizi.
    """

    ieraksts = datubaze.atrast_lietotaju(lietotajvards)

    # Ja lietotajs nav atrasts, pieslegsanas neizdodas.
    if ieraksts is None:
        return None

    lietotaja_id = ieraksts[0]
    saglabata_vertiba = ieraksts[2]

    # Parbaudam paroli pret saglabato jaucejvertibu.
    if parbaudit_paroli(parole, saglabata_vertiba):
        return lietotaja_id
    else:
        return None
