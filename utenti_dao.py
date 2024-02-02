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

import sqlite3

def elimina_account(current_user_id):
    # Abilita il supporto delle chiavi esterne (senza di questo non vengono abilitate le FK e di conseguenza non riuscivo a sfruttare l'ON DELETE CASCADE settato sulle FK della tabella recensioni)
    pragma_query = 'PRAGMA foreign_keys = ON'
    
    # Query per eliminare l'account
    delete_query = 'DELETE FROM utenti WHERE id = ?'

    connection = sqlite3.connect('db/mangiato.db')
    cursor = connection.cursor()

    success = False

    try:
        # Esegui l'istruzione PRAGMA foreign_keys = ON
        cursor.execute(pragma_query)

        # Esegui l'eliminazione dell'account
        cursor.execute(delete_query, (current_user_id,))
        connection.commit()
        success = True
    except Exception as e:
        print(f'Errore: {e}')
        connection.rollback()
   
    cursor.close()
    connection.close()

    return success
