import random
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine

db_url = "postgresql://postgres:1234@localhost:5432/football-game"
engine = create_engine(db_url)

# 1. Генерируем игроков
positions = ['Қорғаушы', 'Жартылай қорғаушы', 'Шабуылшы', 'Қақпашы']
real_names = [
    'Бауыржан Исламхан', 'Асхат Тағыберген', 'Максим Самородов', 'Ислам Чесноков',
    'Абат Айымбетов', 'Игорь Шацкий', 'Алибек Касым', 'Ян Вороговский',
    'Рамазан Оразов', 'Эльхан Астанов', 'Александр Марочкин', 'Темирлан Ерланов',
    'Султанбек Астанов', 'Артур Шушеначев', 'Еркин Тапалов', 'Роман Асранкулов',
    'Марат Быстров', 'Бахтиёр Зайнутдинов', 'Нуралы Алип', 'Лев Скворцов',
    'Иван Свиридов', 'Вячеслав Швырев', 'Андрей Уланов', 'Данил Устименко', 'Никита Пивцов'
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

# 2. Генерируем матчи (около 50 игр)
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

# 3. Генерируем статистику (около 1000 строк в сумме для ТЗ)
# Для каждого матча запишем перформанс всех 25 игроков
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