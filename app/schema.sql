DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT,
    skills_required TEXT,
    application_link TEXT NOT NULL,  -- Make it required
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posted_date TEXT NOT NULL,
    source TEXT NOT NULL  -- Add source tracking
);

CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date);