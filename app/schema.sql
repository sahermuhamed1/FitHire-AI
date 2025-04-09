-- Schema for FitHire AI database

-- Drop existing tables (if they exist)
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create jobs table
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT,
    description TEXT,
    location TEXT,
    skills_required TEXT,
    application_link TEXT,
    posted_date TEXT,
    source TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index for jobs
CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date);

-- Insert default admin user (password: admin123)
INSERT OR IGNORE INTO users (username, email, password_hash, is_admin)
VALUES ('admin', 'admin@fithire.com', 'pbkdf2:sha256:150000$vFj3SkRn$c076d2b9972c9153316315bd3c52273a484a34f087051842b09be13bc32aa0a2', 1);