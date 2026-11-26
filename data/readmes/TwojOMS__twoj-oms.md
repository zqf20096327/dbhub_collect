<p>
  <a href="https://twojoms.pl">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-ciemne.svg">
      <img src="docs/assets/logo.svg" alt="Twój OMS" height="56">
    </picture>
  </a>
</p>

[![CI](https://github.com/TwojOMS/twoj-oms/actions/workflows/ci.yml/badge.svg)](https://github.com/TwojOMS/twoj-oms/actions/workflows/ci.yml)

Panel do obsługi zamówień dla małej sprzedaży internetowej w Polsce, instalowany na własnym serwerze.
Zamówienia z Allegro, ERLI i WooCommerce na jednej liście, faktury (inFakt, Fakturownia, KSeF), nadawanie
paczek (DPD, InPost, Allegro, ERLI), zwroty, magazyn, koszty i raporty. Node.js 24 z wbudowanym SQLite,
Fastify, widoki renderowane na serwerze. Licencja MIT.

**[Demo](https://demo.twojoms.pl)** (bez zakładania konta: przycisk „Wejdź do demo”, dane zmyślone, reset co godzinę) ·
**[Instalacja](docs/instalacja-docker.md)** · **[Mapa kodu](docs/architektura.md)** · **[Dla agenta AI](AGENTS.md)** ·
**[twojoms.pl](https://twojoms.pl)**

![Lista zamówień w demo: zamówienia z Allegro, sklepu WooCommerce i ERLI, przesyłki Allegro, DPD i InPost](docs/assets/lista-zamowien.png)

> **English in short.** Self-hosted order management panel for small Polish online sellers: Allegro, ERLI
> and WooCommerce orders, inFakt/Fakturownia/KSeF invoicing, DPD/InPost shipping. Node.js 24 with the built-in
> `node:sqlite`, Fastify, server-rendered EJS with htmx, no frontend build step. The UI, code comments and
> documentation are in Polish. The [live demo](https://demo.twojoms.pl) needs no account. MIT licence, no
> warranty, no support. If you drive the repo with an AI agent, start with [AGENTS.md](AGENTS.md).

## Stos

- **Środowisko:** Node.js 24 lub nowszy. SQLite jest wbudowany (`node:sqlite`): bez serwera bazy i bez modułów
  natywnych do kompilowania.
- **Aplikacja:** Fastify 5, widoki EJS renderowane na serwerze, interakcje przez htmx; frontend nie ma kroku budowania.
- **Język:** JavaScript i TypeScript. Node uruchamia pliki `.ts` wprost (`erasableSyntaxOnly`), `npm run typy`
  sprawdza typy.
- **Zależności:** 10 produkcyjnych, wszystkie w [package.json](package.json).
- **Testy:** Vitest, ok. 1400 plików testów; linii testów jest dwa razy więcej niż kodu w `src/`.
- **Serwer:** Linux z Dockerem. Instrukcję sprawdzono na Debianie 13: 2 rdzenie, 4 GB RAM, 16 GB dysku.

## Szybki start: próba bez kluczy

Potrzebujesz Gita i Node.js 24 lub nowszego (`node --version`). Node pobierz z [nodejs.org](https://nodejs.org/) —
pakiety systemowe są za stare (Debian 13 ma 20.x, Ubuntu 24.04 ma 18.x).

```bash
git clone https://github.com/TwojOMS/twoj-oms.git
cd twoj-oms
npm ci
node scripts/instalacja-demo.mjs --katalog "$HOME/oms-demo" --port 39151
node scripts/instalacja-otworz.mjs --katalog "$HOME/oms-demo" --port 39151
```

W PowerShellu na Windowsie zamiast `npm ci` wpisz `npm.cmd ci`. Przy domyślnej polityce wykonywania skryptów
`npm` uruchamia `npm.ps1` i kończy się błędem „running scripts is disabled”. Pozostałe polecenia działają bez zmian.

Ostatnie polecenie uruchamia panel pod `http://127.0.0.1:39151/login` i działa do Ctrl+C. Login i hasło
administratora są w `~/oms-demo/administrator-proby.env`, a w panelu czekają trzy zmyślone zamówienia.

Katalog podaje się ścieżką bezwzględną (stąd `$HOME`) i musi leżeć poza repozytorium. Trafia do niego baza,
hasło próby i `klucz.env`, którym OMS szyfruje w bazie hasła i tokeny integracji. Nie kasuj tego klucza:
bez niego OMS nie wstanie, a nowy klucz nie odczyta zapisanych poświadczeń. Na serwerze klucz leży osobno,
poza katalogiem danych ([Klucz poświadczeń](docs/instalacja-docker.md#klucz-poświadczeń)). Szczegóły próby
i jej ograniczenia: [docs/instalacja-klienta.md](docs/instalacja-klienta.md).

## Jak jest zbudowany

Każda funkcja to moduł: katalog `src/moduly/<nazwa>/` z plikiem `modul.ts`. Moduł podaje, czego `wymaga`,
sprawdza swoje zmienne środowiska, wnosi migracje, uprawnienia i pozycje menu, a `zbuduj(ctx)` oddaje
trasy HTTP, usługi i zegary. Skład jest w jednym miejscu, `src/moduly/lista.ts`; kolejność budowy wynika z `wymaga`.

| Katalog | Co tam jest |
|---|---|
| `src/core` | rdzeń bez wiedzy o firmie: kontrakt modułu, składanie aplikacji, migracje, uprawnienia, warstwa WWW |
| `src/moduly` | moduły funkcji, tabela niżej |
| `src/domena` | reguły biznesowe bez HTTP i bez bazy: status zamówienia, filtry listy, mapowania kanałów |
| `src/integracje` | szew między modułami a klientami usług zewnętrznych |
| `src/oms` | dostęp do bazy (`src/oms/db/`) i klienci API: Allegro, ERLI, WooCommerce, kurierzy, KSeF, inFakt, Fakturownia, GUS, Meta, GA4 |

| Moduł | Zakres |
|---|---|
| `zamowienia` | lista i karta zamówienia, wyszukiwanie, filtry, wydruki, zamówienia ręczne |
| `kanaly` | kanały sprzedaży (Allegro, ERLI, WooCommerce): pobieranie zamówień, mapowanie, stan połączeń |
| `faktury` | faktury i proformy w PDF, inFakt albo Fakturownia, KSeF, sprzedaż do UE (WDT), paczka dla biura rachunkowego |
| `wysylka` | nadawanie paczek (DPD, InPost, Allegro, ERLI), etykiety, śledzenie, nadanie hurtem |
| `magazyn` | karty produktów, powiązania z ofertami w kanałach, stany; wysyłanie stanów do kanałów jest domyślnie wyłączone |
| `zwroty` | zwroty i korekty |
| `koszty` | koszty z KSeF i wpisane ręcznie, zestawienia |
| `raporty`, `marketing` | raporty sprzedaży i finansów, kampanie (Meta, GA4) |
| `wiadomosci` | wiadomości do klientów, poczta |
| `automatyzacje` | reguły „gdy zdarzenie, zrób akcję” z dziennikiem wykonań |
| `ustawienia` | konta z rolami i uprawnieniami do zakładek, integracje |
| `zdrowie` | `/health`, kopie zapasowe, alarmy |
| `api` | API v1 dla programów, na kluczach z zakresami |
| `rdzen` | wspólne tabele i dane firmy (NIP, rachunek), z których korzystają pozostałe moduły |

Droga jednego zamówienia od Allegro do wiersza na liście, warstwy i miejsca, w których łatwo się zgubić:
[docs/architektura.md](docs/architektura.md). Nowy kanał sprzedaży albo kurier jako moduł:
[docs/kanal-jako-modul.md](docs/kanal-jako-modul.md), [docs/kurier-jako-modul.md](docs/kurier-jako-modul.md).

## Integracje

Każda integracja jest opcjonalna i działa na własnych kluczach. Bez żadnego klucza panel pracuje w trybie
próby (`OMS_TRYB=proba`), który odmawia startu, gdy wykryje jakikolwiek klucz integracji. Kanały, kurierów
i pocztę podłącza się w panelu (Ustawienia → Integracje), bez edycji pliku.

| Obszar | Integracje | Instrukcje |
|---|---|---|
| Kanały sprzedaży | Allegro, ERLI, WooCommerce | [konto Allegro](docs/allegro-podlaczenie.md), [oferty Allegro](docs/kanal-allegro-oferty.md), [ERLI](docs/kanal-erli.md), [stany w WooCommerce](docs/kanal-woo.md) |
| Faktury | inFakt, Fakturownia, KSeF | [program do faktur](docs/modul-faktur.md), [Fakturownia](docs/fakturownia.md), [klienci WDT](docs/konfiguracja-wdt.md), [schematy KSeF](docs/ksef/README.md) |
| Wysyłka | DPD, InPost, Wysyłam z Allegro, ERLI | [DPD](docs/kurier-dpd.md), [InPost](docs/kurier-inpost.md) |
| Druk | drukarka etykiet przy komputerze z Windowsem | [agent druku](deploy/drukarka/README.md) |
| Magazyn | karty produktów, stany w kanałach | [magazyn](docs/magazyn.md) |
| Pozostałe | GUS (REGON), Meta, GA4, poczta SMTP | [poczta wychodząca](docs/poczta-smtp.md) |

Wszystkie zmienne środowiska: [docs/zmienne.md](docs/zmienne.md), generowany z rejestru `docs/konfiguracja.json`;
opis: [docs/konfiguracja.md](docs/konfiguracja.md).

## API

API v1 dla sklepu, arkusza, skryptu albo agenta AI: klucze z zakresami, opis w OpenAPI
([docs/api/openapi.json](docs/api/openapi.json)), przykłady w [docs/api/README.md](docs/api/README.md).
Demo ma jawny klucz tylko do odczytu:

```bash
curl -s "https://demo.twojoms.pl/api/v1/zamowienia?ile=3" \
  -H "Authorization: Bearer toms_demodemo_tylko-odczyt_demo-twojoms_Pracownia-Polcien"
```

## Instalacja na serwerze

- **Docker na Linuksie:** [docs/instalacja-docker.md](docs/instalacja-docker.md). Od czystego Debiana do panelu
  w sieci lokalnej, dalej dostęp z zewnątrz przez HTTPS, przejście z próby na pracę, integracje po kolei i kopie.
- **Przez agenta AI:** [docs/instalacja-przez-agenta.md](docs/instalacja-przez-agenta.md). Scenariusz krok po
  kroku z miejscami, w których agent musi się zatrzymać i zapytać człowieka.
- **Aktualizacje:** [docs/aktualizacje-klienta.md](docs/aktualizacje-klienta.md). Własne zmiany trzymaj w osobnej
  gałęzi, nowe wydania dołączaj przez `git merge` albo `git rebase`; migracje bazy są wyłącznie addytywne.
  Klon sprzed 25 listopada 2026: [Uporządkowanie historii repozytorium](docs/aktualizacje-klienta.md#uporządkowanie-historii-repozytorium-listopad-2026).

Panel ma pracować w sieci zaufanej albo za reverse proxy z HTTPS i kontrolą dostępu, nie wprost w internecie
([SECURITY.md](SECURITY.md)).

Wolisz, żeby ktoś postawił go za Ciebie? Opisz, jak sprzedajesz: [twojoms.pl/wdrozenie](https://twojoms.pl/wdrozenie.html).

## Rozwój i testy

```bash
npm run sprawdz                      # pełna bramka, jak w CI
npm run typy                         # tylko kontrola typów
npx vitest run tests/moduly/zwroty   # testy jednego modułu
```

Bramka to kontrola typów, Prettier, pięciu strażników (migracji, konfiguracji, kanałów, kurierów, sekretów)
i wszystkie testy.

Testy PDF czytają wygenerowane dokumenty programem `pdftotext` z Popplera (`apt install poppler-utils`). Bez
niego te testy się pomijają, a na początku przebiegu pojawia się ostrzeżenie z liczbą pominiętych plików; CI
tego repozytorium Popplera instaluje. Pełna bramka trwa długo, więc w trakcie pracy uruchamiaj testy
dotkniętego modułu.

Zasady zmian: [CONTRIBUTING.md](CONTRIBUTING.md) (najpierw test, potem kod). Reguły repozytorium i mapa kodu dla
agenta: [AGENTS.md](AGENTS.md), [docs/dla-agenta/](docs/dla-agenta/). Lukę bezpieczeństwa zgłoś prywatnie, nie
w Issues: [SECURITY.md](SECURITY.md).

## Czego się spodziewać

- Program powstał dla jednej polskiej firmy handlowej i pracuje w niej na co dzień. VAT, KSeF, WDT, kurierzy
  i bank działają według polskich reguł; interfejs, kod i dokumentacja są po polsku.
- Numery `PRZ-nnn` w dokumentach i testach to zadania z wewnętrznej tablicy, której nie ma w tym repozytorium.
- **Brak gwarancji i brak wsparcia** (licencja MIT). Wystawianie faktur, nadawanie paczek i wysyłka do KSeF
  mają skutki poza komputerem. Pierwsze uruchomienie z prawdziwymi kluczami zrób na koncie testowym
  i sprawdź każdą integrację osobno.

## Licencja

[MIT](LICENSE). Nazwy Allegro, ERLI, WooCommerce, inFakt, Fakturownia, KSeF, DPD, InPost, Meta i inne należą do
ich właścicieli; repozytorium nie jest z nimi powiązane.
