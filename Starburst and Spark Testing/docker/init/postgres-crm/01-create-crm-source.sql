CREATE TABLE IF NOT EXISTS public.customers (
    customer_id VARCHAR(64),
    email VARCHAR(255),
    created_at TIMESTAMP,
    country VARCHAR(8),
    status VARCHAR(32)
);

TRUNCATE TABLE public.customers;

INSERT INTO public.customers (customer_id, email, created_at, country, status) VALUES
('crm-1001', 'alice@example.com', '2026-06-01 10:15:00', 'US', 'ACTIVE'),
('crm-1002', 'bob@example.org', '2026-06-02 11:30:00', 'CA', 'INACTIVE'),

-- Invalid: bad email
('crm-1003', 'not-an-email', '2026-06-03 09:00:00', 'US', 'ACTIVE'),

-- Invalid: missing email
('crm-1004', NULL, '2026-06-03 11:00:00', 'GB', 'ACTIVE'),

-- Invalid: missing created_at
('crm-1005', 'missing-created-at@example.com', NULL, 'DE', 'ACTIVE'),

-- Invalid: status not in canonical enum
('crm-1006', 'wrong-status@example.com', '2026-06-04 10:00:00', 'FR', 'PENDING');
