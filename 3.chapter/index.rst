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

System zawiera zestaw skryptów SQL i procedur składowanych wspomagających zarządzanie danymi i generowanie raportów.

Skrypt tworzenia bazy danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

    -- create_crm_database.sql
    -- Skrypt tworzący kompletną strukturę bazy danych CRM
    
    CREATE DATABASE IF NOT EXISTS crm_system
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci;
    
    USE crm_system;
    
    -- Włączenie trybu strict
    SET sql_mode = 'STRICT_ALL_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE';

Procedury składowane
~~~~~~~~~~~~~~~~~~~~

**1. Procedura dodawania nowego kontaktu z automatycznym tagowaniem**

.. code-block:: sql

    DELIMITER //
    
    CREATE PROCEDURE sp_add_contact(
        IN p_first_name VARCHAR(50),
        IN p_last_name VARCHAR(50),
        IN p_email VARCHAR(100),
        IN p_company_id INT,
        IN p_assigned_to INT,
        OUT p_contact_id INT
    )
    BEGIN
        DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            ROLLBACK;
            RESIGNAL;
        END;
        
        START TRANSACTION;
        
        -- Wstawienie kontaktu
        INSERT INTO contacts (
            first_name, last_name, email, 
            company_id, assigned_to, lead_status
        ) VALUES (
            p_first_name, p_last_name, p_email,
            p_company_id, p_assigned_to, 'new'
        );
        
        SET p_contact_id = LAST_INSERT_ID();
        
        -- Automatyczne tagowanie na podstawie domeny email
        IF p_email LIKE '%@gmail.com' OR p_email LIKE '%@outlook.com' THEN
            INSERT INTO contact_tags (contact_id, tag_id)
            SELECT p_contact_id, tag_id 
            FROM tags WHERE name = 'B2C';
        END IF;
        
        COMMIT;
    END //
    
    DELIMITER ;

**2. Funkcja obliczająca wartość klienta**

.. code-block:: sql

    DELIMITER //
    
    CREATE FUNCTION fn_calculate_contact_value(p_contact_id INT)
    RETURNS DECIMAL(10,2)
    READS SQL DATA
    DETERMINISTIC
    BEGIN
        DECLARE v_interaction_count INT;
        DECLARE v_task_completion_rate DECIMAL(5,2);
        DECLARE v_days_since_creation INT;
        DECLARE v_value DECIMAL(10,2);
        
        -- Liczba interakcji
        SELECT COUNT(*) INTO v_interaction_count
        FROM interactions
        WHERE contact_id = p_contact_id;
        
        -- Wskaźnik ukończonych zadań
        SELECT 
            COALESCE(
                100.0 * SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / 
                NULLIF(COUNT(*), 0), 
                0
            )
        INTO v_task_completion_rate
        FROM tasks
        WHERE contact_id = p_contact_id;
        
        -- Dni od utworzenia
        SELECT DATEDIFF(NOW(), created_at)
        INTO v_days_since_creation
        FROM contacts
        WHERE contact_id = p_contact_id;
        
        -- Wzór na wartość klienta
        SET v_value = (v_interaction_count * 10) + 
                      (v_task_completion_rate * 5) + 
                      (LEAST(v_days_since_creation, 365) * 0.5);
        
        RETURN v_value;
    END //
    
    DELIMITER ;

Widoki (Views)
~~~~~~~~~~~~~~

**1. Widok aktywnych leadów**

.. code-block:: sql

    CREATE OR REPLACE VIEW v_active_leads AS
    SELECT 
        c.contact_id,
        CONCAT(c.first_name, ' ', c.last_name) AS full_name,
        c.email,
        c.lead_status,
        comp.name AS company_name,
        u.username AS assigned_to_user,
        COUNT(DISTINCT i.interaction_id) AS interaction_count,
        MAX(i.interaction_date) AS last_interaction,
        COUNT(DISTINCT t.task_id) AS pending_tasks
    FROM contacts c
    LEFT JOIN companies comp ON c.company_id = comp.company_id
    LEFT JOIN users u ON c.assigned_to = u.user_id
    LEFT JOIN interactions i ON c.contact_id = i.contact_id
    LEFT JOIN tasks t ON c.contact_id = t.contact_id 
        AND t.status IN ('pending', 'in_progress')
    WHERE c.lead_status IN ('new', 'contacted', 'qualified')
    GROUP BY c.contact_id;

**2. Widok podsumowania użytkowników**

.. code-block:: sql

    CREATE OR REPLACE VIEW v_user_performance AS
    SELECT 
        u.user_id,
        u.username,
        COUNT(DISTINCT c.contact_id) AS total_contacts,
        COUNT(DISTINCT i.interaction_id) AS total_interactions,
        COUNT(DISTINCT t.task_id) AS total_tasks,
        SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
        AVG(CASE 
            WHEN t.status = 'completed' 
            THEN DATEDIFF(t.updated_at, t.created_at) 
            ELSE NULL 
        END) AS avg_task_completion_days
    FROM users u
    LEFT JOIN contacts c ON u.user_id = c.assigned_to
    LEFT JOIN interactions i ON u.user_id = i.user_id
    LEFT JOIN tasks t ON u.user_id = t.assigned_to
    WHERE u.is_active = TRUE
    GROUP BY u.user_id;

