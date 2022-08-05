#################
#  IMPORTATION  #
#################

from tkinter import *
from random import randint

##################
#  ALL VARIABLE  #
##################



###########
#  CLASS  #
###########

class MainFrame():
    def __init__(self, application, gui):
        space = Label(gui, text = "", font = ("Courier", 80)).pack()
        self.nameOfGame = Label(gui, text = "SNAKE", font = ("Courier", 50), bg = "black", fg = "yellow").pack()
        space = Label(gui, text = "", font = ("Courier", 120)).pack()
        self.playButton = Button(gui, text = "PLAY", font = ("Courier", 30), bg = "black", fg = "blue", command = lambda : self.playGame(application, gui)).pack()
        space = Label(gui, text = "", font = ("Courier", 10)).pack()
        self.leaveButton = Button(gui, text = "LEAVE", font = ("Courier", 20), bg = "black", fg = "green", command = application.destroy).pack()
        
        
    def playGame(self, application, gui):
        self.deleteDisplay(gui)
        
        playFrame = Frame()
        playFrame.pack()
        gameCanvas = GameFrame(application, playFrame)        
        
        
    def deleteDisplay(self, gui):
        gui.destroy()


class GameFrame():
    def __init__(self, application, gui):
        self.gameCanvas = Canvas(gui, height = 400, width = 400, bg = "green")
        self.gameCanvas.pack()
        self.infoCanvas = Canvas(gui, height = 100, width = 600, bg = "yellow")
        self.infoCanvas.pack()
        
        self.leaveButton = Button(gui, text = "<- RETURN TO MAIN MENU", font = ("Courier", 10), bg = "red", command = lambda : self.leaveGame(application, gui)).place(x = 0, y = 406)
        
        
        self.direction = [1,0] ### HELP FOR DIRECTION : direction[0] -> right-left  direction[1] -> up-down ; 1 = movement, 0 = no movement ###
        self.playerSpeed = 400 ### The speed variable is in milliseconds  
        

        self.playerParts = [[self.gameCanvas.create_oval(40, 40, 80, 80, fill = "black", outline = "blue"), [40,40]]]
    
    
    
        application.bind("<Right>", self.right)
        application.bind("<Left>", self.left)
        application.bind("<Down>", self.down)
        application.bind("<Up>", self.up)
        
        
        
        self.x_apple = randint(1,9)*40
        self.y_apple = randint(1,9)*40
        self.apple = self.gameCanvas.create_rectangle(self.x_apple, self.y_apple, self.x_apple+40, self.y_apple+40, fill = "black", outline = "red")
        
        
        self.appleCaught = 0
        self.infoAppleCaught = self.infoCanvas.create_text(50, 50, text = str(self.appleCaught))
    
        
        self.isPlaying = True
        self.play(application, gui)
        
        
    def GetXPlayer(self):
        return self.playerParts[0][1][0]
    def GetYPlayer(self):
        return self.playerParts[0][1][1]
        

    def SetDirection(self, event, value):
        self.direction = value
        
    def right(self, event):
        if self.direction != [-1,0] or len(self.playerParts) <= 1 :
            self.SetDirection(event, [1,0])            
    def left(self, event):
        if self.direction != [1,0] or len(self.playerParts) <= 1:
            self.SetDirection(event, [-1,0])
    def down(self, event):
        if self.direction != [0,-1] or len(self.playerParts) <= 1:
            self.SetDirection(event, [0,1])
    def up(self, event):
        if self.direction != [0,1] or len(self.playerParts) <= 1:
            self.SetDirection(event, [0,-1])


    def GetPlayerSpeed(self):
        return self.playerSpeed
    
        
        
    def leaveGame(self, application, gui):
        self.isPlaying = False
        self.deleteDisplay(gui)
        
        mainFrame = Frame()
        mainFrame.pack()
        mainCanvas = MainFrame(application, mainFrame)
        
    
    def loseGame(self, application, gui, infoDeath, score):
        self.isPlaying = False
        self.deleteDisplay(gui)
        
        loseFrame = Frame()
        loseFrame.pack()
        loseFrame = LoseFrame(application, loseFrame, infoDeath, score)
        
        
    def deleteDisplay(self, gui):
        gui.destroy()
        
        
    
    def play(self, application, gui):            
        
        ### MOVE THE PLAYER ### 
        
        # BODY #
        for i in range(len(self.playerParts)-1, 0, -1):
            self.playerParts[i][1][0] = self.playerParts[i-1][1][0]
            self.playerParts[i][1][1] = self.playerParts[i-1][1][1]
            
            self.gameCanvas.delete(self.playerParts[i][0])
            self.playerParts[i][0] = self.gameCanvas.create_rectangle(self.playerParts[i][1][0], self.playerParts[i][1][1], self.playerParts[i][1][0]+40, self.playerParts[i][1][1]+40, fill = "black", outline = "blue")
        
        # HEAD #
        self.playerParts[0][1][0] += 40*self.direction[0]
        self.playerParts[0][1][1] += 40*self.direction[1]
        
        self.gameCanvas.delete(self.playerParts[0][0])
        self.playerParts[0][0] = self.gameCanvas.create_oval(self.playerParts[0][1][0], self.playerParts[0][1][1], self.playerParts[0][1][0]+40, self.playerParts[0][1][1]+40, fill = "black", outline = "blue")
        
        
        ### DEATH ###
        
        # CHECK IF THE SNAKE ISN'T OUT OF MAP #
        
        if (self.playerParts[0][1][0] < 0 or 400 <= self.playerParts[0][1][0]) or (self.playerParts[0][1][1] < 0 or 400 <= self.playerParts[0][1][1]):
            self.loseGame(application, gui, "You were out of the map !", self.appleCaught)
            
        # CHECK IF THE SNAKE IS TOUCHING HIMSELF BY HIS HEAD
            
        for i in range(1, len(self.playerParts)):
            if (self.playerParts[i][1][0] == self.playerParts[0][1][0] and self.playerParts[i][1][1] == self.playerParts[0][1][1]):
                self.loseGame(application, gui, "You touched your body with your head !", self.appleCaught)
            
        ### MOVE THE APPLE ###
        
        self.gameCanvas.delete(self.apple)
        if self.GetXPlayer() == self.x_apple and self.GetYPlayer() == self.y_apple :
            self.x_apple = randint(0,9)*40
            self.y_apple = randint(0,9)*40
            self.appleCaught += 1
            
            ## DISPLAY NEW PART OF SNAKE -> MATHEMATIQUES ##
            self.playerParts.append([self.gameCanvas.create_rectangle(0, 0, 0 , 0), [self.playerParts[-1][1][0] - self.direction[0] * 40, self.playerParts[-1][1][1] - self.direction[1] * 40]])
            
        self.apple = self.gameCanvas.create_rectangle(self.x_apple, self.y_apple, self.x_apple+40, self.y_apple+40, fill = "black", outline = "red")

        
        ### DISPLAY ADVANCEMENT OF THE GAME
        self.infoCanvas.itemconfig(self.infoAppleCaught, text = str(self.appleCaught))
        
        
        
        if self.isPlaying :
            application.after(self.GetPlayerSpeed(), lambda : self.play(application, gui))
        
    
    
