import sqlite3
from datetime import datetime, timedelta
import random

# Função para criar a tabela de acelerômetros
def create_accelerometer_table():
    connection = sqlite3.connect('Data/sensors.db')
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

# Função para criar a tabela de severidade
def create_severity_table():
    connection = sqlite3.connect('Data/severidade.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS severity_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            severity_value REAL
        )
    ''')
    connection.commit()
    connection.close()

# Função para criar a tabela de envelope
def create_envelope_table():
    connection = sqlite3.connect('Data/envelope.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS envelope_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            envelope_value REAL
        )
    ''')
    connection.commit()
    connection.close()

# Função para inserir dados simulados nos acelerômetros a cada 2 minutos começando dois dias atrás
def insert_accelerometer_data():
    connection = sqlite3.connect('Data/sensors.db')
    cursor = connection.cursor()

    now = datetime.now() - timedelta(days=2)  # Começando 2 dias atrás
    for i in range(0, 2 * 24 * 60, 2):  # 2 dias * 24 horas * 60 minutos, intervalo de 2 minutos
        timestamp = now + timedelta(minutes=i)
        sensor1_value = random.uniform(20, 40)
        sensor2_value = random.uniform(15, 35)
        sensor3_value = random.uniform(10, 30)

        cursor.execute('''
            INSERT INTO sensor_data (timestamp, sensor1_value, sensor2_value, sensor3_value)
            VALUES (?, ?, ?, ?)
        ''', (timestamp.strftime('%Y-%m-%d %H:%M:%S'), sensor1_value, sensor2_value, sensor3_value))

    connection.commit()
    connection.close()

# Função para inserir dados simulados de severidade a cada 2 minutos começando dois dias atrás
def insert_severity_data():
    connection = sqlite3.connect('Data/severidade.db')
    cursor = connection.cursor()

    now = datetime.now() - timedelta(days=2)
    for i in range(0, 2 * 24 * 60, 2):
        timestamp = now + timedelta(minutes=i)
        severity_value = random.uniform(0.5, 5.0)  # Valores simulados de severidade

        cursor.execute('''
            INSERT INTO severity_data (timestamp, severity_value)
            VALUES (?, ?)
        ''', (timestamp.strftime('%Y-%m-%d %H:%M:%S'), severity_value))

    connection.commit()
    connection.close()

# Função para inserir dados simulados de envelope a cada 2 minutos começando dois dias atrás
def insert_envelope_data():
    connection = sqlite3.connect('Data/envelope.db')
    cursor = connection.cursor()

    now = datetime.now() - timedelta(days=2)
    for i in range(0, 2 * 24 * 60, 2):
        timestamp = now + timedelta(minutes=i)
        envelope_value = random.uniform(1.0, 10.0)  # Valores simulados de envelope

        cursor.execute('''
            INSERT INTO envelope_data (timestamp, envelope_value)
            VALUES (?, ?)
        ''', (timestamp.strftime('%Y-%m-%d %H:%M:%S'), envelope_value))

    connection.commit()
    connection.close()

# Criar as tabelas e inserir os dados simulados
create_accelerometer_table()
insert_accelerometer_data()

create_severity_table()
insert_severity_data()

create_envelope_table()
insert_envelope_data()

print("Bancos de dados criados e dados inseridos com sucesso!")
