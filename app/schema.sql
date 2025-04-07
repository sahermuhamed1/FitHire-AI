DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT,
    skills_required TEXT,
    application_link TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posted_date TEXT NOT NULL
);

-- Remove the unique index and create a regular index
CREATE INDEX IF NOT EXISTS idx_jobs_application_link ON jobs(application_link);