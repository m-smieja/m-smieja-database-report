Analiza bazy danych oraz optymalizacja zapytań
===============================================

Ten rozdział przedstawia kompleksową analizę wydajności bazy danych CRM oraz strategie optymalizacji zapytań. Skupiamy się na praktycznych aspektach utrzymania wysokiej wydajności systemu oraz mechanizmach zapewniających bezpieczeństwo danych.

Wybór systemu zarządzania bazą danych
--------------------------------------

Dla implementacji systemu CRM wybrano **PostgreSQL 15** ze względu na:

* **Zaawansowane możliwości indeksowania** - wsparcie dla indeksów B-tree, Hash, GiST, SP-GiST, GIN oraz BRIN
* **ACID compliance** - pełna zgodność z wymogami transakcyjności
* **Wsparcie dla JSON/JSONB** - możliwość przechowywania danych semi-strukturalnych
* **Partycjonowanie tabel** - natywne wsparcie dla partycjonowania deklaratywnego
* **Rozbudowane mechanizmy backup** - pg_dump, pg_basebackup, PITR
* **Replikacja** - streaming replication, logical replication

Analiza wydajności zapytań
---------------------------

Identyfikacja wolnych zapytań
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PostgreSQL oferuje kilka narzędzi do analizy wydajności:

**1. Włączenie logowania wolnych zapytań:**

.. code-block:: sql

    -- postgresql.conf
    log_min_duration_statement = 100  -- loguj zapytania > 100ms
    log_statement = 'mod'             -- loguj DML
    log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '

**2. Wykorzystanie pg_stat_statements:**

.. code-block:: sql

    -- Instalacja rozszerzenia
    CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
    
    -- Analiza najwolniejszych zapytań
    SELECT 
        round(total_exec_time::numeric, 2) AS total_time_ms,
        calls,
        round(mean_exec_time::numeric, 2) AS mean_time_ms,
        round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS percentage,
        query
    FROM pg_stat_statements
    ORDER BY total_exec_time DESC
    LIMIT 10;

**3. Analiza aktualnie wykonywanych zapytań:**

.. code-block:: sql

    SELECT 
        pid,
        now() - pg_stat_activity.query_start AS duration,
        query,
        state
    FROM pg_stat_activity
    WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
    AND state = 'active';

Analiza planów wykonania
~~~~~~~~~~~~~~~~~~~~~~~~

**Przykład analizy złożonego zapytania:**

.. code-block:: sql

    EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
    SELECT 
        c.contact_id,
        c.first_name,
        c.last_name,
        comp.name as company_name,
        COUNT(DISTINCT i.interaction_id) as interaction_count,
        MAX(i.interaction_date) as last_interaction
    FROM contacts c
    LEFT JOIN companies comp ON c.company_id = comp.company_id
    LEFT JOIN interactions i ON c.contact_id = i.contact_id
    WHERE c.lead_status = 'qualified'
    AND i.interaction_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY c.contact_id, c.first_name, c.last_name, comp.name
    ORDER BY interaction_count DESC
    LIMIT 20;

**Analiza wyników EXPLAIN:**

.. code-block:: text

    Limit (cost=1245.67..1245.72 rows=20) (actual time=45.123..45.125 rows=20)
      -> Sort (cost=1245.67..1248.17 rows=1000) (actual time=45.122..45.123 rows=20)
            Sort Key: (count(DISTINCT i.interaction_id)) DESC
            -> GroupAggregate (cost=0.85..1220.35 rows=1000) (actual time=0.054..44.897 rows=523)
                  -> Nested Loop Left Join (cost=0.85..1170.35 rows=5000)
                        -> Nested Loop Left Join (cost=0.42..420.35 rows=1000)
                              -> Index Scan on contacts c (cost=0.29..320.35 rows=1000)
                                    Index Cond: (lead_status = 'qualified'::text)
                              -> Index Scan on companies comp (cost=0.13..0.20 rows=1)
                                    Index Cond: (company_id = c.company_id)
                        -> Index Scan on interactions i (cost=0.43..0.70 rows=5)
                              Index Cond: (contact_id = c.contact_id)
                              Filter: (interaction_date >= (CURRENT_DATE - '30 days'))

Optymalizacja zapytań
---------------------

Strategie indeksowania
~~~~~~~~~~~~~~~~~~~~~~

**1. Indeksy podstawowe (już zaimplementowane):**

.. code-block:: sql

    -- Indeksy pojedyncze dla kluczy obcych
    CREATE INDEX idx_contacts_company ON contacts(company_id);
    CREATE INDEX idx_contacts_assigned ON contacts(assigned_to);
    CREATE INDEX idx_interactions_contact ON interactions(contact_id);
    CREATE INDEX idx_interactions_user ON interactions(user_id);

**2. Indeksy złożone dla częstych zapytań:**

