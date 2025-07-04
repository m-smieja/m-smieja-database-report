Rozdział 2 - Analiza Szczegółowa
=================================

Ten rozdział zawiera pięć niezależnych projektów zarządzanych jako osobne repozytoria, 
każdy skupiający się na kluczowym aspekcie systemu bazy danych.

.. toctree::
   :maxdepth: 2
   :caption: Podrozdziały:
   
   2.1/index
   2.2/index
   2.3/index
   2.4/index
   2.5/index

Wprowadzenie
------------

W tym rozdziale przedstawiamy pięć kluczowych komponentów systemu bazy danych, 
które zostały wydzielone jako niezależne moduły. Każdy z nich jest zarządzany 
w osobnym repozytorium Git, co umożliwia specjalizację zespołów i niezależny 
rozwój poszczególnych aspektów.

Struktura projektów
-------------------

.. list-table:: Subrepozytoria w rozdziale 2
   :header-rows: 1
   :widths: 10 35 30 25

   * - Nr
     - Nazwa
     - Autorzy
     - Repozytorium
   * - 2.1
     - Wydajność, Skalowanie i Replikacja
     - Broksonn
     - `GitHub <https://github.com/Broksonn/Wydajnosc_Skalowanie_i_Replikacja>`_
   * - 2.2
     - Sprzęt dla bazy danych
     - oszczeda
     - `GitHub <https://github.com/oszczeda/Sprzet-dla-bazy-danych>`_
   * - 2.3
     - Konfiguracja baz danych
     - Chaiolites
     - `GitHub <https://github.com/Chaiolites/Konfiguracja_baz_danych>`_
   * - 2.4
     - Bezpieczeństwo
     - BlazejUl
     - `GitHub <https://github.com/BlazejUl/bezpieczenstwo>`_
   * - 2.5
     - Kopie zapasowe i odzyskiwanie danych
     - m-smieja
     - `GitHub <https://github.com/m-smieja/Kopie_zapasowe_i_odzyskiwanie_danych>`_

Instrukcja aktualizacji
-----------------------

Aby zaktualizować zawartość wszystkich podrozdziałów::

    git submodule update --remote --merge

Aby pracować nad konkretnym modułem::

    cd 2.chapter/2.1
    git checkout main
    # wprowadź zmiany
    git add .
    git commit -m "Opis zmian"
    git push origin main

Współpraca
----------

Każdy podrozdział jest zarządzany przez dedykowany zespół. W celu wprowadzenia 
zmian w danym module, skontaktuj się z odpowiednim autorem lub stwórz Pull Request 
w odpowiednim repozytorium.
