# CDS

Cross-platform training app (Web, iPhone, Android) built on the CDS Flask backend and Flutter frontend.

## Structure

```
CDS/
├── backend/    # Flask server (CDS + JSON API for Flutter)
└── frontend/   # Flutter app
```

## Run locally

### Backend

```bash
cd backend
./run.sh
```

Server starts at `http://localhost:8080`.

### Frontend

```bash
cd frontend
flutter run -d chrome   # Web
flutter run -d ios      # iPhone simulator
flutter run -d android  # Android emulator
```

## API

Flutter uses JSON endpoints under `/api/*` (login, main menu, exams, admin). The original HTML templates remain available for web admin tasks.
