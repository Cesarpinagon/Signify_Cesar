from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Cambia si tu servidor MySQL está en otro lugar
        user='root',  # Cambia por tu nombre de usuario de MySQL
        password='cesar123',  # Cambia por tu contraseña de MySQL
        database='signify'  # Nombre de la base de datos
    )
    return connection

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para el cuestionario
@app.route('/quiz')
def quiz_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM quizzes')
    quiz = cursor.fetchall()  # Obtén todas las preguntas
    cursor.close()
    connection.close()
    return render_template('quiz.html', quiz=quiz)

# Ruta para manejar el envío del cuestionario
@app.route('/submit', methods=['POST'])
def submit():
    correct_answers = {}
    
    # Primero, obtenemos las preguntas y respuestas correctas de la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT id, correct_option FROM quizzes')
    questions = cursor.fetchall()

    for question in questions:
        question_id = f'question{question["id"]}'  # Generar el id de la pregunta
        correct_answers[question_id] = question['correct_option']

    score = 0
    total_questions = len(questions)

    # Verifica las respuestas
    for i in range(total_questions):
        question_key = f'question{i + 1}'
        answer = request.form.get(question_key)
        if answer and int(answer) == correct_answers[question_key]:  # Compara la respuesta con la opción correcta
            score += 1

    cursor.close()
    connection.close()

    # Calcula la calificación
    return render_template('result.html', score=score, total=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
