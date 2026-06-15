# Spark + Trino canonical schema enforcement demo

This is an all-local, free/open-source implementation using Trino + Spark.

Trino is the open-source SQL query engine that Starburst is built on. The same architectural pattern can be implemented with Starburst Enterprise or Starburst Galaxy, but this local demo intentionally avoids requiring a Starburst account, cloud service, paid tier, or enterprise image access.

This local demo uses Trino, the open-source distributed SQL engine that Starburst is built on. The same architecture maps to Starburst Enterprise or Starburst Galaxy, but this demo is intentionally all-local and free/open-source.

## Demo objectives

1. Show Trino reading from two different source systems with different source schemas.
2. Show Spark consuming the federated Trino query.
3. Show Spark enforcing a central canonical customer schema.
4. Show accepted records landing in `governed.public.customer_standard`.
5. Show rejected records landing in `governed.public.customer_rejects` with rejection reasons.
6. Show Trino querying the raw sources and governed outputs.

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
        |
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
WebApp MySQL source ───┘
                                                             │
                                                             └─ Trino SQL consumption
```

## Canonical customer schema

The central schema contract lives at:

```text
contracts/customer_canonical_schema.json
```

The accepted output table is:

```text
governed.public.customer_standard
```

The rejected output table is:

```text
governed.public.customer_rejects
```

## Expected demo results

| Metric             | Expected count |
| ------------------ | -------------: |
| CRM source rows    |              6 |
| WebApp source rows |              7 |
| Accepted rows      |              4 |
| Rejected rows      |              9 |

## Quick start

Run:

```bash
chmod +x scripts/*.sh
make all
```

If Docker is not installed, run:

```bash
make prereqs
```

Then log out and back in if your user was newly added to the `docker` group.

## Manual run order

```bash
cd spark-trino-schema-demo
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

## Open UIs

Trino UI/API:

```text
http://localhost:8080
```

Spark master UI:

```text
http://localhost:8081
```

Spark worker UI:

```text
http://localhost:8082
```

## Important demonstration talking points

### Trino role

Federated SQL access layer. It reads across PostgreSQL and MySQL source schemas and exposes a single query interface.

Trino connects to:

* PostgreSQL CRM source through the `crm` catalog
* MySQL WebApp source through the `webapp` catalog
* PostgreSQL governed output through the `governed` catalog

The demo proves this with SQL queries that read from all three catalogs.

### Spark role

Processing and enforcement layer. It reads the federated Trino query, normalizes records into a central schema, validates them, and writes accepted/rejected outputs.

Spark:

* reads the federated query from Trino
* normalizes source-specific field names and types
* checks the result against the central schema contract
* rejects invalid rows with explicit rejection reasons
* writes valid rows into the governed accepted table
* writes invalid rows into the quarantine/reject table

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

Count accepted and rejected rows:

```bash
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM governed.public.customer_standard"
./bin/trino --server http://localhost:8080 --user demo --execute "SELECT count(*) FROM governed.public.customer_rejects"
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

### Port already in use

Run:

```bash
make check-ports
```

Then identify the blocking process:

```bash
sudo lsof -i :8080
```

### Trino starts but catalog is missing

Check the mounted catalog files:

```bash
ls -la trino/etc/catalog
docker logs trino
```

Expected catalog files:

```text
crm.properties
webapp.properties
governed.properties
```

### Spark job fails downloading Maven packages

The first Spark run downloads JDBC drivers into the `spark_ivy_cache` Docker volume.

If dependency download fails, check outbound internet access from the container:

```bash
docker compose run --rm spark-submit "curl -I https://repo1.maven.org/maven2/"
```

If curl is unavailable in the Spark image, inspect DNS/networking from the host instead.

### Reset everything

```bash
make clean
make all
```

## Demo narrative

```text
Trino is used first as the federated SQL access layer. It reads from two different systems, PostgreSQL and MySQL, without forcing the data to be copied into a single source first.

Spark then reads the federated Trino query, applies the canonical schema contract, and separates valid records from invalid records.

The accepted records are written to the governed standard table. The rejected records are written to a quarantine table with explicit rejection reasons.

Finally, Trino is used again as the analytics/query layer to inspect the trusted table and the rejected records.
```
