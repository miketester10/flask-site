# import module
import os
from datetime import date, datetime 
from flask import Flask, flash, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import mangiato_dao, utenti_dao

from model import User


# create the application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'possiamo inserire qualsiasi valore quì' # serve per gestire le sessioni dell'utente

login_manager = LoginManager()
login_manager.init_app(app)

# creo root / per pagina principale Home
@app.route('/')
def index():
  piatti_db = mangiato_dao.get_piatti()
  return render_template('index.html', piatti=piatti_db)

# creo root per piatti singoli, dove in ogni pagina c'è un tipo di piatto e la sua recensione
@app.route('/piatti/<int:id_piatto>')
def piatto_singolo(id_piatto):
  recensioni_db = mangiato_dao.get_recensioni_by_id_piatto(id_piatto)
  piatto_singolo_db = mangiato_dao.get_piatto(id_piatto)
  return render_template('piatti.html', piatto=piatto_singolo_db, recensioni=recensioni_db)

# creo root /about per pagina Chi Siamo
@app.route('/about')
def about():
  return render_template('about.html')

# creo root /contacts per pagina Contatti
@app.route('/contacts')
def contacts():
  return render_template('contacts.html')

# creo root /newrecensione per inserire nuove recensioni dei piatti
@app.route('/newrecensione/<int:id>/', methods=['GET','POST'])
@login_required
def newrecensione(id):

  # estraggo i dati del form
  recensione = request.form.to_dict()

  # validazione dati lato backend
  if recensione['recensione'] == '':
    app.logger.info('La recensione non può essere vuota')
    return redirect(url_for('piatto_singolo', id_piatto=id))
  recensione['data'] = date.today().strftime("%d/%m/%Y")

  # estraggo i dati della foto inserita
  foto = request.files['file']

  # Genera un timestamp per rendere il nome del file univoco, in modo da evitare conflitti se la foto non viene caricata, perchè senno genera un errore di sistema
  timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

  # salvo la foto nella cartella 'static', se la foto è stata inserita nel form
  if foto.filename != '':

      # Combina il timestamp con il nome del file originale
      nome_file_univoco = f"{timestamp}_{foto.filename}"
      
      # Salva la foto nella cartella 'static' con un nome univoco
      foto.save(os.path.join('static', nome_file_univoco))

      # Aggiunge la key 'file' al dizionario assegnandoli il valore 'nome_file_univoco'
      recensione['file'] = nome_file_univoco
  else:
      recensione['file'] = None

  recensione['id_piatto'] = id
  recensione['id_utente'] = current_user.id

  success = mangiato_dao.nuova_recensione(recensione)

  if success:
    flash('Recensione creata correttamente!', 'success')
  else:
    flash('Errore durante la creazione della recensione. Riprova!', 'danger')
  
  return redirect(url_for('piatto_singolo', id_piatto=id))

@app.route('/elimina_recensione/<int:recensione_id>/', methods=['GET','POST'])
@login_required
def elimina_recensione(recensione_id):

  recensione = mangiato_dao.get_recensione_by_recensione_id(recensione_id)
  
  # validazione dati lato backend
  try:
    if current_user.id == recensione['id_utente']:

      # elimino la foto da cartella 'static' se esiste
      if recensione['file']:
        if os.path.exists(os.path.join('static', recensione['file'])):
          os.remove(os.path.join('static', recensione['file']))
          print(f"Il file {(os.path.join('static', recensione['file']))} è stato eliminato.")
        else:
          print(f"Il file {(os.path.join('static', recensione['file']))} non esiste.") 

      success = mangiato_dao.elimina_recensione(recensione_id)

      if success:
        flash('Recensione eliminata correttamente!', 'success')
      else:
        flash('Errore durante l\'eliminazione della recensione. Riprova!', 'danger')

      return redirect(url_for('le_mie_recensioni'))

    else:
      flash('Non sei autorizzato ad eliminare questa recensione!', 'danger')
      return redirect(url_for('le_mie_recensioni'))
  except Exception as e:
    flash('Non sei autorizzato ad eliminare questa recensione!', 'danger')
    return redirect(url_for('le_mie_recensioni'))


