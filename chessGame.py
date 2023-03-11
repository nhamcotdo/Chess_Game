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
                newCol, newRow = newPos
                col, row = game.curSelectedPiece.curPos
                game.chess_board[row][col] = ' '
                game.chess_board[newRow][newCol] = game.curSelectedPiece.curPiece
                if game.curSelectedPiece.curPiece in 'kKR1r1R2r2':
                    game.isMoved[game.curSelectedPiece.curPiece] = True

                if game.curSelectedPiece.curPiece == 'K' and col - newCol == -2:
                    col1, row1 = 7, 7
                    newCol, newRow = 5, 7
                    game.chess_board[newRow][newCol] = game.chess_board[row1][col1]
                    game.chess_board[row1][col1] = ' '

                if game.curSelectedPiece.curPiece == 'K' and col - newCol == 2:
                    col1, row1 = 0, 7
                    newCol, newRow = 2, 7
                    game.chess_board[newRow][newCol] = game.chess_board[row1][col1]
                    game.chess_board[row1][col1] = ' '

                game.curSelectedPiece = None
                game.isBotTurn = not game.isBotTurn

        elif game.isBotTurn:
            print('Caculating..........')
            col, row, newCol, newRow = CPUMiniMaxTurn(
                game.chess_board, game.isBotTurn)
            print(col, row, newCol, newRow)
            game.printBoard()
            if game.chess_board[col][row] in 'kKR1r1R2r2':
                game.isMoved[game.chess_board[col][row]] = True
            game.chess_board[newCol][newRow] = game.chess_board[col][row]
            game.chess_board[col][row] = ' '
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
