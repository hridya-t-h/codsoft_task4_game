from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    rounds = session.get('rounds')
    user_score = session.get('user_score', 0)
    computer_score = session.get('computer_score', 0)
    user_choice = session.get('user_choice')
    computer_choice = session.get('computer_choice')
    result = session.get('result')
    final_result = session.get('final_result')

    return render_template(
        'index.html', 
        rounds=rounds, 
        user_score=user_score, 
        computer_score=computer_score, 
        user_choice=user_choice, 
        computer_choice=computer_choice,
        result=result,
        final_result=final_result
    )

@app.route('/start_game', methods=['POST'])
def start_game():
    rounds = int(request.form['rounds'])
    session['rounds'] = rounds
    session['user_score'] = 0
    session['computer_score'] = 0
    session['user_choice'] = None
    session['computer_choice'] = None
    session['result'] = None
    session['final_result'] = None

    return redirect(url_for('index'))

@app.route('/play', methods=['POST'])
def play():
    if 'rounds' not in session or session['rounds'] <= 0:
        return redirect(url_for('index'))

    user_choice = request.form['choice']
    computer_choice = random.choice(['rock', 'paper', 'scissors'])
    result = determine_winner(user_choice, computer_choice)

    session['user_choice'] = user_choice
    session['computer_choice'] = computer_choice
    session['result'] = result

    if result == 'user':
        session['user_score'] += 1
    elif result == 'computer':
        session['computer_score'] += 1

    session['rounds'] -= 1

    if session['rounds'] == 0:
        if session['user_score'] > session['computer_score']:
            session['final_result'] = 'You win the game!'
        elif session['user_score'] < session['computer_score']:
            session['final_result'] = 'Computer wins the game!'
        else:
            session['final_result'] = 'It\'s a tie!'

    return redirect(url_for('index'))

@app.route('/new_game', methods=['POST'])
def new_game():
    session.pop('rounds', None)
    session.pop('user_score', None)
    session.pop('computer_score', None)
    session.pop('user_choice', None)
    session.pop('computer_choice', None)
    session.pop('result', None)
    session.pop('final_result', None)

    return redirect(url_for('index'))

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        return 'user'
    else:
        return 'computer'

if __name__ == "__main__":
    app.run(debug=True)
