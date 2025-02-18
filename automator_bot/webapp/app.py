from flask import Flask, render_template, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.achievement_service import AchievementService

app = Flask(__name__)

@app.route('/')
def index():
    # Получаем user_id из параметров запроса
    user_id = request.args.get('user_id', type=int)
    if user_id:
        user_data = AchievementService.get_user_level(user_id)
        return render_template('game.html', user_data=user_data)
    return render_template('game.html')

@app.route('/api/user-stats/<int:user_id>')
def get_user_stats(user_id):
    user_data = AchievementService.get_user_level(user_id)
    return jsonify({
        'level': user_data['level'],
        'exp': user_data['exp'],
        'next_level': user_data['next_level'],
        'achievements': len(user_data['achievements']),
        'days_active': user_data.get('days_active', 7)  # Пока заглушка
    })

@app.route('/api/play-quiz', methods=['POST'])
def play_quiz():
    # Логика викторины
    pass

@app.route('/api/play-image-game', methods=['POST'])
def play_image_game():
    # Логика игры с картинками
    pass

if __name__ == '__main__':
    app.run(debug=True) 