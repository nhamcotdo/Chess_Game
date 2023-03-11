from termcolor import colored
from movement import *


class Game:
    Bot = True
    LastMove = [-1, -1]

    def __init__(self, isBotFirst=Bot, chessBoard=[["r1", "n", "b", "q", "k", "b", "n", "r2"],
                 ["p", "p", "p", "p", "p", "p", "p", "p"],
                 [" ", " ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " ", " "],
                 ["P", "P", "P", "P", "P", "P", "P", "P"],
                 ["R1", "N", "B", "Q", "K", "B", "N", "R2"]]) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Chess Game")
        # bot luôn là chữ thường
        # chessBoard=[
        #         ["r1", "n", "b", "q", "k", "b", "n", "r2"],
        #         ["p", "p", "p", "p", "p", "p", "p", "p"],
        #         [" ", " ", " ", " ", " ", " ", " ", " "],
        #         [" ", " ", " ", " ", " ", " ", " ", " "],
        #         [" ", " ", " ", " ", " ", " ", " ", " "],
        #         [" ", " ", " ", " ", " ", " ", " ", " "],
        #         ["P", "P", "p", "P", "P", "P", "P", "P"],
        #         ["R1", "N", "B", "Q", "K", "B", "N", "R2"]]
        
        self.chess_board = chessBoard
        self.curSelectedPiece = None
        self.isBotTurn = isBotFirst
        self.isMoved = {'k': False, 'K': False, 'r1': False,
                        'R1': False, 'r2': False, 'R2': False}

    def checkClickPosition(self, mouse_pos):
        x, y = mouse_pos
        col, row = x // square_size, y // square_size

        # print(col, row)
        piece = self.chess_board[row][col]

        if piece != ' ' and piece != 'dot' and piece.islower() == self.isBotTurn:
            canGos = CanGo(self.chess_board, col, row,
                           self.isBotTurn, self.isMoved)
            if canGos:
                self.curSelectedPiece = CurrSelectedPiece(
                    piece, (col, row), canGos)
                return canGos
        self.curSelectedPiece = None
        return []

    def isValidMove(self, mouse_pos):
        x, y = mouse_pos
        col, row = x // square_size, y // square_size

        if self.curSelectedPiece.curPos == (col, row):
            self.curSelectedPiece = None
            return False

        if (col, row) in self.curSelectedPiece.canGoList:
            return (col, row)

        return False

    def printBoard(self):
        print("+", *range(8), "+")

        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                if self.chess_board[i][j] == ' ':
                    print(self.chess_board[i][j], end=" ")
                elif self.chess_board[i][j].islower():
                    print(colored(self.chess_board[i][j][0], 'red'), end=" ")
                else:
                    print(colored(self.chess_board[i][j][0], 'blue'), end=" ")
            print(i,)

        print("+", *range(8), "+")
        print()

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess_board[row][col]
                if piece != " ":
                    x = col * square_size + square_size // 2
                    y = row * square_size + square_size // 2
                    self.screen.blit(pieces[piece],
                                     pieces[piece].get_rect(center=(x, y)))

    def draw_canGo(self):
        if not self.curSelectedPiece:
            return

        for canGo in self.curSelectedPiece.canGoList:
            colGo, rowGo = canGo
            xGo = colGo * square_size + square_size // 2
            yGo = rowGo * square_size + square_size // 2
            self.screen.blit(pieces['dot'],
                             pieces['dot'].get_rect(center=(xGo, yGo)))

    def draw_chessboard(self):
        for row in range(8):
            for col in range(8):
                x = col * square_size
                y = row * square_size
                if self.LastMove[0] == row and self.LastMove[1] == col:
                    color = green
                elif (row + col) % 2 == 0:
                    color = white
                else:
                    color = black
                pygame.draw.rect(self.screen, color, pygame.Rect(
                    x, y, square_size, square_size))

    def isFinish(self):
        U = False
        L = False
        for _ in self.chess_board:
            U = U or ('K' in _)
            L = L or ('k' in _)
        return not (U and L)

    def makeMove(self, row, col, newRow, newCol, pawnPro=' '):
        curPiece = self.chess_board[row][col]
        self.chess_board[newRow][newCol] = curPiece
        self.chess_board[row][col] = ' '

        if curPiece in 'kKR1r1R2r2':
            self.isMoved[curPiece] = True

        #  Quân trắng
        if curPiece == 'K' and col - newCol == -2:
            #  Di chuyển quân xe phải để nhập thành
            row1, col1 = 7, 7
            newRow, newCol = 7, 5
            self.chess_board[newRow][newCol] = self.chess_board[row1][col1]
            self.chess_board[row1][col1] = ' '

        if curPiece == 'K' and col - newCol == 2:
            #  Di chuyển quân xe trái để nhập thành
            row1, col1 = 7, 0
            newRow, newCol = 7, 3
            self.chess_board[newRow][newCol] = self.chess_board[row1][col1]
            self.chess_board[row1][col1] = ' '

        #  Quân trắng
        if curPiece == 'k' and col - newCol == -2:
            #  Di chuyển quân xe phải để nhập thành
            row1, col1 = 0, 7
            newRow, newCol = 0, 5
            self.chess_board[newRow][newCol] = self.chess_board[row1][col1]
            self.chess_board[row1][col1] = ' '

        if curPiece == 'k' and col - newCol == 2:
            #  Di chuyển quân xe trái để nhập thành
            row1, col1 = 0, 0
            newRow, newCol = 0, 3
            self.chess_board[newRow][newCol] = self.chess_board[row1][col1]
            self.chess_board[row1][col1] = ' '

        if curPiece[0] == 'P' and newRow == 0:
            pawnPro = self.pawnPromotion()
            self.chess_board[newRow][newCol] = pawnPro

        if curPiece[0] == 'p' and newRow == 7:
            self.chess_board[newRow][newCol] = pawnPro

    def pawnPromotion(self):
        start_X = 2 * square_size
        start_Y = 3 * square_size
        for row in range(1):
            for col in range(4):
                x = start_X + col * square_size
                y = start_Y + row * square_size
                color = blue
                pygame.draw.rect(self.screen, color, pygame.Rect(
                    x, y, square_size, square_size))
                xP = x + square_size // 2
                yP = y + square_size // 2
                self.screen.blit(
                    pieces[pieces_pawn_pro[col]], pieces[pieces_pawn_pro[col]].get_rect(center=(xP, yP)))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    # Check if the user released the mouse button while dragging the piece
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    x = x // square_size
                    y = y // square_size
                    print(x, y)

                    if y != 3:
                        continue
                    else:
                        if x == 2:
                            return pieces_pawn_pro[0]
                        elif x == 3:
                            return pieces_pawn_pro[1]
                        elif x == 4:
                            return pieces_pawn_pro[2]
                        elif x == 5:
                            return pieces_pawn_pro[3]