Triggery
~~~~~~~~

**Trigger aktualizujący timestamp modyfikacji**

.. code-block:: sql

    DELIMITER //
    
    CREATE TRIGGER trg_contacts_update_timestamp
    BEFORE UPDATE ON contacts
    FOR EACH ROW
    BEGIN
        SET NEW.updated_at = CURRENT_TIMESTAMP;
        
        -- Automatyczna zmiana statusu przy pierwszym kontakcie
        IF OLD.lead_status = 'new' AND NEW.lead_status = 'new' THEN
            IF EXISTS (
                SELECT 1 FROM interactions 
                WHERE contact_id = NEW.contact_id
            ) THEN
                SET NEW.lead_status = 'contacted';
            END IF;
        END IF;
    END //
    
    DELIMITER ;

Skrypty administracyjne
~~~~~~~~~~~~~~~~~~~~~~~

**1. Skrypt czyszczenia starych danych**

.. code-block:: sql

    -- cleanup_old_data.sql
    -- Usuwa interakcje starsze niż 2 lata
    
    DELETE FROM interactions
    WHERE interaction_date < DATE_SUB(NOW(), INTERVAL 2 YEAR)
    AND contact_id IN (
        SELECT contact_id FROM contacts 
        WHERE lead_status = 'lost'
    );
    
    -- Archiwizacja nieaktywnych kontaktów
    INSERT INTO contacts_archive
    SELECT * FROM contacts
    WHERE updated_at < DATE_SUB(NOW(), INTERVAL 1 YEAR)
    AND lead_status IN ('lost', 'unqualified');

**2. Skrypt generowania raportów**

.. code-block:: sql

    -- monthly_report.sql
    -- Generuje miesięczny raport aktywności
    
    SELECT 
        DATE_FORMAT(NOW(), '%Y-%m') AS report_month,
        COUNT(DISTINCT c.contact_id) AS new_contacts,
        COUNT(DISTINCT i.interaction_id) AS total_interactions,
        COUNT(DISTINCT CASE 
            WHEN i.type = 'meeting' THEN i.interaction_id 
        END) AS meetings_held,
        COUNT(DISTINCT CASE 
            WHEN t.status = 'completed' THEN t.task_id 
        END) AS tasks_completed,
        COUNT(DISTINCT CASE 
            WHEN c.lead_status = 'customer' THEN c.contact_id 
        END) AS new_customers
    FROM contacts c
    LEFT JOIN interactions i ON c.contact_id = i.contact_id
        AND MONTH(i.interaction_date) = MONTH(NOW())
        AND YEAR(i.interaction_date) = YEAR(NOW())
    LEFT JOIN tasks t ON c.contact_id = t.contact_id
        AND MONTH(t.updated_at) = MONTH(NOW())
        AND YEAR(t.updated_at) = YEAR(NOW())
    WHERE MONTH(c.created_at) = MONTH(NOW())
        AND YEAR(c.created_at) = YEAR(NOW());

Dokumentacja API bazy danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

System udostępnia zestaw procedur składowanych stanowiących API dla aplikacji:

.. list-table:: API procedur składowanych
   :header-rows: 1
   :widths: 30 40 30

   * - Procedura
     - Opis
     - Parametry
   * - sp_add_contact
     - Dodaje nowy kontakt
     - first_name, last_name, email, company_id, assigned_to
   * - sp_log_interaction
     - Rejestruje interakcję
     - contact_id, user_id, type, subject, description
   * - sp_create_task
     - Tworzy nowe zadanie
     - title, contact_id, assigned_to, due_date, priority
   * - sp_update_lead_status
     - Aktualizuje status leada
     - contact_id, new_status, reason
   * - sp_get_user_dashboard
     - Pobiera dane do dashboardu
     - user_id, date_from, date_to

Podsumowanie
------------

Zaprojektowana baza danych CRM zapewnia:

* **Skalowalność** - struktura pozwala na obsługę od kilkuset do kilkudziesięciu tysięcy kontaktów
* **Integralność danych** - klucze obce i ograniczenia zapewniają spójność
* **Wydajność** - przemyślane indeksy przyspieszają typowe zapytania
* **Łatwość raportowania** - widoki i procedury ułatwiają generowanie statystyk
* **Audytowalność** - śledzenie historii zmian i interakcji

System jest gotowy do implementacji i może być łatwo rozszerzony o dodatkowe funkcjonalności, takie jak integracja z systemami mailingowymi, zaawansowane raportowanie czy automatyzacja procesów sprzedażowych.
