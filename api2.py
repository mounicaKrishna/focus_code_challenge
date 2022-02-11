from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mysqlmounika@123',
    port='3306',
    database='focus'
)

app = Flask(__name__)
CORS(app)

@app.route('/port', methods=['GET'])
def func_name():
	return jsonify({'message' : 'It works!'})

def check_question_exists(question):
	cursor = db.cursor()
	cursor.execute('SELECT * FROM ques_and_answer Where Question like "%' + question + '%"')

	questions = cursor.fetchall()

	all_ques = cursor.execute('SELECT * FROM ques_and_answer')
	all_ques_fetch = cursor.fetchall()
	total_ques_count = len(all_ques_fetch)
	return questions,total_ques_count

@app.route('/search-question', methods=['POST'])
def search_question():
	# print("request", request)
	input_json = request.get_json(force=True)
	question_to_search = input_json["question"]
	cursor = db.cursor()
	questions, total_ques_count = check_question_exists(question_to_search)

	output_json = {}
	if len(questions) >0:
		for question in questions:

			output_json["answer 1"] = question[2]
			output_json["answer 2"] = question[3]
			output_json["answer 3"] = question[4]
	else:
		total_ques_count=str(total_ques_count+1)
		cursor.execute('Insert INTO ques_and_answer (id, Question) Values ( CAST(' + total_ques_count +' AS UNSIGNED), "' + question_to_search + '")')
		db.commit()
		output_json["question"] = question_to_search
		output_json["answer 1"] = "This is a New Question, we will get the answers shortly"
	return jsonify(output_json)

@app.route('/update-question', methods=['POST'])
def update_question():
	input_json = request.get_json(force=True)
	question_to_search = input_json["question"]
	answer1 = input_json["answer1"]
	answer2 = input_json["answer2"]
	answer3 = input_json["answer3"]

	cursor = db.cursor()

	questions, total_ques_count = check_question_exists(question_to_search)
	if len(questions) > 0:

		cursor.execute('UPDATE ques_and_answer SET Answer1 = "'+ answer1 + '", Answer2 = "'+ answer2 +'" ,Answer3= "'+ answer3+ '" WHERE Question like "%' + question_to_search + '%"')
		db.commit()
	else:
		total_ques_count = str(total_ques_count + 1)
		cursor.execute('Insert INTO ques_and_answer (id, Question, Answer1, Answer2, Answer3) Values ( CAST(' + total_ques_count +' AS UNSIGNED), "' + question_to_search + '", "'+ answer1 +'", "'+ answer2 +'", "'+ answer3 +'")')
		#  WHERE Question like "%' + question_to_search + '%"
		db.commit()
	output = {"response": "successfull updated the db"}
	return jsonify(output["response"])

if __name__ == '__main__':
	app.run(port=8080)