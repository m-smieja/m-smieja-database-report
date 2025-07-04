Projekt, nadzór koncepcji, modele
==================================

Model konceptualny
------------------

Model konceptualny przedstawia wysokopoziomową strukturę systemu bazy danych.
Koncentruje się na głównych encjach i relacjach między nimi, abstrahując od
szczegółów implementacyjnych.

Główne encje
~~~~~~~~~~~~

* **Użytkownik** - podstawowa jednostka w systemie
* **Projekt** - grupuje powiązane dane
* **Dokument** - pojedynczy element danych
* **Uprawnienia** - definiuje dostęp do zasobów

Model logiczny
--------------

Model logiczny przekształca koncept w struktury możliwe do implementacji
w systemie bazodanowym. Definiuje tabele, kolumny, typy danych oraz
ograniczenia.

Przykład definicji tabeli::

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

Model fizyczny
--------------

Model fizyczny uwzględnia specyfikę konkretnego systemu zarządzania bazą danych.
Obejmuje:

* Partycjonowanie tabel
* Indeksy i ich typy
* Przestrzenie tabel (tablespaces)
* Parametry storage
* Strategie backup

Nadzór koncepcji
----------------

System nadzoru zapewnia spójność między modelami konceptualnym, logicznym
i fizycznym. Wykorzystuje narzędzia do:

* Walidacji schematów
* Śledzenia zmian
* Generowania dokumentacji
* Testowania integralności
