Projekt bazy danych - System CRM
==================================

Ten rozdział przedstawia kompleksowy projekt bazy danych dla systemu zarządzania kontaktami i relacjami z klientami (mini CRM). System został zaprojektowany z myślą o małych i średnich przedsiębiorstwach, umożliwiając efektywne zarządzanie kontaktami, firmami, interakcjami oraz zadaniami.

Model konceptualny
------------------

Model konceptualny przedstawia wysokopoziomowy widok systemu, koncentrując się na głównych encjach biznesowych i ich wzajemnych relacjach.

Główne encje systemu
~~~~~~~~~~~~~~~~~~~~

1. **Kontakt (Contact)** - osoba fizyczna będąca klientem lub potencjalnym klientem
2. **Firma (Company)** - organizacja, z którą współpracujemy
3. **Interakcja (Interaction)** - zapis każdego kontaktu z klientem
4. **Zadanie (Task)** - planowane działania związane z klientem
5. **Użytkownik (User)** - pracownik korzystający z systemu
6. **Tag** - etykiety do kategoryzacji kontaktów

Diagram konceptualny
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │   USERS     │      │  COMPANIES  │      │    TAGS     │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                     │
           │                    │                     │
           ▼                    ▼                     ▼
    ┌─────────────────────────────────────────────────┐
    │                  CONTACTS                        │
    │  • Dane osobowe                                  │
    │  • Status lead                                   │
    │  • Przypisanie do użytkownika                   │
    └─────────────┬──────────────┬────────────────────┘
                  │              │
                  ▼              ▼
        ┌──────────────┐  ┌──────────────┐
        │ INTERACTIONS │  │    TASKS     │
        │ • Historia   │  │ • Planowane  │
        │   kontaktów  │  │   działania  │
        └──────────────┘  └──────────────┘

Relacje między encjami
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    [Użytkownik] 1 ------- * [Kontakt] (zarządza)
    [Użytkownik] 1 ------- * [Zadanie] (przypisany do)
    [Użytkownik] 1 ------- * [Interakcja] (rejestruje)
    
    [Kontakt] * ------- 0..1 [Firma] (pracuje w)
    [Kontakt] 1 ------- * [Interakcja] (uczestniczy)
    [Kontakt] * ------- * [Tag] (posiada)
    [Kontakt] 1 ------- * [Zadanie] (dotyczy)
    
    [Firma] 1 ------- * [Interakcja] (związana z)

Model logiczny
--------------

Model logiczny przekształca koncepcje biznesowe w struktury danych możliwe do implementacji w systemie relacyjnej bazy danych.

Struktura tabel
~~~~~~~~~~~~~~~

**Tabela: users**

.. list-table::
   :header-rows: 1
   :widths: 20 20 10 50

   * - Kolumna
     - Typ danych
     - Null
     - Opis
   * - user_id
     - INT
     - NOT NULL
     - PK, AUTO_INCREMENT
   * - username
     - VARCHAR(50)
     - NOT NULL
     - Unikalna nazwa użytkownika
   * - email
     - VARCHAR(100)
     - NOT NULL
     - Email użytkownika (UNIQUE)
   * - password_hash
     - VARCHAR(255)
     - NOT NULL
     - Zahashowane hasło
   * - first_name
     - VARCHAR(50)
     - NOT NULL
     - Imię użytkownika
   * - last_name
     - VARCHAR(50)
     - NOT NULL
     - Nazwisko użytkownika
   * - is_active
     - BOOLEAN
     - NOT NULL
     - Status aktywności (domyślnie TRUE)
   * - created_at
     - TIMESTAMP
     - NOT NULL
     - Data utworzenia konta
   * - last_login
     - TIMESTAMP
     - NULL
     - Data ostatniego logowania

**Tabela: companies**

.. list-table::
   :header-rows: 1
   :widths: 20 20 10 50

   * - Kolumna
     - Typ danych
     - Null
     - Opis
   * - company_id
     - INT
     - NOT NULL
     - PK, AUTO_INCREMENT
   * - name
     - VARCHAR(100)
     - NOT NULL
     - Nazwa firmy
   * - nip
     - VARCHAR(15)
     - NULL
     - NIP firmy (UNIQUE)
   * - industry
     - VARCHAR(50)
     - NULL
     - Branża
   * - website
     - VARCHAR(255)
     - NULL
     - Strona internetowa
   * - phone
     - VARCHAR(20)
     - NULL
     - Telefon główny
   * - address
     - TEXT
     - NULL
     - Adres siedziby
   * - created_by
     - INT
     - NOT NULL
     - FK -> users.user_id
   * - created_at
     - TIMESTAMP
     - NOT NULL
     - Data dodania

