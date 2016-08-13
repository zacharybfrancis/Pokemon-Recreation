#Pokemon
#Zachary Francis zbf Section N

from tkinter import *
import random
import string
from PIL import Image
from PIL import ImageTk

class Button(object):

    def __init__(self, x, y, sizeX, sizeY, pokemonOrText, useButtonLogo):
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.selected = False
        self.pokemon = pokemonOrText
        self.logoButton = useButtonLogo
        self.fill = "white"

    def isPressed(self, x, y):
        if(x > self.x and x < self.x+self.sizeX and y > self.y and
            y < self.y+self.sizeY):
            return True
        return False

    def draw(self, canvas):
        if(self.selected):
            if(isinstance(self.pokemon, FireType)):
                self.fill = "orange"
            elif(isinstance(self.pokemon, WaterType)):
                self.fill = "deepskyblue"
            elif(isinstance(self.pokemon, LeafType)):
                self.fill = "green"
            elif(isinstance(self.pokemon, ElectricType)):
                self.fill = "yellow"
        else:
            self.fill = "white"
        canvas.create_rectangle(self.x, self.y, self.x+self.sizeX,
                                self.y+self.sizeY, fill=self.fill)
        self.pokemon.draw(canvas, self.x+(self.sizeX/2), self.y+(self.sizeY/2))

    def drawNormalButton(self, canvas):
        if(self.logoButton):
            image = Image.open("button.gif")
            maxSize = (self.sizeX, self.sizeY)
            image.thumbnail(maxSize, Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(image)
            self.image = tkimage
            canvas.create_image(self.x+(self.sizeX/2), self.y+(self.sizeY/2),
                                anchor="center", image=self.image)
            canvas.create_text(self.x+(self.sizeX/2), self.y+(self.sizeY/2),
                                text="%s" % self.pokemon)
        else:
            canvas.create_rectangle(self.x, self.y, self.x+self.sizeX,
                                    self.y+self.sizeY, fill="white")
            canvas.create_text(self.x+(self.sizeX/2), self.y+(self.sizeY/2),
                                text="%s" % self.pokemon, fill=self.fill)

class Player(object):

    def __init__(self, fileName, data):
        self.x = data.width/2
        self.y = data.height/2
        self.size = 25
        self.pokemon = []
        self.starter = None
        self.file = fileName
        self.healthPotions = 0
        self.strengthPotions = 0

    def replenishPokemon(self):
        for pokemon in self.pokemon:
            if(pokemon.health > 0):
                pokemon.resetStats()

    def getCoordinates(self):
        return (self.x, self.y)

    def move(self, dirX, dirY, data):
        if(dirX == 0 and dirY == -1):
            move = self.y - 25
            if(move >= 0):
                self.file = "walkingAway.gif"
                self.y = move
        elif(dirX == 0 and dirY == 1):
            move = self.y + 25
            if(move+25 <= data.height):
                self.file = "walkingForward.gif"
                self.y = move
        elif(dirX == -1 and dirY == 0):
            move = self.x - 25
            if(move >= 0):
                self.file = "walkingLeft.gif"
                self.x = move
        elif(dirX == 1 and dirY == 0):
            move = self.x + 25
            if(move+25 <= data.width):
                self.file = "walkingRight.gif"
                self.x = move

    def draw(self, canvas):
        image = Image.open(self.file)
        maxSize = (25, 25)
        image.thumbnail(maxSize, Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)
        self.image = tkimage
        canvas.create_image(self.x+(25/2), self.y+(25/2), anchor="center",
                            image=self.image)

class Pokemon(object):

    def __init__(self, name, ownedByPlayer, fileName):
        self.name = name
        self.owned = ownedByPlayer
        self.size = 50
        self.health = 100
        self.strength = ""
        self.fill = None
        self.defenseUp = False
        self.strengthAttacks = 4
        self.file = fileName

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def resetStats(self):
        self.health = 100
        self.strengthAttacks = 4
        self.resetDefense()

    def combatAttackTest(self, opponent):
        if(opponent.defenseUp):
            return 5
        else:
            return 10

    def attackWithStrengthTest(self, opponent):
        if(opponent.defenseUp):
            if(opponent.strength == self.strength or
                opponent.strength in self.weakness):
                return 0
            elif(self.strength in opponent.weakness):
                return 10
            else:
                return 7
        else:
            if(opponent.strength == self.strength or
                opponent.strength in self.weakness):
                return 2
            elif(self.strength in opponent.weakness):
                return 20
            else:
                return 15

    def aiMove(self, opponent):
        moveScores = dict()
        defense = False
        if(self.strengthAttacks > 0):
            moveScores["attackWithStrength"] = self.attackWithStrengthTest(
                                                                    opponent)
        moveScores["combatAttack"] = self.combatAttackTest(opponent)
        if(self.health < 30):
            defense = True
        if(defense):
            key = max(moveScores)
            return random.choice(["defenseUp", key])
        else:
            r = random.randint(1,3)
            if(r > 1): return max(moveScores)
            else: return min(moveScores)

    def combatAttackAI(self, opponent):
        if(opponent.defenseUp):
            damage = random.randint(2,5)
            opponent.health -= damage
        else:
            damage = random.randint(7,10)
            opponent.health -= damage

    def attackWithStrengthAI(self, opponent):
        if(opponent.defenseUp):
            if(opponent.strength == self.strength or
                opponent.strength in self.weakness):
                opponent.health -= 0
            elif(self.strength in opponent.weakness):
                damage = random.randint(7,10)
                opponent.health -= damage
            else:
                damage = random.randint(4,7)
                opponent.health -= damage
        else:
            if(opponent.strength == self.strength or
                opponent.strength in self.weakness):
                damage = random.randint(0,2)
                opponent.health -= damage
            elif(self.strength in opponent.weakness):
                damage = random.randint(17,20)
                opponent.health -= damage
            else:
                damage = random.randint(12,15)
                opponent.health -= damage
        self.strengthAttacks -= 1

    def combatAttack(self, opponent):
        if(opponent.defenseUp):
            opponent.health -= 7
        else:
            opponent.health -= 12

    def attackWithStrength(self, opponent):
        if(opponent.defenseUp):
            if(opponent.strength == self.strength or
                opponent.strength in self.weakness):
                opponent.health -= 3
            elif(self.strength in opponent.weakness):
                opponent.health -= 15
            else:
                opponent.health -= 10
        else:
            if(opponent.strength == self.strength or
                opponent.strength in self.weakness):
                opponent.health -= 5
            elif(self.strength in opponent.weakness):
                opponent.health -= 25
            else:
                opponent.health -= 20
        self.strengthAttacks -= 1

    def raiseDefense(self):
        self.defenseUp = True

    def resetDefense(self):
        self.defenseUp = False

    def runAway(self, data):
        data.waiting = None
        data.turn = None
        data.opponent.resetStats()
        data.opponent.resetDefense()
        data.opponent = None
        data.lastMove = None
        data.clickCount = None
        data.battleOver = None
        data.currPlayerPokemon = None

    def draw(self, canvas, x, y):
        image = Image.open(self.file)
        maxSize = (self.size, self.size)
        image.thumbnail(maxSize, Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)
        self.image = tkimage
        canvas.create_image(x, y, anchor="center", image=self.image)
        canvas.create_text(x, y+(self.size/2), text="%s" % str(self.name),
                            anchor="n")

    def drawInBattle(self, canvas, data):
        if(self.owned):
            image = Image.open(self.file)
            maxSize = (self.size, self.size)
            image.thumbnail(maxSize, Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(image)
            self.image = tkimage
            canvas.create_image(84+(self.size/2), (((data.height/2)+60)/2),
                                anchor="center", image=self.image)
            canvas.create_text(84+(self.size/2),(((data.height/2)+60)/2)+
                                (self.size/2)-140, text="Health: %d/100" %
                                self.health, anchor="n")
        else:
            image = Image.open(self.file)
            maxSize = (self.size, self.size)
            image.thumbnail(maxSize, Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(image)
            self.image = tkimage
            canvas.create_image(data.width-103, (((data.height/2)+60)/2),
                                anchor="center", image=self.image)
            canvas.create_text(data.width-84-(self.size/2),
                                (((data.height/2)+60)/2)+(self.size/2)-140,
                                text="Health: %d/100" % self.health,
                                anchor="n")

    def displayInfo(self, canvas, x, y):
        self.draw(canvas, x, y)
        canvas.create_text(x, y+(self.size/2)+15, text="Health: %s" %
                            str(self.health), anchor="n")
        canvas.create_text(x, y+(self.size/2)+30, text="Strength Attacks: %s" %
                            str(self.strengthAttacks), anchor="n")

class FireType(Pokemon):

    def __init__(self, name, ownedByPlayer, fileName):
        super().__init__(name, ownedByPlayer, fileName)
        self.strength = "Fire"
        self.fill = "orange"
        self.weakness = ["Water", "MewTwo"]
        self.moves = [["Attack (%s)" % self.strength, "Combat Attack"],
                        ["Defense Up", "Run"]]

class WaterType(Pokemon):

    def __init__(self, name, ownedByPlayer, fileName):
        super().__init__(name, ownedByPlayer, fileName)
        self.strength = "Water"
        self.fill = "blue"
        self.weakness = ["Electric", "Grass", "MewTwo"]
        self.moves = [["Attack (%s)" % self.strength, "Combat Attack"],
                        ["Defense Up", "Run"]]

class LeafType(Pokemon):

    def __init__(self, name, ownedByPlayer, fileName):
        super().__init__(name, ownedByPlayer, fileName)
        self.strength = "Leaf"
        self.fill = "green"
        self.weakness = ["Fire", "MewTwo"]
        self.moves = [["Attack (%s)" % self.strength, "Combat Attack"],
                        ["Defense Up", "Run"]]

class ElectricType(Pokemon):

    def __init__(self, name, ownedByPlayer, fileName):
        super().__init__(name, ownedByPlayer, fileName)
        self.strength = "Electric"
        self.fill = "yellow"
        self.weakness = ["MewTwo"]
        self.moves = [["Attack (%s)" % self.strength, "Combat Attack"],
                        ["Defense Up", "Run"]]

class MewTwo(Pokemon):

    def __init__(self, name, ownedByPlayer, fileName):
        super().__init__(name, ownedByPlayer, fileName)
        self.strength = "MewTwo"
        self.weakness = []
        self.moves = [["Attack (%s)" % self.strength, "Combat Attack"],
                        ["Defense Up", "Run"]]
        self.strengthAttacks = 100
        self.health = 300
        self.fill = "purple"

class Bush(object):

    def __init__(self, x, y, fileName):
        self.x = x
        self.y = y
        self.size = 25
        self.chanceOfPokemon = random.randint(0,11)
        self.chanceOfPotion = random.randint(12,30)
        self.file = fileName

    def walkedThroughByPlayer(self, x, y):
        if(x == self.x and y == self.y):
            return True
        return False

    def draw(self, canvas):
        image = Image.open(self.file)
        maxSize = (self.size, self.size)
        image.thumbnail(maxSize, Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)
        self.image = tkimage
        canvas.create_image(self.x+(self.size/2), self.y+(self.size/2),
                            anchor="center", image=self.image)

class MoveButton(object):

    def __init__(self, x, y, text, data):
        self.x = x
        self.y = y
        self.text = text
        self.sizeX = (data.width-40)/2
        self.sizeY = ((data.height)-20-((data.height/2)+140))/2
        self.fill = "black"

    def isPressed(self, x, y):
        if(x > self.x and x < self.x+self.sizeX and y > self.y and y < self.y+
            self.sizeY):
            return True
        return False

    def draw(self, canvas, data):
        canvas.create_rectangle(self.x, self.y, self.x+self.sizeX, self.y+
                                self.sizeY, fill="white")
        canvas.create_text(self.x+self.sizeX/2, self.y+self.sizeY/2,
                            font=("Arial", 20), text=self.text, fill=self.fill)

class Portal(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 25

    def isEntered(self, x, y):
        if(x == self.x and y == self.y):
            return True
        return False

    def draw(self, canvas):
        image = Image.open("portal.gif")
        maxSize = (self.size, self.size)
        image.thumbnail(maxSize, Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)
        self.image = tkimage
        canvas.create_image(self.x+(self.size/2), self.y+(self.size/2),
                            anchor="center", image=self.image)

def init(data):
    data.screen = "startscreen"
    initStartScreen(data)

def initStartScreen(data):
    data.startButton = Button((data.width/2)-180, (data.height/2)+175, 60, 60,
                        "Start", True)
    data.helpButton = Button((data.width/2)+120, (data.height/2)+175, 60, 60,
                            "Help", True)

def initHelp(data):
    data.backButton = Button(35, 35, 60, 60, "Back", True)

def initSelection(data):
    data.instructionsHeight = 100
    initStarters(data)
    numButtonsPerRow = len(data.starters[0])
    numRows = len(data.starters)
    buttonWidth = data.width/numButtonsPerRow
    buttonHeight = (data.height - data.instructionsHeight)/numRows
    data.buttons = []
    for row in range(numRows):
        for col in range(numButtonsPerRow):
            data.buttons.append(Button(col*buttonWidth,
                                (row*buttonHeight)+data.instructionsHeight,
                                buttonWidth, buttonHeight,
                                data.starters[row][col], False))
    data.pokemonSelected = []

def initStarters(data):
    starter1 = FireType("Charmander", True, "charmander.gif")
    starter2 = WaterType("Squirtle", True, "squirtle.gif")
    starter3 = LeafType("Bulbasaur", True, "bulbasaur.gif")
    starter4 = ElectricType("Pikachu", True, "pikachu.gif")
    data.starters = [[starter1, starter2], [starter3, starter4]]

def initMap(data):
    data.gridBlockSize = 25
    data.player = Player("walkingForward.gif", data)
    for pokemon in data.pokemonSelected:
        data.player.pokemon.append(pokemon)
    data.pokemonSelected = None
    data.player.starter = data.player.pokemon[0]
    initBushes(data)
    initPossiblePokemonOwned(data)
    data.inventory = Button(data.width-70, data.height-20, 70, 20, "Inventory",
                        False)
    data.inventory.fill = "black"

def initBushes(data):
    data.bushes = []
    data.usedPoints = []
    for x in range(75):
        randX = random.randrange(0, data.width, data.gridBlockSize)
        randY = random.randrange(0, data.height, data.gridBlockSize)
        while((randX, randY) == data.player.getCoordinates() and (randX, randY)
                not in data.usedPoints):
            randX = random.randrange(0, data.width, data.gridBlockSize)
            randY = random.randrange(0, data.height, data.gridBlockSize)
        data.usedPoints.append((randX, randY))
        data.bushes.append(Bush(randX, randY, "bush.gif"))
    randX = random.randrange(0, data.width, data.gridBlockSize)
    randY = random.randrange(0, data.height, data.gridBlockSize)
    while((randX, randY) == data.player.getCoordinates() and (randX, randY)
            not in data.usedPoints):
            randX = random.randrange(0, data.width, data.gridBlockSize)
            randY = random.randrange(0, data,height-50, data.gridBlockSize)
    data.portal = Portal(randX, randY)
    initWildPokemon(data)

def initWildPokemon(data):
    wild1 = FireType("Torchick", False, "torchick.gif")
    wild2 = WaterType("Mudkip", False, "mudkip.gif")
    wild3 = LeafType("Treeko", False, "treeko.gif")
    wild4 = ElectricType("Voltorb", False, "voltorb.gif")
    data.wildPokemon = [wild1, wild2, wild3, wild4]

def initPossiblePokemonOwned(data):
    data.owned1 = FireType("Torchick", True, "torchick.gif")
    data.owned2 = WaterType("Mudkip", True, "mudkip.gif")
    data.owned3 = LeafType("Treeko", True, "treeko.gif")
    data.owned4 = ElectricType("Voltorb", True, "voltorb.gif")

def initInventory(data):
    data.backToMapButton = Button(35, 35, 60, 60, "Back", True)
    data.pokeOptions = []
    for i in range(len(data.player.pokemon)):
        data.pokeOptions.append(Button(data.width-130, 175+(110*i), 80, 20,
                                "Add Health", False))
        data.pokeOptions.append(Button(data.width-130, 205+(110*i), 95, 20,
                                "Add Strength", False))
        data.pokeOptions[i].fill = data.pokeOptions[i+1+(i*1)].fill = "black"

def initHealth(data):
    data.healthTimer = 0

def initStrength(data):
    data.strengthTimer = 0

def initFinalBattle(data):
    data.opponent = MewTwo("MewTwo", False, "mewtwo.gif")
    data.turn = data.opponent
    data.waiting = data.player.starter
    data.currPlayerPokemon = data.player.starter
    data.counter = 0
    data.returnCounter = 0
    data.lastMove = ""
    data.clickCount = 0
    data.battleOver = False
    initMoveButtons(data)
    data.finalBattle = True

def initWildBattle(data):
    data.opponent = random.choice(data.wildPokemon)
    data.turn = data.opponent
    data.waiting = data.player.starter
    data.currPlayerPokemon = data.player.starter
    data.counter = 0
    data.returnCounter = 0
    data.lastMove = ""
    data.clickCount = 0
    data.battleOver = False
    initMoveButtons(data)
    data.finalBattle = False

def initMoveButtons(data):
    data.moveButtons = []
    for row in range(len(data.waiting.moves)):
        for col in range(len(data.waiting.moves[0])):
            data.moveButtons.append(MoveButton(20+((data.width-40)/2)*col,
                                    (data.height/2)+140+(((data.height)-20-
                                    ((data.height/2)+140))/2)*row,
                                    data.waiting.moves[row][col], data))

def initCollect(data):
    data.collectButton = Button((data.width/2)-180, (data.height/2)+100, 60,
                                60, "Collect", True)
    data.returnToMapButton = Button((data.width/2)+90, (data.height/2)+100,
                                    120, 60, "To Map", True)

def initConfirm(data):
    data.yesButton = Button((data.width/2)-180, (data.height/2)+100, 60,
                                60, "Yes", True)
    data.noButton = Button((data.width/2)+90, (data.height/2)+100,
                                    120, 60, "No", True)

def mousePressed(event, data):
    if(data.screen == "startscreen"):
        mousePressedStartScreen(event, data)
    elif(data.screen == "help"):
        mousePressedHelp(event, data)
    elif(data.screen == "selection"):
        mousePressedSelection(event, data)
    elif(data.screen == "map"):
        mousePressedMap(event, data)
    elif(data.screen == "inventory"):
        mousePressedInventory(event, data)
    elif(data.screen == "health"):
        pass
    elif(data.screen == "strength"):
        pass
    elif(data.screen == "battle"):
        mousePressedBattle(event, data)
    elif(data.screen == "collectscreen"):
        mousePressedCollect(event, data)
    elif(data.screen == "confirm"):
        mousePressedConfirm(event, data)
    elif(data.screen == "winscreen"):
        pass

def mousePressedStartScreen(event, data):
    if(data.startButton.isPressed(event.x, event.y)):
        initSelection(data)
        data.screen = "selection"
    elif(data.helpButton.isPressed(event.x, event.y)):
        initHelp(data)
        data.screen = "help"

def mousePressedHelp(event, data):
    if(data.backButton.isPressed(event.x, event.y)):
        data.screen = "startscreen"

def mousePressedSelection(event, data):
    for button in data.buttons:
        if(button.isPressed(event.x, event.y)):
            if(not button.selected):
                if(len(data.pokemonSelected) < 1):
                    button.selected = True
                    data.pokemonSelected.append(button.pokemon)
            else:
                button.selected = False
                data.pokemonSelected.remove(button.pokemon)

def mousePressedMap(event, data):
    if(data.inventory.isPressed(event.x, event.y)):
        initInventory(data)
        data.screen = "inventory"

def mousePressedInventory(event, data):
    if(data.backToMapButton.isPressed(event.x, event.y)):
        data.screen = "map"
    for i in range(len(data.pokeOptions)):
        if(data.pokeOptions[i].isPressed(event.x, event.y)):
            pokeIndex = (i//2)%3
            if(i%2 == 0):
                if(data.player.healthPotions > 0 and
                    data.player.pokemon[pokeIndex].health < 100):
                    data.player.pokemon[pokeIndex].health = 100
                    data.player.healthPotions -= 1
            else:
                if(data.player.strengthPotions > 0 and
                    data.player.pokemon[pokeIndex].strengthAttacks < 4):
                    data.player.pokemon[pokeIndex].strengthAttacks = 4
                    data.player.strengthPotions -= 1

def mousePressedBattle(event, data):
    runaway = False
    if(data.turn == data.currPlayerPokemon and not data.battleOver and
        data.clickCount < 1):
        if(data.moveButtons[0].isPressed(event.x, event.y) and
            data.turn.strengthAttacks > 0):
            data.turn.attackWithStrength(data.waiting)
            data.lastMove = "attackWithStrength"
            data.clickCount += 1
        elif(data.moveButtons[1].isPressed(event.x, event.y)):
            data.turn.combatAttack(data.waiting)
            data.lastMove = "combatAttack"
            data.clickCount += 1
        elif(data.moveButtons[2].isPressed(event.x, event.y)):
            data.turn.raiseDefense()
            data.lastMove = "defenseUp"
            data.clickCount += 1
        elif(data.moveButtons[3].isPressed(event.x, event.y)):
            data.screen = "map"
            data.turn.runAway(data)
            runaway = True
        if(not runaway):
            data.waiting.resetDefense()
            if(data.waiting.health <= 0):
                data.waiting.health = 0
                data.battleOver = True

def addPokemonToPokeball(data):
    if(str(data.opponent) == "Torchick"):
        data.player.pokemon.append(data.owned1)
    if(str(data.opponent) == "Mudkip"):
        data.player.pokemon.append(data.owned2)
    if(str(data.opponent) == "Treeko"):
        data.player.pokemon.append(data.owned3)
    if(str(data.opponent) == "Voltorb"):
        data.player.pokemon.append(data.owned4)

def mousePressedCollect(event, data):
    if(data.collectButton.isPressed(event.x, event.y)):
        addPokemonToPokeball(data)
        data.currPlayerPokemon.runAway(data)
        data.screen = "map"
    elif(data.returnToMapButton.isPressed(event.x, event.y)):
        data.currPlayerPokemon.runAway(data)
        data.screen = "map"

def mousePressedConfirm(event, data):
    if(data.yesButton.isPressed(event.x, event.y)):
        initFinalBattle(data)
        data.screen = "battle"
    elif(data.noButton.isPressed(event.x, event.y)):
        data.screen = "map"

def keyPressed(event, data):
    if(data.screen == "startscreen"):
        pass
    elif(data.screen == "help"):
        pass
    elif(data.screen == "selection"):
        keyPressedSelection(event, data)
    elif(data.screen == "map"):
        keyPressedMap(event, data)
    elif(data.screen == "inventory"):
        pass
    elif(data.screen == "health"):
        pass
    elif(data.screen == "strength"):
        pass
    elif(data.screen == "battle"):
        keyPressedBattle(event, data)
    elif(data.screen == "collectscreen"):
        pass
    elif(data.screen == "confirm"):
        pass
    elif(data.screen == "winscreen"):
        keyPressedWIN(event, data)

def keyPressedSelection(event, data):
    if(event.keysym == "Return"):
        initMap(data)
        data.screen = "map"

def playerOnBush(data):
    for bush in data.bushes:
        if(bush.walkedThroughByPlayer(data.player.x, data.player.y)):
            wildPokemonAppear = random.randint(0,11)
            potionAppear = random.randint(12,30)
            if(wildPokemonAppear == bush.chanceOfPokemon):
                initWildBattle(data)
                data.screen = "battle"
            elif(potionAppear == bush.chanceOfPotion):
                r = random.randint(0,1)
                if(r == 0):
                    initHealth(data)
                    data.screen = "health"
                    data.player.healthPotions += 1
                else:
                    initStrength(data)
                    data.screen = "strength"
                    data.player.strengthPotions += 1

def keyPressedMap(event, data):
    if(event.keysym == "Up"):
        data.player.move(0, -1, data)
    elif(event.keysym == "Down"):
        data.player.move(0, 1, data)
    elif(event.keysym == "Left"):
        data.player.move(-1, 0, data)
    elif(event.keysym == "Right"):
        data.player.move(1, 0, data)
    playerOnBush(data)
    if(data.portal.isEntered(data.player.x, data.player.y)):
        initConfirm(data)
        data.screen = "confirm"

def makeAIMove(data):
    if(data.lastMove == "defenseUp"):
        data.turn.raiseDefense()
    elif(data.lastMove == "combatAttack"):
        data.turn.combatAttackAI(data.waiting)
    elif(data.lastMove == "attackWithStrength"):
        data.turn.attackWithStrengthAI(data.waiting)
    if(data.waiting.health <= 0):
        data.waiting.health = 0
        currIndex = data.player.pokemon.index(data.waiting)
        if(len(data.player.pokemon) == 1):
            data.battleOver = True
        elif(len(data.player.pokemon) == 2):
            if(currIndex == 0):
                data.currPlayerPokemon = data.player.pokemon[currIndex+1]
                data.waiting = data.currPlayerPokemon
            else:
                data.waiting.health = 0
                data.battleOver = True
        else:
            if(currIndex < 2):
                data.currPlayerPokemon = data.player.pokemon[currIndex+1]
                data.waiting = data.currPlayerPokemon
            else:
                data.waiting.health = 0
                data.battleOver = True

def keyPressedBattle(event, data):
    if(not data.battleOver):
        if(data.turn == data.opponent):
            if(event.keysym == "Return"):
                data.returnCounter += 1
                if(data.returnCounter%3 == 1):
                    data.lastMove = data.turn.aiMove(data.waiting)
                    data.clickCount = 0
                elif(data.returnCounter%3 == 2):
                    makeAIMove(data)
                    data.waiting.resetDefense()
                    data.turn, data.waiting = data.waiting, data.turn
        elif(data.turn == data.currPlayerPokemon):
            if(event.keysym == "Return"):
                if(data.clickCount == 1):
                    data.returnCounter += 1
                if(data.returnCounter%3 == 0):
                    data.turn, data.waiting = data.waiting, data.turn
    else:
        if(event.keysym == "Return"):
            if(data.currPlayerPokemon.health == 0):
                data.screen = "startscreen"
            elif(data.opponent.health == 0):
                if(len(data.player.pokemon) < 3 and not data.finalBattle):
                    initCollect(data)
                    data.screen = "collectscreen"
                elif(data.finalBattle):
                    data.screen = "winscreen"
                else:
                    data.screen = "map"
                data.player.replenishPokemon()

def keyPressedWIN(event, data):
    if(event.keysym == "Return"):
        data.screen = "startscreen"

def timerFired(data):
    if(data.screen == "startscreen"):
        pass
    elif(data.screen == "help"):
        pass
    elif(data.screen == "selection"):
        pass
    elif(data.screen == "map"):
        pass
    elif(data.screen == "inventory"):
        timerFiredInventory(data)
    elif(data.screen == "health"):
        timerFiredHealth(data)
    elif(data.screen == "strength"):
        timerFiredStrength(data)
    elif(data.screen == "battle"):
        timerFiredBattle(data)
    elif(data.screen == "collectscreen"):
        pass
    elif(data.screen == "confirm"):
        pass

def timerFiredInventory(data):
    for i in range(len(data.pokeOptions)):
        pokeIndex = (i//2)%3
        if(i%2 == 0):
            if(data.player.healthPotions == 0 or
                data.player.pokemon[pokeIndex].health == 100):
                data.pokeOptions[i].fill = "grey"
        else:
            if(data.player.strengthPotions == 0 or
                data.player.pokemon[pokeIndex].strengthAttacks == 4):
                data.pokeOptions[i].fill = "grey"

def timerFiredHealth(data):
    if(data.healthTimer < 15):
        data.healthTimer += 1
    else:
        data.screen = "map"

def timerFiredStrength(data):
    if(data.strengthTimer < 15):
        data.strengthTimer += 1
    else:
        data.screen = "map"

def timerFiredBattle(data):
    if(data.counter != None and data.counter != 20):
        data.counter += 1

def drawStartScreenButtons(canvas, data):
    data.startButton.drawNormalButton(canvas)
    data.helpButton.drawNormalButton(canvas)

def redrawAllStartScreen(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    image = Image.open("introScreen.gif")
    maxSize = (300, 300)
    image.thumbnail(maxSize, Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(image)
    data.introScreen = tkimage
    canvas.create_image(data.width/2, (data.height/2)+50, anchor="center",
                        image=data.introScreen)
    image = Image.open("logo.gif")
    maxSize = (data.width-100, 184)
    image.thumbnail(maxSize, Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(image)
    data.logo = tkimage
    canvas.create_image(data.width/2, (data.height/2)-175, anchor="center",
                        image=data.logo)
    drawStartScreenButtons(canvas, data)

def drawHelpText(canvas, data):
    canvas.create_text(data.width/2, (data.height/2)-140, font=("Arial", 20),
                        text="Welcome to Pokemon!", fill="orange")
    text = """
        When you click start, on the Start Screen, you will have the ability
    to choose one of four starter Pokemon. This Pokemon will remain your
    starter Pokemon for the remainder of the game. However, choose wisely
    as certain Pokemon have different strengths and weaknesses. You will
    then be put into an enviornment that contains wild Pokemon. Watch
    out for bushes as wild Pokemon like to hide in these. Also, there may be
    health and strength potions found in these bushes. Since you may run in
    to these Pokemon, you should know your options. First off, the wild
    Pokemon will most likely catch you off guard, so it will have its chance
    to attack first. After that you may either run away, or keep fighting it.
    However, if you run away, any damage done to your Pokemon will remain and
    your strength attacks will not replenished. But, if you battle it out
    and win, you will have both replenished fully and you will have the option
    to capture the Pokemon you defeated. But, if your Pokemon die, you will be
    forced to restart the game. If you are battling with more than one Pokemon
    and one of your Pokemon die, the next Pokemon you have (the most recent
    capture) will be automatically used. Also, these Pokemon that die during
    battle will not be revived if you defeat the opponent. Your goal is to
    beat what lies in the Portal..."""
    canvas.create_text(50, (data.height/2)-130,
                        text=text, fill="yellow", anchor="nw")
    canvas.create_text(data.width/2, data.height-50, font=("Arial, 25"),
                        text="Good Luck!", fill="green")

def redrawAllHelp(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    canvas.create_text(data.width/2, (data.height/2)-200, font=("Arial", 50),
                        text="Help", fill="red")
    data.backButton.drawNormalButton(canvas)
    drawHelpText(canvas, data)

def drawInstructions(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.instructionsHeight,
                            fill="red")
    canvas.create_text(data.width/2, 50, font=("Arial", 20), text="Please " +
                        "select a starter Pokemon. Press enter when done.",
                        fill="white")

def drawGrid(canvas, data):
    for button in data.buttons:
        button.draw(canvas)

def redrawAllSelection(canvas, data):
    drawInstructions(canvas, data)
    drawGrid(canvas, data)

def drawMapEnviornment(canvas, data):
    image = Image.open("grass.gif")
    maxSize = (data.width, data.height)
    image.thumbnail(maxSize, Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(image)
    data.grassBackground = tkimage
    canvas.create_image(data.width/2, data.height/2, anchor="center",
                        image=data.grassBackground)
    for bush in data.bushes:
        bush.draw(canvas)
    data.portal.draw(canvas)

def redrawAllMap(canvas, data):
    drawMapEnviornment(canvas, data)
    data.player.draw(canvas)
    data.inventory.drawNormalButton(canvas)

def redrawAllInventory(canvas, data):
    data.backToMapButton.drawNormalButton(canvas)
    for i in range(len(data.player.pokemon)):
        data.player.pokemon[i].displayInfo(canvas, 120, 175+(110*i))
    canvas.create_text(data.width/2, 100, font=("Arial", 18), text=
                        "Health Potions: %d\nStrength Potions: %d" %
                        (data.player.healthPotions,
                        data.player.strengthPotions))
    for option in data.pokeOptions:
        option.drawNormalButton(canvas)

def redrawAllHealth(canvas, data):
    canvas.create_text(data.width/2, data.height/2, font=("Arial", 25), text=
                        "Health Potion found!", fill="red")

def redrawAllStrength(canvas, data):
    canvas.create_text(data.width/2, data.height/2, font=("Arial", 25), text=
                        "Strength Potion found!", fill="green")

def drawOpponentAttackMessage(canvas, data):
    if(data.lastMove == "defenseUp"):
        canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                            20), text="%s decided to up its defense " %
                            str(data.turn) + "for a turn.")
    elif(data.lastMove == "combatAttack"):
        canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                            20), text="%s decided to attack with combat." %
                            str(data.turn))
    else:
        canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                            20), text="%s decided to attack with " %
                            str(data.turn) + "its strength.")

def drawPlayerBattleMessage(canvas, data):
    if(data.clickCount == 0):
        canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                            20), text="It is your turn.")
        canvas.create_text(data.width/2, (data.height/2)+110, text="Click" +
                            " on desired move to continue.")
    elif(data.clickCount == 1):
        if(data.lastMove == "defenseUp"):
            canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                                20), text="You decided to up your defense" +
                                " for a turn.")
        elif(data.lastMove == "combatAttack"):
            canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                                20), text="You decided to attack with combat.")
        else:
            canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                                20), text="You decided to attack with your" +
                                " strength.")

