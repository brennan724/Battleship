# battleship.py
# Brennan Kuo and Ryan Schloessman, CS 111, 3/8/14

import random
from graphics import *
import time
import sys
import os

#creates a lists of the ships that will need to be placed along with their given length
ships = [['Aircraft Carrier', 5],['Battleship',4],['Submarine',3],['Destroyer',3],['Patrol Boat',2]]
class BattleshipBoard:
	def __init__(self,window,text):
		self.window = window
		self.text = text
		self.board = [['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-'],
					  ['-','-','-','-','-','-','-','-','-','-']]

	# Draws the lines and blue squares in each window for the game
	def drawGrid(self):
		# Prints vertical lines on window
		for i in range(1,11):
			line = Line(Point((i*40),0),Point((i*40),400))
			line.draw(self.window)
		# Prints horizontal lines on window
			line = Line(Point(0,(i*40)),Point(400,(i*40)))
			line.draw(self.window)
		# Draws each square blue
		for row in range(10):
			for col in range(10):
				self.drawSquare(row,col, 'blue')

	# Draws a square in given row and column and given color
	def drawSquare(self,row,col,color):
		# Sets start points and end points for each square depending on row/column, since grid is 400 by 400 every square is 40 by 40
		rowGridStart, rowGridEnd = (row * 40), ((row + 1) * 40)
		colGridStart, colGridEnd = (col * 40), ((col + 1) * 40)
		square = Rectangle(Point(colGridStart,rowGridStart),Point(colGridEnd,rowGridEnd))
		# Determines color based on parameter and draws it 
		square.setFill(color)
		square.draw(self.window)

	# Determines if player's ship placement is legal
	def isLegalPlacement(self,rowStart,colStart,rowEnd,colEnd,lengthOfShip):
		check = 0
		# If ship is going up and down, loops through every spot in the ship to check if the spot is empty ('-')
		if abs(rowStart - rowEnd) == (lengthOfShip - 1) and colStart == colEnd:
			for i in range(min(rowStart,rowEnd),(max(rowStart,rowEnd) + 1)):
				if self.board[i][colStart] == '-':
					# If spot is empty, check accumulates
					check += 1
		# If ship is going left and right, loops through every spot in the ship to check if the spot is empty ('-')
		elif abs(colStart - colEnd) == (lengthOfShip - 1) and rowStart == rowEnd:
			for i in range(min(colStart,colEnd),(max(colStart,colEnd) + 1)):
					if self.board[rowStart][i] == '-':
						# If spot is empty, check accumulates
						check += 1
		# If and only if every spot is empty(check = # of spots on given ship), it returns true
		if check == lengthOfShip:
			return True
		return False
	
	# Determines if AI's ship placement is legal. Only difference from player's is that the AI's ships can't be next to each other
	# The reason behind not having the ships touch adjacently is for strategic purposes, it is more optimal if ships are not touching
	def shipsNotTouching(self,rowStart,colStart,rowEnd,colEnd,lengthOfShip):
		check = 0
		# If ship is going up and down, loops through spots to check if its empty and that the spots on either side of each spot are also empty
		if abs(rowStart - rowEnd) == (lengthOfShip - 1) and colStart == colEnd:
			for i in range(min(rowStart,rowEnd),(max(rowStart,rowEnd) + 1)):
				# Checks most up and down ships
				if 0 < colStart < 9:
					if self.board[i][colStart] == '-' and self.board[i][colStart + 1] == '-' and self.board[i][colStart - 1] == '-':
						check += 1
				# Checks those that are bordering right side of window
				elif colStart == 9:
					if self.board[i][colStart] == '-' and self.board[i][colStart - 1] == '-':
						check += 1
				# Checks those that are bordering left side of window 
				else:
					if self.board[i][colStart] == '-' and self.board[i][colStart + 1] == '-':
						check += 1
		# If ship is going right and left, loops through spots to check if its empty and that the spots on either side of each spot are also empty
		elif abs(colStart - colEnd) == (lengthOfShip - 1) and rowStart == rowEnd:
			for i in range(min(colStart,colEnd),(max(colStart,colEnd) + 1)):
				# Checks most sideways ships
				if 0 < rowStart < 9:
					if self.board[rowStart][i] == '-' and self.board[rowStart + 1][i] == '-' and self.board[rowStart - 1][i] == '-':
						check += 1
				# Checks ships bordering bottom of window
				elif rowStart == 9:
					if self.board[rowStart][i] == '-' and self.board[rowStart - 1][i] == '-':
						check += 1
				# Checks ships bordering the top of the window
				else:
					if self.board[rowStart][i] == '-' and self.board[rowStart + 1][i] == '-':
						check += 1
		# If every spot is empty and the spot on either side are also empty, returns that the move is legal
		if check == lengthOfShip:
			return True
		return False
		# This check knowingly does not account for ships touching on their ends(T-Bone)

	# Checks if there is a ship in a given row/column, changes the color of the sqare to either red(Hit) or white(Miss)
	# Also returns True(if Hit) or False(if Miss) and changes the board(List) to keep track of previous spots shot at
	def isHit(self,row,column):
		# Bells and whistles, the given square flashes red and white
		for i in range(5):
			self.drawSquare(row,column,'red')
			time.sleep(.1)
			self.drawSquare(row,column,'white')
			time.sleep(.1)
		# If shot is a miss: returns False, colors the square white, changes the board and tells the user
		if self.board[row][column] == '-':
			self.board[row][column] = 'M'
			self.drawSquare(row,column,'white')
			self.instructions('Miss!','black')
			return False
		# If shot is a hit: returns True, colors the square red, changes board and tells the user
		else:
			self.board[row][column] = 'H'
			self.drawSquare(row,column,'red')
			self.instructions('HIT','red')
			return True

	# Checks if user and AI moves are legal
	def isLegalMove(self,row,column):
		# Makes sure move is on the board(Used more for the AI when adding or subtracting from a target location)
		if 0 <= row <= 9 and 0 <= column <= 9:
			# Checks if location has been shot at before, if not it returns True
			if self.board[row][column] != 'H' and self.board[row][column] != 'M':
				return True
		#If either conditional returns False, function returns False
		return False

	# Checks if given ship has been sunk
	def isShipSunk(self,ship):
		check = 0
		# Searches through board for the ship if its there check accumulates
		for row in self.board:
			for item in row:
				if ship == item:
					check += 1
		# If after checking through the board check is still 0 then the ship has been sunk and function returns True, elsewise returns False
		if check == 0:
			return True
		return False

	# Checks if game is over
	def isGameOver(self):
		check = 0
		# Looks through board for hits, if there are 17 (sum number of spaces on the ships) function returns True
		for row in self.board:
			for item in row:
				if item == 'H':
					check += 1
		if check == 17:
			return True 
		return False

	# Prints out instructions(words) in a given color on a given board
	def instructions(self,words,color):
			self.text.setText(words)
			self.text.setTextColor(color)
			self.text.setSize(12)
			time.sleep(.25)
