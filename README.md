# CDS



Cross-platform training app (Web, iPhone, Android) built on the CDS Flask backend and Flutter frontend.



## Structure



```

CDS/

├── backend/    # Flask server (CDS + JSON API for Flutter)

└── frontend/   # Flutter app (Web / iOS / Android)

```



## Run locally



### Backend



```bash

cd backend

./run.sh

```



Server starts at `http://0.0.0.0:8080` (accessible from simulators and LAN devices).



### Frontend



```bash

cd frontend

flutter pub get

flutter run -d chrome    # Web

flutter run -d ios       # iPhone simulator

flutter run -d android   # Android emulator

```



Or use helper scripts:



```bash

cd frontend

chmod +x scripts/run_ios.sh scripts/run_android.sh

./scripts/run_ios.sh

./scripts/run_android.sh

```



## iPhone / Android



The Flutter app includes the same features as the HTML version:



- Login / password reset

- Main menu

- Multi-question exams (`exercise.html`)

- Exam finish and analysis (`finish.html`, `analysis.html`, `comments.html`)

- Single-question mode (`exercise2.html`, `analysis2.html`)

- Admin screens



### Simulator / emulator (default)



| Platform | Default API URL |

|---|---|

| Web | `http://localhost:8080` |

| iPhone simulator | `http://localhost:8080` |

| Android emulator | `http://10.0.2.2:8080` |



### Physical iPhone / Android device



1. Connect the phone and Mac to the same Wi‑Fi network.

2. Find your Mac IP address:



   ```bash

   ipconfig getifaddr en0

   ```



3. Start the backend on the Mac.

4. Launch the app and enter the server URL on the login screen, e.g.:



   ```

   http://192.168.0.42:8080

   ```



Alternatively, pass the URL at build time:



```bash

flutter run -d ios --dart-define=API_BASE_URL=http://192.168.0.42:8080

flutter run -d android --dart-define=API_BASE_URL=http://192.168.0.42:8080

```



### Platform notes



- **iOS**: App Transport Security allows local HTTP (`NSAllowsLocalNetworking`).

- **Android**: Cleartext HTTP is enabled for development (`network_security_config.xml`).



## API



Flutter uses JSON endpoints under `/api/*`. The original HTML templates remain available for web admin tasks.