def drawBattleOverScreen(canvas, data):
    if(data.battleOver):
        if(data.currPlayerPokemon.health == 0):
            canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                                20), text="Battle over, you were defeated.")
            canvas.create_text(data.width/2, (data.height/2)+110, text="Press"+
                                " enter to go back to Start Screen.")
        elif(data.opponent.health == 0 and not data.finalBattle):
            canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                                15), text="Battle over, opponent was defeated."+
                                " Health and Attacks will be replenished.")
            canvas.create_text(data.width/2, (data.height/2)+110, text="Press" +
                                " enter to continue.")
        elif(data.opponent.health == 0 and data.finalBattle):
            canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                                15), text="Battle over, Boss was defeated."+
                                " Congratulations!")
            canvas.create_text(data.width/2, (data.height/2)+110, text="Press" +
                                " enter to continue.")

def drawBattleMessage(canvas, data):
    if(not data.battleOver):
        if(data.returnCounter%3 == 0):
            canvas.create_text(data.width/2, (data.height/2)+90, font=("Arial",
                                20), text="It is %s's turn." %
                                str(data.opponent))
            canvas.create_text(data.width/2, (data.height/2)+110,
                                text="Press enter to continue.")
        elif(data.returnCounter%3 == 1):
            drawOpponentAttackMessage(canvas, data)
            canvas.create_text(data.width/2, (data.height/2)+110,
                                text="Press enter to continue.")
        elif(data.returnCounter%3 == 2):
            drawPlayerBattleMessage(canvas, data)
            if(data.clickCount == 1):
                canvas.create_text(data.width/2, (data.height/2)+110,
                                    text="Press enter to continue.")
    else:
        drawBattleOverScreen(canvas, data)

