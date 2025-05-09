# run this file to run the game!!!!

from runner import play_game, summarize_result
from agents import (
    offensive_heuristic_1,
    defensive_heuristic_1
)

# Minimax vs Alpha-beta
result = play_game(
    player1_type="minimax",
    player1_heuristic=offensive_heuristic_1,
    player1_depth=3,
    player2_type="alphabeta",
    player2_heuristic=defensive_heuristic_1,
    player2_depth=3
)

summarize_result(result)
