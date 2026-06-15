CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE IF NOT EXISTS user_profiles (
    id INT,
    email_address VARCHAR(255),
    signup_epoch BIGINT,
    country_code VARCHAR(8),
    is_active TINYINT
);

TRUNCATE TABLE user_profiles;

INSERT INTO user_profiles (id, email_address, signup_epoch, country_code, is_active) VALUES
(2001, 'carl@example.com', 1719849600, 'US', 1),
(2002, 'dana@example.com', 1722535200, 'GB', 0),

-- Invalid: bad email
(2003, 'bad-email', 1722535300, 'US', 1),

-- Invalid: missing email
(2004, NULL, 1722535400, 'US', 1),

-- Invalid: missing timestamp
(2005, 'missing-signup@example.com', NULL, 'US', 1),

-- Invalid: bad country code
(2006, 'bad-country@example.com', 1722535500, 'USA', 1),

-- Invalid: unknown active flag
(2007, 'bad-status@example.com', 1722535600, 'CA', 9);
