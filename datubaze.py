"""
Datubazes modulis.

Sis modulis atbild par SQLite datubazes izveidi un visam darbibam ar to:
lietotaju saglabasanu, saglabato speletaju parvaldibu un meklesanas
vestures pierakstisanu. Datubaze satur tris savstarpeji saistitas tabulas.
"""

import sqlite3
from datetime import datetime


# Datubazes faila nosaukums. Fails tiek izveidots projekta mape.
DB_FAILS = "dota_tracker.db"


def izveidot_savienojumu():
    """Izveido un atgriez savienojumu ar datubazi."""

    savienojums = sqlite3.connect(DB_FAILS)

    # Iesledz arejo atslegu atbalstu, lai saglabatu datu integritati.
    savienojums.execute("PRAGMA foreign_keys = ON")

    return savienojums


def inicializet_datubazi():
    """Izveido visas nepieciesamas tabulas, ja tas vel neeksiste."""

    savienojums = izveidot_savienojumu()
    kursors = savienojums.cursor()

    # 1. tabula: lietotaji (lietotaja konts un parole)
    kursors.execute("""
        CREATE TABLE IF NOT EXISTS lietotaji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lietotajvards TEXT UNIQUE NOT NULL,
            paroles_hash TEXT NOT NULL,
            registracijas_datums TEXT NOT NULL
        )
    """)

    # 2. tabula: saglabatie_speletaji (lietotaja izveletie Dota 2 speletaji)
    kursors.execute("""
        CREATE TABLE IF NOT EXISTS saglabatie_speletaji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lietotaja_id INTEGER NOT NULL,
            dota_id INTEGER NOT NULL,
            vards TEXT NOT NULL,
            pievienosanas_datums TEXT NOT NULL,
            FOREIGN KEY (lietotaja_id) REFERENCES lietotaji (id)
        )
    """)

    # 3. tabula: meklesanas_vesture (katra lietotaja veiktie meklejumi)
    kursors.execute("""
        CREATE TABLE IF NOT EXISTS meklesanas_vesture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lietotaja_id INTEGER NOT NULL,
            meklejums TEXT NOT NULL,
            laiks TEXT NOT NULL,
            FOREIGN KEY (lietotaja_id) REFERENCES lietotaji (id)
        )
    """)

    savienojums.commit()
    savienojums.close()


def pievienot_lietotaju(lietotajvards, paroles_hash):
    """Pievieno jaunu lietotaju. Atgriez True, ja izdevas."""

    savienojums = izveidot_savienojumu()
    kursors = savienojums.cursor()

    datums = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        kursors.execute(
            "INSERT INTO lietotaji (lietotajvards, paroles_hash, registracijas_datums) "
            "VALUES (?, ?, ?)",
            (lietotajvards, paroles_hash, datums)
        )
        savienojums.commit()
        izdevas = True

    except sqlite3.IntegrityError:
        # Sada kluda rodas, ja lietotajvards jau eksiste (UNIQUE ierobezojums).
        izdevas = False

    savienojums.close()

    return izdevas


def atrast_lietotaju(lietotajvards):
    """Atrod lietotaju pec lietotajvarda. Atgriez ierakstu vai None."""

    savienojums = izveidot_savienojumu()
    kursors = savienojums.cursor()

    kursors.execute(
        "SELECT id, lietotajvards, paroles_hash FROM lietotaji WHERE lietotajvards = ?",
        (lietotajvards,)
    )
    ieraksts = kursors.fetchone()

    savienojums.close()

    return ieraksts


def saglabat_speletaju(lietotaja_id, dota_id, vards):
    """Saglaba speletaju lietotaja izleses saraksta."""

    savienojums = izveidot_savienojumu()
    kursors = savienojums.cursor()

    datums = datetime.now().strftime("%Y-%m-%d %H:%M")

    kursors.execute(
        "INSERT INTO saglabatie_speletaji (lietotaja_id, dota_id, vards, pievienosanas_datums) "
        "VALUES (?, ?, ?, ?)",
        (lietotaja_id, dota_id, vards, datums)
    )

    savienojums.commit()
    savienojums.close()


def iegut_saglabatos_speletajus(lietotaja_id):
    """Atgriez visus konkreta lietotaja saglabatos speletajus ka sarakstu."""

    savienojums = izveidot_savienojumu()
    kursors = savienojums.cursor()

    # Datu aizsardziba: tiek izvaditi tikai si lietotaja ieraksti.
    kursors.execute(
        "SELECT dota_id, vards, pievienosanas_datums FROM saglabatie_speletaji "
        "WHERE lietotaja_id = ? ORDER BY pievienosanas_datums DESC",
        (lietotaja_id,)
    )
    ieraksti = kursors.fetchall()

    savienojums.close()

    return ieraksti


def pierakstit_meklejumu(lietotaja_id, meklejums):
    """Pieraksta lietotaja veikto meklejumu vesture."""

    savienojums = izveidot_savienojumu()
    kursors = savienojums.cursor()

    laiks = datetime.now().strftime("%Y-%m-%d %H:%M")

    kursors.execute(
        "INSERT INTO meklesanas_vesture (lietotaja_id, meklejums, laiks) "
        "VALUES (?, ?, ?)",
        (lietotaja_id, meklejums, laiks)
    )

    savienojums.commit()
    savienojums.close()


def iegut_meklesanas_vesturi(lietotaja_id, limits=10):
    """Atgriez lietotaja pedejos meklejumus (pec noklusejuma 10)."""

    savienojums = izveidot_savienojumu()
    kursors = savienojums.cursor()

    kursors.execute(
        "SELECT meklejums, laiks FROM meklesanas_vesture "
        "WHERE lietotaja_id = ? ORDER BY id DESC LIMIT ?",
        (lietotaja_id, limits)
    )
    ieraksti = kursors.fetchall()

    savienojums.close()

    return ieraksti
