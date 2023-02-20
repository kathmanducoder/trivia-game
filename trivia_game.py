#!/usr/bin/env python 

import json
import requests
import sqlite3

# pull in json data from opentdb api url
url = "https://opentdb.com/api.php?amount=25&category=9&type=boolean" 
response = requests.get(url)
data = response.json()

# data['results'] contains a list of dictionaries.
# Each dictionary is a trivia entry and has following keys:
# 	category
#	type
# 	question
# 	correct_answer
# 	incorrect_answers
results = data['results']

######## SQLITE DATABASE SETUP #########
# create sqlite database in RAM
db = sqlite3.connect(':memory:')

# get a cursor object. we will use the cursor to pass sql statements
cursor = db.cursor() 

#create trivia table
#	id 			INTEGER PRIMARY KEY
#	question	TEXT
#	answer		TEXT
cursor.execute('''CREATE TABLE trivia(id INTEGER PRIMARY KEY, question TEXT, answer TEXT)''')
db.commit()

for trivia_entry in results:
  question = trivia_entry['question']
  # replace some html characters in question
  question = question.replace("&quot;", '"')
  question = question.replace("&#039;", "'")
  answer = trivia_entry['correct_answer']
  # insert question and answer to trivia database
  cursor.execute('''INSERT INTO trivia(question,answer) VALUES(?,?)''', (question, answer))

# commit all the insertion to trivia database
db.commit()

print("########################################################")
print()
print("           Welcome to my trivia game.")
print("          Type 'Quit' to end the game.")
print()
print("########################################################")
print()
question_number, total_correct = 0, 0

while (True):
  question_number += 1
  # select a random row from the database
  cursor.execute('''SELECT * FROM trivia ORDER BY RANDOM() LIMIT 1''')
  question, answer = "", ""
  for row in cursor:
    question, answer = row[1], row[2]
  #print question
  print("Question %d: %s True or False?" % (question_number,question))
  user_answer = input("> ")
  if user_answer.lower() == answer.lower():
    print("That's right!")
    total_correct += 1
  elif user_answer.lower() == 'quit':
    print()
    print("Quitting game.")
    question_number -= 1
    break
  else:
    print("Sorry. The correct answer is: %s" % answer)
  print("Score: %d/%d" % (total_correct, question_number))
  print()

final_score_percent = 0
if question_number != 0:
  final_score_percent = (total_correct * 100)/question_number
print("Final Score: %d%% (%d/%d)" % (final_score_percent, total_correct, question_number))	
print()

# close sqlite database
db.close()