**Tabela: contacts**

.. list-table::
   :header-rows: 1
   :widths: 20 20 10 50

   * - Kolumna
     - Typ danych
     - Null
     - Opis
   * - contact_id
     - INT
     - NOT NULL
     - PK, AUTO_INCREMENT
   * - first_name
     - VARCHAR(50)
     - NOT NULL
     - Imię
   * - last_name
     - VARCHAR(50)
     - NOT NULL
     - Nazwisko
   * - email
     - VARCHAR(100)
     - NULL
     - Email kontaktu
   * - phone
     - VARCHAR(20)
     - NULL
     - Telefon
   * - position
     - VARCHAR(100)
     - NULL
     - Stanowisko
   * - company_id
     - INT
     - NULL
     - FK -> companies.company_id
   * - assigned_to
     - INT
     - NOT NULL
     - FK -> users.user_id
   * - lead_status
     - ENUM
     - NOT NULL
     - 'new', 'contacted', 'qualified', 'customer', 'lost'
   * - created_at
     - TIMESTAMP
     - NOT NULL
     - Data utworzenia
   * - updated_at
     - TIMESTAMP
     - NOT NULL
     - Data ostatniej aktualizacji

**Tabela: interactions**

.. list-table::
   :header-rows: 1
   :widths: 20 20 10 50

   * - Kolumna
     - Typ danych
     - Null
     - Opis
   * - interaction_id
     - INT
     - NOT NULL
     - PK, AUTO_INCREMENT
   * - contact_id
     - INT
     - NOT NULL
     - FK -> contacts.contact_id
   * - user_id
     - INT
     - NOT NULL
     - FK -> users.user_id
   * - type
     - ENUM
     - NOT NULL
     - 'email', 'phone', 'meeting', 'note'
   * - subject
     - VARCHAR(200)
     - NOT NULL
     - Temat interakcji
   * - description
     - TEXT
     - NULL
     - Szczegółowy opis
   * - interaction_date
     - TIMESTAMP
     - NOT NULL
     - Data i czas interakcji
   * - duration_minutes
     - INT
     - NULL
     - Czas trwania (dla spotkań/rozmów)

**Tabela: tasks**

.. list-table::
   :header-rows: 1
   :widths: 20 20 10 50

   * - Kolumna
     - Typ danych
     - Null
     - Opis
   * - task_id
     - INT
     - NOT NULL
     - PK, AUTO_INCREMENT
   * - title
     - VARCHAR(200)
     - NOT NULL
     - Tytuł zadania
   * - description
     - TEXT
     - NULL
     - Opis zadania
   * - contact_id
     - INT
     - NOT NULL
     - FK -> contacts.contact_id
   * - assigned_to
     - INT
     - NOT NULL
     - FK -> users.user_id
   * - due_date
     - DATE
     - NOT NULL
     - Termin wykonania
   * - priority
     - ENUM
     - NOT NULL
     - 'low', 'medium', 'high'
   * - status
     - ENUM
     - NOT NULL
     - 'pending', 'in_progress', 'completed', 'cancelled'
   * - created_at
     - TIMESTAMP
     - NOT NULL
     - Data utworzenia

**Tabela: tags**

.. list-table::
   :header-rows: 1
   :widths: 20 20 10 50

   * - Kolumna
     - Typ danych
     - Null
     - Opis
   * - tag_id
     - INT
     - NOT NULL
     - PK, AUTO_INCREMENT
   * - name
     - VARCHAR(50)
     - NOT NULL
     - Nazwa tagu (UNIQUE)
   * - color
     - VARCHAR(7)
     - NULL
     - Kolor w formacie HEX

**Tabela: contact_tags** (tabela łącząca)

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Kolumna
     - Typ danych
     - Opis
   * - contact_id
     - INT
     - FK -> contacts.contact_id
   * - tag_id
     - INT
     - FK -> tags.tag_id

Model fizyczny
--------------

Model fizyczny uwzględnia specyficzne wymagania wybranego systemu zarządzania bazą danych (MySQL/PostgreSQL) oraz optymalizacje wydajnościowe.

Indeksy
~~~~~~~

