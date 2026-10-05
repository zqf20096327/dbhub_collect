# TuttiTrip

> [!NOTE]
> **To monorepo złożone z submodułów gita.** Katalogi [`frontend/`](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-frontend), [`backend/`](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-backend) i [`worker/`](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-worker) to odnośniki do osobnych repozytoriów w organizacji [HackYeah-TuttiTripTeam](https://github.com/HackYeah-TuttiTripTeam). Kliknięcie takiego katalogu na GitHubie przenosi do innego repozytorium, na commit zapisany w tym repozytorium. Wszystkie te repozytoria są publiczne.

> [!NOTE]
> **Jak powstał kod.** TuttiTrip powstał z pomocą asystentów kodowania (Claude Code, Codex). Ludzie z zespołu odpowiadali za architekturę rozwiązania, rozplanowanie funkcji, działanie aplikacji i to, jak się z niej korzysta.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/readme/01-hero-ciemny.webp">
  <img src="docs/readme/01-hero.webp" alt="Strona TuttiTrip z hasłem „Plan, po którym nikt nie czuje, że przegrał”, polem do wpisania pierwszego zdania oraz planem wyjazdu do Gdańska na laptopie i telefonie.">
</picture>

TuttiTrip to planer wyjazdów rodzinnych i grupowych, który układa plan, po którym nikt w grupie nie czuje, że przegrał. Projekt powstaje na hackathonie HackYeah 2026.

To repozytorium zbiera trzy części aplikacji jako submoduły gita: frontend, backend i workera. Kod każdej części żyje w osobnym repozytorium, a tutaj jest opis całości i instrukcja uruchomienia.

## Problem

W grupie zwykle jedna osoba planuje cały wyjazd. Każdy chce czegoś innego: dziecko park rozrywki, nastolatek coś ze znajomymi, babcia muzeum i odpoczynek, partner tanio i blisko. Plany z czatbotów brzmią dobrze, ale często pomijają godziny otwarcia, odległości, tempo najwolniejszej osoby i wymagania co do noclegu.

## Co robi TuttiTrip

- Organizator opisuje wyjazd jednym zdaniem („Gdańsk, trzy dni, dzieci 6 i 13 lat, babcia”), a asystent dopytuje tylko o to, co najbardziej zmienia plan. Odpowiedzi zbiera kartami i suwakami. Pozostałych uczestników organizator dodaje jako profile, więc nie muszą zakładać kont.
- Dla każdego miejsca każda osoba ma „chcę”, „nie chcę” albo „obojętnie”, a przy „nie chcę” podaje powód. Aplikacja pokazuje werdykt z uzasadnieniem. Organizator może go nadpisać i widzi, ile to kosztuje (sprawiedliwość, budżet, czas).
- Plan układa deterministyczny solver, który dzieli zadowolenie między osoby możliwie po równo, z uwzględnieniem wag i budżetu grupy.
- Linter planu sprawdza godziny otwarcia, dystanse, tempo, przerwy, budżet i wymagania noclegowe. Działa też na planie z innego narzędzia, np. wklejonym z czatbota.
- Wymagania wobec noclegu (basen, kuchnia, parking, konkretna platforma) są kontraktem sprawdzanym dla każdej nocy.
- Wydatki zasilają budżet planu i rozliczenie. W trakcie wyjazdu plan można przeliczyć, gdy pada deszcz albo dziecko jest zmęczone.

Nowe jest to, że model językowy prowadzi rozmowę i pisze uzasadnienia, ale o planie decyduje zwykły kod (solver, linter, reguły cenowe, rozliczenie). Te same dane wejściowe dają ten sam plan, a liczbę naruszeń reguł da się policzyć i porównać z planem z czatbota. Testy architektury w backendzie pilnują, żeby ta logika nie zależała od frameworka webowego, agentów AI ani bazy.

## TuttiTrip w obrazkach

Plansze to makiety zbudowane na tokenach, krojach, ikonach i logo z naszego design systemu, na danych przykładowych (rodzina w Gdańsku). Odwzorowują frontend z gałęzi `develop`. Miara sprawiedliwości (wagi osób, suwak α, ocena i weto) jest już w aplikacji, ale jej ekran wygląda inaczej niż na planszach. Przeplanowanie po nagłym zdarzeniu (plansza z deszczem) jest w budowie i nie ma jeszcze ekranu. Zrzuty z działającej aplikacji są [niżej](#zrzuty-z-działającej-aplikacji).

<table>
  <tr>
    <td width="50%"><img width="100%" src="docs/readme/02-problem.webp" alt="Plan poniedziałku z czatbota z trzema problemami: muzeum zamknięte w poniedziałek, 9 km pieszo z babcią, budżet przekroczony o 240 zł. Obok wynik sprawdzenia: 3 problemy kontra 0 w planie TuttiTrip."><br><sub>Plan z czatbota: 3 problemy na 5 punktów. Plan TuttiTrip dla tej samej rodziny: 0.</sub></td>
    <td width="50%"><img width="100%" src="docs/readme/13-ai.webp" alt="Sześć kart pokazujących, gdzie w TuttiTrip pracuje AI, ze statusem „Działa”, „W budowie” albo „W planach” i nazwami modeli, pod spodem pasek o frameworku Pydantic AI."><br><sub>Gdzie pracuje AI. Działają wywiad głosem i kartami AG-UI, modele decyzyjne i uzasadnienia; nagłe zdarzenia są w budowie, a planowanie przez MCP oraz mapy i kalendarz w planach. Wszystko na Pydantic AI.</sub></td>
  </tr>
  <tr>
    <td><img width="100%" src="docs/readme/03-interview.webp" alt="Wywiad z asystentem: zdanie organizatora, karta z pytaniem i panel „Co już wiem” z faktami o wyjeździe."><br><sub>Wywiad jednym zdaniem albo głosem. Asystent pyta kartami, a fakty trafiają do panelu „Co już wiem”.</sub></td>
    <td><img width="100%" src="docs/readme/04-fairness.webp" alt="Wykres zadowolenia pięciu osób w skali 0–100 z podłogą 40 punktów. W planie TuttiTrip najniższy wynik ma Kuba, 58; w planie z czatbota babcia miała 22."><br><sub>Najmniej zadowolona osoba: 58 punktów zamiast 22.</sub></td>
  </tr>
  <tr>
    <td><img width="100%" src="docs/readme/05-decision.webp" alt="Telefon z propozycją przeniesienia Westerplatte na sobotę i kartą „Czeka na Twoją decyzję”: sprawiedliwość 0,87 na 0,71, Kuba 58 na 34, budżet plus 80 zł."><br><sub>Organizator widzi koszt decyzji, zanim ją wymusi (makieta, w aplikacji ten widok wygląda inaczej).</sub></td>
    <td><img width="100%" src="docs/readme/08-vote.webp" alt="Strona głosowania dla babci Heli otwarta z linku: oceny „Chcę”, „Obojętnie”, „Nie chcę” i weto, obok kod QR."><br><sub>Babcia głosuje z linku albo kodu QR, bez konta.</sub></td>
  </tr>
  <tr>
    <td><img width="100%" src="docs/readme/07-settle.webp" alt="Telefon z listą wydatków wyjazdu, obok suma 586 zł, „3 przelewy zamiast 6” i niepewny odczyt paragonu z przerywanym obrysem."><br><sub>Wydatek zdaniem albo zdjęciem paragonu, saldo każdej osoby i najmniej przelewów.</sub></td>
    <td><img width="100%" src="docs/readme/06-replan.webp" alt="Telefon z planem dnia po komunikacie „Silny deszcz od 11:00”: muzea zamiast parku i molo, obok panel „Co sprawdził kod” z zerem problemów."><br><sub>Deszcz od 11:00: model rozpoznaje zdarzenie, solver przelicza resztę dnia (w budowie).</sub></td>
  </tr>
  <tr>
    <td colspan="2"><img width="100%" src="docs/readme/10-devices.webp" alt="TuttiTrip na laptopie i telefonie, w jasnym i ciemnym motywie."><br><sub>PWA na telefon i laptop, po polsku i angielsku, w jasnym i ciemnym motywie, z serwerem MCP udostępniającym dane wyjazdu.</sub></td>
  </tr>
</table>

### Zrzuty z działającej aplikacji

Prawdziwy frontend z gałęzi `develop` na danych testowych (MSW). Zmieniliśmy tylko nazwę konta testowego i adres źródła cen. Zrzuty z laptopa przełączają się na ciemny motyw razem z GitHubem. Więcej ekranów jest w [README frontendu](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-frontend#zrzuty-ekranu).

<table>
  <tr>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/readme/desktop-pl-dark-05-wywiad-karty.webp">
        <img width="100%" src="docs/readme/desktop-pl-light-05-wywiad-karty.webp" alt="Wywiad po pierwszym zdaniu: karta budżetu i panel „Co już wiem” z oznaczeniem „ustalił asystent”.">
      </picture>
      <br><sub>Wywiad po pierwszym zdaniu: karta budżetu i panel „Co już wiem”.</sub>
    </td>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/readme/desktop-pl-dark-08-plan.webp">
        <img width="100%" src="docs/readme/desktop-pl-light-08-plan.webp" alt="Plan dnia w Warszawie z godzinami, kosztem planu, noclegiem i znacznikami „Cena zweryfikowana” ze źródłem.">
      </picture>
      <br><sub>Plan ze skrótem wersji, kosztem dla grupy i znacznikami weryfikacji cen i godzin.</sub>
    </td>
  </tr>
  <tr>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/readme/desktop-pl-dark-11-rozliczenie.webp">
        <img width="100%" src="docs/readme/desktop-pl-light-11-rozliczenie.webp" alt="Rozliczenie wyjazdu: saldo każdej osoby i lista przelewów.">
      </picture>
      <br><sub>Rozliczenie: saldo każdej osoby i najmniejsza liczba przelewów.</sub>
    </td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/readme/desktop-pl-dark-12-glosowanie-z-linku.webp">
        <img width="100%" src="docs/readme/desktop-pl-light-12-glosowanie-z-linku.webp" alt="Strona głosowania dla osoby bez konta, otwarta z linku, z ocenami miejsc i wetem.">
      </picture>
      <br><sub>Głosowanie z linku dla osoby bez konta, z wetem.</sub>
    </td>
  </tr>
</table>

Na telefonie: wyjazd zakładany głosem, zgoda na przekroczenie budżetu i głosowanie z linku bez konta.

<table>
  <tr>
    <td width="33%"><img width="100%" src="docs/readme/telefon-pl-light-03-utworz-glosowo.webp" alt="Zakładanie wyjazdu głosem na telefonie."></td>
    <td width="33%"><img width="100%" src="docs/readme/telefon-pl-light-09-plan-zgoda-budzet.webp" alt="Plan na telefonie z prośbą o zgodę na przekroczenie budżetu."></td>
    <td width="33%"><img width="100%" src="docs/readme/telefon-pl-light-12-glosowanie-z-linku.webp" alt="Głosowanie z linku bez konta, z wetem, na telefonie."></td>
  </tr>
</table>

## Środowiska

| Środowisko | Aplikacja | API (Swagger) |
| --- | --- | --- |
| produkcja (`main`) | https://tuttitrip.gburek.app | https://tuttitrip-api.gburek.app/api/v1/docs |
| develop | https://tuttitrip-develop.gburek.app | https://tuttitrip-api-develop.gburek.app/api/v1/docs |

Wszystkie endpointy backendu są pod `/api/v1/`. Ten sam adres działa też przez domenę aplikacji, np. https://tuttitrip.gburek.app/api/v1/docs.

Aplikacja to PWA, więc na telefonie można ją dodać do ekranu głównego.

Dane z TuttiTrip można podłączyć do Claude, ChatGPT i Claude Code przez serwer MCP (`https://tuttitrip-api.gburek.app/api/v1/mcp`). Instrukcja krok po kroku, wymagane plany i co widać po zalogowaniu: [Serwer MCP w README backendu](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-backend/blob/main/README.md#serwer-mcp).

Prezentacje z [`docs/presentations`](docs/presentations) są na https://tuttitrip-decks.gburek.app (lista pod `/`, np. https://tuttitrip-decks.gburek.app/TuttiTrip_pitch_deck). Każda inna gałąź tego repozytorium dostaje własny adres `https://tuttitrip-decks-<gałąź>.gburek.app`.

## Repozytoria

| Katalog | Repozytorium | Co zawiera |
| --- | --- | --- |
| [`frontend/`](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-frontend) | `tuttitrip-frontend` | aplikacja webowa (PWA) |
| [`backend/`](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-backend) | `tuttitrip-backend` | API, baza danych, solver i linter |
| [`worker/`](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-worker) | `tuttitrip-worker` | zadania w tle: agenci AI, embeddingi, przeliczenia |

Wszystkie trzy repozytoria są publiczne, więc `git clone --recurse-submodules` pobierze je bez dostępu do organizacji.

## Architektura

![Diagram architektury w czterech kolumnach: ludzie, aplikacja, backend oraz worker i modele, połączone kropkowanymi liniami, pod nim lista technologii.](docs/readme/14-stack.webp)

To samo w wersji, którą GitHub rysuje z kodu:

```mermaid
flowchart LR
    user["Organizator<br/>(telefon lub przeglądarka)"]
    fe["frontend<br/>React + Vite, PWA<br/>Cloudflare Workers"]
    be["backend<br/>FastAPI<br/>S1 szybko decyduje, S2 (LLM) pisze, S3 czeka na zgodę"]
    db[("PostgreSQL 18<br/>+ pgvector<br/>+ kolejki DBOS")]
    wk["worker<br/>DBOS + Pydantic AI"]
    gb["Modele na GB10<br/>Qwen, basal, Laya"]
    openr["OpenRouter<br/>zapas modeli"]
    rt["OpenAI Realtime<br/>mowa"]
    gm["Google Maps<br/>mapa i karta miejsca"]
    auth["Auth0"]

    user --> fe
    fe -- "REST (typy z OpenAPI)" --> be
    fe -. logowanie .-> auth
    fe -. "audio (WebRTC)" .-> rt
    fe -. mapa .-> gm
    be -. "sideband mowy" .-> rt
    be -- "dane, zlecanie zadań" --> db
    be --> gb
    wk -- "pobiera zadania, zapisuje wyniki" --> db
    wk --> gb
    wk -. zapas .-> openr
```

Szczegółowy diagram, decyzje D1 do D7 z powodami, mapa modeli, warunki Google Maps i słownik są w [docs/architektura.md](docs/architektura.md).

- Frontend ([tuttitrip-frontend](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-frontend)): React 19, TypeScript, Vite, TanStack Router i Query, shadcn/ui na Tailwind v4. Działa jako PWA na Cloudflare Workers. Typy zapytań generuje z `/api/v1/openapi.json` backendu, więc niezgodność z API wychodzi już przy kompilacji. API woła pod własną domeną (`/api/v1/...`), a Worker przekazuje te zapytania do backendu swojego środowiska.
- Backend ([tuttitrip-backend](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-backend)): Python 3.14, FastAPI, Pydantic, SQLAlchemy i Alembic, PostgreSQL 18 z pgvector, logowanie przez Auth0. Domeny (wyjazdy, profile, wywiad, planowanie, noclegi, wydatki) są osobnymi modułami. Solver sprawiedliwości, linter i rozliczenie to czysta logika bez zależności od frameworka. Długich operacji backend nie wykonuje sam, tylko zleca je workerowi przez kolejkę DBOS i odczytuje ich stan.
- Worker ([tuttitrip-worker](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-worker)): trwałe workflowy [DBOS](https://docs.dbos.dev/) z agentami [Pydantic AI](https://ai.pydantic.dev/). Postęp zapisuje w Postgresie, więc po restarcie kończy zadanie od ostatniego kroku i nie powtarza udanych wywołań modelu. Modele bierze z jednego katalogu Pydantic AI: Qwen3.8-27B i modele decyzyjne (basal, Laya) działają na GB10, a OpenRouter jest zapasem. Embeddingi liczy lokalnie (Ollama, `nomic-embed-text`). Backend i worker łączy wersjonowany kontrakt, który CI sprawdza w obu repozytoriach.

## Klonowanie

```bash
git clone --recurse-submodules https://github.com/HackYeah-TuttiTripTeam/tuttitrip.git
cd tuttitrip
```

Jeśli repozytorium jest już sklonowane bez submodułów albo chcesz pobrać najnowsze `main` każdej części:

```bash
git submodule update --init --remote
```

Submoduły śledzą gałąź `main`. W tym repozytorium zapisany jest konkretny commit każdej części. Żeby przesunąć go na aktualne `main`:

```bash
git submodule update --remote
git add frontend backend worker
git commit -m "Aktualizacja submodułów"
git push
```

Do pracy nad kodem lepiej klonować repozytoria części osobno. Każde ma własne CI, gałąź `develop` i podglądy dla gałęzi.

## Uruchomienie lokalne

Wymagania:

- Docker z Docker Compose (lokalny Postgres z pgvector),
- [uv](https://docs.astral.sh/uv/) dla backendu i workera (sam pobierze Pythona 3.14),
- Node.js 22+ i pnpm (przez `corepack`) dla frontendu,
- opcjonalnie: klucz OpenRouter albo lokalny model zgodny z API OpenAI dla agentów oraz [Ollama](https://ollama.com) z `nomic-embed-text` dla embeddingów. Testy nie potrzebują żadnego z nich.

Backend startuje pierwszy, bo do niego należą schemat bazy, migracje i tabele DBOS.

### 1. Backend

API wystartuje na http://localhost:8000.

```bash
cd backend
uv sync
cp .env.example .env
docker compose up -d --wait db
uv run alembic upgrade head
uv run dbos migrate -s postgresql://tuttitrip:tuttitrip@localhost:5432/tuttitrip
uv run uvicorn tuttitrip.main:app --reload
```

### 2. Worker

W drugim terminalu:

```bash
cd worker
uv sync
cp .env.example .env    # domyślne wartości pasują do bazy z compose backendu
uv run tuttitrip-worker
```

Czy backend i worker się widzą, sprawdzisz tak:

```bash
curl -X POST localhost:8000/api/v1/jobs/ping          # zwraca workflow_id
curl localhost:8000/api/v1/jobs/ping/<workflow_id>    # status SUCCESS
```

### 3. Frontend

W trzecim terminalu. Aplikacja wystartuje na http://localhost:5173.

```bash
cd frontend
corepack enable
pnpm install
cp .env.example .env.local
pnpm api:sync    # typy API z lokalnego backendu
pnpm dev
```

Bez zmiennych `VITE_AUTH0_*` aplikacja działa z wyłączonym logowaniem. Frontend można też podłączyć do wdrożonego API: `VITE_API_URL=https://tuttitrip-api-develop.gburek.app`.

Szczegóły (zmienne środowiskowe, port bazy inny niż 5432, uruchamianie w kontenerach, testy i lint, zasady architektury) są w README każdej części:

- [frontend/README.md](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-frontend/blob/main/README.md)
- [backend/README.md](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-backend/blob/main/README.md)
- [worker/README.md](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-worker/blob/main/README.md)

## Jak pracujemy

Zadania prowadzimy w projekcie GitHub organizacji. Pracę nad zadaniem zaczynamy na gałęzi `feature/...` od `develop` i otwieramy PR do `develop`. PR do `develop` mergujemy przez "Squash and merge", a wydanie to PR z `develop` do `main` mergowany przez "Create a merge commit". Każda gałąź dostaje własny podgląd frontendu i API.

Zgłoszenia i PR mają stały format. Tytuł zgłoszenia zaczyna się od `feat:`, `docs:`, `chore:` albo `bug:` (np. `feat(frontend): Filtrowanie wyjazdów po dacie`), a treść ma sekcje Opis, Dlaczego, Kryteria akceptacji, Definition of Done i Obszar. Zgłoszenie błędu opisuje dodatkowo kroki do odtworzenia, oczekiwane i faktyczne zachowanie oraz środowisko. Formularz New issue prowadzi przez te pola, a zgłoszenia w innym formacie bot zamyka z komentarzem, co poprawić. Tytuł PR ma te same prefiksy, tylko poprawka to `bugfix:`, a wydanie `release:`. Opis PR piszemy po polsku według szablonu. Notatki wydań powstają same w GitHub Releases. Szczegóły są w [CONTRIBUTING.md](https://github.com/HackYeah-TuttiTripTeam/.github/blob/main/CONTRIBUTING.md).

## Powiadomienia (Discord)

Na kanał zespołu na Discordzie trafiają:

- wyniki workflow z czterech repozytoriów: CI, wdrożenia (z adresem: produkcja, `develop`, podgląd PR, API gałęzi), sprzątanie i sprawdzenia formatu. Wysyła je `.github/workflows/discord-notify.yml` w każdym repozytorium przez wspólny workflow z repozytorium [`.github`](https://github.com/HackYeah-TuttiTripTeam/.github),
- zmiany w projekcie GitHub (nowy element, zmiana Status, Area, Priority, archiwizacja, usunięcie) oraz nowe, zamknięte i scalone issue i PR. Wysyła je Worker Cloudflare `tuttitrip-discord-relay` (`https://tuttitrip-hooks.gburek.app`) z webhooka organizacji.

Żeby kanał nie zarastał: uruchomienia `skipped` nie są wysyłane, sprawdzenia formatu, usuwanie gałęzi, notatki wydań i sprzątanie piszą tylko przy błędzie, a sukces na gałęzi roboczej i anulowanie to jedna linia. Pełną wiadomość dostają sukcesy na `main` i `develop` oraz każdy błąd.

Webhook Discorda jest sekretem `DISCORD_WEBHOOK_URL` w każdym repozytorium i w Workerze. Konfiguracja, rotacja webhooka i szczegóły zasad: [CONTRIBUTING.md, "Powiadomienia (Discord)"](https://github.com/HackYeah-TuttiTripTeam/.github/blob/main/CONTRIBUTING.md#powiadomienia-discord).

## Zespół

| Imię i nazwisko | Rola | Obszary |
| --- | --- | --- |
| Łukasz Gęborys | Lider zespołu | AI i Data Science, cyberbezpieczeństwo, zarządzanie projektem i produktem |
| Cyprian Gburek | Uczestnik | AI i Data Science, Backend Developer, bazy danych, inżynieria danych, DevOps i chmura, Frontend Developer, prezentacje i wystąpienia publiczne, zarządzanie projektem i produktem, architektura oprogramowania, wytwarzanie oprogramowania, aplikacje webowe i mobilne |
| Angelika Korcz | Uczestniczka | cyberbezpieczeństwo |
| Michał Sadrzak | Uczestnik | AI i Data Science, UI, aplikacje webowe i mobilne, wytwarzanie oprogramowania |
| Tomasz Florczak | Uczestnik | inne technologie |
