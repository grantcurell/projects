# Spark + Trino canonical schema enforcement demo

This is an all-local, free/open-source implementation using Trino + Spark.

Trino is the open-source SQL query engine that Starburst is built on. The same architectural pattern can be implemented with Starburst Enterprise or Starburst Galaxy, but this local demo intentionally avoids requiring a Starburst account, cloud service, paid tier, or enterprise image access.

## Demo objectives

1. Show Trino reading from two different source systems with different source schemas.
2. Show Spark consuming the federated Trino query.
3. Show Spark enforcing a central canonical customer schema.
4. Show accepted records landing in `governed.public.customer_standard`.
5. Show rejected records landing in `governed.public.customer_rejects` with rejection reasons.
6. Show Trino querying the raw sources and governed outputs.
7. Show the same governed accepted/rejected datasets published to Iceberg tables for lakehouse-style querying.

## Architecture

```text
Ubuntu host
  |
  +-- Docker Compose network: spark-trino-demo-net
        |
        +-- Trino single-node coordinator
        |     +-- catalog: crm      -> PostgreSQL CRM source
        |     +-- catalog: webapp   -> MySQL WebApp source
        |     +-- catalog: governed -> PostgreSQL governed output
        |     +-- catalog: iceberg  -> Nessie catalog + local Parquet warehouse
        |
        +-- Nessie (Iceberg catalog service)
        +-- Spark standalone master
        +-- Spark standalone worker
        +-- Spark submit container
        |
        +-- PostgreSQL source database: CRM schema
        +-- MySQL source database: WebApp schema
        +-- PostgreSQL governed database: canonical accepted and rejected tables
```

```text
CRM PostgreSQL source ─┐
                       ├─ Trino federated SQL ─ Spark validation ─ governed PostgreSQL output
WebApp MySQL source ───┘                                      │
                                                              ├─ Trino CTAS sync ─ Iceberg tables (Parquet)
                                                              └─ Trino SQL consumption (Postgres + Iceberg)
```

## Project layout

```text
Starburst and Spark Testing/
  .env                          # image tags, ports, demo credentials
  docker-compose.yml            # Trino, Spark, and database services
  Makefile                      # make up, pipeline, demo, assert, ...

  contracts/
    customer_canonical_schema.json   # central schema contract + validation rules

  docker/init/
    postgres-crm/01-create-crm-source.sql       # CRM seed data (6 rows)
    mysql-webapp/01-create-webapp-source.sql    # WebApp seed data (7 rows)
    postgres-governed/01-create-governed-schema.sql  # accepted + reject tables

  jobs/
    enforce_customer_schema.py    # Spark: read Trino, validate, write governed tables

  data/
    iceberg/warehouse/            # local Iceberg Parquet files (created on make up)

  trino/etc/
    config.properties             # coordinator settings
    catalog/crm.properties        # Postgres CRM connector
    catalog/webapp.properties     # MySQL WebApp connector
    catalog/governed.properties   # Postgres governed connector
    catalog/iceberg.properties    # Nessie-backed Iceberg connector

  scripts/                        # numbered setup, smoke, pipeline, demo scripts
                                  # 07b_sync_iceberg_governed.sh publishes Postgres -> Iceberg
```

## Default images and versions

Configured in `.env`:

| Component | Image |
| --------- | ----- |
| Trino | `trinodb/trino:481` |
| Nessie | `ghcr.io/projectnessie/nessie:0.100.0` |
| Spark | `apache/spark:4.1.2` |
| PostgreSQL | `postgres:16` |
| MySQL | `mysql:8.4` |
| Trino CLI / JDBC | `481` |
| PostgreSQL JDBC | `42.7.11` |

## Source schemas: CRM vs WebApp

The demo intentionally uses two different source designs. Trino reads each as-is; Spark normalizes them into one canonical shape.

| Canonical field | CRM (`crm.public.customers`) | WebApp (`webapp.appdb.user_profiles`) |
| --------------- | ---------------------------- | ------------------------------------- |
| `customer_id` | `customer_id` (string) | `id` (int) → prefixed `app-` in Spark |
| `email` | `email` | `email_address` |
| `created_at` | `created_at` (timestamp) | `signup_epoch` (unix seconds) |
| `country` | `country` | `country_code` |
| `status` | `status` (string) | `is_active` (0/1/9 → ACTIVE/INACTIVE) |

