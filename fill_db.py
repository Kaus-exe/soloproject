import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

db_url = "postgresql://postgres:1234@localhost:5432/football-game"
engine = create_engine(db_url)

query = """
SELECT m.match_date, m.opponent, m.venue, m.attendance, 
       p.name as player_name, p.position, p.market_value,
       s.goals, s.assists, s.rating
FROM player_stats s
JOIN matches m ON s.match_id = m.match_id
JOIN players p ON s.player_id = p.player_id
ORDER BY m.match_date;
"""
df = pd.read_sql(query, engine)

df['match_date'] = pd.to_datetime(df['match_date'])
df = df.sort_values(by='match_date').reset_index(drop=True)

df['rolling_attendance'] = df['attendance'].rolling(window=5).mean()
df['attendance_change_pct'] = df['attendance'].pct_change() * 100

pivot_attendance = df.pivot_table(
    values='attendance',
    index='opponent',
    columns='venue',
    aggfunc='mean'
)
print(pivot_attendance)

plt.figure(figsize=(12, 6))
plt.plot(df['match_date'], df['attendance'], label='Нақты келушілер', color='lightgray', alpha=0.5)
plt.plot(df['match_date'], df['rolling_attendance'], label='Тегістелген тренд (5 ойын)', color='gold', linewidth=3)
plt.title('«Қайрат» матчтарына көрермендердің келу динамикасы', fontsize=16)
plt.xlabel('Уақыт (Күндер)')
plt.ylabel('Көрермен саны')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

labels = df['venue'].value_counts().index
sizes = df['venue'].value_counts().values
colors = ['#ffcc00', '#333333']

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, shadow=True)
plt.title('Ойындардың өту орны бойынша үлесі (Үйде vs Қонақта)')
plt.show()

if 'player_name' in df.columns and 'goals' in df.columns:
    top_players = df.groupby('player_name')['goals'].sum().sort_values(ascending=False).head(5)
    plt.figure(figsize=(10, 5))
    plt.bar(top_players.index, top_players.values, color='gold', edgecolor='black')
    plt.title('ФК «Қайрат» ТОП-5 үздік сұрмергендері', fontsize=14)
    plt.xlabel('Ойыншының аты-жөні')
    plt.ylabel('Соғылған голдар саны')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df['market_value'], df['rating'], color='black', alpha=0.6, edgecolors='gold')
plt.title('Ойыншының нарықтық құны мен рейтингінің тәуелділігі', fontsize=14)
plt.xlabel('Нарықтық құны')
plt.ylabel('Рейтинг (Бағалау)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

if 'goals' in df.columns:
    plt.figure(figsize=(8, 5))
    plt.hist(df['goals'], bins=range(0, int(df['goals'].max()) + 2), align='left', color='lightgray', edgecolor='black', rwidth=0.8)
    plt.title('Матчтардағы соғылған голдар жиілігі (Таралуы)', fontsize=14)
    plt.xlabel('Соғылған голдар саны')
    plt.ylabel('Матчтар саны')
    plt.xticks(range(0, int(df['goals'].max()) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

print("Аналитика аяқталды! Графиктер көрсетілді.")