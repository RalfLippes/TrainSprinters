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

Vervolgens roep je een van de algoritmes aan door de naam van dit algoritme mee te geven. Deze algoritmes slaan altijd een dataframe van de beste oplossing op als csv bestand in de map data/output. Per algoritme moet je soms ook nog een of meerdere extra argumenten meegeven. De structuur van de mee te geven argumenten is [holland/nationaal] [algoritme] [tijd] [plotten]. Tijd en plotten hebben standaard waarden: respectievelijk '60 seconden' en 'niet plotten'. Om andere waarden dan deze standaard waarden te krijgen, moet je expliciet argumenten meegeven. Als je dus de baseline voor 60 seconden zou willen runnen zonder te plotten (voor de holland data), dan voer je in:

```
python main.py holland baseline
```

Als je Simulated annealing op nationale data zou willen runnen met de standaardwaarden zou je dat algoritme kunnen runnen met: 

```
python main.py nationaal simulated_annealing 
```

Om greedy 1000 seconden te laten lopen en van de gevonden scores een histogram te maken zou je bijvoorbeeld dit invoeren:

```
python main.py nationaal greedy --time 1000 --plot_scores
```

Hieronder een lijst met de mogelijke argumenten per 'categorie', de verschillende algoritmes hebben ook twee bestandsnamen, onder deze bestandsnamen worden dataframes en plots opgeslagen:

- **holland/nationaal**:
  - **holland**: Gebruikt de data van Noord- en Zuid-Holland
  - **nationaal**: Gebruikt de data van heel Nederland

- **algoritme**:
  - **simulated_annealing**: Gebruikt simulated annealing. Slaat de beste oplossing en een histogram op in de map data/output onder de respectievelijke namen simulated_best_solution_nationaal.csv (of .holland.csv) en simulated_annealing_histogram_nationaal.png (of .holland.png).

 voorbeeld:
 ```
python main.py holland simulated_annealing --time 100 --plot_scores 
```
  - **baseline**: Gebruikt een willekeurig algoritme. Slaat de beste oplossing en een histogram op onder de namen baseline_best_solution_nationaal.csv en baseline_histogram_nationaal.csv.
 voorbeeld:
 ```
python main.py holland baseline --time 100 --plot_scores 
```
  - **annealing_steps**: Gebruikt het annealing steps algoritme. Slaat de beste oplossing en een histogram op onder de namen annealing_steps_best_solution_nationaal.csv en annealing_steps_histogram_nationaal.csv.
 voorbeeld:
 ```
python main.py holland annealing_steps --time 100 --plot_scores 
```
  - **greedy**: Gebruikt een greedy algoritme. Slaat de beste oplossing en een histogram op onder de namen greedy_best_solution_nationaal.csv en greedy_histogram_nationaal.csv.
 voorbeeld:
 ```
python main.py holland greedy --time 100 --plot_scores 
```
  - **hill_climber**: Gebruikt een hill climber algoritme. Slaat de beste oplossing en een histogram op onder de namen hill_climber_best_solution_nationaal.csv en hill_climber_histogram_nationaal.csv. **LET OP** Dit algoritme vereist specificatie van wat voor algoritme algoritme een initiële oplossing aan hill climber geeft, en welk algoritme nieuwe trajecten toevoegt. De opties hiervoor zijn:
    - **--start_algorithm**:
      - **greedy**: Gebruikt greedy als start algoritme.
      - **baseline**: Gebruikt baseline als start algoritme.
      - **annealing_steps**: Gebruikt annealing steps als start algoritme.
    - **--creating_algorithm**
      - **baseline**: Gebruikt random algoritme om nieuwe trajecten te maken.
      - **annealing_steps**: Gebruikt annealing steps om nieuwe trajecten te maken
  
Een voorbeeld van het runnen van hill climber op nationale data met een random (baseline) initiële oplossing en annealing steps om nieuwe trajecten te maken, voor 100 seconden plus het maken van een histogram van de scores:

```
python main.py nationaal hill_climber --time 100 --plot_scores --start_algorithm baseline --creating_algorithm annealing_steps
```

- **hill_climber2**: gebruikt een hill climber algoritme op iteratieve wijze. Runt het hill climber algoritme eerst een aantal keer met laag aantal iteraties. Voor de beste oplossing runt hij het hill_climber algoritme nogmaals met 2000000 iteraties. Dit algoritme vereist dezelfde specificaties als de reguliere hill_climber

een voorbeeld van het runnen van hill climber2 op holland data met een annealing initiële oplossing en annealing steps om nieuwe trajecten te maken, voor 100 seconden plus het maken van een histogram van de scores:

```
python main.py nationaal hill_climber2 --time 200 --plot_scores --start_algorithm baseline --creating_algorithm annealing_steps
```

- **tijd: standaard = 60**
  - **--time [0-oneindig]**: Bepaalt hoe lang het gekozen algoritme draait.
- **plotten: standaard = nee**
  - **--plot_scores**: Bepaalt of histogram van scores opgeslagen moet worden.

### Andere experimenten uitvoeren

Behalve het runnen van een algoritme en de scores te plotten is het ook mogelijk om een ander experiment uit te voeren. De naam van het experiment komt dan op de plaats van het algoritme. Dit vereist verder geen extra argumenten. Een voorbeeld is:

```
python main.py nationaal temp_cool
```

De mogelijke experimenten zijn:

- **experimenten**:
  - **temp_cool**: Vindt de beste temperatuur en cooling rate voor simulated annealing. Zal verschillende waarden vinden voor nationaal en holland.
  - **find_iteration**: Maakt een plot van het aantal iteraties dat hill_climber gerund heeft, en wat de high score was bij die iteratie.  Werkt voor holland en nationaal.

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor algoritmes
    - **/code/algorithms/call_algorithm**: bevat de code om een algoritme aan te roepen of een experiment uit te voeren.
  - **/code/classes**: bevat de vier benodigde classes voor deze case
  - **/code/visualisation**: bevat de code voor de visualisaties
- **/data**: bevat de verschillende databestanden die nodig zijn om de programma's te draaien
  - **/data/Noord_Holland**: bevat de data voor Noord- en Zuid-Holland (stations en verbindingen)
  - **/data/Nationaal**: bevat de data voor heel Nederland (stations en verbindingen)
  - **/data/output**: bevat de resultaten (dataframes, plots) die verkregen zijn 

## Auteurs
- Ralf Lippes
- Seb Dackus
- Mark van den Hoorn
