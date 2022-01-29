from ctypes import sizeof
from fileinput import filename
import pandas as pd
import time 
import os 

class Card:
    def __init__(self, side1, side2, initialdate):
        self.nextrep_due = initialdate
        self.side_1 = side1
        self.side_2 = side2
        self.box = 0

class Deck:
    def __init__(self, name):
            self.name = os.path.basename(name)[:-4]
            self.cards = []
            self.cardNum = 0
            self.cardDistribution = []
            self.box_number = 4
            self.box_time = [0, 60*10, 60*60*24, 60*60*24*30] # 0, 10 mins, 1 día, 1 mes
            self.cardDistribution = [0 for x in range(self.box_number)]
            self.unpack(name)

    def unpack(self, fileName):

        file_datastruct = pd.read_csv(fileName, header=None)
        #print(file_datastruct)
        if len(file_datastruct.columns) == 4:
            for index, card in file_datastruct.iterrows():
                next_rep = 0
                if type(card[2])==int:
                    next_rep = card[2]
                else:
                    next_rep = int(time.time())

                self.cards.append(Card(card[0], card[1], card[2]))
                self.cardDistribution[card[3]] += 1


        elif len(file_datastruct.columns) == 2:
            for index, card in file_datastruct.iterrows():
                self.cards.append(Card(card[0], card[1], int(time.time())))
        else:
            print('Wrong csv format!')
        
        self.cardNum = len(self.cards)
    
    def nextCard(self):
        if self.cards[0].nextrep_due <=  int(time.time()):
            return self.cards[0].side_1, self.cards[0].side_2
        else:
            return None , None
        
    def response(self, bool_resp):
        if bool_resp == True:
            if  self.cards[0].box < self.box_number-1:
                self.cards[0].box = self.cards[0].box+1
        else:
            self.cards[0].box = 0 
            
        self.cards[0].nextrep_due = int(time.time()) + self.box_time[self.cards[0].box]
        self.cards.sort(key=lambda x: x.nextrep_due)
        
    def save(self):
        
        data = []
        for item in self.cards:
            data.append([item.side_1, item.side_2, item.nextrep_due, item.box])
        savefile = pd.DataFrame(data, columns=['side_1','side_2','next_rep', 'current_box'])

        outname = self.name + '.csv'
        outdir = './saved_decks/'

        if not os.path.exists(outdir):
            os.mkdir(outdir)
        fullname = os.path.join(outdir, outname)    
        
        savefile.to_csv(fullname , header=False, index=False) 





