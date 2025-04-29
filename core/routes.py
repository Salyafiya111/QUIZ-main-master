from flask import Flask,render_template,redirect,url_for,Blueprint,request
from .db import modify_db,query_db

bp = Blueprint('main',__name__)
@bp.route("/")
def index():
    polls = query_db("SELECT * FROM POLL")
    return render_template('index.html',polls=polls)

@bp.route('/poll/create', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        modify_db('INSERT INTO POLL (title, description) VALUES (?, ?)', (title, description))
        return redirect(url_for('main.index'))
    # Обработка GET-запроса - возвращаем форму создания опроса
    return render_template('create_poll.html')

@bp.route('/poll/<int:poll_id>', methods=['GET', 'POST'])
def take_poll(poll_id):
    if request.method == 'POST':
        choice_id = request.form.get('choice')

        if not choice_id:
            return redirect(url_for('main.take_poll', poll_id=poll_id))

        modify_db('UPDATE CHOICES SET votes = votes + 1 WHERE id = ?', (choice_id,))

        # Исправлено имя конечной точки
        return redirect(url_for('main.results', poll_id=poll_id))

    poll = query_db('SELECT * FROM POLL WHERE id = ?', (poll_id,), one=True)
    choices = query_db('SELECT * FROM CHOICES WHERE poll_id = ?', (poll_id,))
    return render_template('quiz.html', poll=poll, choices=choices)

@bp.route('/poll/<int:poll_id>/results')
def results(poll_id):
    poll = query_db('SELECT * FROM POLL WHERE ID = ?',(poll_id,),one = True)
    choices = query_db('SELECT * FROM CHOICES WHERE poll_id = ?',(poll_id,))
    return render_template('results.html',poll = poll,choices = choices)

@bp.route('/poll/<int:poll_id>/add_choice', methods=['GET', 'POST'])
def add_choice(poll_id):
    if request.method == 'POST':
        choice_text = request.form['choice_text']
        modify_db('INSERT INTO CHOICES(poll_id, choice_text, votes) VALUES (?, ?, 0)', (poll_id, choice_text))
        return redirect(url_for('main.take_poll', poll_id=poll_id))
    return render_template('add_choice.html', poll_id=poll_id)
