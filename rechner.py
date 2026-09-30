import datetime

# 1. HIER GIBST DU DEINE DATEN EIN (Einfach die Zahlen/Daten anpassen):
ZUKUNFTS_DATUM = "24.12.2026"  # Dein Wunschdatum in der Zukunft (Format: TT.MM.JJJJ)

# Trage hier deinen aktuellen gezählten Bestand ein:
BESTAND = {
    "Gabapentin": 100,
    "Metformin": 100,
    "Ozempic": 12,
    "Pravastatin": 90,
    "Omeprazol": 100,
    "MetoHexal": 100,
    "MetoProlol": 100,
    "Ultibro": 100,
    "RamiLich": 180
}

# 2. DEIN TÄGLICHER BEDARF (Bleibt fest eingestellt):
BEDARF = {
    "Gabapentin": 3,   # 2 mo / 1 ab
    "Metformin": 2,    # 1 mo / 1 ab
    "Ozempic": 1/7,    # 1x pro Woche mittwochs (= 0.1428 pro Tag)
    "Pravastatin": 1,  # 1 ab
    "Omeprazol": 1,    # 1 mo
    "MetoHexal": 1,    # 1 ab
    "MetoProlol": 1,   # 1 mo
    "Ultibro": 1,      # 1 mo
    "RamiLich": 1      # 1 ab
}

# 3. DIE AUTOMATISCHE BERECHNUNG
heute = datetime.date.today()
ziel_datum = datetime.datetime.strptime(ZUKUNFTS_DATUM, "%d.%m.%Y").date()
tage_bis_ziel = (ziel_datum - heute).days

# Erstelle die neue README.md Datei
markdown_text = f"""# 📋 Mein Medikamenten-Inventar

* **Aktuelles Datum (läuft autonom mit):** {heute.strftime('%d.%m.%Y')}
* **Dein gewähltes Zukunftsdatum:** {ziel_datum.strftime('%d.%m.%Y')} (In {tage_bis_ziel} Tagen)

---

### Bestands-Vorschau für den {ziel_datum.strftime('%d.%m.%Y')}:

| Medikament | Eingetragener Bestand heute | Verbraucht bis dahin | Restbestand am {ZUKUNFTS_DATUM} | Reicht ab da noch für... | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
"""

for med, start in BESTAND.items():
    verbrauch = round(tage_bis_ziel * BEDARF[med], 1)
    if med == "Ozempic":
        rest = int(start - (tage_bis_ziel / 7))
        rest_tage = rest * 7
        reichweite = f"{rest} Wochen"
    else:
        rest = int(start - verbrauch)
        rest_tage = int(rest / BEDARF[med]) if BEDARF[med] > 0 else 0
        reichweite = f"{rest_tage} Tage"
    
    if rest <= 0:
        rest = 0
        reichweite = "0 Tage"
        status = "🔴 **ALLE! Bereits vorher nachbestellen!**"
    elif rest_tage < 14 if med != "Ozempic" else rest < 2:
        status = "🟡 **Wird knapp! Nachbestellen.**"
    else:
        status = "🟢 Genug vorhanden"

    markdown_text += f"| **{med}** | {start} | {int(verbrauch) if med != 'Ozempic' else int(tage_bis_ziel / 7)} | **{rest}** | **{reichweite}** | {status} |\n"

# In Datei schreiben
with open("README.md", "w", encoding="utf-8") as f:
    f.write(markdown_text)

print("Deine Medikamenten-Tabelle wurde erfolgreich für die Zukunft berechnet!")
