import sqlite3
import os

# Caminhos para os bancos de dados
DB_PATH_ACCELEROMETER = os.path.join(os.path.dirname(__file__), '..', 'Data', 'sensors.db')
DB_PATH_SEVERITY = os.path.join(os.path.dirname(__file__), '..', 'Data', 'severidade.db')
DB_PATH_ENVELOPE = os.path.join(os.path.dirname(__file__), '..', 'Data', 'envelope.db')

# Função para buscar dados dos sensores de acelerômetro
def fetch_sensor_data(start_timestamp, end_timestamp):
    connection = sqlite3.connect(DB_PATH_ACCELEROMETER)
    cursor = connection.cursor()
    
    # Consulta SQL para selecionar os dados dentro do intervalo de tempo
    query = '''
        SELECT timestamp, sensor1_value, sensor2_value, sensor3_value
        FROM sensor_data
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
    '''
    cursor.execute(query, (start_timestamp, end_timestamp))
    data = cursor.fetchall()
    connection.close()

    return data

# Função para buscar dados de severidade
def fetch_severity_data(start_date=None, end_date=None):
    try:
        connection = sqlite3.connect(DB_PATH_SEVERITY)
        cursor = connection.cursor()

        query = "SELECT timestamp, severity_value FROM severity_data"
        params = ()

        if start_date and end_date:
            query += " WHERE timestamp BETWEEN ? AND ?"
            params = (start_date, end_date)

        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()

        return data
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados de severidade: {e}")
        return []

# Função para buscar dados de envelope
def fetch_envelope_data(start_date=None, end_date=None):
    try:
        connection = sqlite3.connect(DB_PATH_ENVELOPE)
        cursor = connection.cursor()

        query = "SELECT timestamp, envelope_value FROM envelope_data"
        params = ()

        if start_date and end_date:
            query += " WHERE timestamp BETWEEN ? AND ?"
            params = (start_date, end_date)

        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()

        return data
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados de envelope: {e}")
        return []

# Função para ler os acelerômetros do banco de dados
def read_acelerometros_from_db():
    try:
        connection = sqlite3.connect(DB_PATH_ACCELEROMETER)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT id FROM sensor_data")
        acelerometros = cursor.fetchall()
        num_sensors = len(acelerometros)
        acelerometro_names = [f"Acelerômetro {i+1}" for i in range(num_sensors)]
        connection.close()
        return acelerometro_names, num_sensors
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados dos acelerômetros: {e}")
        return [], 0

# Função para atualizar os nomes dos acelerômetros no sistema (apenas para fins de interface)
def update_acelerometro_names(new_names):
    pass
