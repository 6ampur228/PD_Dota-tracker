"""
Dota 2 Statistikas Sekotajs - galvenais modulis.

Programma lauj lietotajam izveidot kontu, pieslegties, meklet Dota 2
speletaju statistiku pec konta id, saglabat iecienitos speletajus un
apskatit savu meklesanas vesturi.

Programma sastav no cetriem moduliem:
  - datubaze.py        (datu glabasana SQLite datubaze)
  - autentifikacija.py (lietotaju registracija un pieslegsanas)
  - dota_api.py        (sazina ar OpenDota API)
  - main.py            (sis modulis - lietotaja saskarsme un programmas plusma)
"""

import datubaze
import autentifikacija
import dota_api


def paradit_speletaja_statistiku(dota_id):
    """Iegut un izvadit speletaja statistiku no API."""

    print("\nMekleju speletaju...")

    # Iegustam speletaja pamatdatus.
    dati = dota_api.iegut_speletaja_datus(dota_id)

    if dati is None:
        print("Speletajs nav atrasts vai profils ir slegts.")
        return None

    # Izvelkam vardu no datu strukturas.
    profils = dati["profile"]
    vards = profils.get("personaname", "Nezinams")

    # Iegustam uzvaru un zaudejumu statistiku.
    uzvaras_dati = dota_api.iegut_uzvaras_zaudejumus(dota_id)
    iecienitie = dota_api.iegut_iecienitos_varonus(dota_id)

    # Datu izvade ekrana.
    print("\n--- Speletaja statistika ---")
    print("Vards:", vards)

    if uzvaras_dati is not None:
        uzvaras = uzvaras_dati.get("win", 0)
        zaudejumi = uzvaras_dati.get("lose", 0)
        kopa = uzvaras + zaudejumi

        print("Uzvaras:", uzvaras)
        print("Zaudejumi:", zaudejumi)

        # Aprekinam uzvaru procentu, ja sples ir speletas.
        if kopa > 0:
            procents = round(uzvaras / kopa * 100, 1)
            print("Uzvaru procents:", str(procents) + "%")

    if iecienitie:
        print("Biezak speletie varoni:", ", ".join(iecienitie))

    print("----------------------------")

    return vards


def meklesanas_izvelne(lietotaja_id):
    """Apstrada speletaja meklesanu un pieprasa saglabasanu."""

    ievade = input("\nIevadi Dota 2 konta id (cipari): ").strip()

    # Parbaudam, vai ievade ir skaitlis.
    if not ievade.isdigit():
        print("Konta id jasastav tikai no cipariem.")
        return

    dota_id = int(ievade)

    # Pierakstam meklejumu lietotaja vesture.
    datubaze.pierakstit_meklejumu(lietotaja_id, ievade)

    # Izvadam statistiku un iegustam speletaja vardu.
    vards = paradit_speletaja_statistiku(dota_id)

    if vards is None:
        return

    # Piedavajam saglabat speletaju izleses saraksta.
    atbilde = input("Vai saglabat so speletaju? (j/n): ").strip().lower()

    if atbilde == "j":
        datubaze.saglabat_speletaju(lietotaja_id, dota_id, vards)
        print("Speletajs saglabats!")


def paradit_saglabatos(lietotaja_id):
    """Izvada lietotaja saglabatos speletajus."""

    speletaji = datubaze.iegut_saglabatos_speletajus(lietotaja_id)

    if not speletaji:
        print("\nTev vel nav saglabatu speletaju.")
        return

    print("\n--- Saglabatie speletaji ---")

    # Ejam cauri saglabato speletaju sarakstam.
    for dota_id, vards, datums in speletaji:
        print("-", vards, "(id:", str(dota_id) + ", pievienots:", datums + ")")

    print("----------------------------")


def paradit_vesturi(lietotaja_id):
    """Izvada lietotaja meklesanas vesturi."""

    vesture = datubaze.iegut_meklesanas_vesturi(lietotaja_id)

    if not vesture:
        print("\nMeklesanas vesture ir tuksa.")
        return

    print("\n--- Meklesanas vesture ---")

    for meklejums, laiks in vesture:
        print("-", meklejums, "(" + laiks + ")")

    print("--------------------------")


def lietotaja_izvelne(lietotaja_id, lietotajvards):
    """Galvena izvelne pec veiksmigas pieslegsanas."""

    print("\nLaipni ludzam,", lietotajvards + "!")

    # Galvenais cikls turpinas, lidz lietotajs izvelas iziet.
    while True:
        print("\n=== GALVENA IZVELNE ===")
        print("1 - Meklet speletaju")
        print("2 - Apskatit saglabatos speletajus")
        print("3 - Apskatit meklesanas vesturi")
        print("4 - Izrakstities")

        izvele = input("Tava izvele: ").strip()

        # Zarosanas atkariba no lietotaja izveles.
        if izvele == "1":
            meklesanas_izvelne(lietotaja_id)

        elif izvele == "2":
            paradit_saglabatos(lietotaja_id)

        elif izvele == "3":
            paradit_vesturi(lietotaja_id)

        elif izvele == "4":
            print("Uz redzesanos!")
            break

        else:
            print("Nederiga izvele. Ludzu, meginiet velreiz.")


def sakuma_izvelne():
    """Sakuma izvelne: registracija vai pieslegsanas."""

    while True:
        print("\n=== DOTA 2 STATISTIKAS SEKOTAJS ===")
        print("1 - Pieslegties")
        print("2 - Registreties")
        print("3 - Iziet no programmas")

        izvele = input("Tava izvele: ").strip()

        if izvele == "1":
            lietotajvards = input("Lietotajvards: ").strip()
            parole = input("Parole: ").strip()

            lietotaja_id = autentifikacija.pieslēgties(lietotajvards, parole)

            if lietotaja_id is not None:
                lietotaja_izvelne(lietotaja_id, lietotajvards)
            else:
                print("Nepareizs lietotajvards vai parole.")

        elif izvele == "2":
            lietotajvards = input("Izvelies lietotajvardu: ").strip()
            parole = input("Izvelies paroli: ").strip()

            izdevas, zinojums = autentifikacija.registrēt(lietotajvards, parole)
            print(zinojums)

        elif izvele == "3":
            print("Uz redzesanos!")
            break

        else:
            print("Nederiga izvele. Ludzu, meginiet velreiz.")


def galvena():
    """Programmas ieejas punkts."""

    # Vispirms sagatavojam datubazi (izveidojam tabulas, ja vajadzigs).
    datubaze.inicializet_datubazi()

    # Palaizam sakuma izvelni.
    sakuma_izvelne()


# Standarta Python ieejas punkts.
if __name__ == "__main__":
    galvena()
