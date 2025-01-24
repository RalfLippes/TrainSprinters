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

Voor alle situaties is het van belang dat je specificeert of je Nationale data of alleen de data van Noord- en Zuid-Holland wilt gebruiken. Dus je begint met:

```
python main.py holland
```

of:

```
python main.py nationaal
```

### Algoritmes gebruiken

Vervolgens roep je een van de algoritmes aan door de naam van dit algoritme mee te geven. Deze algoritmes slaan altijd een dataframe van de beste oplossing op als csv bestand in de map data/output. Per algoritme moet je soms ook nog een of meerdere extra argumenten meegeven. De structuur van de mee te geven argumenten is [holland/nationaal] [algoritme] [tijd] [plotten]. Algoritme, tijd en plotten hebben standaard waarden: respectievelijk 'baseline', '60 seconden' en 'niet plotten'. Om andere waarden dan deze standaard waarden te krijgen, moet je expliciet argumenten meegeven. Als je dus de baseline voor 60 seconden zou willen runnen zonder te plotten (voor de holland data), dan voer je in:

```
python main.py holland 
```

Als je Simulated annealing op nationale data zou willen runnen met de standaardwaarden zou je dat algoritme kunnen runnen met: 

```
python main.py nationaal simulated_annealing 
```

Om greedy 1000 seconden te laten lopen en van de gevonden scores een plot te maken zou je bijvoorbeeld dit invoeren:

```
python main.py nationaal greedy --time 1000 --plot_scores
```

Hieronder een lijst met de mogelijke argumenten per 'categorie', de verschillende algoritmes hebben ook twee bestandsnamen, onder deze bestandsnamen worden dataframes en plots opgeslagen:

- **holland/nationaal**:
  - **holland**: Gebruikt de data van Noord- en Zuid-Holland
  - **nationaal**: Gebruikt de data van heel Nederland

- **algoritme: standaard = baseline**
  - **baseline**: Gebruikt een willekeurig algoritme.
  - **simulated_annealing**: Gebruikt simulated annealing. Slaat de beste oplossing en een histogram op in de map data/output onder de respectievelijke namen simulated_best_solution_nationaal.csv (of .holland.csv) en simulated_annealing_histogram_nationaal.png (of .holland.png).

- **tijd: standaard = 60**
  - **--time [0-oneindig]**: Bepaalt hoe lang het gekozen algoritme draait.

- **plotten: standaard = nee**
  - **--plot_scores**: Bepaalt of histogram van scores opgeslagen moet worden.

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