.. code-block:: sql

    -- Indeksy dla tabeli contacts
    CREATE INDEX idx_contacts_company ON contacts(company_id);
    CREATE INDEX idx_contacts_assigned ON contacts(assigned_to);
    CREATE INDEX idx_contacts_status ON contacts(lead_status);
    CREATE INDEX idx_contacts_email ON contacts(email);
    
    -- Indeksy dla tabeli interactions
    CREATE INDEX idx_interactions_contact ON interactions(contact_id);
    CREATE INDEX idx_interactions_user ON interactions(user_id);
    CREATE INDEX idx_interactions_date ON interactions(interaction_date);
    CREATE INDEX idx_interactions_type ON interactions(type);
    
    -- Indeksy dla tabeli tasks
    CREATE INDEX idx_tasks_contact ON tasks(contact_id);
    CREATE INDEX idx_tasks_assigned ON tasks(assigned_to);
    CREATE INDEX idx_tasks_due_date ON tasks(due_date);
    CREATE INDEX idx_tasks_status ON tasks(status);
    
    -- Indeks złożony dla wyszukiwania zadań
    CREATE INDEX idx_tasks_status_due ON tasks(status, due_date);

Ograniczenia (Constraints)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    -- Klucze obce z kaskadowym usuwaniem
    ALTER TABLE contacts
        ADD CONSTRAINT fk_contacts_company 
        FOREIGN KEY (company_id) REFERENCES companies(company_id) 
        ON DELETE SET NULL;
    
    ALTER TABLE interactions
        ADD CONSTRAINT fk_interactions_contact
        FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
        ON DELETE CASCADE;
    
    -- Ograniczenia CHECK
    ALTER TABLE tasks
        ADD CONSTRAINT chk_due_date 
        CHECK (due_date >= CURRENT_DATE);
    
    ALTER TABLE interactions
        ADD CONSTRAINT chk_duration 
        CHECK (duration_minutes >= 0);

Partycjonowanie
~~~~~~~~~~~~~~~

Dla dużych instalacji zaleca się partycjonowanie tabeli interactions według daty:

.. code-block:: sql

    -- Partycjonowanie tabeli interactions (PostgreSQL)
    CREATE TABLE interactions_partitioned (
        LIKE interactions INCLUDING ALL
    ) PARTITION BY RANGE (interaction_date);
    
    -- Tworzenie partycji miesięcznych
    CREATE TABLE interactions_2024_01 
        PARTITION OF interactions_partitioned
        FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

Opis danych przechowywanych w bazie
------------------------------------

System CRM przechowuje kompleksowe informacje o relacjach biznesowych, umożliwiając śledzenie całego cyklu życia klienta.

Kategorie danych
~~~~~~~~~~~~~~~~

**1. Dane osobowe kontaktów**
   - Informacje identyfikacyjne (imię, nazwisko)
   - Dane kontaktowe (email, telefon)
   - Informacje zawodowe (stanowisko, firma)
   - Status w procesie sprzedaży

**2. Dane firmowe**
   - Podstawowe informacje (nazwa, NIP)
   - Dane branżowe i kontaktowe
   - Powiązania z kontaktami

**3. Historia interakcji**
   - Wszystkie formy kontaktu (email, telefon, spotkania)
   - Szczegółowe notatki z rozmów
   - Czas i data każdej interakcji

**4. Zarządzanie zadaniami**
   - Planowane działania
   - Priorytety i terminy
   - Status realizacji

Statystyki danych
~~~~~~~~~~~~~~~~~

System został zaprojektowany z myślą o następujących wolumenach danych:

.. list-table:: Przewidywane wolumeny danych
   :header-rows: 1
   :widths: 30 20 50

   * - Tabela
     - Liczba rekordów
     - Przyrost miesięczny
   * - users
     - 10-50
     - 1-2
   * - companies
     - 100-1,000
     - 10-50
   * - contacts
     - 1,000-10,000
     - 100-500
   * - interactions
     - 10,000-100,000
     - 1,000-5,000
   * - tasks
     - 1,000-5,000
     - 100-300

Prezentacja skryptów wspomagających
------------------------------------

System zawiera dwa główne moduły Python wspomagające pracę z bazą danych CRM bez znajomości SQL.

Moduł raportowania i analizy danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Moduł ``crm_reporter.py`` wykorzystuje biblioteki numpy, pandas i matplotlib do generowania kompleksowych raportów i wizualizacji danych CRM.

**Główna klasa i funkcjonalności:**

