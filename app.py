import logging

from random import randint
import banidb

from flask import Flask, render_template

from flask_ask import Ask, statement,  question, session


app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():

    welcome_msg = render_template('Waheguru ji ka Khalsa, Waheguru ji ki Fateh')
    return statement(welcome_msg)


@ask.intent("Random_Shabad")
def shabad_random():
    random_shabad = banidb.random()['verses'][0]['verse']
    msg = f"Waheguru ji, Here is Random Shabad {random_shabad}"
    return statement(random_shabad)


if __name__ == '__main__':
    app.run()