class AI:
	def __init__(self,shipBoard,firingBoard):
		self.shipBoard = shipBoard
		self.firingBoard = firingBoard
		self.simpleFireLst = ['M']
		self.smartFireLst = ['HR']
		self.smartNum = 1
		self.ridNum = 1
		self.targetShips = [['','',''],['','',''],['','',''],['','',''],['','','']]

	# Randomly places ships of AI given that they match shipsNotTouching or isLegalPlacement criteria
	def placement(self):
		# Creates random number 0-2 
		x = random.randint(0,2)
		# Loops through list of ships
		for ship in ships:
			while True:
				# Infinitely loops through random start and end points until they fit the criteria
				rowStart = random.randint(0,9)
				colStart = random.randint(0,9)
				rowEnd = random.randint(0,9)
				colEnd = random.randint(0,9)
				randomPlacementList = [firingBoard.shipsNotTouching(rowStart,colStart,rowEnd,colEnd,ship[1]),
								firingBoard.shipsNotTouching(rowStart,colStart,rowEnd,colEnd,ship[1]),
								firingBoard.isLegalPlacement(rowStart,colStart,rowEnd,colEnd,ship[1])]
				# ~67% of the time(if random int: x = 0 or 1) ships will be placed by shipsNotTouching, but so the user does not recognize 
				# the pattern that ships are not ever touching adjacently, ~33% of the time they are able to be touching(if random int = 2)
				if randomPlacementList[x]:
					# If it meets the criteria then it places the ship down before looping through the next ship
					for i in range(ship[1]):
						if rowStart == rowEnd:
							firingBoard.board[rowStart][min(colStart,colEnd) + i] = ship[0]
						else:
							firingBoard.board[min(rowStart,rowEnd) + i][colStart] = ship[0]
					break
	
	# Finds largest ship left on firingBoard and returns it's length
	def findLargestShip(self):
		largestLengthOfShip = 5
		if shipboard.isSunk('Aircraft Carrier'):
			largestLengthOfShip = 4
			if shipBoard.isSunk('Battleship'):
				largestLengthOfShip = 3
				if shipBoard.isSunk('Submarine') and shipBoard.isSunk('Destroyer'):
					largestLengthOfShip = 2
		return largestLengthOfShip

	# Checks every space in shipBoard to see if there are any 5 adjacent spaces left on Board
	def fiveSpacesInRowOrCol(self):
		for row in range(10):
			for column in range(10):
				checkVert = 0
				checkHori = 0
				# If spot is 2 spaces away from both edges of the board, 
				# checks horizontally and vertically for 5 adjacent unused shot at spots
				if 1 < row < 8 and 1 < column < 8:
					for i in range(row - 2, row + 3):
						if shipBoard.isLegalMove(i,column):
							checkVert += 1
					for i in range(column - 2, column +3):
						if shipBoard.isLegalMove(row,i):
							checkHori += 1
				# If spot is only 2 spaces away vertically, it only checks vertically(so the computer doesn't return an error)
				elif 1 < row < 8:
					for i in range(row - 2, row + 3):
						if shipBoard.isLegalMove(i,column):
							checkVert += 1
				# If spot is only 2 spaces away horizonatlly, it only checks horizontally(so the computer doesn't return an error)
				elif 1 < column < 8:
					for i in range(column - 2, column + 3):
						if shipBoard.isLegalMove(row,i):
							checkHori += 1
				# If there are 5 adjacent spots either direction, returns True, elsewise returns false
				if checkHori == 5 or checkVert == 5:
					return True
		return False
	
	# Checks if AI's random move(simpleMove) is optimal
	def isOptimalMove(self,row,column):
		checkRight = 0
		checkLeft = 0
		checkUp = 0
		checkDown = 0
		# If there are still five adjacent unshot spots: length = 2
		if self.fiveSpacesInRowOrCol():
			length = 2
		# If there are only 4 adjacent spots or lower: length = 1
		else:
			length = 1
		# Checks spot(s) downward of the possible AI shot, if they are unshot, check accumulates
		for i in range(row + 1, row + length + 1):
			if shipBoard.isLegalMove(i,column):
				checkDown += 1
		# Checks spot(s) upward of the possible AI shot, if they are unshot, check accumulates
		for i in range(row - length, row):
			if shipBoard.isLegalMove(i,column):
				checkUp += 1
		# Checks spot(s) to the right of the possible AI shot, if they are unshot, check accumulates
		for i in range(column + 1, column + length + 1):
			if shipBoard.isLegalMove(row,i):
				checkRight += 1
		# Checks spot(s) tothe left of the possible AI shot, if they are unshot, check accumulates
		for i in range(column - length, column):
			if shipBoard.isLegalMove(row,i):
				checkLeft += 1
		# If the largest ship left is the Patrol Boat then returns true if the possible AI shot has at least one unshot adjacent square
		if self.findLargestShip == 2 and length == 1:
			if checkDown == length or checkUp == length or checkRight == length or checkLeft == length:
				return True
			return False
		# Otherwise it returns True if the possible AI shot has length adjacent unshot squares either upwards and downwards or right and left of it
		else:
			if (checkDown == length and checkUp == length) or (checkRight == length and checkLeft == length):
				return True
			return False
		# If neither conditional is True then there is a more optimal shot and it returns False
			 
	# Decides AI's move
	def simpleMove(self):
		# simpleFireLst starts at 'M', if it's last index is 'H':
		# it runs smartMove based on the last item in smartFireLst
		if self.simpleFireLst[-1] == 'H':
			self.smartMove(self.smartFireLst[-1])
		else:
			# If the last shot wasn't a hit it continues choosing a random shots until it is legal and optimal
			while True:
				ranRow = random.randint(0,9)
				ranCol = random.randint(0,9)
				if shipBoard.isLegalMove(ranRow,ranCol):
					if self.isOptimalMove(ranRow,ranCol):
						# If the shot is going to be a hit, records row, col, and ship name in the 1st targetShips index
						if shipBoard.board[ranRow][ranCol] != '-':
							self.targetShips[0][2] = shipBoard.board[ranRow][ranCol]
							self.targetShips[0][0] = ranRow
							self.targetShips[0][1] = ranCol						
						# Actually checks that it's a hit, if so it adds 'H' to the end of simpleFireLst so smartMove is run next turn
						if shipBoard.isHit(ranRow, ranCol):
							self.simpleFireLst.append('H')
						break

	def smartMove(self,direction):
		# direction is decided by the last item in smartFireLst, this starts out as 'HR'(Hit Right)
		if direction == 'HR':
			# Sets next variable to hit left from the target shot(the Hit from simpleMove)
			next = 'HL'
			# Sets row and column to that directly right of the target shot(the Hit from simpleMove)
			row, col = self.targetShips[0][0], self.targetShips[0][1] + self.smartNum
		elif direction == 'HL':
			# Sets next variable to hit downwards from the target shot(the Hit from simpleMove)
			next = 'HD'
			# Sets row and column to that directly left of the target shot(the Hit from simpleMove)
			row, col = self.targetShips[0][0], self.targetShips[0][1] - self.smartNum
		elif direction == 'HD':
			# Sets next variable to hit upwards from the target shot(the Hit from simpleMove)
			next = 'HU'
			# Sets row and column to that directly downwards of the target shot(the Hit from simpleMove)
			row, col = self.targetShips[0][0] + self.smartNum, self.targetShips[0][1]
		else:
			# Sets next variable to hit right from the target shot(the Hit from simpleMove)
			next = 'HR'
			# Sets row and column to that directly upwards of the target shot(the Hit from simpleMove)
			row, col = self.targetShips[0][0] - self.smartNum, self.targetShips[0][1]
		# If move is legal function checks if the next shot will hit a ship different from the target ship(In the instance that the ships are adjacently placed)
		if shipBoard.isLegalMove(row,col):
			if shipBoard.board[row][col] != '-' and shipBoard.board[row][col] != self.targetShips[0][2]:
				# If shot will hit ship different from the target ship, records it as a 2nd target ship(or 3rd/4th/5th if prior target ship slot has been taken)
				if self.targetShips[1] == ['','','']:
					self.targetShips[1][0],self.targetShips[1][1],self.targetShips[1][2] = row,col,shipBoard.board[row][col]
				elif self.targetShips[2] == ['','','']:
					self.targetShips[2][0],self.targetShips[2][1],self.targetShips[2][2] = row,col,shipBoard.board[row][col]
				elif self.targetShips[3] == ['','','']:
					self.targetShips[3][0],self.targetShips[3][1],self.targetShips[3][2] = row,col,shipBoard.board[row][col]
				else:
					self.targetShips[4][0],self.targetShips[4][1],self.targetShips[4][2] = row,col,shipBoard.board[row][col]
			# If it is a hit smartNum has 1 added to hit so the AI will fire in the same direction, just one space further of the target square
			if shipBoard.isHit(row,col):
				self.smartNum += 1
			# If it is a miss, smartNum is reset back to 1 and smartFireLst is appended with next so it will fire 1 space away from the target space in next direction
			else:
				self.smartNum = 1
				self.smartFireLst.append(next)
		# If the move is not legal(shot is off the grid ie: row = 10) smarNum is reset and 
		# smartFireLst is appended with next so it will fire 1 space away from the target space in next direction
		else:
			self.smartNum = 1
			self.smartFireLst.append(next)
			self.smartMove(self.smartFireLst[-1])
		# Once the target ship has been sunk it tells the player 
		if shipBoard.isShipSunk(self.targetShips[0][2]):
			shipBoard.instructions('Your ' + self.targetShips[0][2] + ' has been sunk!','blue')
			# If there are secondary target ships they all shift so there is a new target ship
			if self.targetShips[1] != ['','','']:
				self.targetShips[0] = self.targetShips[1]
				self.targetShips[1] = self.targetShips[2]
				self.targetShips[2] = self.targetShips[3]
				self.targetShips[3] = self.targetShips[4]
				self.targetShips[4] = ['','','']
			# If there are no secondary target ships, simpleFireLst gets appended with 'Sunk' so it will go back to trying random numbers
			else:
				self.simpleFireLst.append('Sunk')
			# After ship is sunk the direction smartMove will start at next is randomly chosen between HR and HD and smartNum is reset
			# This is done so AI doesn't always fire right then left after getting a hit(Then the player would place all ships vertically)
			nextDirectionList = ['HR','HD']
			x = random.randint(0,1)
			self.smartFireLst.append(nextDirectionList[x])
			self.smartNum = 1

