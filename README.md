# TrainSprinters

RailNL wil een nieuwe dienstregeling voor hun treinen, zowel voor Noord- en Zuid-Holland als voor heel Nederland. Hiervoor stellen ze respectievelijk maximaal 7 en maximaal 20 trajecten (treinen) beschikbaar. Om een goede dienstregeling te maken is een scorefunctie gegeven:

K = p*10000 - (T*100 + Min)

Waarin K de kwaliteit van de lijnvoering is, p de fractie van de bereden verbindingen (dus tussen 0 en 1), T het aantal trajecten en Min het aantal minuten in alle trajecten samen.
Om een zo goed mogelijke dienstregeling te maken is het dus van belang dat zoveel mogelijk verbindingen gereden worden, maar het aantal gebruikte trajecten en de totale reistijd geminimaliseerd worden. 

## Aan de slag

### Vereisten

Deze codebase is volledig geschreven in Python 3.10.8. In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

Of via conda:

```
conda install --file requirements.txt
```

### Gebruik

Om de verschillende onderdelen te kunnen runnen, is het nodig om bepaalde argumenten mee te geven met het aanroepen van main.py. Hieronder staat uitgelegd hoe dit werkt.

Een voorbeeldje kan gerund worden door aanroepen van:

```
python main.py
```

Het bestand geeft een voorbeeld voor gebruik van de verschillende functies.

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor algoritmes
    - **/code/algorithms/call_algorithm**: bevat de code om een algoritme aan te roepen
  - **/code/classes**: bevat de vier benodigde classes voor deze case
  - **/code/experiments**: bevat de code om experimenten uit te voeren
  - **/code/other_functions**: bevat 'extra' code die niet in andere mapjes thuis hoort
  - **/code/visualisation**: bevat de code voor de visualisaties
- **/data**: bevat de verschillende databestanden die nodig zijn om de programma's te draaien
  - **/data/Noord_Holland**: bevat de data voor Noord- en Zuid-Holland (stations en verbindingen)
  - **/data/Nationaal**: bevat de data voor heel Nederland (stations en verbindingen)
  - **/data/output**: bevat de resultaten (dataframes, plots) die verkregen zijn 

## Auteurs
- Ralf Lippes
- Seb Dackus
- Mark van den Hoorn