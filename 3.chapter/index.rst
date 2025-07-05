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
