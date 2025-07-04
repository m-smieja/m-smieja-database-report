Analiza bazy danych
===================

Struktura tabel
---------------

Baza danych składa się z 25 tabel podzielonych na następujące kategorie:

* **Tabele podstawowe** (8 tabel) - przechowują kluczowe dane systemu
* **Tabele słownikowe** (5 tabel) - zawierają dane referencyjne
* **Tabele relacyjne** (7 tabel) - łączą encje w relacje wiele-do-wielu
* **Tabele audytu** (5 tabel) - śledzą zmiany w systemie

Kluczowe tabele
~~~~~~~~~~~~~~~

.. list-table:: Najważniejsze tabele systemu
   :header-rows: 1
   :widths: 20 30 50

   * - Nazwa tabeli
     - Liczba rekordów
     - Opis
   * - users
     - ~50,000
     - Dane użytkowników systemu
   * - projects
     - ~5,000
     - Projekty i ich metadane
   * - documents
     - ~2,000,000
     - Główna tabela z dokumentami

Relacje między tabelami
-----------------------

System wykorzystuje następujące typy relacji:

1. **One-to-Many** - np. użytkownik -> projekty
2. **Many-to-Many** - np. użytkownicy <-> role
3. **Self-referencing** - np. hierarchia kategorii

Integralność referencyjna
~~~~~~~~~~~~~~~~~~~~~~~~~

Wszystkie klucze obce posiadają zdefiniowane akcje:

* ``ON DELETE CASCADE`` - dla danych zależnych
* ``ON DELETE RESTRICT`` - dla danych krytycznych
* ``ON UPDATE CASCADE`` - dla wszystkich relacji

Optymalizacja
-------------

Zastosowane metody optymalizacji:

Indeksy
~~~~~~~

* B-tree dla kolumn wyszukiwania
* GiST dla danych przestrzennych
* GIN dla wyszukiwania pełnotekstowego
* Partial indexes dla filtrowanych zapytań

Partycjonowanie
~~~~~~~~~~~~~~~

Tabele z dużą ilością danych są partycjonowane według:

* Daty (tabele logów i audytu)
* Zakresu ID (tabele transakcyjne)
* Listy wartości (tabele słownikowe)

Materialized Views
~~~~~~~~~~~~~~~~~~

Dla często wykonywanych, złożonych zapytań utworzono zmaterializowane widoki
z automatycznym odświeżaniem.
