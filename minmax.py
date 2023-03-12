import random
from cmath import inf
import json
import re
from time import time
from reward import *



pawnPromotions = ['r', 'n', 'q', 'b']
cache_moves = {}
with open("./moves_cache.json", "r") as f:
    print("Open cache file")
    try:
        cache_moves = json.load(f)
        print("cache total: " + str(len(cache_moves['lower'])))
        # if the file is empty the ValueError will be thrown
    except ValueError:
        cache_moves = {'lower': {}, 'upper': {}, 'eval': {}}


def CPUMiniMaxTurn(board, islower, isMoved, depth=4):
    global totalNode
    global totalNodeInCache
    global cache_moves
    global ab_Max
    global ab_Min

    ab_Max = inf
    ab_Min = -inf


    startTime = time()
    totalNode = 0
    totalNodeInCache = 0

    label = 'lower' if islower else 'upper'
    li = CanGoList(board, islower, isMoved)
    Max = -inf

    cache = cache_moves[label].get(re.sub(
        '(\[)|(\])|(")|( )', '', json.dumps(board)))
    if cache:
        return cache[0]

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

    with open("./moves_cache.json", "w") as f:
        cache_moves[label][re.sub(
            '(\[)|(\])|(")|( )', '', json.dumps(board))] = (r, Max)
        json.dump(cache_moves, f)

    print('Total nodes', totalNode)
    print('Total nodes found in cache', totalNodeInCache)
    print('Time:', time() - startTime)
    print('Max:', Max)
    return r

def Minimax(node, depth, Pmax, Pnow, isMoved={'k': False, 'K': False, 'r1': False,
                                              'R1': False, 'r2': False, 'R2': False}, alpha=-inf, beta=inf):
    """
    node là node hiện tại
    depth là độ sâu
    Pmax là player cần tìm Max
    Pnow là player hiện tại
    isMoved dùng để kiểm tra các quân xe, vua có di chuyển hay chưa để nhập thành
    alpha là giá trị tốt nhất của người chơi maximizing (mặc định là -inf)
    beta là giá trị tốt nhất của người chơi minimizing (mặc định là inf)
    """
    global totalNode
    global ab_Max
    global ab_Min

    totalNode += 1
    if isFinish(node) or depth == 0:
        return reward(node, Pmax)
    if Pmax == Pnow:
        Max = -inf
        for row, col, newRow, newCol in CanGoList(node, Pnow, isMoved):
            if 'p' in node[row][col] and row == 6:
                for pro in pawnPromotions:
                    child = [_[:] for _ in node]
                    pawnPromotion(child, row, col, newRow, newCol, pro)
                    Max = max(Max, Minimax(child, depth - 1, Pmax, not Pnow, isMoved, alpha, beta))
                    alpha = max(alpha, Max)
                    if beta <= alpha:
                        break
            else:
                child = [_[:] for _ in node]
                makeMove(child, row, col, newRow, newCol, isMoved)
                rsl_minimax = Minimax(child, depth - 1, Pmax, not Pnow, isMoved, alpha, beta)
                Max = max(Max, rsl_minimax)
                alpha = max(alpha, Max)
                if beta <= alpha:
                    break
  
        return Max
    else:
        Min = inf
        for row, col, newRow, newCol in CanGoList(node, Pnow, isMoved):
            if 'p' in node[row][col] and row == 6:
                for pro in pawnPromotions:
                    child = [_[:] for _ in node]
                    pawnPromotion(child, row, col, newRow, newCol, pro)
                    Min = min(Min, Minimax(child, depth - 1, Pmax, not Pnow, isMoved, alpha, beta))
                    beta = min(beta, Min)
                    if beta <= alpha:
                        break
            else:
                child = [_[:] for _ in node]
                makeMove(child, row, col, newRow, newCol, isMoved)
                rsl_minimax = Minimax(child, depth - 1, Pmax, not Pnow, isMoved, alpha, beta)
                Min = min(Min, rsl_minimax)
                beta = min(beta, Min)
                if beta <= alpha:
                    break

        return Min

