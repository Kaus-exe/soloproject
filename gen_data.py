import random
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine

db_url = "postgresql://postgres:1234@localhost:5432/football-game"
engine = create_engine(db_url)

positions = ['Қорғаушы', 'Жартылай қорғаушы', 'Шабуылшы', 'Қақпашы']
real_names = [
    'Бауыржан Исламхан', 'Жоао Пауло', 'Вадим Ульянов', 'Элдер Сантана',
    'Олжас Байбек', 'Александр Мартынович', 'Егор Ткаченко', 'Ян Вороговский',
    'Рамазан Оразов', 'Гиорги Зария', 'Дмитрий Сергеев', 'Андрей Уланов',
    'Султанбек Астанов', 'Артур Шушеначев', 'Еркебулан Сейдахмет', 'Лев Кургин',
    'Марат Быстров', 'Бахтиёр Зайнутдинов', 'Нуралы Алип', 'Адилет Садыбеков',
    'Иван Свиридов', 'Вячеслав Швырев', 'Валерий Громыко', 'Данил Устименко', 'Лука Гадрани'
]

players_list = []
for i in range(25):
    players_list.append({
        'name': real_names[i],
        'position': random.choice(positions),
        'age': random.randint(18, 35),
        'market_value': random.randint(200000, 2000000)
    })
df_players = pd.DataFrame(players_list)


opponents = ['Астана', 'Тобол', 'Ордабасы', 'Актобе', 'Шахтер', 'Елимай', 'Жетысу']
matches_list = []
start_date = datetime(2025, 1, 1)

for i in range(1, 51):
    venue = random.choice(['Home', 'Away'])
    attendance = random.randint(8000, 23000) if venue == 'Home' else random.randint(2000, 10000)
    current_date = start_date + timedelta(days=i * 7)

    matches_list.append({
        'match_date': current_date.strftime('%Y-%m-%d'),
        'opponent': random.choice(opponents),
        'venue': venue,
        'attendance': attendance
    })
df_matches = pd.DataFrame(matches_list)
df_matches.to_sql('matches', engine, if_exists='append', index=False)

stats_list = []
for m_id in range(1, 51):
    for p_id in range(1, 26):
        stats_list.append({
            'match_id': m_id,
            'player_id': p_id,
            'goals': random.choices([0, 1, 2], weights=[85, 12, 3])[0],
            'assists': random.choices([0, 1], weights=[90, 10])[0],
            'rating': round(random.uniform(5.0, 9.5), 1)
        })
df_stats = pd.DataFrame(stats_list)
df_stats.to_sql('player_stats', engine, if_exists='append', index=False)

print("База данных успешно заполнена! Сгенерировано более 1000 строк.")