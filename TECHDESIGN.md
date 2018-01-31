# Technisch Ontwerp - Trivia Royale (IK22)

## Controllers
Deze functies zullen zich bevinden in `application.py`, waarbij er verschillende routes zijn op de website.

### De taakbalk: layout.html
`layout.html` vormt het bedieningspaneel van de gebruiker, met de volgende knoppen:
* Play!
* Log Out

En als de gebruiker nog niet is ingelogd:
* Play!
* Log In
* Register

### Route Homepage "/": index.html
#### method: "GET"
`index.html` dient als de homepage van de website. Op deze pagina kun je kijken naar de high scores leaderboard.

### Route Inloggen "/login": login.html
#### methods: "GET" & "POST"
Op deze pagina kan de gebruiker inloggen.

### Route Registreren "/register": register.html
#### methods: "GET" & "POST"
Op deze pagina kan de gebruiker een account registreren.

### Route Uitloggen "/logout"
#### Geen scherm!
Door middel van deze knop kan de gebruiker uitloggen, waarbij deze wordt geredirect naar index.html.

### Route Triviaspel: `/pregame` --> `/question` --> `/proceed`/`/proceedonline`:
#### methods: "GET" & "POST"
Als de gebruiker het spel wil spelen is `pregame.html` de eerste pagina die hij tegenkomt.

#### /pregame
In `/triviaroyale` zit een bestand `categories.py`, waarin zich een dictionary _categories_ bevindt waarbij de keys de nummers van de categorieën zijn en de values de namen van de categorieën.
In `helpers.py` staat een functie getTrivia() die een willekeurig gekozen categorie returnt. Vervolgens worden twee categorieën door middel van een UPDATE toegevoegd aan tabel categories in de database `triviaroyale.db`.
De twee categorieën worden vervolgens weergegeven op `pregame.html`, waarbij de gebruiker kan kiezen van welke categorie er een vraag moet worden gekozen.
Als de gebruiker op een knop heeft geklikt wordt de naam van de categorie gebruikt in een andere dictionary _urls_ in `urls.py`, die een url geeft om een vraag van die categorie op te halen uit de online triviadatabase.

#### /question
Er wordt een variabele _triviafile_ gebruikt om het .json bestand van de triviavraag te bewaren. Vervolgens worden de antwoorden gehusseld en opgeslagen in de tabel `Results`.
Nu kan de gebruiker ze op `question.html` zien. Als de gebruiker op het juiste antwoord heeft geklikt wordt zijn score met 10 punten verhoogd. Zo niet, dan wordt zijn score gereset naar 0.
Na het geven van een antwoord wordt de gebruiker geredirect naar `proceed.html` of, indien de gebruiker is ingelogd, naar `proceedonline.html`.

#### /proceed | /proceedonline
Op `proceed.html` kan de gebruiker het correcte antwoord op de vraag zien en indien de gebruiker is ingelogd wordt ook de huidige score weergegeven. Verder is er de mogelijkheid om verder te spelen of om terug te keren naar de homepagina.

## Models / Helpers
### models.py
In `models.py` staan classes en functies die voor interactie zorgen tussen application.py en triviaroyale.db zoals __User__, __Results__ en __Choice__.

### helpers.py
* randomcategory(): kiest een willekeurige categorie uit.
* getTrivia(): haalt aan de hand van een opgegeven categorie een .json bestand op van https://opentdb.com.
* triviaItems(): zet de elementen van het .json bestand om naar bruikbare variabelen.
* shuffle(): husselt de vier antwoorden door elkaar.

## Plugins en Frameworks
### [Flask](http://flask.pocoo.org/)
### [Bootstrap](https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css)
### [SQLAlchemy](https://www.sqlalchemy.org/)