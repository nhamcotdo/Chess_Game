from setting import *

liR = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
liL = [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)]
liD = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
liU = [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]
liRD = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
liLU = [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
liRU = [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)]
liLD = [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
liN = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
liK = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]


def Rr(chessboard, col, row):
    """Các nước có thể đi của quân Xe"""
    return Go(chessboard, col, row, liR) + Go(chessboard, col, row, liL) + Go(chessboard, col, row, liU) + Go(chessboard, col, row, liD)


def Bb(chessboard, col, row):
    """Các nước có thể đi của quân Tượng"""
    return Go(chessboard, col, row, liRD) + Go(chessboard, col, row, liLU) + Go(chessboard, col, row, liRU) + Go(chessboard, col, row, liLD)


def Qq(chessboard, col, row):
    """Các nước có thể đi của quân Hậu"""
    return Rr(chessboard, col, row) + Bb(chessboard, col, row)


def Nn(chessboard, col, row):
    """Các nước có thể đi của quân Mã"""
    return Go(chessboard, col, row, liN, isContinue=True)


def Kk(chessboard, col, row, isMoved):
    """Các nước có thể đi của quân Vua"""
    li = []
    li = li + Go(chessboard, col, row, liK, isContinue=True)

    if isMoved:
        if chessboard[row][col].islower():
            if not (isMoved['k'] or isMoved['r1']) and chessboard[0][1] == ' ' and chessboard[0][2] == ' ' and chessboard[0][3] == ' ':
                li.append((2, 0))
            if not (isMoved['k'] or isMoved['r2']) and chessboard[0][5] == ' ' and chessboard[0][6] == ' ':
                li.append((6, 0))
        if chessboard[row][col].isupper():
            if not (isMoved['K'] or isMoved['R1']) and chessboard[7][1] == ' ' and chessboard[7][2] == ' ' and chessboard[7][3] == ' ':
                li.append((2, 7))
            if not (isMoved['K'] or isMoved['R2']) and chessboard[7][5] == ' ' and chessboard[7][6] == ' ':
                li.append((6, 7))

    return li


def Pp(chessboard, col, row):
    """Các nước có thể đi của quân Tốt"""
    li = []
    dx = 1
    if not chessboard[row][col].islower():
        dx = -1
    # nước có thể đi
    if row == 1 or row == 6:
        li = li + Go(chessboard, col, row,
                     [(0, dx), (0, 2*dx)], canFight=False)
    else:
        li = li + Go(chessboard, col, row, [(0, dx)], canFight=False)
    # nước có thể ăn (tốt ăn chéo)
    li = li + Go(chessboard, col, row, [(-1, dx), (1, dx)], needFight=True)
    return li


def Go(chessboard, x, y, l, isContinue=False, canFight=True, needFight=False):
    li = []
    for dx, dy in l:
        x1 = x+dx
        y1 = y+dy
        if x1 < 0 or x1 >= 8 or y1 < 0 or y1 >= 8:
            if not isContinue:
                break
            else:
                continue
        if chessboard[y1][x1] != ' ':
            if canFight and chessboard[y][x].islower() != chessboard[y1][x1].islower():
                li.append((x1, y1))
            if not isContinue:
                break
            else:
                continue
        if not needFight:
            li.append((x1, y1))
    return li


def isFinish(chessboard):
    U = False
    L = False
    for _ in chessboard:
        U = U or ('K' in _)
        L = L or ('k' in _)
    return not (U and L)


class CurrSelectedPiece:
    def __init__(self, curPiece, curPos, canGoList):
        self.curPiece = curPiece
        self.curPos = curPos
        self.canGoList = canGoList

    def __str__(self) -> str:
        return f'curPiece: {self.curPiece} curPos: {self.curPos} canGoList: {self.canGoList}'


def CanGoList(chessboard, isLower, isMoved):
    """ return tất cả các nước có thể di chuyển (y,x) -> (y1,x1)"""
    li = []
    for row in range(8):
        for col in range(8):
            piece = chessboard[row][col]
            if piece != ' ' and piece.islower() == isLower:
                l = CanGo(chessboard, col, row, isLower, isMoved)
                for newCol, newRow in l:
                    li = li + [(row, col, newRow, newCol)]
    return li


def CanGo(chessboard, col, row, islower, isMoved={}):
    """Danh sách các vị trí có thể di chuyển của quân ở vị trí x, y"""
    piece = chessboard[row][col]
    if piece.islower() != islower:
        return []
    if 'r' in piece.lower():
        return Rr(chessboard, col, row)
    if 'n' in piece.lower():
        return Nn(chessboard, col, row)
    if 'b' in piece.lower():
        return Bb(chessboard, col, row)
    if 'q' in piece.lower():
        return Qq(chessboard, col, row)
    if 'k' in piece.lower():
        return Kk(chessboard, col, row, isMoved)
    if 'p' in piece.lower():
        return Pp(chessboard, col, row)
    return []


def makeMove(chessboard, row, col, newRow, newCol, isMoved):
    curPiece = chessboard[row][col]
    chessboard[newRow][newCol] = curPiece
    chessboard[row][col] = ' '

    if curPiece in 'kKR1r1R2r2':
        isMoved[curPiece] = True

    #  Quân trắng
    if curPiece == 'K' and col - newCol == -2:
        #  Di chuyển quân xe phải để nhập thành
        row1, col1 = 7, 7
        newRow, newCol = 7, 5
        chessboard[newRow][newCol] = chessboard[row1][col1]
        chessboard[row1][col1] = ' '

    if curPiece == 'K' and col - newCol == 2:
        #  Di chuyển quân xe trái để nhập thành
        row1, col1 = 7, 0
        newRow, newCol = 7, 3
        chessboard[newRow][newCol] = chessboard[row1][col1]
        chessboard[row1][col1] = ' '

    #  Quân trắng
    if curPiece == 'k' and col - newCol == -2:
        #  Di chuyển quân xe phải để nhập thành
        row1, col1 = 0, 7
        newRow, newCol = 0, 2
        chessboard[newRow][newCol] = chessboard[row1][col1]
        chessboard[row1][col1] = ' '

    if curPiece == 'k' and col - newCol == 2:
        #  Di chuyển quân xe trái để nhập thành
        row1, col1 = 0, 0
        newRow, newCol = 0, 3
        chessboard[newRow][newCol] = chessboard[row1][col1]
        chessboard[row1][col1] = ' '

def pawnPromotion(chessboard, row, col, newRow, newCol, pro):
    chessboard[newRow][newCol] = pro
    chessboard[row][col] = ' '