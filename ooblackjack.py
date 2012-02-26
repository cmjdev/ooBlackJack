#!/usr/bin/python

## Author: Christopher Johnson
## Date..: February 22, 2012
## Rev...: February 25, 2012
##
## CHANGES:
##  - Cleaned up all GUI code
##  - Rewrote and simplified Player class
##  - Added ability to play another round
##
## TODO:
##  - Fix dealer AI when player busts or holds
##  - Write wager system to track games
##  - Implement 'Ace Case' into scoring
##  - Write 'Blackjack' into score module

from Tkinter import *
import random, time

# Class to set up and maintain GUI
class MyApp:

    def __init__(self, parent):
        
        # Create root window and properties
        root = parent
        root.title('ooBlackJack')
        root.geometry('400x300')
        root.resizable(width=FALSE, height=FALSE)
        root.wm_attributes('-topmost', True)

        # Create dealer frame
        dealerFrame = LabelFrame(root, text='Dealer', borderwidth=1)
        dealerFrame.pack(side=TOP, padx=10, pady=5, fill=BOTH)

        # Create dealer canvas for displaying cards
        self.dCanvas = Canvas(dealerFrame, height=90)
        self.dCanvas.pack(fill=BOTH)

        # Create player frame
        playerFrame = LabelFrame(root, text='Player', borderwidth=1)
        playerFrame.pack(side=TOP, padx=10, fill=BOTH)

        # Create player canvas for displaying cards
        self.pCanvas = Canvas(playerFrame, height=100)
        self.pCanvas.pack(side=TOP, fill=BOTH)

        # Create control frame
        controlFrame = Frame(root)
        controlFrame.pack(side=BOTTOM,  padx=10, pady=10,fill=X)

        # Create control buttons
        self.buttonRight = Button(controlFrame, text='Hit Me!', command=self.hitMe)
        self.buttonRight.pack(side=RIGHT)

        self.buttonLeft = Button(controlFrame, text='Stand', command=self.dealerPlay, state=DISABLED)
        self.buttonLeft.pack(side=RIGHT)

        # Create status area
        statusLabel = Label(controlFrame, text='Status: ', fg='grey')
        statusLabel.pack(side=LEFT)

        self.statusText = StringVar(None)
        self.statusText.set('cmjdev.tumblr')
        status = Label(controlFrame, textvariable=self.statusText, fg='grey')
        status.pack(side=LEFT)

    def clearCanvas(self, canvas):
        canvas.delete(ALL)

    def display(self, canvas, hand):

        # Clear canvas
        self.clearCanvas(canvas)
        
        # Set initial card position position
        x=10; x1=60; y=10; y1=80

        # List to determine face card and suit
        face = {0:'K', 1:'A', 11:'J', 12:'Q'}
        suit = {0:'S ', 1:'H ', 2:'C ', 3:'D '}

        for i in range(len(hand)):

            s = '' # Variable to build card information
            value = hand[i] % 13        # determine card value
            whichSuit = hand[i] % 4     # determine card suit

            # Draw blank card
            canvas.create_rectangle(x,y,x1,y1, fill='grey90', outline='grey80')
            
            # Choose color for suit
            s = suit[whichSuit]
            color = ''

            if whichSuit % 2: color='red'
            else: color='grey20'

            # Draw card suit
            canvas.create_text(x1,y1-2, anchor=SE, justify=RIGHT, text=s, fill=color)

            # Check for face card
            if value in face: s = face[value]
            else: s = str(value)

            # Draw card value
            canvas.create_text(x+4,y+3, anchor=NW, text=s, fill=color)

            # Increment position for next card
            x += 60 ; x1 += 60


    def newGame(self):

        # Reset buttons
        self.buttonRight['text'] = 'Hit Me!'
        self.buttonRight['command'] = self.hitMe

        # Reset status
        self.statusText.set('cmjdev.tumblr')

        # Display turn card
        self.clearCanvas(self.pCanvas)
        self.clearCanvas(self.dCanvas)
        
        player.newRound()
        dealer.newRound()

    def hitMe(self):

        self.buttonLeft['state'] = NORMAL
        player.deal()
        self.display(self.pCanvas, player.hand)

        if player.broke:
            self.dealerPlay()
            
    def stand(self): # module for future player status TODO
        
        self.dealerPlay()

    def dealerPlay(self):

        # Disable buttons
        self.buttonLeft['state'] = DISABLED
        self.buttonRight['state'] = DISABLED

        # Play dealer's hand
        dealer.play()
        self.display(self.dCanvas, dealer.hand)
        self.endGame()

    def endGame(self):

        # Determine the winner
        if dealer.broke:
            if player.broke:
                self.statusText.set('All players broke!')
            else: self.statusText.set('You win!')
        elif player.broke:
            self.statusText.set('Dealer wins!')
        elif player.score > dealer.score:
            self.statusText.set('You win!')
        else: self.statusText.set('Dealer wins!')        

        # Change right button for New Game
        self.buttonRight['state'] = NORMAL
        self.buttonRight['text'] = 'Next Round'
        self.buttonRight['command'] = self.newGame


# Class for back-end of game
class Player:

    # Initialize class with player data
    def __init__(self):

        self.broke = False
        self.hold = False
        self.score = 0

        # Initialize a deck of cards
        self.deck = range(1,53)

        # Shuffle the deck
        random.shuffle(self.deck)

        # Assign player an empty hand
        self.hand = []

    # Re-initialize object for new round
    def newRound(self):

        self.__init__()

    # Deal a card to the player's hand
    def deal(self):

        self.hand.append(self.deck.pop())
        self.updateScore()

    # Automatically play hand
    def play(self):

        while(not(self.broke) and not(self.hold)):
            self.deal()

            if self.score >= 17: self.hold = True


    # Update score variable
    def updateScore(self):

        update = self.hand[-1] % 13

        if update == 1: self.score += 11
        elif (update < 1) or (update > 10): self.score += 10
        else: self.score += update

        if self.score > 21: self.broke = True

        
root = Tk()
app = MyApp(root)

player = Player()
dealer = Player()

root.mainloop()