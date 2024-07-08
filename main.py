import copy
import random

class Board:
    def __init__(self, board=[["","",""],["","",""],["","",""]]):
      #board=[["","",""],["","",""],["","",""]] is an optional parameter(choice either board or [["","",""],["","",""],["","",""]])
        self.board = copy.deepcopy(board)
    
    def place_token(self, token, row, column):
      if self.board[row][column] == "":
        self.board[row][column] = token
        return True
      return False
    
    def print_board(self):
      for row in range(3):
        print(self.board[row])
        
    def tie(self):
      for row in range(3):
        for column in range(3):
          if self.board[row][column] == "":
            return False
      return True
    
    def check(self, token, opponent, row, column):
      # row win
      if self.board[row].count(token) == 3:
          return 1
      #column win
      count = 0
      for r in range(3):
        if self.board[r][column] == token:
          count += 1
        else:
          break
        if count == 3:
          return 1
          
      #diagonal win
      if row == column:
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == token:
          return 1
      if row == 2 - column:
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == token:
          return 1
          
      #row block
      if self.board[row].count(opponent) ==2 and self.board[row][column] == token:
        return -1
      
      #column block
      count_opponent = 0
      count_token = 0
      for r in range(3):
        if self.board[r][column] == token:
          count_token += 1
        elif self.board[r][column] == opponent:
          count_opponent += 1
      if count_opponent == 2 and count_token == 1:
        return -1
        
      #diagonal block
      count_opponent = 0
      count_token = 0
      if row == column:
        for i in range(3):
          if self.board[i][i] == token:
            count_token += 1
          elif self.board[i][i] == opponent:
            count_opponent += 1
        if count_opponent == 2 and count_token == 1:
          return -1
          
      if row == 2 - column:
        for i in range(3):
          if self.board[i][2-1] == token:
            count_token += 1
          elif self.board[i][2-i] == opponent:
            count_opponent += 1
        if count_opponent == 2 and count_token == 1:
          return -1
          
      return 0
            
class Node:
    def __init__(self, board):
        self.board = Board(board)
        self.priority = 0
        self.row = 0
        self.column = 0
        self.nodes = []    

corners = [[0,0], [0,2], [2,0], [2,2]]
sides = [[0,1], [1,0], [1,2], [2,1]]
main_board = Board()

class Computer:
    def __init__(self, token, opponent):
        self.token = token
        self.opponent = opponent
        self.node = None
      
    def best_move(self):
        self.node = Node(main_board.board)#main board - 2D list
        
        #build tree
        for r in range(3):
          for c in range(3):
            n = Node(self.node.board.board) #new node
            n.row = r
            n.column = c
            placed = n.board.place_token(self.token, r, c) # placed = true of false depending on line 12 & 13
            if placed: #if true
              self.node.nodes.append(n)
              n.priority = n.board.check(self.token, self.opponent, r, c) # priority = what returned (-1, 0, 1)
        
        #search tree
        best = 0
        best_node = None
        for node in self.node.nodes: # loop through tree
          if best == 0 and node.priority == -1: #-1 == block best == 0 -> best node to choose
            best = node.priority # replace best node with a block
            best_node = node #node that is best(one that blocks)
          elif node.priority == 1: #1 == win
            best = node.priority #replace best node with win
            best_node = node #node that is best(one that wins)
          
        return best_node
        
    def make_move(self):
      move_node = self.best_move()
      if move_node == None:
        if self.node.board == [["","",""],["","",""],["","",""]]: #if board is empty
          choice = random.choice(corners) # pick a corner
          corners.remove(choice)#remove corner from available choices
          return choice
        else:
          if main_board.board[1][1] == "": #if center is empty
            main_board.place_token(self.token, 1, 1) #place token [1, 1]
            return [1, 1]
          if main_board.board[1][1] == self.token: #if center has token
            if sides != []: #if a side is empty
              choice = random.choice(sides)#pick a side
              placed = main_board.place_token(self.token, choice[0], choice[1]) #place token
              sides.remove(choice)#remove side from list
              if placed:
                return choice#return random side
            
          if main_board.board[0][0] == self.token and main_board.board[2][2] == "": #if a corner has your token and the corner diagonal is empty place token
            main_board.place_token(self.token, 2, 2)
            corners.remove([2, 2])# remove corner
            return [2, 2]
          elif main_board.board[2][2] == self.token and main_board.board[0][0] == "":
            main_board.place_token(self.token, 0 ,0)
            corners.remove([0,0])
            return [0, 0]
          elif main_board.board[0][2] == self.token and main_board.board[2][0] == "":
            main_board.place_token(self.token, 2 ,0)
            corners.remove([2,0])
            return (2, 0)
          elif main_board.board[2][0] == self.token and main_board.board[0][2] == "":
            main_board.place_token(self.token, 0 ,2)
            corners.remove([0,2])
            return (0, 2)
          if corners != []: #if there's a available corner
            choice = random.choice(corners) #pick a random corner
            placed = main_board.place_token(self.token, choice[0], choice[1])#place token there
            corners.remove(choice)#remove cormer
            if placed:
              return choice#return random corner
          if sides != []: #if a side is empty
            choice = random.choice(sides)#pick a side
            placed = main_board.place_token(self.token, choice[0], choice[1]) #place token
            sides.remove(choice)#remove side from list
            if placed:
              return choice#return random side
            
        return []
      else: #if there is a best move- can win or block
        main_board.place_token(self.token, move_node.row, move_node.column)
        return [move_node.row, move_node.column]
      
class Player:
  def __init__(self, token):
    self.token = token
    
player = Player("X")
computer = Computer("O", "X")
turn = player
main_board.print_board()
while True: #infinite loop
  if turn == player: #if turn is player
    column = int(input("What column would you like to put your token? Enter 1-3: "))
    row = int(input("What row would you like to put your token? Enter 1-3: ")) 
    placed = main_board.place_token(turn.token, row - 1, column - 1)#place token
    while not placed: #if place is taken
      print("Sorry that place is taken")
      column = int(input("What column would you like to put your token? Enter 1-3: "))
      row = int(input("What row would you like to put your token? Enter 1-3: "))
      placed = main_board.place_token(player.token, row - 1, column - 1)# place token
    win = main_board.check(player.token, computer.token, row - 1, column - 1)#check to see if Player won (pass in check function)
    if win == 1: #if 1 is returned after check function
      print ("")      
      main_board.print_board()#print board
      print("Player Wins") 
      break #get out of "While True" loop
    else:
      tie = main_board.tie() #if entire board is full
      if tie:
        print ("")
        main_board.print_board()#print board
        print("It's a Tie")
        break#get out of "While True" loop
    turn = computer #computer's turn
  else:
    spot = computer.make_move() #spot is move made - what is returned after make move function
    if spot != []: #spot isn't empty, Computer made a move, isn't a tie
      win = main_board.check(computer.token, player.token, spot[0], spot[1])#check to see if Computer won (pass in check function)
      if win == 1:#if 1 is returned after check function
        print ("")        
        main_board.print_board()#print board
        print("Computer Wins")
        break#get out of "While True" loop
      else:
        tie = main_board.tie() #if entire board is full
        if tie:
          print ("")
          main_board.print_board()#print board
          print("It's a Tie")
          break#get out of "While True" loop
    turn = player #Player's turn
  print ("")
  main_board.print_board()#print board
  
Computer("O", "X")
