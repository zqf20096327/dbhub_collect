# Solea Tram - Tidbyt App

Application Tidbyt pour afficher les prochains passages de tram Solea à Mulhouse.

## Structure du projet

```
tidbyt-solea/
├── server.py          # Serveur API Python (lit les données GTFS)
├── solea_tram.star    # App Tidbyt en Starlark
├── requirements.txt   # Dépendances Python
├── start.sh           # Script de démarrage du serveur
├── venv/              # Environnement virtuel Python
└── *.txt              # Fichiers GTFS (stops, routes, etc.)
```

## Installation

### 1. Prérequis

- Python 3.x
- Pixlet (installé via `brew install tidbyt/tidbyt/pixlet`)

### 2. Démarrer le serveur API

```bash
cd tidbyt-solea
./start.sh
```

Le serveur démarre sur `http://localhost:5555`

### 3. Tester l'API

```bash
# Rechercher une station
curl http://localhost:5555/search/republique

# Voir les prochains départs
curl http://localhost:5555/departures/190967
```

### 4. Prévisualiser l'app Tidbyt

```bash
pixlet serve solea_tram.star
```

Ouvrir `http://localhost:8080` dans le navigateur.

## Configuration de l'app

L'app accepte deux paramètres :

- `api_url` : URL du serveur API (défaut: `http://localhost:5555`)
- `stop_id` : ID de l'arrêt à afficher

### Trouver l'ID de votre arrêt

```bash
curl http://localhost:5555/search/VOTRE_ARRET
```

Stations populaires :
| Station | ID |
|---------|------|
| REPUBLIQUE | 190967 |
| GARE CENTRALE | 61967 |
| PORTE JEUNE | 190958 |
| PORTE HAUTE | 190957 |

## Pousser vers le Tidbyt

### Générer l'image

```bash
pixlet render solea_tram.star
```

### Pousser vers votre Tidbyt

```bash
pixlet push YOUR_DEVICE_ID solea_tram.webp
```

## Déploiement permanent

Pour que l'app fonctionne 24/7 sur votre Tidbyt, vous devez :

1. **Héberger le serveur API** quelque part (Raspberry Pi, VPS, etc.)
2. **Configurer l'URL** dans l'app
3. **Publier l'app** sur le Tidbyt Community ou utiliser un cron pour pusher régulièrement

### Option : Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5555
CMD ["python", "server.py"]
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Documentation |
| `GET /stops` | Liste des stations de tram |
| `GET /search/<query>` | Rechercher une station |
| `GET /departures/<stop_id>` | Prochains départs |

### Paramètres de /departures

- `limit` : Nombre de résultats (défaut: 5)
- `tram_only` : Filtrer bus (défaut: true)

## Mise à jour des données GTFS

Les données GTFS sont mises à jour périodiquement par Solea. Pour les mettre à jour :

```bash
curl -L -o gtfs.zip "https://transport.data.gouv.fr/resources/80787/download"
unzip -o gtfs.zip
# Redémarrer le serveur
```

## Apercu

L'affichage montre :
- Nom de la station
- Numéro de ligne avec couleur
- Destination
- Minutes avant le départ (vert si < 2min)

## Licence

Données GTFS sous licence Etalab (Open Data).
