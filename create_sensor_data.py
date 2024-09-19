import sqlite3
from datetime import datetime, timedelta
import random

# Função para criar a tabela se não existir
def create_table():
    connection = sqlite3.connect('sensors.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            sensor1_value REAL,
            sensor2_value REAL,
            sensor3_value REAL
        )
    ''')
    connection.commit()
    connection.close()

# Função para inserir dados simulados para os últimos 7 dias com intervalo de minuto a minuto
def insert_linear_data():
    connection = sqlite3.connect('sensors.db')
    cursor = connection.cursor()

    # Data e hora atuais
    now = datetime.now()

    # Parâmetros para simulação de vibração
    base_value = 20  # Valor base da vibração
    linear_trend = 0.001  # Tendência linear suave para os valores
    noise_level = 0.1  # Nível de ruído aleatório pequeno

    # Inserir dados para os últimos 7 dias, a cada minuto
    for i in range(7 * 24 * 60):  # 7 dias * 24 horas * 60 minutos
        timestamp = now - timedelta(minutes=i)
        trend = base_value + (linear_trend * i)  # Tendência linear
        sensor1_value = trend + random.uniform(-noise_level, noise_level)  # Pequenas variações aleatórias
        sensor2_value = trend + random.uniform(-noise_level, noise_level)
        sensor3_value = trend + random.uniform(-noise_level, noise_level)

        cursor.execute('''
            INSERT INTO sensor_data (timestamp, sensor1_value, sensor2_value, sensor3_value)
            VALUES (?, ?, ?, ?)
        ''', (timestamp.strftime('%Y-%m-%d %H:%M:%S'), sensor1_value, sensor2_value, sensor3_value))

    connection.commit()
    connection.close()

# Criar a tabela e inserir os dados simulados
create_table()
insert_linear_data()
print("Dados lineares inseridos com sucesso!")
