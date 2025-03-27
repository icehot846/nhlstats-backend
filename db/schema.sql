-- ============================
-- Teams Table
-- ============================
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    abbreviation VARCHAR(10) UNIQUE NOT NULL
);

-- ============================
-- Players Table (Skaters)
-- ============================
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player_id INTEGER UNIQUE NOT NULL,
    team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    position VARCHAR(10),
    games_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    points INTEGER,
    plus_minus INTEGER,
    penalty_minutes INTEGER,
    power_play_goals INTEGER,
    shorthanded_goals INTEGER,
    game_winning_goals INTEGER,
    overtime_goals INTEGER,
    shots INTEGER,
    shooting_percentage NUMERIC(5, 3),
    avg_time_on_ice INTEGER,
    faceoff_win_percentage NUMERIC(5, 3)
);

-- ============================
-- Goalies Table
-- ============================
CREATE TABLE goalies (
    id SERIAL PRIMARY KEY,
    player_id INTEGER UNIQUE NOT NULL,
    team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    games_played INTEGER,
    games_started INTEGER,
    wins INTEGER,
    losses INTEGER,
    overtime_losses INTEGER,
    goals_against_avg NUMERIC(5, 3),
    save_percentage NUMERIC(5, 3),
    shots_against INTEGER,
    saves INTEGER,
    goals_against INTEGER,
    shutouts INTEGER
);

CREATE TABLE IF NOT EXISTS top_scorers (
    player_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    team_abbr VARCHAR(5),
    team_name TEXT,
    position VARCHAR(5),
    headshot TEXT,
    team_logo TEXT,
    goals INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS top_goalies (
    player_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    team_abbr VARCHAR(5),
    team_name TEXT,
    position VARCHAR(5),
    headshot TEXT,
    team_logo TEXT,
    wins INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
