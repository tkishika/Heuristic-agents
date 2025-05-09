import random
import time
import copy

class GameState:
    def __init__(self, board, player):
        self.board = board  # 2D list
        self.player = player  # 1 (Red) or -1 (Blue)

    def get_possible_moves(self):
        moves = []
        direction = -1 if self.player == 1 else 1
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == self.player:
                    for dr, dc in [(direction, 0), (direction, -1), (direction, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            if (dc == 0 and self.board[nr][nc] == 0) or (dc != 0 and self.board[nr][nc] == -self.player):
                                moves.append(((r, c), (nr, nc)))
        return moves

    def apply_move(self, move):   # defining move 
        (r1, c1), (r2, c2) = move
        new_board = copy.deepcopy(self.board)
        new_board[r2][c2] = new_board[r1][c1]
        new_board[r1][c1] = 0
        return GameState(new_board, -self.player)

    def is_terminal(self):
        # Check if a piece reached the opposite end

        if any(cell == -1 for cell in self.board[7]):  # Blue wins
            return True
        if any(cell == 1 for cell in self.board[0]):   # Red wins
            return True
        # Check if either player has no pieces left
        return all(cell != 1 for row in self.board for cell in row) or  all(cell != -1 for row in self.board for cell in row)
def defensive_heuristic_1(state):
    return 2 * sum(cell == state.player for row in state.board for cell in row) + random.random()

def offensive_heuristic_1(state):
    return 2 * (30 - sum(cell == -state.player for row in state.board for cell in row)) + random.random()

def offensive_heuristic_2(state):
    score = 0
    for r in range(8):
        for c in range(8):
            if state.board[r][c] == state.player:
                score += (state.player * r)
                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8 and state.board[nr][nc] == -state.player:
                        score += 3
    return score + random.random()

defensive_rows = {1: range(5, 8), -1: range(0, 3)}
def defensive_heuristic_2(state):
    score = 0
    for r in range(8):
        for c in range(8):
            if state.board[r][c] == state.player:
                score += 2
                if r in defensive_rows[state.player]:
                    score += 2
            elif state.board[r][c] == -state.player:
                if r in defensive_rows[-state.player]:
                    score -= 1
    return score + random.random()

def minimax(state, depth, eval_fn, is_maximizing, tracker):  #defining minimax
    tracker['nodes'] += 1
    if depth == 0 or state.is_terminal():
        return eval_fn(state), None

    best_move = None
    if is_maximizing:
        max_eval = float('-inf')
        for move in state.get_possible_moves():
            eval, _ = minimax(state.apply_move(move), depth - 1, eval_fn, False, tracker)
            if eval > max_eval:
                max_eval, best_move = eval, move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in state.get_possible_moves():
            eval, _ = minimax(state.apply_move(move), depth - 1, eval_fn, True, tracker)
            if eval < min_eval:
                min_eval, best_move = eval, move
        return min_eval, best_move

def alphabeta(state, depth, eval_fn, alpha, beta, is_maximizing, tracker):
    tracker['nodes'] += 1
    if depth == 0 or state.is_terminal():
        return eval_fn(state), None

    best_move = None
    if is_maximizing:
        value = float('-inf')
        for move in state.get_possible_moves():
            eval, _ = alphabeta(state.apply_move(move), depth - 1, eval_fn, alpha, beta, False, tracker)
            if eval > value:
                value, best_move = eval, move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = float('inf')
        for move in state.get_possible_moves():
            eval, _ = alphabeta(state.apply_move(move), depth - 1, eval_fn, alpha, beta, True, tracker)
            if eval < value:
                value, best_move = eval, move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move
