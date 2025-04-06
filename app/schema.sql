DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT,
    skills_required TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);