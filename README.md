# Database Report

Kompleksowa dokumentacja systemu bazy danych.

## Struktura

- **Rozdział 1** - Wstęp
- **Rozdział 2** - Analiza szczegółowa (5 submodułów)
  - 2.1 - Wydajność, Skalowanie i Replikacja (Broksonn)
  - 2.2 - Sprzęt dla bazy danych (oszczeda)
  - 2.3 - Konfiguracja baz danych (Chaiolites)
  - 2.4 - Bezpieczeństwo (BlazejUl)
  - 2.5 - Kopie zapasowe i odzyskiwanie danych (m-smieja)
- **Rozdział 3** - Projekt, nadzór koncepcji, modele
- **Rozdział 4** - Analiza bazy danych
- **Rozdział 5** - Opis repozytoriów

## Budowanie dokumentacji

### Aktywacja środowiska
```bash
source venv/bin/activate  # lub ./activate.sh
```

### HTML
```bash
make html
# lub
./build.sh html
```

### PDF
```bash
sphinx-build -b pdf . _build/pdf
# lub
./build.sh pdf
```

## Praca z submodułami

### Klonowanie
```bash
git clone --recurse-submodules git@github.com:m-smieja/Database_report.git
```

### Aktualizacja wszystkich submodułów
```bash
git submodule update --remote --merge
```

### Praca z konkretnym submodułem
```bash
cd 2.chapter/2.1
git pull origin main
# wprowadź zmiany
git add .
git commit -m "Opis zmian"
git push origin main
cd ../..
git add 2.chapter/2.1
git commit -m "Update submodule 2.1"
```

## Autorzy submodułów

- **2.1** - Broksonn (Wydajność, Skalowanie i Replikacja)
- **2.2** - oszczeda (Sprzęt dla bazy danych)
- **2.3** - Chaiolites (Konfiguracja baz danych)
- **2.4** - BlazejUl (Bezpieczeństwo)
- **2.5** - m-smieja (Kopie zapasowe i odzyskiwanie danych)

## Autor dokumentacji

Milosz Smieja

## Licencja

MIT License