def drawMoveButtons(canvas, data):
    for move in data.moveButtons:
        if(move.text.startswith("Attack") and
            data.currPlayerPokemon.strengthAttacks == 0):
            move.fill = "grey"
        move.draw(canvas, data)

def createActionBox(canvas, data):
    canvas.create_rectangle(0, (data.height/2)+60, data.width, data.height,
                            fill="blanchedalmond")
    canvas.create_rectangle(20, (data.height/2)+140, data.width-20,
                            data.height-20, fill="white")

def drawBattleField(canvas, data):
    image = Image.open("pokefield.gif")
    maxSize = (600, (data.height/2)+60)
    image.thumbnail(maxSize, Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(image)
    data.pokefield = tkimage
    canvas.create_image(data.width/2, ((data.height/2)+60)/2, anchor="center",
                        image=data.pokefield)

def determineTypeOfEncounter(data):
    if(isinstance(data.opponent, FireType)):
        return "orange"
    elif(isinstance(data.opponent, WaterType)):
        return "deepskyblue"
    elif(isinstance(data.opponent, LeafType)):
        return "green"
    elif(isinstance(data.opponent, ElectricType)):
        return "yellow"
    else:
        return "purple"

def redrawAllBattle(canvas, data):
    if(data.finalBattle and data.counter != None and data.counter < 20):
        if(data.counter%5 == 0 or data.counter%5 == 1 or data.counter%5 == 2):
            fill = determineTypeOfEncounter(data)
            canvas.create_rectangle(0, 0, data.width, data.height, fill=fill)
        canvas.create_text(data.width/2, data.height/2, font=("Arial", 25),
                            text="You've encountered %s!" % str(data.opponent))
    elif(data.counter != None and data.counter < 20):
        if(data.counter%5 == 0 or data.counter%5 == 1 or data.counter%5 == 2):
            fill = determineTypeOfEncounter(data)
            canvas.create_rectangle(0, 0, data.width, data.height, fill=fill)
        canvas.create_text(data.width/2, data.height/2, font=("Arial", 25),
                            text="You've encountered a wild %s!" %
                            str(data.opponent))
    else:
        data.counter = None
        drawBattleField(canvas, data)
        data.opponent.drawInBattle(canvas, data)
        data.currPlayerPokemon.drawInBattle(canvas, data)
        createActionBox(canvas, data)
        drawMoveButtons(canvas, data)
        drawBattleMessage(canvas, data)

def redrawAllCollect(canvas, data):
    data.collectButton.drawNormalButton(canvas)
    data.returnToMapButton.drawNormalButton(canvas)
    data.opponent.draw(canvas, data.width/2, data.height/2)
    canvas.create_text(data.width/2, (data.height/2)-100, font=("Arial", 20),
                        text="Would you like to keep this Pokemon?")

def redrawAllConfirm(canvas, data):
    data.yesButton.drawNormalButton(canvas)
    data.noButton.drawNormalButton(canvas)
    canvas.create_text(data.width/2, (data.height/2)-100, font=("Arial", 20),
                        text="Are you sure you want to face MewTwo?")

def redrawAllWin(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill="black")
    canvas.create_text(data.width/2, 100, font=("Arial", 30),
                        text="You win!", fill="green")
    image = Image.open("badges.gif")
    maxSize = (200, 150)
    image.thumbnail(maxSize, Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(image)
    data.badge = tkimage
    canvas.create_image(data.width/2, data.height/2-100, anchor="center",
                        image=data.badge)
    canvas.create_text(data.width/2, (data.height/2)+50, font=("Arial", 20),
                        text="You are now ready to move on to the real " +
                        "Pokemon World\n\t and earn those gym badges!",
                        fill="green")
    canvas.create_text(data.width/2, (data.height/2)+150, font=("Arial", 15),
                        text="Press enter to replay the game.", fill="white")

def redrawAll(canvas, data):
    if(data.screen == "startscreen"):
        redrawAllStartScreen(canvas, data)
    elif(data.screen == "help"):
        redrawAllHelp(canvas, data)
    elif(data.screen == "selection"):
        redrawAllSelection(canvas, data)
    elif(data.screen == "map"):
        redrawAllMap(canvas, data)
    elif(data.screen == "inventory"):
        redrawAllInventory(canvas, data)
    elif(data.screen == "health"):
        redrawAllHealth(canvas, data)
    elif(data.screen == "strength"):
        redrawAllStrength(canvas, data)
    elif(data.screen == "battle"):
        redrawAllBattle(canvas, data)
    elif(data.screen == "collectscreen"):
        redrawAllCollect(canvas, data)
    elif(data.screen == "confirm"):
        redrawAllConfirm(canvas, data)
    elif(data.screen == "winscreen"):
        redrawAllWin(canvas, data)

def run(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100
    init(data)
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()
    print("bye!")

run()
