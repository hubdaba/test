import sys
import random
class game_state:
    
    def __init__(self, board):
        self.board = board

    def successors(self):
        suc = []
        for i in range(len(self.board)):
            for j in range(self.board[i]):
                newBoard = self.board[:]
                if not newBoard[i] == j:
                    newBoard[i] = j
                    sum = 0
                    for num in newBoard:
                        sum += num
                    if sum is not 0:
                        suc.append(game_state(newBoard))
        return suc

    def __str__(self):
        return str(self.board)

    def get_hash(self, piece):
        newboard = self.board[:]
        alist = sorted(newboard,key = lambda(k):k)
        return (str(alist), piece)

    def score(self, piece):
        sum = 0
        for freq in self.board:
            sum += freq
        if sum == 1:
            return -1 * piece
        return None

    def getScore(self, piece, scores):
        score = self.score(piece)
        hash = self.get_hash(piece)
        if score is not None:
            scores[hash] = score
            return score
        if scores.has_key(hash):
            return scores[hash]
        succ = self.successors()
        currBest = succ[0].getScore(-1 * piece, scores)
        for state in succ:
            next_score = state.getScore(-1 * piece, scores)
            if currBest is None:
                currBest = next_score
            if piece > 0:
                if next_score > currBest:
                    currBest = next_score
            else:
                if currBest > next_score:
                    currBest = next_score
        scores[hash] = currBest
        return currBest

def simulate(scores, init, piece):
    currState = init
    currPiece = piece
    succ = currState.successors()
    bestMove = scores[succ[0].get_hash(-1 * currPiece)]
    nextBoard = succ[0]
    for move in succ:
        hash = move.get_hash(currPiece * -1)
        if piece > 0:
            if scores[hash] > bestMove:
                bestMove = scores[hash]
                nextBoard = move
        if piece < 0:
            if scores[hash] < bestMove:
                bestMove = scores[hash]
                nextBoard = move
    print nextBoard

def nextBestMove(scores, board, piece):
    succ = board.successors();
    bestMove = scores[succ[0].get_hash(-1 * piece)]
    posMoves = []
    for move in succ:
        hash = move.get_hash(piece * -1)
        if piece > 0:
            if scores[hash] == 1:
                posMoves.append(move)
        if piece < 0:
            if scores[hash] == -1:
                posMoves.append(move)
    for num in posMoves:
        print num

scores = None
while True:
    print "what is the board's current state"
    line = sys.stdin.readline()
    piece = line.split(" ")
    intPiece = []
    for num in piece:
        intPiece.append(int(num))
    board = game_state(intPiece)
    valid = True
    if scores is None:
        scores = {}
        board.getScore(1, scores)
    else:
        hash1 = board.get_hash(1)
        hash2 = board.get_hash(-1)
        if not scores.has_key(hash2) and not scores.has_key(hash1):
            print "not a valid board"
            valid = False
    if valid:
        nextBestMove(scores, board, 1)

