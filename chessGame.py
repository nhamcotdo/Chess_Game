from minmax import *
from game import *

game = Game(False)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game.isBotTurn and not game.curSelectedPiece and event.type == pygame.MOUSEBUTTONUP:
            # Check if the user released the mouse button while dragging the piece
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos
            # print(x // square_size, y // square_size)
            canGoList = game.checkClickPosition(mouse_pos)
            # print(canGoList, game.curSelectedPiece)

        elif not game.isBotTurn and game.curSelectedPiece and event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            newPos = game.isValidMove(mouse_pos)
            # print(game.curSelectedPiece)
            if newPos:
                newCol, newRow = newPos
                col, row = game.curSelectedPiece.curPos
                game.makeMove(row, col, newRow, newCol)
                game.curSelectedPiece = None
                game.isBotTurn = not game.isBotTurn

                game.LastMove[0] = newRow
                game.LastMove[1] = newCol

        elif game.isBotTurn:
            print('Caculating..........')
            row, col, newRow, newCol, pawnPro = CPUMiniMaxTurn(
                game.chess_board.copy(), game.isBotTurn, game.isMoved.copy())
            print(row, col, newCol, newRow, pawnPro)
            game.makeMove(row, col, newRow, newCol, pawnPro)
            game.isBotTurn = not game.isBotTurn
            game.printBoard()

            game.LastMove[0] = newRow
            game.LastMove[1] = newCol

    if game.isFinish():
        print('You win' if game.isBotTurn else 'Bot win')
        running = False
    # Draw the chessboard and pieces
    game.draw_chessboard()
    game.draw_pieces()
    game.draw_canGo()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
