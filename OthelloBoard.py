import copy
import pyxel
import OthelloArenaPython.OthelloLogic as OthelloLogic

class OthelloBoard:
    def __init__(self, x=0, y=0, size=8):
        self.x = x
        self.y = y
        self.size = size
        self.reset()
        self.IMG_SIZE = 16
    def reset(self):
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
        self.board[int(self.size/2)-1][int(self.size/2)-1] = 1
        self.board[int(self.size/2)][int(self.size/2)-1]=-1
        self.board[int(self.size/2)-1][int(self.size/2)]=-1
        self.board[int(self.size/2)][int(self.size/2)]=1
        self.lastPut = [-1, -1]
    def setBoard(self,board):
        self.board = copy.deepcopy(board)
    def getBoard(self):
        return self.board
    def execute(self, action, player):
        moves = self.getMoves(player=player)
        if not (action in moves):
            print(self.board)
            print('合法手ではない手が打たれました' + action)
            return False
        self.board = OthelloLogic.execute(board=self.board,action=action,player=player,size=len(self.board)) 
        self.lastPut = action
        return True
    def getMoves(self, player):
        return OthelloLogic.getMoves(board=self.board,player=player,size=len(self.board))
    def input(self, mouse_x, mouse_y, player):
        img_size = self.IMG_SIZE
        for m in self.getMoves(player=player):
            if img_size*m[1] <= mouse_x-self.x < img_size*(m[1]+1) and img_size*m[0] <= mouse_y-self.y < img_size*(m[0]+1):
                return self.execute(action=m,player=player)
        return False
    def drawBoard(self, player=0, showPut=True, reverse=False):
        img_size = self.IMG_SIZE
        for u in range(len(self.board)):
            for v in range(len(self.board[u])):
                p = self.board[u][v]
                type : int = 0
                if u == self.lastPut[1] and v == self.lastPut[0]:
                    type = 2
                p_ = p if reverse == False else -p
                pyxel.blt(x=img_size*u+self.x,y=img_size*v+self.y,img=0,u=img_size*(p+1),v=type*img_size,w=img_size,h=img_size)
        if player == 0 or showPut == False:
            return
        for m in OthelloLogic.getMoves(board=self.board,player=player,size=len(self.board)):
            p = self.board[m[1]][m[0]]
            pyxel.blt(x=img_size*m[1]+self.x,y=img_size*m[0]+self.y,img=0,u=img_size*(p+1),v=img_size,w=img_size,h=img_size)
    #def drawBoard(board, player, lastPut=None, reverse=False):
    #    None
    #def drawSmaleBoard(board, player, lastPut=None, reverse=False):
    #    None
    def count(self):
        c = [0, 0, 0]
        playerId = [1, -1]
        for p in range(2):
            for b1 in self.board:
                for b2 in b1:
                    c[2] += 1
                    if (b2 == playerId[p]):
                        c[p] += 1
        return c
    def space(self):
        s = 0
        for b1 in self.board:
            for b2 in b1:
                if b2 == 0:
                    s += 1
        return s