.. code-block:: python

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime, timedelta
    
    class CRMReporter:
        """Klasa do generowania raportów z bazy danych CRM"""
        
        def generate_lead_funnel_report(self, start_date=None, end_date=None):
            """
            Generuje raport lejka sprzedażowego z wizualizacją
            """
            query = """
            SELECT lead_status, COUNT(*) as count,
                   AVG(DATEDIFF(NOW(), created_at)) as avg_age_days
            FROM contacts
            GROUP BY lead_status
            ORDER BY FIELD(lead_status, 'new', 'contacted', 
                          'qualified', 'customer', 'lost')
            """
            
            df = pd.read_sql(query, self.connection)
            
            # Obliczenie procentów i wizualizacja
            total = df['count'].sum()
            df['percentage'] = (df['count'] / total * 100).round(2)
            
            # Wykres lejkowy
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#95a5a6']
            
            ax1.barh(df.index, df['count'], color=colors)
            ax1.set_yticklabels(df['lead_status'])
            ax1.set_title('Lejek sprzedażowy')
            
            ax2.pie(df['count'], labels=df['lead_status'], 
                   colors=colors, autopct='%1.1f%%')
            
            return {'data': df, 'figure': fig}

Funkcja ``generate_lead_funnel_report`` analizuje przepływ kontaktów przez kolejne etapy procesu sprzedaży. Wykorzystuje pandas do agregacji danych według statusu leada, oblicza procentowy udział każdego etapu oraz średni czas przebywania kontaktu w systemie. Matplotlib generuje dwa typy wizualizacji: wykres słupkowy poziomy pokazujący liczebność każdego etapu oraz wykres kołowy przedstawiający rozkład procentowy.

**Analiza wydajności użytkowników:**

.. code-block:: python

    def analyze_user_performance(self, period_days=30):
        """
        Analizuje wydajność użytkowników w zadanym okresie
        """
        query = f"""
        SELECT u.username,
               COUNT(DISTINCT c.contact_id) as managed_contacts,
               COUNT(DISTINCT i.interaction_id) as interactions_made,
               COUNT(DISTINCT CASE WHEN t.status = 'completed' 
                    THEN t.task_id END) as tasks_completed,
               COUNT(DISTINCT CASE WHEN c.lead_status = 'customer' 
                    THEN c.contact_id END) as new_customers
        FROM users u
        LEFT JOIN contacts c ON u.user_id = c.assigned_to
        LEFT JOIN interactions i ON u.user_id = i.user_id
        LEFT JOIN tasks t ON u.user_id = t.assigned_to
        WHERE u.is_active = TRUE
        GROUP BY u.user_id
        """
        
        df = pd.read_sql(query, self.connection)
        
        # Obliczenie metryk wydajności
        df['task_completion_rate'] = (
            df['tasks_completed'] / df['tasks_created'].replace(0, 1) * 100
        ).round(2)
        
        # Score wydajności - ważona suma metryk
        df['performance_score'] = (
            df['new_customers'] * 100 +
            df['interactions_made'] * 5 +
            df['task_completion_rate']
        )
        
        return df.sort_values('performance_score', ascending=False)

Metoda agreguje dane o aktywności każdego użytkownika, łącząc informacje z tabel kontaktów, interakcji i zadań. Pandas umożliwia obliczenie złożonych metryk jak wskaźnik ukończonych zadań czy score wydajności będący ważoną sumą różnych wskaźników. Wynik sortowany jest według obliczonego score, co pozwala szybko zidentyfikować najefektywniejszych pracowników.

Moduł wyszukiwania bez znajomości SQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Moduł ``crm_search.py`` udostępnia intuicyjny interfejs do przeszukiwania bazy danych poprzez nazwane parametry zamiast pisania zapytań SQL.

**Wyszukiwanie kontaktów z filtrami:**

.. code-block:: python

    class CRMSearch:
        """Klasa do wyszukiwania w bazie CRM bez SQL"""
        
        def find_contacts(self, first_name=None, last_name=None, 
                         email=None, company_name=None, 
                         lead_status=None, created_after=None,
                         has_interactions=None, limit=100):
            """
            Wyszukuje kontakty według podanych kryteriów
            """
            conditions = []
            params = []
            
            # Budowanie warunków dynamicznie
            if first_name:
                conditions.append("c.first_name LIKE %s")
                params.append(f"%{first_name}%")
                
            if email:
                conditions.append("c.email LIKE %s")
                params.append(f"%{email}%")
                
            if lead_status:
                if isinstance(lead_status, list):
                    placeholders = ','.join(['%s'] * len(lead_status))
                    conditions.append(f"c.lead_status IN ({placeholders})")
                    params.extend(lead_status)
                else:
                    conditions.append("c.lead_status = %s")
                    params.append(lead_status)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            query = f"""
            SELECT c.*, comp.name as company_name,
                   COUNT(i.interaction_id) as interaction_count
            FROM contacts c
            LEFT JOIN companies comp ON c.company_id = comp.company_id
            LEFT JOIN interactions i ON c.contact_id = i.contact_id
            WHERE {where_clause}
            GROUP BY c.contact_id
            LIMIT %s
            """
            
            params.append(limit)
            self.cursor.execute(query, params)
            return self.cursor.fetchall()

