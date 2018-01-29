# Technisch Ontwerp - Trivia Royale (IK22)

## Controllers
Deze functies zullen zich bevinden in application.py, waarbij er verschillende routes zijn op de website.

### De taakbalk: layout.html
layout.html vormt het bedieningspaneel van de gebruiker, met de volgende knoppen:
* Play now!
* Leaderboards
* Profile
* Log Out

En als de gebruiker nog niet is ingelogd:
* Log In
* Register

### Route Homepage "/": index.html
index.html dient als de homepage van de website. Op deze pagina kun je kijken naar de daily leaderboard en/of de all-time leaderboard.

### Route Inloggen "/login": login.html
#### methods: "GET" & "POST"
Op deze pagina kan de gebruiker inloggen.

### Route Registreren "/register": register.html
#### methods: "GET" & "POST"
Op deze pagina kan de gebruiker een account registreren.

### Route Uitloggen "/logout"
#### Geen scherm!
Door middel van deze knop kan de gebruiker uitloggen, waarbij deze wordt geredirect naar index.html.

### Route Pregame "/pregame":
#### methods: "GET" & "POST"
Als de gebruiker het spel wil spelen is pregame de eerste pagina die hij tegenkomt.

#### /pregame
Er is een bestand categories.py, waarin zich een dictionary _categories_ bevindt waarbij de keys de nummers van de categorieën zijn en de values de namen van de categorieën.
In helpers.py komt een functie getTrivia() die een willekeurig gekozen categorie returnt. Vervolgens worden twee categorieën door middel van een UPDATE toegevoegd aan tabel categories in de database triviaroyale.db.
De twee categorieën worden vervolgens weergegeven op pregame.html, waarbij de gebruiker kan kiezen van welke categorie er een vraag moet worden gekozen.
Als de gebruiker op een knop heeft geklikt wordt de naam van de categorie gebruikt in een andere dictionary urls in urls.py, die een url geeft om een vraag van die categorie op te halen uit de online triviadatabase.

#### /question
Er wordt een variabele _result_ gebruikt om het json bestand van de triviavraag te bewaren. result["question"] toont de vraag, result["correct_answer"] toont het juiste antwoord en result["incorrect answers"] geeft de onjuiste antwoorden.
Deze waardes worden weer opgeslagen in een tabel _trivia_ in de database, zodat de gebruiker ze op question.html kan zien. Als de gebruiker op correct_answer klikt wordt zijn score met een punt verhoogd. Zo niet, dan wordt zijn score gereset naar 0.
Na het geven van een antwoord wordt de gebruiker geredirect naar answers.html.

### Route Leaderboards "/leaderboards": leaderboards.html
#### methods: "GET" & "POST"
Op deze pagina kunnen gebruikers verschillende leaderboards bekijken.

### Route Player Profile "/profile": profile.html
#### methods: "GET" & "POST"
Op deze pagina is het persoonlijke profiel te zien van een gebruiker. Er zijn verschillende stats zichtbaar, zoals:
* Username
* Best Score
* Questions answered
* Correct answers given
* Correct / Wrong ratio

## Models / Helpers
### models.py
In models.py staan classes en functies die voor interactie zorgen tussen application.py en triviaroyale.db

### helpers.py
Functies die wij willen gebruiken van CS50:
* login_required(f): zorgt ervoor dat een gebruiker ingelogd moet zijn om naar een pagina te gaan.

Eigen functies:
* randomcategory(): kiest een willekeurige categorie uit.
* getTrivia(): haalt aan de hand van een opgegeven categorie een .json bestand op van https://opentdb.com.
* triviaItems(): zet de elementen van het .json bestand om naar bruikbare variabelen.

## Plugins en Frameworks
### [Flask](http://flask.pocoo.org/)
### [Bootstrap](https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css)
### [Jinja2](http://jinja.pocoo.org/docs/2.10/)