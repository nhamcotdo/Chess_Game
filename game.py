from termcolor import colored
from movement import *


class Game:
    Bot = True

    def __init__(self, isBotFirst=Bot) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Chess Game")
        # bot luôn là chữ thường
        self.chess_board = [
            ["r1", "n1", "b1", "q", "k", "b2", "n2", "r2"],
            ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
            ["R1", "N1", "B1", "Q", "K", "B2", "N2", "R2"]
        ]
        self.curSelectedPiece = None
        self.isBotTurn = isBotFirst
        self.isMoved = {'k': False, 'K': False, 'r1': False, 'R1': False, 'r2': False, 'R2': False}

    def checkClickPosition(self, mouse_pos):
        x, y = mouse_pos
        col, row = x // square_size, y // square_size

        # print(col, row)
        piece = self.chess_board[row][col]

        if piece != ' ' and piece != 'dot' and piece.islower() == self.isBotTurn:
            canGos = CanGo(self.chess_board, col, row, self.isBotTurn, self.isMoved)
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
                if (row + col) % 2 == 0:
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