Seed SQL files plant both valid and invalid rows. Invalid values are rejected against `contracts/customer_canonical_schema.json`, not because Trino cannot read the sources.

**CRM rejects (4):** bad email, missing email, missing `created_at`, invalid status (`PENDING`).

**WebApp rejects (5):** bad email, missing email, missing timestamp, country `USA` (3 letters), `is_active = 9` (unmapped status).

## Canonical customer schema

The central schema contract lives at:

```text
contracts/customer_canonical_schema.json
```

Spark enforces column names, types, and row-level rules defined there (email regex, 2-letter country, status enum, etc.).

The accepted output table is:

```text
governed.public.customer_standard
```

The rejected output table is:

```text
governed.public.customer_rejects
```

`docker/init/postgres-governed/01-create-governed-schema.sql` adds Postgres `CHECK` constraints on the accepted table as a second line of defense.

After each pipeline run, `scripts/07b_sync_iceberg_governed.sh` copies the governed Postgres tables into Iceberg:

```text
iceberg.governed.customer_standard
iceberg.governed.customer_rejects
```

Iceberg metadata is stored in Nessie; Parquet data files are written under `data/iceberg/warehouse/` on the host.

## Expected demo results

| Metric             | Expected count |
| ------------------ | -------------: |
| CRM source rows    |              6 |
| WebApp source rows |              7 |
| Accepted rows      |              4 |
| Rejected rows      |              9 |
| Iceberg accepted   |              4 |
| Iceberg rejected   |              9 |

## Quick start

```bash
cd "Starburst and Spark Testing"
chmod +x scripts/*.sh
make all
```