.. code-block:: sql

    -- Indeks dla filtrowania kontaktów po statusie i dacie
    CREATE INDEX idx_contacts_status_created 
    ON contacts(lead_status, created_at DESC)
    WHERE lead_status IN ('new', 'contacted', 'qualified');
    
    -- Indeks dla analizy interakcji w czasie
    CREATE INDEX idx_interactions_date_type 
    ON interactions(interaction_date DESC, type)
    INCLUDE (contact_id, user_id);
    
    -- Indeks częściowy dla aktywnych zadań
    CREATE INDEX idx_tasks_active 
    ON tasks(assigned_to, due_date)
    WHERE status IN ('pending', 'in_progress');

**3. Indeksy funkcyjne:**

.. code-block:: sql

    -- Indeks dla wyszukiwania case-insensitive
    CREATE INDEX idx_contacts_email_lower 
    ON contacts(LOWER(email));
    
    -- Indeks dla wyszukiwania pełnotekstowego
    CREATE INDEX idx_contacts_fulltext 
    ON contacts USING gin(
        to_tsvector('polish', 
            coalesce(first_name, '') || ' ' || 
            coalesce(last_name, '') || ' ' || 
            coalesce(email, '')
        )
    );

Optymalizacja zapytań agregujących
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Wykorzystanie Materialized Views:**

.. code-block:: sql

    -- Widok zmaterializowany dla statystyk użytkowników
    CREATE MATERIALIZED VIEW mv_user_stats AS
    SELECT 
        u.user_id,
        u.username,
        COUNT(DISTINCT c.contact_id) as total_contacts,
        COUNT(DISTINCT CASE 
            WHEN c.lead_status = 'customer' 
            THEN c.contact_id 
        END) as customers,
        COUNT(DISTINCT i.interaction_id) as total_interactions,
        COUNT(DISTINCT CASE 
            WHEN i.type = 'meeting' 
            THEN i.interaction_id 
        END) as meetings,
        AVG(CASE 
            WHEN t.status = 'completed' 
            THEN EXTRACT(EPOCH FROM (t.updated_at - t.created_at))/86400 
        END) as avg_task_completion_days
    FROM users u
    LEFT JOIN contacts c ON u.user_id = c.assigned_to
    LEFT JOIN interactions i ON u.user_id = i.user_id
    LEFT JOIN tasks t ON u.user_id = t.assigned_to
    WHERE u.is_active = TRUE
    GROUP BY u.user_id;
    
    -- Indeks na widoku
    CREATE UNIQUE INDEX idx_mv_user_stats_user_id ON mv_user_stats(user_id);
    
    -- Automatyczne odświeżanie co godzinę
    CREATE OR REPLACE FUNCTION refresh_user_stats()
    RETURNS void AS $$
    BEGIN
        REFRESH MATERIALIZED VIEW CONCURRENTLY mv_user_stats;
    END;
    $$ LANGUAGE plpgsql;

**2. Optymalizacja podzapytań:**

.. code-block:: sql

    -- Zamiast podzapytania skorelowanego
    -- WOLNE:
    SELECT c.*,
           (SELECT COUNT(*) FROM interactions 
            WHERE contact_id = c.contact_id) as int_count
    FROM contacts c;
    
    -- SZYBKIE - użycie JOIN z agregacją:
    SELECT c.*, COALESCE(i.int_count, 0) as int_count
    FROM contacts c
    LEFT JOIN (
        SELECT contact_id, COUNT(*) as int_count
        FROM interactions
        GROUP BY contact_id
    ) i ON c.contact_id = i.contact_id;

Partycjonowanie danych
~~~~~~~~~~~~~~~~~~~~~~

**Implementacja partycjonowania dla tabeli interactions:**

.. code-block:: sql

    -- Utworzenie tabeli partycjonowanej
    CREATE TABLE interactions_partitioned (
        LIKE interactions INCLUDING ALL
    ) PARTITION BY RANGE (interaction_date);
    
    -- Tworzenie partycji miesięcznych
    CREATE TABLE interactions_2024_01 
        PARTITION OF interactions_partitioned
        FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
        
    CREATE TABLE interactions_2024_02 
        PARTITION OF interactions_partitioned
        FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
    
    -- Automatyczne tworzenie partycji
    CREATE OR REPLACE FUNCTION create_monthly_partition()
    RETURNS void AS $$
    DECLARE
        start_date date;
        end_date date;
        partition_name text;
    BEGIN
        start_date := date_trunc('month', CURRENT_DATE);
        end_date := start_date + interval '1 month';
        partition_name := 'interactions_' || to_char(start_date, 'YYYY_MM');
        
        EXECUTE format('CREATE TABLE IF NOT EXISTS %I 
                       PARTITION OF interactions_partitioned 
                       FOR VALUES FROM (%L) TO (%L)',
                       partition_name, start_date, end_date);
    END;
    $$ LANGUAGE plpgsql;

