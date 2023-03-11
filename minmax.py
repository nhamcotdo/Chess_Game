import random
from game import *
from cmath import inf

pawnPromotions = ['r', 'n', 'q', 'b']


def CPUMiniMaxTurn(board, islower, isMoved, depth=2):
    #######################################################
    #  Nên dùng Minimax với độ sâu từ 2 đến 4             #
    #######################################################
    li = CanGoList(board, islower, isMoved)
    Max = -inf

    for row, col, newRow, newCol in li:
        if 'p' in board[row][col] and row == 6:
            for pawnPro in pawnPromotions:
                child = [_[:] for _ in board]

                pawnPromotion(child, row, col, newRow, newCol, pawnPro)
                vl = Minimax(child, depth-1, islower,
                             not islower, isMoved.copy())
                if Max < vl or (Max == vl and random.choice([0, 1]) == 0):
                    Max = vl
                    r = (row, col, newRow, newCol, pawnPro)
        else:
            child = [_[:] for _ in board]

            makeMove(child, row, col, newRow, newCol, isMoved)
            vl = Minimax(child, depth-1, islower,
                         not islower, isMoved.copy())
            if Max < vl or (Max == vl and random.choice([0, 1]) == 0):
                Max = vl
                r = (row, col, newRow, newCol, ' ')

    print(Max)
    return r

# Board: Bàn cờ hiện tại
# islower: lượt của quân viết thường (True) hay quân viết hoa (False)
# return: giá trị của bàn cờ đối với quân viết thường


def value(board, isLower):
    val = 0
    for y in range(8):
        for x in range(8):
            c = board[y][x]
            if c == ' ':
                continue
            if 'p' in c.lower():
                val += 1 if c.islower() == isLower else -1
                if (c.islower() == isLower and y == 1) or (not c.islower() == isLower and y == 6):
                    val += 5 if c.islower() == isLower else -5
            elif 'n' in c.lower():
                val += 3 if c.islower() == isLower else -3
            elif 'b' in c.lower():
                val += 3 if c.islower() == isLower else -3
            elif 'r' in c.lower():
                val += 5 if c.islower() == isLower else -5
            elif 'q' in c.lower():
                val += 20 if c.islower() == isLower else -20
            elif 'k' in c.lower():
                val += 1000 if c.islower() == isLower else -1000
            else:
                print('Unknown piece:', c)
    return val

# node là node hiện tại
# depth là độ sâu
# Pmax là player cần tìm Max
# Pnow là player hiện tại


def Minimax(node, depth, Pmax, Pnow, isMoved={'k': False, 'K': False, 'r1': False,
                                              'R1': False, 'r2': False, 'R2': False}):

    if isFinish(node) or depth == 0:
        return value(node, Pmax)
    if Pmax == Pnow:
        Max = -inf
        for row, col, newRow, newCol in CanGoList(node, Pnow, isMoved):
            if 'p' in node[row][col] and row == 6:
                for pro in pawnPromotions:
                    child = [_[:] for _ in node]
                    pawnPromotion(child, row, col, newRow, newCol, pro)
                    Max = max(Max, Minimax(child, depth -
                                           1, Pmax, not Pnow, isMoved))
            else:
                makeMove(child, row, col, newRow, newCol, isMoved)
                Max = max(Max, Minimax(child, depth -
                          1, Pmax, not Pnow, isMoved))
        return Max
    else:
        Min = inf
        for row, col, newRow, newCol in CanGoList(node, Pnow, isMoved):
            child = [_[:] for _ in node]
            if 'p' in node[row][col] and row == 6:
                for pro in pawnPromotions:
                    child = [_[:] for _ in node]
                    pawnPromotion(child, row, col, newRow, newCol, pro)
                    Min = min(Min, Minimax(child, depth -
                                           1, Pmax, not Pnow, isMoved))
            else:
                makeMove(child, row, col, newRow, newCol, isMoved)
                Min = min(Min, Minimax(child, depth -
                          1, Pmax, not Pnow, isMoved))
        return Min
