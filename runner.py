import time
from agents import GameState, minimax, alphabeta

# Main function for a game between two AI agents
def play_game(player1_type, player1_heuristic, player1_depth,
              player2_type, player2_heuristic, player2_depth):

    # Seting up the initial 8x8 game board
    board = [[0 for _ in range(8)] for _ in range(8)]

    # Place Blue pieces (-1) on the top two rows
    for r in range(2):
        for c in range(8):
            board[r][c] = -1

    # Place Red pieces (1) on the bottom two rows
    for r in range(6, 8):
        for c in range(8):
            board[r][c] = 1

    # Initialize the game state with Red's turn
    state = GameState(board, 1)
    move_count = 0

    # Track stats for each player
    stats = {
        1: {"nodes": 0, "captures": 0, "times": []}, 
        -1: {"nodes": 0, "captures": 0, "times": []},
    }

    # Run the game loop until one side wins
    while not state.is_terminal():
        player = state.player
        start = time.time()
        tracker = {"nodes": 0}  # To count nodes evaluated in the current move

        # Choose settings based on which player's turn it is
        if player == 1:
            agent_type = player1_type
            heuristic = player1_heuristic
            depth = player1_depth
        else:
            agent_type = player2_type
            heuristic = player2_heuristic
            depth = player2_depth

        # Decide move using minimax or alpha-beta pruning
        if agent_type == "minimax":
            _, move = minimax(state, depth, heuristic, True, tracker)
        else:
            _, move = alphabeta(state, depth, heuristic, float('-inf'), float('inf'), True, tracker)

        end = time.time()

        # If no move is found, exit loop
        if move is None:
            break

        before_pieces = sum(cell == -player for row in state.board for cell in row)

        state = state.apply_move(move)

        # Count opponent's pieces after move to detect captures
        after_pieces = sum(cell == -player for row in state.board for cell in row)

        # Update stats
        stats[player]["captures"] += before_pieces - after_pieces
        stats[player]["nodes"] += tracker["nodes"]
        stats[player]["times"].append(end - start)

        move_count += 1

    # Determine winner based on final player turn
    winner = "Red (1)" if state.player == -1 else "Blue (-1)"

    return {
        "final_board": state.board,
        "winner": winner,
        "stats": stats,
        "moves": move_count
    }

def summarize_result(result):
    print(f"\nWinner: {result['winner']}")
    for player in [1, -1]:
        times = result["stats"][player]["times"]
        avg_time = sum(times) / len(times) if times else 0
        avg_nodes = result["stats"][player]["nodes"] / len(times) if times else 0
        print(f"\nPlayer {player} Stats:")
        print(f"  Total Nodes: {result['stats'][player]['nodes']}")
        print(f"  Avg Nodes/Move: {avg_nodes:.2f}")
        print(f"  Avg Time/Move: {avg_time:.4f} sec")
        print(f"  Captures: {result['stats'][player]['captures']}")
    print(f"Total Moves: {result['moves']}")
