from movement import *
totalNode = 0
totalNodeInCache = 0

def reward(board, isLower):
    global totalNodeInCache
    global totalNode
    
    totalNode += 1

    # cache = cache_moves['eval'].get(re.sub(
    #     '(\[)|(\])|(")|( )', '', json.dumps(board)))
    # if cache:
    #     totalNodeInCache += 1
    #     return cache

    totalPoints = 0
    totalPoints += value(board, isLower) * 10
    totalPoints += matchStatus(board, isLower) * 3 + \
        matchStatus(board, not isLower) * 2

    # cache_moves['eval'][re.sub(
    #         '(\[)|(\])|(")|( )', '', json.dumps(board))] = totalPoints

    return totalPoints


def value(board, isLower):
    """
    Board: Bàn cờ hiện tại
    islower: lượt của quân viết thường (True) hay quân viết hoa (False)
    return: giá trị của bàn cờ đối với quân viết thường
    """
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


def matchStatus(board, isLower):
    """
    return:
    0: NORMAL
    1: STEALMATE
    2: CHECK
    inf: CHECKMATE
    """
    king = 'k' if isLower else 'K'
    canGosOfKing = set()
    row, col = 0, 0
    for y in range(8):
        for x in range(8):
            c = board[y][x]
            if c == king:
                canGosOfKing = set(Kk(board, x, y))
                row, col = y, x
                break

    enermyList = set([(newCol, newRow) for x, y, newRow, newCol in CanGoList(
        chessboard=board, isLower=not isLower)])

    canGosOfKing = canGosOfKing.difference(enermyList)

    if isLower:
        if (col, row) in enermyList:
            if canGosOfKing:
                return 2
            else:
                return 1000
        if not canGosOfKing:
            return 1
    else:
        if (col, row) in enermyList:
            if canGosOfKing:
                return -2
            else:
                return -1000
        if not canGosOfKing:
            return -1

    return 0