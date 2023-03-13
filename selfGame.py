from Minmax import *
from game import *

game = Game(True)
count = 1
step = 1
A = 0
B = 0
# Game loop
running = True
while running:
    # Handle events
    print('step:', step)
    step += 1
    if not game.isBotTurn:
        print('Caculating..........')
        row, col, newRow, newCol, pawnPro = CPUMiniMaxTurn(
            game.chess_board.copy(), game.isBotTurn, game.isMoved.copy(), position=game.pos.copy(), depth=random.choice([2,3]))
        # print(row, col, newCol, newRow, pawnPro)
        # print(game.pos)
        game.makeMove(row, col, newRow, newCol, pawnPro)
        game.isBotTurn = not game.isBotTurn

        game.LastMove[0] = newRow
        game.LastMove[1] = newCol

    elif game.isBotTurn:
        print('Caculating..........')
        row, col, newRow, newCol, pawnPro = CPUMiniMaxTurn(
            game.chess_board.copy(), game.isBotTurn, game.isMoved.copy(), position=game.pos.copy(), depth=random.choice([3,4]))
        # print(row, col, newCol, newRow, pawnPro)
        # print(game.pos)
        game.makeMove(row, col, newRow, newCol, pawnPro)
        game.isBotTurn = not game.isBotTurn

        game.LastMove[0] = newRow
        game.LastMove[1] = newCol

    game.printBoard()

    if game.isFinish():
        print(count)
        if game.isBotTurn:
            A += 1
        else:
            B += 1
        print(A, '/', B)
        count+=1
        step = 0
        print('You win' if game.isBotTurn else 'Bot win')
        game = Game(game.isBotTurn)
        running = False
    # Draw the chessboard and pieces
    # game.draw_chessboard()
    # game.draw_pieces()
    # game.draw_canGo()

    # Update the display
    # pygame.display.flip()

# Quit Pygame
pygame.quit()
