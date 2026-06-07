-- 1
SELECT * FROM matches WHERE venue = 'Home';

-- 2
SELECT * FROM matches WHERE opponent = 'Астана';

-- 3
SELECT * FROM matches WHERE attendance > 15000;

-- 4
SELECT * FROM players WHERE position = 'Шабуылшы';

-- 5
SELECT * FROM players WHERE market_value > 1000000;

-- 6
SELECT opponent, COUNT(*) as match_count
FROM matches
GROUP BY opponent
HAVING COUNT(*) > 3;

-- 7
SELECT venue, AVG(attendance) as avg_attendance
FROM matches
GROUP BY venue
HAVING AVG(attendance) > 10000;

-- 8
SELECT position, AVG(age) as avg_age
FROM players
GROUP BY position
HAVING AVG(age) > 25;

-- 9
SELECT player_id, MAX(goals) as max_goals
FROM player_stats
GROUP BY player_id
HAVING MAX(goals) >= 2;

-- 10
SELECT player_id, AVG(rating) as avg_rating
FROM player_stats
GROUP BY player_id
HAVING AVG(rating) > 7.5;

-- 11
SELECT p.name, s.goals, s.assists
FROM players p
JOIN player_stats s ON p.player_id = s.player_id;

-- 12
SELECT m.match_date, m.opponent, s.rating
FROM matches m
JOIN player_stats s ON m.match_id = s.match_id;

-- 13
SELECT p.name, s.goals
FROM players p
JOIN player_stats s ON p.player_id = s.player_id
WHERE s.goals > 0;

-- 14
SELECT p.name, m.opponent, s.rating
FROM player_stats s
JOIN matches m ON s.match_id = m.match_id
JOIN players p ON s.player_id = p.player_id
WHERE m.venue = 'Home';

-- 15
SELECT p.name, m.opponent, s.assists
FROM player_stats s
JOIN matches m ON s.match_id = m.match_id
JOIN players p ON s.player_id = p.player_id
WHERE m.venue = 'Away' AND s.assists > 0;

-- 16
SELECT p.name, p.market_value, s.rating
FROM players p
JOIN player_stats s ON p.player_id = s.player_id
WHERE p.market_value > 500000;

-- 17
SELECT m.match_date, m.attendance, s.goals
FROM matches m
JOIN player_stats s ON m.match_id = s.match_id
WHERE m.match_date > '2025-01-01';

-- 18
SELECT p.name, p.age, s.goals, s.assists
FROM players p
JOIN player_stats s ON p.player_id = s.player_id
WHERE p.age <= 20;

-- 19
SELECT p.name, s.match_id
FROM players p
LEFT JOIN player_stats s ON p.player_id = s.player_id;

-- 20
SELECT m.opponent, s.rating
FROM player_stats s
RIGHT JOIN matches m ON s.match_id = m.match_id;

-- 21
SELECT match_date, venue, attendance,
       SUM(attendance) OVER(PARTITION BY venue ORDER BY match_date) as cumulative_attendance
FROM matches;

-- 22
SELECT name, position, market_value,
       DENSE_RANK() OVER(PARTITION BY position ORDER BY market_value DESC) as value_rank
FROM players;

-- 23
SELECT name, position, age,
       MAX(age) OVER(PARTITION BY position) as max_age_in_position
FROM players