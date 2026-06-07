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

# 1. Сызықтық график (Линейный — Динамика посещаемости)
plt.figure(figsize=(11, 5))
plt.plot(df['match_date'], df['attendance'], label='Нақты келушілер', color='#333333', alpha=0.3, linestyle=':')
plt.plot(df['match_date'], df['rolling_attendance'], label='Тегістелген тренд (5 ойын)', color='#FFD700', linewidth=3)
plt.title('«Қайрат» матчтарына көрермендердің келу динамикасы', fontsize=14, fontweight='bold')
plt.xlabel('Уақыт')
plt.ylabel('Көрермен саны')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.4)
plt.savefig('dashboard_line.png', dpi=150)
plt.show()

# 2. Дөңгелек диаграмма (Круговая — Үйде vs Қонақта)
labels = df['venue'].value_counts().index
sizes = df['venue'].value_counts().values
colors = ['#FFD700', '#222222']

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}, shadow=True, textprops={'fontweight': 'bold'})
plt.title('Ойындардың өту орны бойынша үлесі', fontsize=13, fontweight='bold')
plt.savefig('dashboard_pie.png', dpi=150)
plt.show()

# 3. Бағанды диаграмма (Столбчатая — ТОП-5 Сұрмергендер)
if 'player_name' in df.columns and 'goals' in df.columns:
    top_players = df.groupby('player_name')['goals'].sum().sort_values(ascending=False).head(5)
    plt.figure(figsize=(10, 5.5))
    plt.bar(top_players.index, top_players.values, color='#FFD700', edgecolor='#222222', linewidth=1.2)
    plt.title('ФК «Қайрат» ТОП-5 үздік сұрмергендері', fontsize=14, fontweight='bold')
    plt.ylabel('Соғылған голдар саны')
    plt.xticks(rotation=20, ha='right', fontsize=10) # Имена развернуты, чтобы не слипались
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig('dashboard_bar.png', dpi=150)
    plt.show()

# 4. Шашырау диаграммасы (Scatter Plot — Рейтинг пен Құны)
plt.figure(figsize=(9, 5))
plt.scatter(df['market_value'], df['rating'], color='#222222', alpha=0.6, edgecolors='#FFD700', s=45)
plt.title('Ойыншының нарықтық құны мен рейтингінің тәуелділігі', fontsize=13, fontweight='bold')
plt.xlabel('Нарықтық құны (Euro)')
plt.ylabel('Рейтинг (Бағалау)')
plt.grid(True, linestyle='--', alpha=0.4)
plt.savefig('dashboard_scatter.png', dpi=150)
plt.show()

# 5. Гистограмма (Таралуы)
if 'goals' in df.columns:
    plt.figure(figsize=(8, 5))
    plt.hist(df['goals'], bins=range(0, int(df['goals'].max()) + 2), align='left', color='#444444', edgecolor='#FFD700', rwidth=0.7)
    plt.title('Матчтардағы соғылған голдар жиілігі', fontsize=13, fontweight='bold')
    plt.xlabel('Соғылған голдар саны')
    plt.ylabel('Матчтар саны')
    plt.xticks(range(0, int(df['goals'].max()) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.savefig('dashboard_hist.png', dpi=150)
    plt.show()

print("Аналитика аяқталды! Барлық графиктер папкаға сақталды.")