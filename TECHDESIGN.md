# Technisch Ontwerp - Trivia Royale (IK22)

## Controllers
Deze functies zullen zich bevinden in application.py, waarbij er verschillende routes zijn op de website.

### De taakbalk: layout.html
layout.html vormt het bedieningspaneel van de gebruiker, met de volgende knoppen:
* Play now! (Offline)
* Play now! (Online)
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

### Route Offline "/pregame_offline": pregame.html -> question.html -> answers.html
#### methods: "GET" & "POST"
Als de gebruiker niet is ingelogd of niet wil dat er gegevens worden opgeslagen in de database, is er de mogelijkheid om het spel offline te spelen.

### Route Online "/pregame_online": pregame.html -> question.html -> answers.html
#### methods: "GET" & "POST"
Als je ervoor kiest om het spel online te spelen worden je gegevens opgeslagen in de database.

### Pregame:
In questions/ zit het bestand categories.py, met daarin een dictionary met als keys alle mogelijke categorieën en als values de getallen die je moet gebruiken om op basis van de gekozen categorie een vraag op te halen uit de online triviadatabase.
Allereerst worden er uit de lijst van categories.py twee categorieën willekeurig uitgekozen, die worden getoond als knoppen op pregame.html, waar de gebruiker dus uit een categorie kan kiezen.
Vervolgens als de gebruiker een categorie heeft gekozen, wordt de value van de categorie gebruikt in de url om een vraag te renderen.

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
* apology(): redirect naar apology.html indien er zich een error 400 voordoet.
* login_required(f): zorgt ervoor dat een gebruiker ingelogd moet zijn om naar een pagina te gaan.

Eigen functies:
* categories(): kiest twee categorieën uit voor pregame.html
* trivia(): haalt aan de hand van een opgegeven categorie een .json bestand op van https://opentdb.com.

## Plugins en Frameworks
### [Flask](http://flask.pocoo.org/)
### [Bootstrap](https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css)
### [Jinja2](http://jinja.pocoo.org/docs/2.10/)