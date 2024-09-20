import sqlite3
import pandas as pd

# Função para exibir os dados gerados no banco de dados
def fetch_sensor_data():
    connection = sqlite3.connect('Data/sensors.db')
    query = '''
        SELECT * FROM sensor_data
    '''
    df = pd.read_sql_query(query, connection)
    connection.close()
    print(df)

# Função para exibir os dados gerados de severidade
def fetch_severity_data():
    connection = sqlite3.connect('Data/severidade.db')
    query = '''
        SELECT * FROM severity_data
    '''
    df = pd.read_sql_query(query, connection)
    connection.close()
    print(df)

# Função para exibir os dados gerados de envelope
def fetch_envelope_data():
    connection = sqlite3.connect('Data/envelope.db')
    query = '''
        SELECT * FROM envelope_data
    '''
    df = pd.read_sql_query(query, connection)
    connection.close()
    print(df)

# Chame as funções para exibir os dados gerados
fetch_sensor_data()
fetch_severity_data()
fetch_envelope_data()
