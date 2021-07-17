# Solving the Calendar and Chessboard Block Puzzles using Dancing Links

## Description
The code in this directory uses Knuth's [Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links) algorithm (a.k.a. DLX) from his excellent paper "[Dancing Links](https://arxiv.org/pdf/cs/0011047.pdf)" to solve several puzzles.
* It solves a [Calendar Block Puzzle](https://www.dragonfjord.com/product/a-puzzle-a-day/) sold by the company [DragonFjord](https://www.dragonfjord.com/). For each date of the year, the challenge is to find an arrangement of the blocks that leaves that date's month and day uncovered, while covering every other space. This is an example of an [Exact Cover Problem](https://en.wikipedia.org/wiki/Exact_cover).
* It also solves a few variations of Dana Scott's chessboard problem from Donald Knuth's Dancing Links paper. I mainly wrote this to test the implementation of DLX.
* As of initial check-in, this (non-concurrent, non-parallel) code running on a 2.2 GHz laptop takes 1:47:32 to find all solutions for all 366 days of the Calendar Block Puzzle. That's about 20 solutions per second.

## Sample solution plots

| Chessboard Block Problem solution | Calendar Puzzle solution (Sep 19th) |
:----------------------------------:|:------------------------------------:
![](/images/plot_chessboard_block_problem_sub3.png) | ![](images/plot_Sep19.png)

## How to find solutions
  * Calendar
    * To compute solutions to each of the 366 Calendar Block Problem variations, choose one of:
      * % make calendar
      * % make calendar_batch
  * Chessboard Block Problem
    * To compute solutions to Data Scott's Chessboard Block Problem, and a few of its variations, choose one of:
      * % make chessboard
      * % make chessboard_batch
      * % ./chessboard_block_problem.py <MONTH> <DAY> where MONTH is one of Jan ... Dec, and DAY is one of 1 ... 31.

## How many solutions to the calendar problem are there?

The number of solutions per day for the calendar problem ranges from 7 (for October 6th) to 216 (for January 25th). For the entire year, there are 24,405. Here's a diagram showing the distribution.
![](/images/calendar_block_problem_solutions_by_date.png)

## Log files for each problem
  * **layouts_**<*problem_name*>
    * All orientations of all blocks.
  * **linfos_**<*problem_name*>
    * All orientations and positions (i.e., the "layout info") of all blocks.
  * **plot_**<*problem_name*>.png
    * A diagram of the first solution found.
  * **prob_**<*problem_name*>
    * The problem matrix.
  * **solns_**<*problem_name*>
    * All solutions found. (Requires layouts and layout info data for interpretation.)
  * **stats_**<*problem_name*>
    * Stats showing the number of nodes traversed ("updates") in the search tree, the number of solutions found, and the elapsed time spent.

## Source files
* exact_cover_problem.py
  * A base class and functions used to read and write problem and solution files related to the Exact Cover Problem.
* block2d.py
  * A base class to represent the blocks in block puzzles
* block2d_problem.py
  * A class to represent the 2D block puzzles---a particular type of Exact Cover Problem.
* calendar_block_problem.py
  * Solves all 366 instances of the Calendar Block Problem.
* chessboard_block_problem.py
  * Solves Dana Scott's chessboard-based bloc problem, including a few variations.
* dlx.py
  * An implementation of Knuth's "Dancing Links" or DLX algorithm.

## Trivia
  * The solution count per day for the Calendar Block Problem ranges from 65 to 1044. Only one day has more than 1,000 solutions.
 
## TODO
  * Add the month name and day to the Calendar Block Problem's solution images.
  * Add solutions to other interesting problems.
  * Add the feature of reconstructing solutions from log files, even if the source code has changed since the log files were generated. This would involve changing the format of some of the log files. 