class User:
	def __init__(self,shipBoard,firingBoard):
		self.shipBoard = shipBoard
		self.firingBoard = firingBoard
	
	# Gets user click and assigns it a row and column value
	def userClick(self,grid):
		while True:	
			clickPoint = grid.window.getMouse()
			# Takes care of the column click
			rowNum = clickPoint.getY()/40
			self.rowNum = rowNum
			# Takes care of the row click, row 0 starts at the bottom of the board
			colNum = clickPoint.getX()/40
			self.colNum = colNum
			# Loops until click is within range of grid and not on the text space below grid
			if rowNum <= 9 and colNum <= 9:
				break

	# Prompts user to place ships
	def placement(self):
		# Loops through every ship in list
		for ship in ships:
			while True:
				# Asks user for start and end points
				shipBoard.instructions('Select start point of your ' + ship[0],'black')
				self.userClick(shipBoard)
				rowStart = self.rowNum
				colStart = self.colNum
				# Turns start point chosen grey and waits for user to choose endpoint
				shipBoard.drawSquare(rowStart,colStart,'grey')
				shipBoard.instructions('Select end point of your ' + ship[0] + '(should be: ' + str(ship[1]) + ' spaces long)','black')
				self.userClick(shipBoard)
				rowEnd = self.rowNum
				colEnd = self.colNum
				# If all spots of the ship are legal sets the ship down there(on the board)
				if self.shipBoard.isLegalPlacement(rowStart,colStart,rowEnd,colEnd,ship[1]):
					for i in range(ship[1]):
						if rowStart == rowEnd:
							shipBoard.board[rowStart][min(colStart,colEnd) + i] = ship[0]
						else:
							shipBoard.board[min(rowStart,rowEnd) + i][colStart] = ship[0]
					break
				# If not all spots are legal, start point is changed back to blue and the user is asked to try again
				else:
					if shipBoard.board[rowStart][colStart] == '-':
						shipBoard.drawSquare(rowStart,colStart,'blue')
					shipBoard.instructions('Invalid placement, try again.','black')
					time.sleep(1)
			# Colors squares grey that have a ship on them
			for row in range(10):
				for column in range(10):
					if shipBoard.board[row][column] != '-':
						shipBoard.drawSquare(row,column,'grey')
		shipBoard.instructions('Please select a place to fire on the other board.','black')

	# Prompts user to choose a place to fire
	def move(self):
		while True:
			firingBoard.instructions('Select a place to fire.','black')
			self.userClick(firingBoard)
			# Checks if the shot is legal
			if firingBoard.isLegalMove(self.rowNum,self.colNum):	
				# If the shot is going to hit a ship, the ship is recorded as shipHit
				if firingBoard.board[self.rowNum][self.colNum] != '-':
					shipHit = self.firingBoard.board[self.rowNum][self.colNum]
				# Checks if the shot is a hit
				if firingBoard.isHit(self.rowNum,self.colNum):
					# If shot is a hit and sinks shipHit, it tells the user
					if firingBoard.isShipSunk(shipHit):
						firingBoard.instructions('You have sunk my ' + shipHit + '!','blue')
				time.sleep(.5)
				break
			# If shot is not valid tells the player and they try again
			else:
				firingBoard.instructions('Invalid choice.','black')

