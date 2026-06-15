#!/usr/bin/env bash
set -euo pipefail

source .env

wait_for_postgres() {
  local container="$1"
  local db="$2"

  echo "Waiting for PostgreSQL container ${container}..."
  until docker exec "$container" pg_isready -U "$DEMO_DB_USER" -d "$db" >/dev/null 2>&1; do
    sleep 2
  done
  echo "${container} is ready."
}

wait_for_mysql() {
  echo "Waiting for MySQL container mysql-webapp..."
  until docker exec mysql-webapp mysqladmin ping -h 127.0.0.1 -u"$DEMO_DB_USER" -p"$DEMO_DB_PASSWORD" --silent >/dev/null 2>&1; do
    sleep 2
  done
  echo "mysql-webapp is ready."
}

wait_for_http() {
  local name="$1"
  local url="$2"
  local attempts="${3:-60}"

  echo "Waiting for ${name} at ${url}..."
  local i=0
  until curl -fsS "$url" >/dev/null 2>&1; do
    i=$((i + 1))
    if [ "$i" -ge "$attempts" ]; then
      echo "ERROR: Timed out waiting for ${name} at ${url}"
      exit 1
    fi
    sleep 3
  done
  echo "${name} is ready."
}

wait_for_trino_queries() {
  local trino_cli="./bin/trino"

  if [ ! -x "$trino_cli" ]; then
    echo "Waiting for Trino HTTP endpoint before query readiness check..."
    wait_for_http "Trino" "http://localhost:${TRINO_HOST_PORT}/v1/info"
    return 0
  fi

  echo "Waiting for Trino to accept queries..."
  local i=0
  local attempts=60
  until "$trino_cli" --server "http://localhost:${TRINO_HOST_PORT}" --user demo --execute "SHOW CATALOGS" >/dev/null 2>&1; do
    i=$((i + 1))
    if [ "$i" -ge "$attempts" ]; then
      echo "ERROR: Timed out waiting for Trino to accept queries."
      docker logs trino 2>&1 | tail -40 || true
      exit 1
    fi
    sleep 3
  done
  echo "Trino is ready for queries."
}

wait_for_spark_master() {
  echo "Waiting for Spark master UI at http://localhost:${SPARK_MASTER_UI_PORT}/..."
  local i=0
  local attempts=60

  while [ "$i" -lt "$attempts" ]; do
    if ! docker ps --format '{{.Names}}' | grep -qx spark-master; then
      echo "ERROR: spark-master container is not running."
      docker logs spark-master 2>&1 | tail -40 || true
      exit 1
    fi

    if curl -fsS "http://localhost:${SPARK_MASTER_UI_PORT}/" >/dev/null 2>&1; then
      echo "Spark master UI is ready."
      return 0
    fi

    i=$((i + 1))
    sleep 3
  done

  echo "ERROR: Timed out waiting for Spark master UI at http://localhost:${SPARK_MASTER_UI_PORT}/"
  docker logs spark-master 2>&1 | tail -40 || true
  exit 1
}

wait_for_postgres postgres-crm "$CRM_POSTGRES_DB"
wait_for_mysql
wait_for_postgres postgres-governed "$GOVERNED_POSTGRES_DB"

wait_for_trino_queries
wait_for_spark_master

echo "All services are ready."
