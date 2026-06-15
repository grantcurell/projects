CREATE TABLE IF NOT EXISTS public.customer_standard (
    customer_id VARCHAR(64) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    country VARCHAR(2) NOT NULL,
    status VARCHAR(16) NOT NULL,
    source_system VARCHAR(32) NOT NULL,
    ingested_at TIMESTAMP NOT NULL,

    CONSTRAINT customer_standard_email_chk
      CHECK (email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'),

    CONSTRAINT customer_standard_country_chk
      CHECK (country ~ '^[A-Z]{2}$'),

    CONSTRAINT customer_standard_status_chk
      CHECK (status IN ('ACTIVE', 'INACTIVE')),

    CONSTRAINT customer_standard_source_system_chk
      CHECK (source_system IN ('CRM', 'WEBAPP'))
);

CREATE TABLE IF NOT EXISTS public.customer_rejects (
    reject_id BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(64),
    email VARCHAR(255),
    created_at TIMESTAMP,
    country VARCHAR(16),
    status VARCHAR(32),
    source_system VARCHAR(32),
    ingested_at TIMESTAMP,
    rejection_reasons TEXT NOT NULL,
    original_payload TEXT NOT NULL,
    rejected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

TRUNCATE TABLE public.customer_rejects;
TRUNCATE TABLE public.customer_standard;