See **[Step-by-step demo walkthrough](#step-by-step-demo-walkthrough)** for the full command-by-command tour with captured output — no live run required.

If Docker is not installed:

```bash
make prereqs
```

Then log out and back in if your user was newly added to the `docker` group. Until then, prefix Docker commands:

```bash
sg docker -c "make all"
```

## Manual run order

```bash
cd "Starburst and Spark Testing"
chmod +x scripts/*.sh
make check-ports
make pull
make cli
make up
make wait
make smoke
make pipeline
make demo
make assert
```

## Step-by-step demo walkthrough

This section is a **read-only walkthrough**. Every command and output below was captured from a successful run on Ubuntu/WSL2. You can follow the story without starting Docker, or use it as a script to compare against your own run.

**Story in one sentence:** Trino reads messy CRM + WebApp sources → Spark enforces the canonical contract → accepted/rejected rows land in Postgres → Trino copies them to Iceberg → Trino queries everything back.

### What each step proves

| Step | Command | Proves |
| ---- | ------- | ------ |
| 1 | `make up` + `make wait` | All containers start; Trino accepts SQL |
| 2 | `make smoke` | Four Trino catalogs work; source row counts are 6 + 7 |
| 3 | `make pipeline` | Spark validates, splits 4 accepted / 9 rejected, syncs to Iceberg |
| 4 | `make demo` | End-to-end SQL results across sources, governed Postgres, and Iceberg |
| 5 | `make assert` | Automated count check passes |

Or run everything at once: `make all` (same steps in order).

---

### Step 1 — Start the stack

```bash
cd "Starburst and Spark Testing"
chmod +x scripts/*.sh
make up
make wait
```

**`make up` output:**

```text
Starting Spark + Trino schema demo stack...
[+] Running 8/8
 ✔ Container postgres-crm       Started
 ✔ Container mysql-webapp       Started
 ✔ Container postgres-governed  Started
 ✔ Container nessie             Started
 ✔ Container trino              Started
 ✔ Container spark-master       Started
 ✔ Container spark-worker-1     Started
Stack start requested.
Run ./scripts/05_wait_for_stack.sh next.
```

**`make wait` output:**

```text
Waiting for PostgreSQL container postgres-crm...
postgres-crm is ready.
Waiting for MySQL container mysql-webapp...
mysql-webapp is ready.
Waiting for PostgreSQL container postgres-governed...
postgres-governed is ready.
Waiting for Trino to accept queries...
Trino is ready for queries.
Waiting for Spark master UI at http://localhost:8081/...
Spark master UI is ready.
All services are ready.
```

At this point you should have eight containers (`postgres-crm`, `mysql-webapp`, `postgres-governed`, `nessie`, `trino`, `spark-master`, `spark-worker-1`, plus ephemeral `spark-submit` during pipeline runs). Trino UI: http://localhost:8080 — username `demo`, no password.

---

### Step 2 — Smoke test (Trino federated reads)

```bash
make smoke
```

**Output:**

```text
SQL> SHOW CATALOGS
"crm"
"governed"
"iceberg"
"system"
"webapp"

SQL> SHOW SCHEMAS FROM iceberg
"governed"
"information_schema"
"system"

SQL> SELECT count(*) AS crm_rows FROM crm.public.customers
"6"

SQL> SELECT count(*) AS webapp_rows FROM webapp.appdb.user_profiles
"7"

SQL>
SELECT source_system, row_count
FROM (
  SELECT 'CRM' AS source_system, count(*) AS row_count FROM crm.public.customers
  UNION ALL
  SELECT 'WEBAPP' AS source_system, count(*) AS row_count FROM webapp.appdb.user_profiles
)
ORDER BY source_system

"CRM","6"
"WEBAPP","7"

Trino smoke test completed.
```

**Takeaway:** Trino sees all four data catalogs (`crm`, `webapp`, `governed`, `iceberg`). Sources contain 13 raw rows total (6 CRM + 7 WebApp) before any validation.

---

### Step 3 — Run the Spark pipeline + Iceberg sync

```bash
make pipeline
```

This truncates governed tables, runs `jobs/enforce_customer_schema.py` on the Spark cluster, then runs `scripts/07b_sync_iceberg_governed.sh`.

**Output (abbreviated — first run also downloads JDBC jars from Maven):**

```text
Clearing governed output tables...
TRUNCATE TABLE
TRUNCATE TABLE
Running Spark schema enforcement job...
 Container trino Running
 Container spark-master Running
 Container spark-worker-1 Running
 ...
26/06/15 16:35:09 INFO SparkContext: Submitted application: spark-trino-canonical-schema-enforcement-demo
 ...
Accepted rows: 4
Rejected rows: 9
Accepted preview:
+-----------+-----------------+-------------------+-------+--------+-------------+
|customer_id|email            |created_at         |country|status  |source_system|
+-----------+-----------------+-------------------+-------+--------+-------------+
|app-2001   |carl@example.com |2024-07-01 16:00:00|US     |ACTIVE  |WEBAPP       |
|app-2002   |dana@example.com |2024-08-01 18:00:00|GB     |INACTIVE|WEBAPP       |
|crm-1001   |alice@example.com|2026-06-01 10:15:00|US     |ACTIVE  |CRM          |
|crm-1002   |bob@example.org  |2026-06-02 11:30:00|CA     |INACTIVE|CRM          |
+-----------+-----------------+-------------------+-------+--------+-------------+

Rejected preview:
+-----------+------------------------------+-------+-------+-------------+----------------------+
|customer_id|email                         |country|status |source_system|rejection_reasons     |
+-----------+------------------------------+-------+-------+-------------+----------------------+
|app-2003   |bad-email                     |US     |ACTIVE |WEBAPP       |["email_invalid"]     |
|app-2004   |NULL                          |US     |ACTIVE |WEBAPP       |["email_invalid"]     |
|app-2005   |missing-signup@example.com    |US     |ACTIVE |WEBAPP       |["created_at_invalid"]|
|app-2006   |bad-country@example.com       |USA    |ACTIVE |WEBAPP       |["country_invalid"]   |
|app-2007   |bad-status@example.com        |CA     |NULL   |WEBAPP       |["status_invalid"]    |
|crm-1003   |not-an-email                  |US     |ACTIVE |CRM          |["email_invalid"]     |
|crm-1004   |NULL                          |GB     |ACTIVE |CRM          |["email_invalid"]     |
|crm-1005   |missing-created-at@example.com|DE     |ACTIVE |CRM          |["created_at_invalid"]|
|crm-1006   |wrong-status@example.com      |FR     |PENDING|CRM          |["status_invalid"]    |
+-----------+------------------------------+-------+-------+-------------+----------------------+

Writing accepted rows to governed.public.customer_standard...
Writing rejected rows to governed.public.customer_rejects...
Schema enforcement job completed successfully.

Syncing governed outputs to Iceberg...
Publishing governed Postgres outputs to Iceberg tables...

SQL> CREATE SCHEMA IF NOT EXISTS iceberg.governed
CREATE SCHEMA

SQL> CREATE TABLE iceberg.governed.customer_standard AS
     SELECT ... FROM governed.public.customer_standard
CREATE TABLE: 4 rows

SQL> CREATE TABLE iceberg.governed.customer_rejects AS
     SELECT ... FROM governed.public.customer_rejects
CREATE TABLE: 9 rows

Iceberg governed tables synced.
Pipeline run completed.
```

**Takeaway:** Spark read the federated Trino query, normalized CRM + WebApp into one shape, applied `contracts/customer_canonical_schema.json`, and wrote 4 trusted rows + 9 quarantined rows. Trino then published the same data to Iceberg Parquet files under `data/iceberg/warehouse/`.

---

### Step 4 — Demo queries (full SQL tour)

```bash
make demo
```

This runs ten Trino queries. Output below is the full captured result.

#### 4a. Trino catalogs

```text
SHOW CATALOGS

 Catalog
----------
 crm
 governed
 iceberg
 system
 webapp
(5 rows)
```

#### 4b. Raw CRM source (PostgreSQL)

```text
SELECT * FROM crm.public.customers ORDER BY customer_id

 customer_id |             email              |         created_at         | country |  status
-------------+--------------------------------+----------------------------+---------+----------
 crm-1001    | alice@example.com              | 2026-06-01 10:15:00.000000 | US      | ACTIVE
 crm-1002    | bob@example.org                | 2026-06-02 11:30:00.000000 | CA      | INACTIVE
 crm-1003    | not-an-email                   | 2026-06-03 09:00:00.000000 | US      | ACTIVE
 crm-1004    | NULL                           | 2026-06-03 11:00:00.000000 | GB      | ACTIVE
 crm-1005    | missing-created-at@example.com | NULL                       | DE      | ACTIVE
 crm-1006    | wrong-status@example.com       | 2026-06-04 10:00:00.000000 | FR      | PENDING
(6 rows)
```

#### 4c. Raw WebApp source (MySQL)

```text
SELECT * FROM webapp.appdb.user_profiles ORDER BY id

  id  |       email_address        | signup_epoch | country_code | is_active
------+----------------------------+--------------+--------------+-----------
 2001 | carl@example.com           |   1719849600 | US           |         1
 2002 | dana@example.com           |   1722535200 | GB           |         0
 2003 | bad-email                  |   1722535300 | US           |         1
 2004 | NULL                       |   1722535400 | US           |         1
 2005 | missing-signup@example.com |         NULL | US           |         1
 2006 | bad-country@example.com    |   1722535500 | USA          |         1
 2007 | bad-status@example.com     |   1722535600 | CA           |         9
(7 rows)
```

#### 4d. Federated view (both sources, one query)

Trino unions CRM and WebApp with inline normalization — the same logic Spark uses downstream:

```text
 source_system | customer_id |             email              | country |  status
---------------+-------------+--------------------------------+---------+----------
 CRM           | crm-1001    | alice@example.com              | US      | ACTIVE
 CRM           | crm-1002    | bob@example.org                | CA      | INACTIVE
 CRM           | crm-1003    | not-an-email                   | US      | ACTIVE
 CRM           | crm-1004    | NULL                           | GB      | ACTIVE
 CRM           | crm-1005    | missing-created-at@example.com   | DE      | ACTIVE
 CRM           | crm-1006    | wrong-status@example.com       | FR      | PENDING
 WEBAPP        | app-2001    | carl@example.com               | US      | ACTIVE
 WEBAPP        | app-2002    | dana@example.com               | GB      | INACTIVE
 WEBAPP        | app-2003    | bad-email                      | US      | ACTIVE
 WEBAPP        | app-2004    | NULL                           | US      | ACTIVE
 WEBAPP        | app-2005    | missing-signup@example.com     | US      | ACTIVE
 WEBAPP        | app-2006    | bad-country@example.com        | USA     | ACTIVE
 WEBAPP        | app-2007    | bad-status@example.com         | CA      | NULL
(13 rows)
```

#### 4e. Accepted rows (Postgres governed)

Only the four rows that passed schema validation:

```text
 customer_id |       email       |         created_at         | country |  status  | source_system
-------------+-------------------+----------------------------+---------+----------+---------------
 app-2001    | carl@example.com  | 2024-07-01 16:00:00.000000 | US      | ACTIVE   | WEBAPP
 app-2002    | dana@example.com  | 2024-08-01 18:00:00.000000 | GB      | INACTIVE | WEBAPP
 crm-1001    | alice@example.com | 2026-06-01 10:15:00.000000 | US      | ACTIVE   | CRM
 crm-1002    | bob@example.org   | 2026-06-02 11:30:00.000000 | CA      | INACTIVE | CRM
(4 rows)
```

#### 4f. Rejected rows with reasons (Postgres governed)

Every invalid row is quarantined with an explicit JSON reason code:

```text
 customer_id |             email              | country | status  | source_system |   rejection_reasons
-------------+--------------------------------+---------+---------+---------------+------------------------
 app-2003    | bad-email                      | US      | ACTIVE  | WEBAPP        | ["email_invalid"]
 app-2004    | NULL                           | US      | ACTIVE  | WEBAPP        | ["email_invalid"]
 app-2005    | missing-signup@example.com     | US      | ACTIVE  | WEBAPP        | ["created_at_invalid"]
 app-2006    | bad-country@example.com        | USA     | ACTIVE  | WEBAPP        | ["country_invalid"]
 app-2007    | bad-status@example.com         | CA      | NULL    | WEBAPP        | ["status_invalid"]
 crm-1003    | not-an-email                   | US      | ACTIVE  | CRM           | ["email_invalid"]
 crm-1004    | NULL                           | GB      | ACTIVE  | CRM           | ["email_invalid"]
 crm-1005    | missing-created-at@example.com | DE      | ACTIVE  | CRM           | ["created_at_invalid"]
 crm-1006    | wrong-status@example.com       | FR      | PENDING | CRM           | ["status_invalid"]
(9 rows)
```

#### 4g. Governed counts (Postgres)

```text
 result_type | row_count
-------------+-----------
 accepted    |         4
 rejected    |         9
(2 rows)
```

#### 4h. Accepted rows (Iceberg)

Same four rows, now queryable as an Iceberg table:

```text
 customer_id |       email       |         created_at         | country |  status  | source_system
-------------+-------------------+----------------------------+---------+----------+---------------
 app-2001    | carl@example.com  | 2024-07-01 16:00:00.000000 | US      | ACTIVE   | WEBAPP
 app-2002    | dana@example.com  | 2024-08-01 18:00:00.000000 | GB      | INACTIVE | WEBAPP
 crm-1001    | alice@example.com | 2026-06-01 10:15:00.000000 | US      | ACTIVE   | CRM
 crm-1002    | bob@example.org   | 2026-06-02 11:30:00.000000 | CA      | INACTIVE | CRM
(4 rows)
```

#### 4i. Rejected rows (Iceberg)

```text
 customer_id |             email              | country | status  | source_system |   rejection_reasons
-------------+--------------------------------+---------+---------+---------------+------------------------
 app-2003    | bad-email                      | US      | ACTIVE  | WEBAPP        | ["email_invalid"]
 app-2004    | NULL                           | US      | ACTIVE  | WEBAPP        | ["email_invalid"]
 app-2005    | missing-signup@example.com     | US      | ACTIVE  | WEBAPP        | ["created_at_invalid"]
 app-2006    | bad-country@example.com        | USA     | ACTIVE  | WEBAPP        | ["country_invalid"]
 app-2007    | bad-status@example.com         | CA      | NULL    | WEBAPP        | ["status_invalid"]
 crm-1003    | not-an-email                   | US      | ACTIVE  | CRM           | ["email_invalid"]
 crm-1004    | NULL                           | GB      | ACTIVE  | CRM           | ["email_invalid"]
 crm-1005    | missing-created-at@example.com | DE      | ACTIVE  | CRM           | ["created_at_invalid"]
 crm-1006    | wrong-status@example.com       | FR      | PENDING | CRM           | ["status_invalid"]
(9 rows)
```

#### 4j. Iceberg counts

```text
 result_type | row_count
-------------+-----------
 accepted    |         4
 rejected    |         9
(2 rows)

Demo queries completed.
```

**Takeaway:** Postgres governed tables and Iceberg copies return identical row sets. Iceberg adds open-table-format storage (Parquet + Nessie catalog) on top of the same governance outcome.

---

### Step 5 — Automated verification

```bash
make assert
```

**Output:**

```text
CRM source rows:              6
WebApp source rows:           7
Accepted governed rows:       4
Rejected governed rows:       9
Accepted Iceberg rows:        4
Rejected Iceberg rows:        9
All expected counts passed.
```

If all six counts match, the demo succeeded.

---

### Rejection cheat sheet

Why each of the 9 rows failed validation:

| Row | Source | Problem | Reason code |
| --- | ------ | ------- | ----------- |
| `crm-1003` | CRM | `not-an-email` | `email_invalid` |
| `crm-1004` | CRM | NULL email | `email_invalid` |
| `crm-1005` | CRM | NULL `created_at` | `created_at_invalid` |
| `crm-1006` | CRM | status `PENDING` (not ACTIVE/INACTIVE) | `status_invalid` |
| `app-2003` | WebApp | `bad-email` | `email_invalid` |
| `app-2004` | WebApp | NULL email | `email_invalid` |
| `app-2005` | WebApp | NULL `signup_epoch` | `created_at_invalid` |
| `app-2006` | WebApp | country `USA` (3 letters, need 2) | `country_invalid` |
| `app-2007` | WebApp | `is_active = 9` (unmapped) | `status_invalid` |

The 4 accepted rows (`crm-1001`, `crm-1002`, `app-2001`, `app-2002`) are the only ones with valid email, timestamp, 2-letter country, and allowed status.

---

### Optional: run it yourself

If you do want to reproduce the output above:

```bash
cd "Starburst and Spark Testing"
chmod +x scripts/*.sh
make all          # or the manual steps in "Manual run order"
```

If Docker permission errors occur, prefix with `sg docker -c "make all"`. First pipeline run takes ~2 minutes while Spark downloads JDBC drivers; subsequent runs are faster.

## Access and login

### Trino UI / CLI

| Setting | Value |
| ------- | ----- |
| URL | http://localhost:8080 |
| Username | `demo` |
| Password | none (local demo, no auth configured) |

### Spark UIs

| Service | URL |
| ------- | --- |
| Master | http://localhost:8081 |
| Worker | http://localhost:8082 |

No login required.

### Direct database ports (optional)

| Database | Host port | DB | User | Password |
| -------- | --------- | -- | ---- | -------- |
| CRM Postgres | `15432` | `crm` | `demo` | `demo_password` |
| Governed Postgres | `15433` | `governed` | `demo` | `demo_password` |
| WebApp MySQL | `13306` | `appdb` | `demo` | `demo_password` |

For the demo story you normally query through Trino, not these ports directly.

## Important demonstration talking points

### Trino role

Federated SQL access layer. It reads across PostgreSQL and MySQL source schemas and exposes a single query interface.

Trino connects to:

* PostgreSQL CRM source through the `crm` catalog
* MySQL WebApp source through the `webapp` catalog
* PostgreSQL governed output through the `governed` catalog
* Iceberg governed tables through the `iceberg` catalog (Nessie + local Parquet)

The demo proves this with SQL queries that read from all four catalogs.

### Spark role

Processing and enforcement layer. It reads the federated Trino query, normalizes records into a central schema, validates them, and writes accepted/rejected outputs.

Spark:

* reads the federated query from Trino via JDBC (`jobs/enforce_customer_schema.py`)
* normalizes source-specific field names and types
* checks the result against the central schema contract
* rejects invalid rows with explicit rejection reasons
* writes valid rows into the governed accepted table
* writes invalid rows into the quarantine/reject table

Each `make pipeline` run appears as a completed application in the Spark master UI.

After Spark finishes, the pipeline syncs governed Postgres outputs to Iceberg via Trino `CREATE TABLE ... AS SELECT` against the `iceberg` catalog.

### Iceberg role

Lakehouse storage layer for the governed outputs. The same accepted and rejected datasets written to Postgres are published as Iceberg tables so you can query them with Trino using open table format semantics (Parquet files, Nessie catalog).

### Canonical schema role

Governance contract. Records that do not conform are rejected and never enter the trusted canonical table.

If data does not match the contract, Spark does not publish it to the trusted table.

The governed PostgreSQL table also has database-level constraints, so even if the Spark job is changed incorrectly, the accepted table still protects itself.

## Useful commands

Show Trino catalogs:

```bash
./bin/trino --server http://localhost:8080 --user demo --execute "SHOW CATALOGS"
```

Count source rows:

```bash
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM crm.public.customers"
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM webapp.appdb.user_profiles"
```

Query rejected rows with reasons:

```bash
./bin/trino --server http://localhost:8080 --user demo --output-format ALIGNED --execute "
SELECT customer_id, email, country, status, source_system, rejection_reasons
FROM governed.public.customer_rejects
ORDER BY customer_id
"
```

Count accepted and rejected rows:

```bash
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM governed.public.customer_standard"
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM governed.public.customer_rejects"
```

Query the Iceberg copies:

```bash
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM iceberg.governed.customer_standard"
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM iceberg.governed.customer_rejects"
```

Run the Spark job again:

```bash
make pipeline
```

Run the demo queries:

```bash
make demo
```

Assert expected counts:

```bash
make assert
```

Stop the stack without deleting data:

```bash
make stop
```

Delete the stack and all volumes:

```bash
make clean
```

## Troubleshooting

### Docker permission denied

If `make pull` or `make up` fails with permission errors on `/var/run/docker.sock`:

```bash
sg docker -c "make up"
```

Or log out and back in after `make prereqs` adds you to the `docker` group.

### Port already in use

```bash
make check-ports
sudo lsof -i :8080
```

### Trino starts but catalog is missing

```bash
ls -la trino/etc/catalog
docker logs trino
```

Expected catalog files: `crm.properties`, `webapp.properties`, `governed.properties`, `iceberg.properties`.

### Iceberg sync fails after pipeline

Ensure Nessie is running (`docker ps` should show `nessie`) and Trino was recreated after catalog changes:

```bash
mkdir -p data/iceberg/warehouse
chmod -R 777 data/iceberg
sg docker -c "docker compose up -d --force-recreate trino"
make wait
./scripts/07b_sync_iceberg_governed.sh
```

If Trino fails to start with Iceberg catalog errors, check `docker logs trino` and `trino/etc/catalog/iceberg.properties`.

### Trino smoke fails with "still initializing"

`make wait` waits until Trino accepts `SHOW CATALOGS`. If you run queries immediately after a fresh start, wait for `make wait` to finish or retry after a few seconds.

### Spark job fails downloading Maven packages

The first Spark run downloads JDBC drivers into the `spark_ivy_cache` Docker volume. Check outbound access from the host:

```bash
curl -I https://repo1.maven.org/maven2/
```

### Pipeline duplicate-key errors

`make pipeline` truncates governed tables before each run and uses a file lock to prevent concurrent runs. If a prior run failed mid-write, run `make pipeline` again or `make clean && make all`.

### Reset everything

```bash
make clean
make all
```

## Demo narrative (summary)

For the full command output tour, see [Step-by-step demo walkthrough](#step-by-step-demo-walkthrough) above.

```text
Trino is used first as the federated SQL access layer. It reads from two different systems, PostgreSQL and MySQL, without forcing the data to be copied into a single source first.

Spark then reads the federated Trino query, applies the canonical schema contract, and separates valid records from invalid records.

The accepted records are written to the governed standard table. The rejected records are written to a quarantine table with explicit rejection reasons.

A follow-on step publishes those same governed tables to Iceberg (`iceberg.governed.customer_standard` and `iceberg.governed.customer_rejects`).

Finally, Trino is used again as the analytics/query layer to inspect the trusted table, the rejected records, and the Iceberg copies.
```