Funkcja umożliwia wyszukiwanie kontaktów używając dowolnej kombinacji kryteriów. System dynamicznie buduje zapytanie SQL na podstawie przekazanych parametrów - dodaje tylko te warunki WHERE, dla których użytkownik podał wartości. Obsługuje różne typy wyszukiwania: częściowe dopasowanie tekstu (LIKE), dokładne dopasowanie, wyszukiwanie w zakresie dat oraz sprawdzanie przynależności do listy wartości.

**Wyszukiwanie zadań z zaawansowanymi filtrami:**

.. code-block:: python

    def find_tasks(self, status=None, priority=None,
                   assigned_to_username=None, overdue_only=False,
                   due_date_from=None, due_date_to=None):
        """
        Wyszukuje zadania z dodatkowymi informacjami kontekstowymi
        """
        conditions = []
        
        if overdue_only:
            conditions.append(
                "t.due_date < CURDATE() AND t.status != 'completed'"
            )
            
        query = f"""
        SELECT t.*, 
               CONCAT(c.first_name, ' ', c.last_name) as contact_name,
               u.username as assigned_username,
               CASE 
                   WHEN t.due_date < CURDATE() AND t.status != 'completed' 
                   THEN DATEDIFF(CURDATE(), t.due_date)
                   ELSE 0
               END as days_overdue
        FROM tasks t
        JOIN contacts c ON t.contact_id = c.contact_id
        JOIN users u ON t.assigned_to = u.user_id
        WHERE {where_clause}
        ORDER BY t.due_date ASC
        """

Metoda łączy dane z wielu tabel, aby dostarczyć pełny kontekst każdego zadania. Automatycznie oblicza dodatkowe metryki jak liczba dni po terminie dla zaległych zadań. Szczególnie użyteczna jest flaga ``overdue_only``, która pozwala szybko znaleźć wszystkie przeterminowane zadania bez konieczności ręcznego porównywania dat.

**Uniwersalne przeszukiwanie:**

.. code-block:: python

    def quick_search(self, search_term, limit=20):
        """
        Szybkie wyszukiwanie we wszystkich tabelach
        """
        results = {}
        
        # Równoległe przeszukiwanie wszystkich typów danych
        results['contacts'] = self.find_contacts(
            first_name=search_term, last_name=search_term, 
            email=search_term, limit=limit
        )
        
        results['companies'] = self.find_companies(
            name=search_term, limit=limit
        )
        
        results['tasks'] = self.find_tasks(
            title_contains=search_term, limit=limit
        )
        
        return results

Funkcja ``quick_search`` implementuje wyszukiwanie globalne - jedna fraza jest szukana we wszystkich istotnych polach wszystkich tabel. Zwraca pogrupowane wyniki, co pozwala użytkownikowi szybko znaleźć poszukiwane informacje niezależnie od tego, czy jest to kontakt, firma czy zadanie.

Podsumowanie
~~~~~~~~~~~~

Przedstawione moduły znacząco ułatwiają pracę z bazą danych CRM:

1. **Moduł raportowania** automatyzuje generowanie złożonych analiz i wizualizacji, wykorzystując możliwości bibliotek pandas i matplotlib do przetwarzania danych i tworzenia profesjonalnych wykresów.

2. **Moduł wyszukiwania** eliminuje barierę techniczną, umożliwiając osobom nieznającym SQL wykonywanie zaawansowanych zapytań poprzez prosty interfejs pythonowy z nazwanymi parametrami.

Oba moduły zaprojektowano z myślą o łatwości użycia, wydajności i możliwości rozbudowy o dodatkowe funkcjonalności.

Podsumowanie
------------

Zaprojektowana baza danych CRM zapewnia:

* **Skalowalność** - struktura pozwala na obsługę od kilkuset do kilkudziesięciu tysięcy kontaktów
* **Integralność danych** - klucze obce i ograniczenia zapewniają spójność
* **Wydajność** - przemyślane indeksy przyspieszają typowe zapytania
* **Łatwość raportowania** - widoki i procedury ułatwiają generowanie statystyk
* **Audytowalność** - śledzenie historii zmian i interakcji

System jest gotowy do implementacji i może być łatwo rozszerzony o dodatkowe funkcjonalności, takie jak integracja z systemami mailingowymi, zaawansowane raportowanie czy automatyzacja procesów sprzedażowych.
