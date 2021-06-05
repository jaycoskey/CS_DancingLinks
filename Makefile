# Solves the Calendar Block Puzzle by DragonFjord (dragonfjord.com)
#     Covers 366 variants---one for each day on the calendar.
calendar:
	./calendar_block_problem.py

calendar_batch:
	./calendar_block_problem.py --batch

# Solves the Chessboard Block Problem by Dana Scott,
#     included in Donald Knuth's Dancing Links paper.
# Covers the full problem and the three sub-problems
#     mentioned in the paper.
chessboard:
	./chessboard_block_problem.py

chessboard_batch:
	./chessboard_block_problem.py --batch

clean:
	rm -rf Jan* Feb* Mar* Apr* May* Jun*
	rm -rf Jul* Aug* Sep* Oct* Nov* Dec*
	rm -rf chessboard_block_problem_*
	rm -rf __pycache__
