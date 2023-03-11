import pygame
# Define the screen size
screen_width = 640
screen_height = 640


# Define some colors
black = (224, 224, 224)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 125, 125)

# Define the size of each square on the chessboard
square_size = 80

# Load the chess piece images
pieces = {}
pieces_pawn_pro = ["Q", "R1", "B", "N"]
pieces["r1"] = pygame.image.load("images/rook.png")
pieces["r2"] = pygame.image.load("images/rook.png")
pieces["n"] = pygame.image.load("images/knight.png")
pieces["b"] = pygame.image.load("images/bishop.png")
pieces["q"] = pygame.image.load("images/queen.png")
pieces["k"] = pygame.image.load("images/king.png")
pieces["p"] = pygame.image.load("images/pawn.png")
pieces["R1"] = pygame.image.load("images/rookb.png")
pieces["R2"] = pygame.image.load("images/rookb.png")
pieces["N"] = pygame.image.load("images/knightb.png")
pieces["B"] = pygame.image.load("images/bishopb.png")
pieces["Q"] = pygame.image.load("images/queenb.png")
pieces["K"] = pygame.image.load("images/kingb.png")
pieces["P"] = pygame.image.load("images/pawnb.png")
pieces["piece"] = pygame.image.load("images/pawnb.png")
pieces["dot"] = pygame.image.load("images/dot.png")