

import cards
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from os import listdir
from os.path import isfile, join
import os

new_stack = button_dialog(
    title='Welcome to SRS lite',
    text='',
    buttons=[
        ('New stack', True),
        ('Load Stack', False),
    ],
).run()

if new_stack == True:
    
    mypath = os.getcwd()
    onlyfiles = [(f,f) for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:]==".csv"]

    address = radiolist_dialog(
        title="New deck",
        text="Which CSV file would you like to open?",
        values= onlyfiles
    ).run()

    mydeck = cards.Deck(address)
    message_dialog(
    title='New deck',
    text='Your new deck has ' + str(mydeck.cardNum) + ' cards').run()

else:
    mypath = os.getcwd() + "/saved_decks/"

    if not os.path.exists('./saved_decks/'):
        os.mkdir('./saved_decks/')

    onlyfiles = [(f,f) for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:]==".csv"]

    address = radiolist_dialog(
        title="New deck",
        text="Which CSV file would you like to open?",
        values= onlyfiles
    ).run()
    mydeck = cards.Deck('./saved_decks/' + address)
    
    cards_progress=mydeck.cardDistribution
    colors = ['red', 'yellow', 'green', 'blue']
    message = 'Your deck has ' + str(mydeck.cardNum) + ' cards \nOf which:'
    for i in range(len(cards_progress)):
        extra_text =  f'\n <style bg="{colors[i]}"> {cards_progress[i]} are at in box n.{i+1}</style>'
        message = message + extra_text


    message_dialog(
    title='New deck',
    text=HTML(message)).run()
    

keep_going=True

while keep_going:
    mycard = mydeck.nextCard()
    if mycard != (None, None):
        message_dialog(
            title='Card',
            text=mycard[0]).run()

        result = button_dialog(
            title='Button dialog example',
            text=mycard[1],
            buttons=[
                ('Yes', True),
                ('No', False),
                ('Quit', None)
            ],
        ).run()

        if result == None:
            keep_going=False
        else:
            mydeck.response(result)
        mydeck.save()
    else:
        message_dialog(
            title='Card',
            text="You've run out of cards to study!").run()
        keep_going=False