class LoseFrame():
    def __init__(self, application, gui, infoDeath, score):
        space = Label(gui, text = "", font = ("Courier", 80)).pack()
        self.infoLosing = Label(gui, text = "YOU LOSE !", font = ("Courier", 30), bg = "black", fg = "red").pack()
        space = Label(gui, text = "", font = ("Courier", 30)).pack()
        self.infoDeath = Label(gui, text = infoDeath, font = ("Courier", 16), bg = "black", fg = "red").pack()
        space = Label(gui, text = "", font = ("Courier", 30)).pack()
        self.infoScore = Label(gui, text = "SCORE : " + str(score), font = ("Courier", 20), bg = "black", fg = "red").pack()
        space = Label(gui, text = "", font = ("Courier", 100)).pack()
        
        self.playCanvas = Canvas(gui, height = 50, width = 300)
        self.playCanvas.pack()
        
        self.mainMenuButton = Button(self.playCanvas, text = "MAIN MENU", font = ("Courier", 16), bg = "black", fg = "blue", command = lambda : self.MainMenu(gui)).place(x = 2, y = 6)
        self.playAgainButton = Button(self.playCanvas, text = "PLAY AGAIN", font = ("Courier", 16), bg = "black", fg = "blue", command = lambda : self.PlayAgain(application, gui)).place(x = 152, y = 6)
        
    
    def MainMenu(self, gui):
        self.deleteDisplay(gui)
        
        mainFrame = Frame(window)
        mainFrame.pack()
        mainCanvas = MainFrame(window, mainFrame)
        
    def PlayAgain(self, application, gui):
        self.deleteDisplay(gui)
    
        playFrame = Frame()
        playFrame.pack()
        gameCanvas = GameFrame(application, playFrame)  
        
    def deleteDisplay(self, gui):
        gui.destroy()
            

#############
#  DISPLAY  #
#############

window = Tk()
window.title("SNAKE")
window.geometry("600x600")
window.resizable(0,0)


mainFrame = Frame(window)
mainFrame.pack()
mainCanvas = MainFrame(window, mainFrame)


window.mainloop()
