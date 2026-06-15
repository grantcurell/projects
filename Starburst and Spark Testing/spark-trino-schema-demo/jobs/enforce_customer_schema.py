import json
import os
import sys
from typing import Dict, List

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def load_contract(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("spark-trino-canonical-schema-enforcement-demo")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def read_federated_sources_from_trino(spark: SparkSession, trino_url: str, trino_user: str) -> DataFrame:
    federated_query = """
        SELECT
            CAST(customer_id AS varchar) AS raw_customer_id,
            CAST(email AS varchar) AS raw_email,
            CAST(created_at AS varchar) AS raw_created_at,
            CAST(country AS varchar) AS raw_country,
            CAST(status AS varchar) AS raw_status,
            'CRM' AS source_system,
            json_format(
              CAST(
                map(
                  ARRAY['source_table', 'customer_id', 'email', 'created_at', 'country', 'status'],
                  ARRAY[
                    'crm.public.customers',
                    CAST(customer_id AS varchar),
                    CAST(email AS varchar),
                    CAST(created_at AS varchar),
                    CAST(country AS varchar),
                    CAST(status AS varchar)
                  ]
                )
              AS json)
            ) AS original_payload
        FROM crm.public.customers

        UNION ALL

        SELECT
            CONCAT('app-', CAST(id AS varchar)) AS raw_customer_id,
            CAST(email_address AS varchar) AS raw_email,
            CAST(from_unixtime(signup_epoch) AS varchar) AS raw_created_at,
            CAST(country_code AS varchar) AS raw_country,
            CAST(
              CASE
                WHEN is_active = 1 THEN 'ACTIVE'
                WHEN is_active = 0 THEN 'INACTIVE'
                ELSE NULL
              END
            AS varchar) AS raw_status,
            'WEBAPP' AS source_system,
            json_format(
              CAST(
                map(
                  ARRAY['source_table', 'id', 'email_address', 'signup_epoch', 'country_code', 'is_active'],
                  ARRAY[
                    'webapp.appdb.user_profiles',
                    CAST(id AS varchar),
                    CAST(email_address AS varchar),
                    CAST(signup_epoch AS varchar),
                    CAST(country_code AS varchar),
                    CAST(is_active AS varchar)
                  ]
                )
              AS json)
            ) AS original_payload
        FROM webapp.appdb.user_profiles
    """

    return (
        spark.read
        .format("jdbc")
        .option("url", trino_url)
        .option("driver", "io.trino.jdbc.TrinoDriver")
        .option("user", trino_user)
        .option("dbtable", f"({federated_query}) AS federated_customer_sources")
        .load()
    )


def normalize_to_candidate_schema(raw_df: DataFrame) -> DataFrame:
    return raw_df.select(
        F.trim(F.col("raw_customer_id")).alias("customer_id"),
        F.lower(F.trim(F.col("raw_email"))).alias("email"),
        F.to_timestamp(F.col("raw_created_at")).alias("created_at"),
        F.upper(F.trim(F.col("raw_country"))).alias("country"),
        F.upper(F.trim(F.col("raw_status"))).alias("status"),
        F.upper(F.trim(F.col("source_system"))).alias("source_system"),
        F.current_timestamp().alias("ingested_at"),
        F.col("original_payload").alias("original_payload")
    )


def assert_structural_schema(candidate_df: DataFrame, contract: Dict) -> None:
    expected_columns = contract["columns"]
    expected_names = [c["name"] for c in expected_columns]

    actual_names = [f.name for f in candidate_df.drop("original_payload").schema.fields]

    if actual_names != expected_names:
        raise RuntimeError(
            "Canonical schema column mismatch. "
            f"Expected {expected_names}, got {actual_names}"
        )

    actual_types = {
        f.name: f.dataType.simpleString()
        for f in candidate_df.drop("original_payload").schema.fields
    }

    expected_types = {
        c["name"]: c["spark_type"]
        for c in expected_columns
    }

    mismatches: List[str] = []
    for name, expected_type in expected_types.items():
        actual_type = actual_types.get(name)
        if actual_type != expected_type:
            mismatches.append(
                f"{name}: expected Spark type {expected_type}, got {actual_type}"
            )

    if mismatches:
        raise RuntimeError(
            "Canonical schema type mismatch: " + "; ".join(mismatches)
        )


def add_validation_errors(candidate_df: DataFrame, contract: Dict) -> DataFrame:
    rules = contract["validation_rules"]
    email_regex = rules["email_regex"]
    country_regex = rules["country_regex"]
    status_values = rules["status_allowed_values"]
    source_values = rules["source_system_allowed_values"]

    validation_exprs = [
        F.when(
            F.col("customer_id").isNull() | (F.length(F.trim(F.col("customer_id"))) == 0),
            F.lit("customer_id_missing")
        ),
        F.when(
            F.col("email").isNull() | (~F.col("email").rlike(email_regex)),
            F.lit("email_invalid")
        ),
        F.when(
            F.col("created_at").isNull(),
            F.lit("created_at_invalid")
        ),
        F.when(
            F.col("country").isNull() | (~F.col("country").rlike(country_regex)),
            F.lit("country_invalid")
        ),
        F.when(
            F.col("status").isNull() | (~F.col("status").isin(status_values)),
            F.lit("status_invalid")
        ),
        F.when(
            F.col("source_system").isNull() | (~F.col("source_system").isin(source_values)),
            F.lit("source_system_invalid")
        )
    ]

    return (
        candidate_df
        .withColumn("validation_errors_raw", F.array(*validation_exprs))
        .withColumn("validation_errors", F.expr("filter(validation_errors_raw, x -> x is not null)"))
        .drop("validation_errors_raw")
    )


def write_postgres_table(df: DataFrame, jdbc_url: str, user: str, password: str, table: str) -> None:
    (
        df.coalesce(1)
        .write
        .format("jdbc")
        .mode("overwrite")
        .option("truncate", "true")
        .option("url", jdbc_url)
        .option("driver", "org.postgresql.Driver")
        .option("user", user)
        .option("password", password)
        .option("dbtable", table)
        .option("numPartitions", "1")
        .save()
    )


def main() -> int:
    contract_path = os.getenv("CONTRACT_PATH", "/opt/spark-apps/contracts/customer_canonical_schema.json")
    trino_url = os.getenv("TRINO_JDBC_URL", "jdbc:trino://trino:8080")
    trino_user = os.getenv("TRINO_USER", "demo")
    governed_jdbc_url = os.getenv("GOVERNED_JDBC_URL", "jdbc:postgresql://postgres-governed:5432/governed")
    governed_user = os.getenv("GOVERNED_DB_USER", "demo")
    governed_password = os.getenv("GOVERNED_DB_PASSWORD", "demo_password")

    contract = load_contract(contract_path)
    spark = build_spark_session()

    print("Reading federated source data from Trino...")
    raw_df = read_federated_sources_from_trino(spark, trino_url, trino_user)

    print("Raw federated source data:")
    raw_df.show(truncate=False)

    print("Normalizing data to canonical candidate schema...")
    candidate_df = normalize_to_candidate_schema(raw_df)

    print("Asserting canonical structural schema...")
    assert_structural_schema(candidate_df, contract)

    print("Applying row-level validation rules...")
    validated_df = add_validation_errors(candidate_df, contract)

    accepted_df = (
        validated_df
        .filter(F.size(F.col("validation_errors")) == 0)
        .select(
            "customer_id",
            "email",
            "created_at",
            "country",
            "status",
            "source_system",
            "ingested_at"
        )
    )

    rejected_df = (
        validated_df
        .filter(F.size(F.col("validation_errors")) > 0)
        .select(
            "customer_id",
            "email",
            "created_at",
            "country",
            "status",
            "source_system",
            "ingested_at",
            F.to_json(F.col("validation_errors")).alias("rejection_reasons"),
            "original_payload"
        )
    )

    accepted_count = accepted_df.count()
    rejected_count = rejected_df.count()

    print(f"Accepted rows: {accepted_count}")
    print(f"Rejected rows: {rejected_count}")

    print("Accepted preview:")
    accepted_df.orderBy("customer_id").show(truncate=False)

    print("Rejected preview:")
    rejected_df.orderBy("customer_id").show(truncate=False)

    print("Writing accepted rows to governed.public.customer_standard...")
    write_postgres_table(
        accepted_df,
        governed_jdbc_url,
        governed_user,
        governed_password,
        "public.customer_standard"
    )

    print("Writing rejected rows to governed.public.customer_rejects...")
    write_postgres_table(
        rejected_df,
        governed_jdbc_url,
        governed_user,
        governed_password,
        "public.customer_rejects"
    )

    expected = contract.get("expected_demo_counts", {})
    expected_accepted = expected.get("accepted_rows")
    expected_rejected = expected.get("rejected_rows")

    if expected_accepted is not None and accepted_count != expected_accepted:
        raise RuntimeError(
            f"Unexpected accepted row count. Expected {expected_accepted}, got {accepted_count}"
        )

    if expected_rejected is not None and rejected_count != expected_rejected:
        raise RuntimeError(
            f"Unexpected rejected row count. Expected {expected_rejected}, got {rejected_count}"
        )

    print("Schema enforcement job completed successfully.")
    spark.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
