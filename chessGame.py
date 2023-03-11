import pygame
from minmax import *

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
            print(x // square_size, y // square_size)
            canGoList = game.checkClickPosition(mouse_pos)
            print(canGoList, game.curSelectedPiece)

        elif not game.isBotTurn and game.curSelectedPiece and event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            newPos = game.isValidMove(mouse_pos)
            print(game.curSelectedPiece)
            if newPos:
                newRow, newCol = newPos
                row, col = game.curSelectedPiece.curPos
                game.chess_board[col][row] = ' '
                if game.curSelectedPiece.curPiece in 'kKR1r1R2r2':
                    game.isMoved[game.curSelectedPiece.curPiece] = True
                game.chess_board[newCol][newRow] = game.curSelectedPiece.curPiece
                game.curSelectedPiece = None
                game.isBotTurn = not game.isBotTurn

        elif game.isBotTurn:
            print('Caculating..........')
            row, col, newRow, newCol = CPUMiniMaxTurn(game.chess_board, game.isBotTurn)
            print(row, col, newRow, newCol)
            game.printBoard()
            if game.curSelectedPiece.curPiece in 'kKR1r1R2r2':
                game.isMoved[game.chess_board[row][col]] = True
            game.chess_board[newRow][newCol] = game.chess_board[row][col]
            game.chess_board[row][col] = ' '
            game.isBotTurn = not game.isBotTurn
            game.printBoard()
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
