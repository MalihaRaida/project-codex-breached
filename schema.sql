CREATE TABLE IF NOT EXISTS users (
    email_hash CHAR(64) NOT NULL,
    password_hash CHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (email_hash, password_hash),
    INDEX idx_email_hash (email_hash),
    INDEX idx_password_hash (password_hash)
);
