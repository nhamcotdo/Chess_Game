from minmax import *
from game import *

game = Game(True)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if not game.isBotTurn:
            print('Caculating..........')
            row, col, newRow, newCol = random.choice(CanGoList(game.chess_board.copy(),isLower=game.isBotTurn,isMoved=game.isMoved,position=game.pos))
            # print(row, col, newCol, newRow, pawnPro)
            print(game.pos)
            game.makeMove(row, col, newRow, newCol, pawnPro)
            game.isBotTurn = not game.isBotTurn
            game.printBoard()

            game.LastMove[0] = newRow
            game.LastMove[1] = newCol

        elif game.isBotTurn:
            print('Caculating..........')
            row, col, newRow, newCol, pawnPro = CPUMiniMaxTurn(
                game.chess_board.copy(), game.isBotTurn, game.isMoved.copy(), position=game.pos.copy(), depth=random.choice([2,3,4]))
            # print(row, col, newCol, newRow, pawnPro)
            print(game.pos)
            game.makeMove(row, col, newRow, newCol, pawnPro)
            game.isBotTurn = not game.isBotTurn
            game.printBoard()

            game.LastMove[0] = newRow
            game.LastMove[1] = newCol

    if game.isFinish():
        print('You win' if game.isBotTurn else 'Bot win')
        game = Game(game.isBotTurn)
        running = False
    # Draw the chessboard and pieces
    game.draw_chessboard()
    game.draw_pieces()
    game.draw_canGo()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
