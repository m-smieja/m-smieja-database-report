Opis repozytoriów
==================

Główne repozytorium
-------------------

Repozytorium główne (``Database_report``) zawiera:

* Dokumentację techniczną (ten dokument)
* Skrypty migracyjne
* Schematy bazy danych
* Procedury administracyjne

Struktura katalogów::

    Database_report/
    ├── 1.chapter/      # Dokumentacja wprowadzająca
    ├── 2.chapter/      # Moduły funkcjonalne (submoduły)
    │   ├── 2.1/        # Wydajność, Skalowanie i Replikacja
    │   ├── 2.2/        # Sprzęt dla bazy danych
    │   ├── 2.3/        # Konfiguracja baz danych
    │   ├── 2.4/        # Bezpieczeństwo
    │   └── 2.5/        # Kopie zapasowe i odzyskiwanie danych
    ├── 3.chapter/      # Modele i koncepcje
    ├── 4.chapter/      # Analiza techniczna
    ├── 5.chapter/      # Ten rozdział
    └── 3rep/           # Repozytoria zewnętrzne

Repozytoria modułów
-------------------

Projekty w rozdziale 2 są zarządzane jako submoduły Git:

* **Wydajnosc_Skalowanie_i_Replikacja** - Optymalizacja wydajności i skalowanie
* **Sprzet-dla-bazy-danych** - Dobór i konfiguracja sprzętu
* **Konfiguracja_baz_danych** - Najlepsze praktyki konfiguracji
* **bezpieczenstwo** - Zabezpieczenia i audyt
* **Kopie_zapasowe_i_odzyskiwanie_danych** - Strategie backup i recovery

Repozytoria zewnętrzne
----------------------

Projekty powiązane, ale zarządzane niezależnie:

.. include:: ../3rep/repos_list.rst

Workflow deweloperski
---------------------

1. Klonowanie z submodułami::

    git clone --recurse-submodules git@github.com:m-smieja/Database_report.git

2. Praca nad dokumentacją::

    cd Database_report
    # edycja plików .rst
    make html  # budowanie HTML
    sphinx-build -b pdf . _build/pdf  # budowanie PDF

3. Aktualizacja submodułów::

    git submodule update --remote --merge

CI/CD
-----

Projekt wykorzystuje GitHub Actions do:

* Automatycznego budowania dokumentacji
* Walidacji składni RST
* Generowania PDF
* Deploymentu na GitHub Pages