Monitoring wydajności
---------------------

Kluczowe metryki do monitorowania
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Wykorzystanie indeksów:**

.. code-block:: sql

    -- Nieużywane indeksy
    SELECT 
        schemaname,
        tablename,
        indexname,
        idx_scan,
        idx_tup_read,
        idx_tup_fetch,
        pg_size_pretty(pg_relation_size(indexrelid)) as index_size
    FROM pg_stat_user_indexes
    WHERE idx_scan = 0
    AND indexrelid NOT IN (
        SELECT conindid FROM pg_constraint WHERE contype = 'p'
    )
    ORDER BY pg_relation_size(indexrelid) DESC;

**2. Cache hit ratio:**

.. code-block:: sql

    -- Powinno być > 99% dla produkcyjnych baz
    SELECT 
        sum(heap_blks_read) as heap_read,
        sum(heap_blks_hit) as heap_hit,
        sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0) as ratio
    FROM pg_statio_user_tables;

**3. Blokady i deadlocki:**

.. code-block:: sql

    -- Monitoring blokad
    SELECT 
        blocked_locks.pid AS blocked_pid,
        blocked_activity.usename AS blocked_user,
        blocking_locks.pid AS blocking_pid,
        blocking_activity.usename AS blocking_user,
        blocked_activity.query AS blocked_statement,
        blocking_activity.query AS blocking_statement
    FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_stat_activity blocked_activity 
        ON blocked_activity.pid = blocked_locks.pid
    JOIN pg_catalog.pg_locks blocking_locks 
        ON blocking_locks.locktype = blocked_locks.locktype
        AND blocking_locks.relation = blocked_locks.relation
        AND blocking_locks.pid != blocked_locks.pid
    JOIN pg_catalog.pg_stat_activity blocking_activity 
        ON blocking_activity.pid = blocking_locks.pid
    WHERE NOT blocked_locks.granted;

Strategia backup i recovery
---------------------------

Mechanizmy wbudowane PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. pg_dump - logiczne kopie zapasowe:**

.. code-block:: bash

    # Pełny backup bazy
    pg_dump -h localhost -U postgres -d crm_system \
            -f /backup/crm_$(date +%Y%m%d_%H%M%S).sql \
            --verbose --format=custom --compress=9
    
    # Backup tylko schematu
    pg_dump -h localhost -U postgres -d crm_system \
            --schema-only -f /backup/crm_schema.sql
    
    # Backup tylko danych
    pg_dump -h localhost -U postgres -d crm_system \
            --data-only -f /backup/crm_data.sql

**2. pg_basebackup - fizyczne kopie zapasowe:**

.. code-block:: bash

    # Backup całego klastra
    pg_basebackup -h localhost -U replicator \
                  -D /backup/base/$(date +%Y%m%d) \
                  -Ft -z -Xs -P -v
    
    # Z kompresją i progresem
    pg_basebackup -h localhost -U replicator \
                  -D /backup/base/latest \
                  -Ft -z -Xs -P -v \
                  --checkpoint=fast \
                  --write-recovery-conf

**3. PITR (Point-In-Time Recovery):**

.. code-block:: sql

    -- postgresql.conf
    wal_level = replica
    archive_mode = on
    archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'
    archive_timeout = 300