# creo root /recensioni per pagina Le mie recensioni
@app.route('/recensioni') # andrebbe chiamato /le_mie_recensioni per coerenza, ma l'ho modificata dopo la root, quindi non voglio cambiare tutti i riferimenti nei template
def le_mie_recensioni():
  recensioni_db = mangiato_dao.get_recensioni(current_user_id=current_user.id)
  return render_template('recensioni.html', recensioni=recensioni_db)

# creo root /iscriviti
@app.route('/iscriviti',methods=['GET','POST'])
def iscriviti():

  # estraggo i dati del form
  iscrizione = request.form.to_dict()

  # validazione dati lato backend
  if iscrizione['nome'] == '':
    app.logger.info('Il nome non può essere vuoto')
    flash('Il nome non può essere vuoto', 'danger')
    return redirect(url_for('index'))
  if iscrizione['cognome'] == '':
    app.logger.info('Il cognome non può essere vuoto')
    flash('Il cognome non può essere vuoto', 'danger')
    return redirect(url_for('index'))
  if iscrizione['username'] == '':
    flash('L\'email non può essere vuota', 'danger')
    return redirect(url_for('index'))
  if iscrizione['matricola'] == '':
    flash('L\'email non può essere vuota', 'danger')
    return redirect(url_for('index'))
  if iscrizione['email'] == '':
    app.logger.info('L\'email non può essere vuota')
    flash('L\'email non può essere vuota', 'danger')
    return redirect(url_for('index'))
  if iscrizione['password'] == '':
    app.logger.info('La password non può essere vuota')
    flash('La password non può essere vuota', 'danger')
    return redirect(url_for('index'))

  # hash della password (rendo la password criptata prima di inviarla al db)
  iscrizione['password'] = generate_password_hash(iscrizione['password'])

  success = utenti_dao.nuovo_utente(iscrizione)

  if success:
    flash('Iscrizione effettuata correttamente!', 'success')
  else:
    flash('Errore durante la registrazione. Riprova!', 'danger')

  print(iscrizione)

  return redirect(url_for('index'))

# creo root /login
@app.route('/login', methods=['GET','POST'])
def login():

  # estraggo i dati del form
  login = request.form.to_dict()
  
  # validazione dati lato backend
  if login['email'] == '':
    app.logger.info('L\'email non può essere vuota')
    flash('L\'email non può essere vuota', 'danger')
    return redirect(url_for('index'))
  if login['password'] == '':
    app.logger.info('La password non può essere vuota')
    flash('La password non può essere vuota', 'danger')
    return redirect(url_for('index'))
  
  utente_db = utenti_dao.get_user_by_email(login['email'])

  if not utente_db or not check_password_hash(utente_db['password'], login['password']): # verifica se l'utente esiste nel db oppure no, oppure (or) se l'utentese esiste verifica se la password corrisponde
    print('L\'utente non esiste')
    flash('Email o password errata!', 'danger')
    return redirect(url_for('index'))
  else:
    new_user = User(id=utente_db['id'], nome=utente_db['nome'], cognome=utente_db['cognome'], username=utente_db['username'], matricola=utente_db['matricola'], email=utente_db['email'], password=utente_db['password'])
    login_user(new_user, True)
    print('Login effettuato')
    flash('Login effettuato', 'success')
    return redirect(url_for('index'))

# carico l'utente (in automatico viene passato l'id dell'utente che ha effettuato il login correttamente alla funzione load_user, ovvero "user_id")
@login_manager.user_loader
def load_user(user_id):
  
  db_user = utenti_dao.get_user_by_id(user_id)

  try:
    user = User(db_user['id'], db_user['nome'], db_user['cognome'], db_user['username'], db_user['matricola'], db_user['email'], db_user['password'])
  except:
    return redirect(url_for('index'))
  
  return user 

# creo root /logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    print('Logout effettuato') # questo messaggio lo stampa nel terminale per noi sviluppatori (lato server)
    flash('Logout effettuato, a presto!', 'success') # questo messaggio viene visualizzato sul browser (lato client, quindi frontend)
    return redirect(url_for('index'))

# creo root /elimina_account (e relative recensioni associate a quell'account)
@app.route("/elimina_account")
@login_required
def elimina_account():
    
    success = utenti_dao.elimina_account(current_user.id)

    if success:
        flash('Account eliminato correttamente!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Errore durante l\'eliminazione dell\'account. Riprova!', 'danger')
    
    return redirect(url_for('index'))