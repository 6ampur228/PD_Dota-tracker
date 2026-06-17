# Dota 2 Statistikas Sekotājs

Konsoles lietotne, kas ļauj meklēt un sekot līdzi Dota 2 spēlētāju statistikai.
Lietotne izmanto publisko [OpenDota API](https://docs.opendota.com/), glabā datus
SQLite datubāzē un aizsargā lietotāju kontus ar paroļu jaukšanu (hash).

Projekts izstrādāts kā mācību projekta darbs IT priekšmetā.

## Funkcionalitāte

- Lietotāja reģistrācija un pieslēgšanās (paroles tiek glabātas kā SHA-256 hash ar sāli)
- Dota 2 spēlētāja meklēšana pēc konta ID
- Spēlētāja statistikas attēlošana: uzvaras, zaudējumi, uzvaru procents, biežāk spēlētie varoņi
- Iecienīto spēlētāju saglabāšana savā kontā
- Personīgā meklēšanas vēsture

## Tehnoloģijas

- **Python 3** – programmēšanas valoda
- **SQLite** – datubāze ar trim tabulām (`lietotaji`, `saglabatie_speletaji`, `meklesanas_vesture`)
- **requests** – bibliotēka HTTP pieprasījumiem
- **OpenDota API** – ārējs datu avots
- **hashlib** – paroļu drošai glabāšanai

## Uzstādīšana

```bash
# Klonē repozitoriju
git clone https://github.com/lietotajvards/dota-tracker.git
cd dota-tracker

# Uzstādi nepieciešamās bibliotēkas
pip install -r requirements.txt
```

## Palaišana

```bash
python main.py
```

Datubāzes fails `dota_tracker.db` tiek izveidots automātiski pirmajā palaišanas reizē.

## Projekta struktūra

| Fails | Apraksts |
|-------|----------|
| `main.py` | Galvenais modulis – lietotāja saskarsme un programmas plūsma |
| `datubaze.py` | Darbs ar SQLite datubāzi |
| `autentifikacija.py` | Reģistrācija, pieslēgšanās un paroļu jaukšana |
| `dota_api.py` | Sazināšanās ar OpenDota API |

## Licence

Projekts izplatīts saskaņā ar [MIT licenci](LICENSE).
