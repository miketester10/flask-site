import sqlite3
 
# inserisco un nuovo utente registrato nel db
def nuovo_utente(iscrizione):

    query = 'INSERT INTO utenti (nome, cognome, username, matricola, email, password) VALUES (?,?,?,?,?,?)'

    connection = sqlite3.connect('db/mangiato.db')
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (iscrizione['nome'], iscrizione['cognome'], iscrizione['username'].lower(), iscrizione['matricola'], iscrizione['email'], iscrizione['password']))
        connection.commit()
        success = True
    except Exception as e:
        print(f'Errore:{e}')
        connection.rollback()  #in caso di errore es.(errore di connessione con il db o altro), devo annullare l'inserimento e tornare allo stato iniziale
    
    cursor.close() # chiude il cursore sia se l'inserimento vada a buon fine oppure no
    connection.close() # chiude la connessione col db sia se l'inserimento vada a buon fine oppure no  

    return success

# ottengo un utente dal db by id
def get_user_by_id(user_id):

    query = 'SELECT * FROM utenti WHERE id = ?'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user

# ottengo un utente dal db by email
def get_user_by_email(email_del_login):

    query = 'SELECT * FROM utenti WHERE email = ?'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (email_del_login,))

    risultato = cursor.fetchone()

    cursor.close()
    connection.close()

    return risultato

def elimina_account(current_user_id):

    query_utente = 'DELETE FROM utenti WHERE id = ?'
    query_recensioni = 'DELETE FROM recensioni WHERE id_utente = ?'

    connection = sqlite3.connect('db/mangiato.db')
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query_utente, (current_user_id,))
        cursor.execute(query_recensioni, (current_user_id,))
        connection.commit()
        success = True
    except Exception as e:
        print(f'Errore:{e}')
        connection.rollback()  #in caso di errore es.(errore di connessione con il db o altro), devo annullare l'eliminazione e tornare allo stato iniziale
    
    cursor.close() # chiude il cursore sia se l'eliminazione vada a buon fine oppure no
    connection.close() # chiude la connessione col db sia se l'eliminazione vada a buon fine oppure no  
    
    return success