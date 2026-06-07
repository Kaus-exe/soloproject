
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    age INTEGER CHECK (age > 0),
    market_value NUMERIC(12, 2) CHECK (market_value >= 0)
);


CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    opponent VARCHAR(100) NOT NULL,
    venue VARCHAR(10) NOT NULL CHECK (venue IN ('Home', 'Away')),
    attendance INTEGER CHECK (attendance >= 0)
);

CREATE TABLE player_stats (
    stat_id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(match_id) ON DELETE CASCADE,
    player_id INTEGER REFERENCES players(player_id) ON DELETE CASCADE,
    goals INTEGER DEFAULT 0 CHECK (goals >= 0),
    assists INTEGER DEFAULT 0 CHECK (assists >= 0),
    rating NUMERIC(3, 1) CHECK (rating >= 0.0 AND rating <= 10.0)
);