# If player wants to play again, function resets the game
def restart_program():
	python = sys.executable
	os.execl(python,python,*sys.argv)

def endClick():
	clickP = endGameWindow.getMouse()
	# Checks if Player clicks no, if so it returns False
	if clickP.getX() < 270 and clickP.getX() > 230:
		if clickP.getY() < 320 and clickP.getY() > 280:
			return False
	# Checks if Player clicks yes, if so it closes the windows and restarts the game
	if clickP.getX() < 170 and clickP.getX() > 130:
		if clickP.getY() < 320 and clickP.getY() > 280:
			window1.close()
			window2.close()
			restart_program()
	# If Player clicks neither yes or no, it runs again until the Player does
	else:
		endClick()
	
if __name__ == '__main__':
	while True:
		#Creates Player and computer windows and creates text for each
		window1 = GraphWin("Battleship Board", 400, 500)
		window2 = GraphWin("Firing Board", 400, 500)
		firingBoardText = Text(Point(200,450), 'Welcome to Battleship! This board holds my ships.')
		firingBoardText.draw(window2)
		shipBoardText = Text(Point(200,450), 'Welcome to Battleship! This is your board.')
		shipBoardText.draw(window1)
		# Creates BattleshipBoard objects based on the windows and text and draws grids on the windows 
		shipBoard = BattleshipBoard(window1,shipBoardText)
		firingBoard = BattleshipBoard(window2,firingBoardText)
		shipBoard.drawGrid()
		firingBoard.drawGrid()
		# Creates User and AI 
		user = User(shipBoard,firingBoard)
		AI = AI(shipBoard,firingBoard)
		time.sleep(.5)
		# Places AI's ships and prompts Player to place their ships
		AI.placement()
		user.placement()
		# User and AI continue to make moves until one of the boards' ships have all been hit
		while True:
			if not shipBoard.isGameOver():	
				user.move()
			if not firingBoard.isGameOver():
				AI.simpleMove()
			if shipBoard.isGameOver() or firingBoard.isGameOver():
				break
		# Once game is over, finds out who lost and tells the player
		if shipBoard.isGameOver():
			shipBoard.instructions('All your ships have been sunk! Thanks for playing Battleship!','black')
			endGameWindow = GraphWin('YOU LOST!', 400, 400)
			endGameText = Text(Point(200,200),'All your ships have been sunk! Thanks for playing Battleship!')

		if firingBoard.isGameOver():
			firingBoard.instructions('You have sunk all of my ships! Thanks for playing Battleship!','black')
			endGameWindow = GraphWin('YOU WON!!',400 , 400)
			endGameText = Text(Point(200,200),'You have sunk all of my ships! Congratulations!')
		# Gives Player the option to play again
		endGameText1 = Text(Point(200,250),'Do you want to play again?')
		# Makes Yes button on window
		playAgainY = Rectangle(Point(130,280),Point(170,320))
		playAgainY.setFill('blue')
		playAgainYText = Text(Point(150,300),'Yes')
		# Makes No button on window
		playAgainN = Rectangle(Point(230,280),Point(270,320))
		playAgainN.setFill('blue')
		playAgainNText = Text(Point(250,300),'No')
		# Draws it all on the endGameWindow
		endGameText.draw(endGameWindow)
		endGameText1.draw(endGameWindow)
		playAgainY.draw(endGameWindow)
		playAgainYText.draw(endGameWindow)
		playAgainN.draw(endGameWindow)
		playAgainNText.draw(endGameWindow)
		# Waits for Player to decide
		again = endClick()
		if again == False:
			break
			