.. code-block:: bash

    # Restore do konkretnego momentu
    pg_ctl stop -D /var/lib/postgresql/data
    
    # Przywrócenie base backup
    rm -rf /var/lib/postgresql/data/*
    tar -xzf /backup/base/20240315/base.tar.gz -C /var/lib/postgresql/data/
    
    # Konfiguracja recovery
    cat > /var/lib/postgresql/data/recovery.signal
    echo "restore_command = 'cp /archive/%f %p'" >> /var/lib/postgresql/data/postgresql.auto.conf
    echo "recovery_target_time = '2024-03-15 14:30:00'" >> /var/lib/postgresql/data/postgresql.auto.conf
    
    pg_ctl start -D /var/lib/postgresql/data

Integracja z narzędziami zewnętrznymi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. pgBackRest - zaawansowane zarządzanie kopiami:**

.. code-block:: ini

    # /etc/pgbackrest/pgbackrest.conf
    [global]
    repo1-path=/backup/pgbackrest
    repo1-retention-full=2
    repo1-retention-diff=4
    repo1-retention-archive=4
    log-level-console=info
    log-level-file=debug
    compress-type=lz4
    compress-level=3
    
    [crm_system]
    pg1-path=/var/lib/postgresql/15/main
    pg1-port=5432
    pg1-user=postgres

.. code-block:: bash

    # Pełny backup
    pgbackrest --stanza=crm_system --type=full backup
    
    # Backup różnicowy
    pgbackrest --stanza=crm_system --type=diff backup
    
    # Backup przyrostowy
    pgbackrest --stanza=crm_system --type=incr backup
    
    # Restore
    pgbackrest --stanza=crm_system --delta restore

**2. Barman - backup i disaster recovery:**

.. code-block:: ini

    # /etc/barman.d/crm_system.conf
    [crm_system]
    description = "CRM Production Database"
    conninfo = host=localhost user=barman dbname=crm_system
    streaming_conninfo = host=localhost user=streaming_barman
    backup_method = postgres
    streaming_archiver = on
    slot_name = barman
    retention_policy = RECOVERY WINDOW OF 7 DAYS

.. code-block:: bash

    # Konfiguracja i test
    barman check crm_system
    barman switch-wal crm_system
    
    # Wykonanie backupu
    barman backup crm_system
    
    # Lista backupów
    barman list-backup crm_system
    
    # Restore do punktu w czasie
    barman recover crm_system latest \
           /var/lib/postgresql/15/restored \
           --target-time "2024-03-15 14:30:00"

Plan testowania recovery
~~~~~~~~~~~~~~~~~~~~~~~~

**1. Procedura testowa:**

.. code-block:: bash

    #!/bin/bash
    # test_recovery.sh
    
    # 1. Utworzenie testowej bazy
    createdb crm_test
    
    # 2. Restore ostatniego backupu
    pg_restore -d crm_test /backup/crm_latest.dump
    
    # 3. Weryfikacja integralności
    psql -d crm_test -c "
        SELECT COUNT(*) FROM contacts;
        SELECT COUNT(*) FROM interactions;
        SELECT COUNT(*) FROM tasks;
    "
    
    # 4. Test aplikacji
    python test_crm_connection.py --database=crm_test
    
    # 5. Cleanup
    dropdb crm_test

**2. Harmonogram testów:**

.. list-table:: Plan testowania procedur recovery
   :header-rows: 1
   :widths: 20 30 30 20

   * - Typ testu
     - Częstotliwość
     - Zakres
     - Odpowiedzialny
   * - pg_dump restore
     - Co tydzień
     - Pełna baza
     - DBA
   * - PITR test
     - Co miesiąc
     - Restore do punktu
     - DBA + DevOps
   * - Disaster recovery
     - Co kwartał
     - Pełny scenariusz
     - Cały zespół
   * - Backup integrity
     - Codziennie
     - Sprawdzenie plików
     - Automat

Kluczowe wnioski
----------------

**Mechanizmy wbudowane** PostgreSQL, takie jak ``pg_dump``, ``pg_basebackup`` czy PITR, oferują solidne podstawy dla większości scenariuszy backup i recovery.

**W środowiskach produkcyjnych** o wysokich wymaganiach dotyczących dostępności i niezawodności, integracja z dedykowanymi narzędziami takimi jak pgBackRest czy Barman staje się niezbędna.

Najważniejsze zalecenia
-----------------------

.. warning::
   
   Kluczowym elementem każdej strategii backup jest regularne testowanie procedur odzyskiwania danych. Kopie zapasowe mają wartość tylko wtedy, gdy można z nich skutecznie odzyskać dane w sytuacji kryzysowej.

**Kompleksowa strategia backup** powinna obejmować:

1. **Tworzenie kopii zapasowych**
   
   * Automatyzacja procesów backup
   * Różne poziomy granularności (pełne, różnicowe, przyrostowe)
   * Przechowywanie kopii w różnych lokalizacjach

2. **Regularne testy restore**
   
   * Zautomatyzowane testy integralności
   * Symulacje awarii i procedur recovery
   * Dokumentowanie czasów odtwarzania (RTO)

3. **Dokumentację procedur**
   
   * Szczegółowe instrukcje krok po kroku
   * Diagramy przepływu dla różnych scenariuszy
   * Kontakty awaryjne i eskalacje

4. **Szkolenie personelu**
   
   * Regularne warsztaty z procedur recovery
   * Symulacje rzeczywistych awarii
   * Certyfikacja wewnętrzna dla administratorów

Podsumowanie
------------

Przedstawiona analiza i optymalizacja bazy danych CRM w PostgreSQL pokazuje, że kluczem do utrzymania wysokiej wydajności jest:

* **Proaktywny monitoring** - identyfikacja problemów zanim wpłyną na użytkowników
* **Przemyślane indeksowanie** - balans między wydajnością zapytań a kosztem utrzymania indeksów
* **Regularna maintenance** - VACUUM, ANALYZE, reindeksacja
* **Solidna strategia backup** - wielopoziomowa ochrona z regularnym testowaniem

System CRM z odpowiednio zoptymalizowaną bazą PostgreSQL jest w stanie obsłużyć dziesiątki tysięcy kontaktów z czasami odpowiedzi poniżej 100ms dla większości operacji.
