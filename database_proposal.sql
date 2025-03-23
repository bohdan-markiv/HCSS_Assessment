-- This file contains a data warehousing proposal

-- Table to store speech data
CREATE TABLE speeches (
    id TEXT PRIMARY KEY,                     -- Unique ID of the speech
    text TEXT NOT NULL,                      -- Full text of the speech
    contains_topic BOOLEAN,                  -- True if the speech mentions a relevant topic
    compound REAL                            -- Compound sentiment score (VADER)
);

-- Table to store metadata about each speech and its speaker
CREATE TABLE metadata (
    id TEXT PRIMARY KEY,                     -- Same ID as in the speeches table (1:1 relationship)
    date TEXT,                               -- Date of the speech (YYYY-MM-DD)
    speaker_id TEXT,                         -- ID of the speaker
    speaker_name TEXT,                       -- Full name of the speaker
    speaker_gender TEXT,                     -- Gender of the speaker ("M" or "F")
    speaker_birth TEXT,                      -- Year of birth (to compute age)
    speaker_party TEXT,                      -- Name of the speaker's political party
    party_orientation TEXT,                  -- Ideological orientation ("Left", "Right", "Center")
    party_status TEXT,                       -- Status of the party ("Active", "Inactive")
    speaker_minister BOOLEAN,                -- Whether the speaker is/was a minister
    age INTEGER,                             -- Speaker's age (at the time of speech)
    month INTEGER,                           -- Month of the speech (1-12)
    isMinister BOOLEAN,                      -- Duplicate of speaker_minister? Consider removing or renaming
    isInCoalition BOOLEAN,                   -- Whether the party is in the governing coalition
    FOREIGN KEY (id) REFERENCES speeches(id)
);

-- Table to store external information about political parties
CREATE TABLE party_details (
    party_name TEXT PRIMARY KEY,             -- The name of the party
    number_of_seats_in_upper_house INTEGER,  -- Number of seats in Eerste Kamer
    number_of_seats_in_lower_house INTEGER,  -- Number of seats in Tweede Kamer
    founding_year INTEGER,                   -- Year the party was founded
    current_leader TEXT,                     -- Name of the current party leader
    EUP_group TEXT,                           -- European Parliament affiliation
    FOREIGN KEY (party_name) REFERENCES metadata(speaker_party)
);
