import sqlite3

def get_piatti():
    
    query = 'SELECT * FROM piatti'
    
    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query)

    piatti = cursor.fetchall()
    print(piatti)

    cursor.close()
    connection.close()

    return piatti

def get_piatto(id):

    query = 'SELECT * FROM piatti WHERE id = ?'
    
    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id,))

    piatto = cursor.fetchone()

    cursor.close()
    connection.close()

    return piatto

# prendo tutte le recensioni filtrando per categoria di piatto es.(Primi, Secondi, Contorni, ecc)
def get_recensioni_by_id_piatto(id_piatto):

    query = '''
                SELECT recensioni.*, utenti.*
                FROM recensioni
                JOIN utenti ON recensioni.id_utente = utenti.id
                WHERE recensioni.id_piatto = ?
                ORDER BY recensioni.data ASC, recensioni.id DESC;
            '''

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id_piatto,))

    recensioni = cursor.fetchall()

    cursor.close()
    connection.close()

    return recensioni

# prendo tutte le recensioni senza filtrare per categoria di piatto
def get_recensioni(current_user_id):

    query = 'SELECT * FROM recensioni WHERE id_utente = ? ORDER BY data ASC, id DESC'
    
    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (current_user_id,))

    recensioni = cursor.fetchall()

    cursor.close()
    connection.close()

    return recensioni

def nuova_recensione(recensione):

    query = 'INSERT INTO recensioni (recensione, data, file, id_piatto, id_utente) VALUES (?, ?, ?, ?, ?)'

    connection = sqlite3.connect('db/mangiato.db')
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (recensione['recensione'], recensione['data'], recensione['file'], recensione['id_piatto'], recensione['id_utente']))
        connection.commit()
        success = True
    except Exception as e:
        print(f'Errore:{e}')
        connection.rollback()  #in caso di errore es.(errore di connessione con il db o altro), devo annullare l'inserimento e tornare allo stato iniziale
    
    cursor.close() # chiude il cursore sia se l'inserimento vada a buon fine oppure no
    connection.close() # chiude la connessione col db sia se l'inserimento vada a buon fine oppure no

    return success

def elimina_recensione(recensione_id):

    query = 'DELETE FROM recensioni WHERE id = ?'

    connection = sqlite3.connect('db/mangiato.db')
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (recensione_id,))
        connection.commit()
        success = True
    except Exception as e:
        print(f'Errore:{e}')
        connection.rollback()  #in caso di errore es.(errore di connessione con il db o altro), devo annullare l'inserimento e tornare allo stato iniziale
    
    cursor.close() # chiude il cursore sia se l'inserimento vada a buon fine oppure no
    connection.close() # chiude la connessione col db sia se l'inserimento vada a buon fine oppure no

    return success

def get_recensione_by_recensione_id(recensione_id):

    query = 'SELECT * FROM recensioni WHERE id = ?'
    
    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (recensione_id,))

    recensione = cursor.fetchone()

    cursor.close()
    connection.close()

    return recensione