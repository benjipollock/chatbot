"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import datetime
from random import randint


@route('/', method='GET')
def index():
    return template("chatbot.html")

jokes = ["Can a kangaroo jump higher than a house? Of course, a house doesn’t jump at all.",
         "My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.",
         "Scientists have now discovered how women keep their secrets. They do so within groups of 40."
         ]


def check_rules(user_message):
    curse_words = ['shit', 'fuck', 'bitch']
    for word in user_message.split(" "):
        if word in curse_words:
            return {"animation": "no", "msg": "Don't say " + word + ". That's a curse word"}
    return None


def check_type_answer(user_message):
    if '?' in user_message:
        type_answer = 'question'
    elif '!' in user_message:
        type_answer = 'exclamation'
    elif '.' in user_message:
        type_answer = 'statement'
    else:
        type_answer = 'statement'
    return type_answer


def evaluate_questions(user_message):
    if 'how' in user_message and 'you' in user_message:
        return {"animation": "giggling", "msg": "I'm great! How are you?"}
    if 'time' in user_message:
        return {"animation": "waiting", "msg": "The time is: " + str(datetime.datetime.now().time())}
    if 'laugh' in user_message or 'joke' in user_message:
        return {"animation": "laughing", "msg": "Here's a joke for you: " + jokes[randint(0, len(jokes)-1)]}
    return {"animation": "confused", "msg": "hmmmmm"}


def evaluate_exclamations():
    return {"animation": "takeoff", "msg": "Don't shout at me!"}


def evaluate_statements(user_message):
    if 'sad' in user_message or 'cry' in user_message:
        return {"animation": "crying", "msg": "Don't worry, be happy"}
    if 'happy' in user_message or 'glad' in user_message or 'good' in user_message or 'great' in user_message:
        return {"animation": "excited", "msg": "Awesome!!"}
    if 'love' in user_message or 'heart' in user_message:
        return {"animation": "inlove", "msg": "Love is great"}
    if 'angry' in user_message or 'mad' in user_message:
        return {"animation": "afraid", "msg": "No need to be mad."}
    if 'laugh' in user_message or 'joke' in user_message:
        return {"animation": "giggling", "msg": "Here's a joke for you: " + jokes[randint(0, len(jokes)-1)]}
    return {"animation": "confused", "msg": "hmmmmm"}


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg').lower()
    # print(user_message)
    answer = check_rules(user_message)
    # print(answer)
    if not answer:
        print(json.dumps(answer))
        if check_type_answer(user_message) == 'question':
            answer = evaluate_questions(user_message)
        elif check_type_answer(user_message) == 'exclamation':
            answer = evaluate_exclamations()
        elif check_type_answer(user_message) == 'statement':
            answer = evaluate_statements(user_message)
    if not answer:
        answer = {"animation": "no", "msg": "I don't understand"}
    return json.dumps(answer)


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
