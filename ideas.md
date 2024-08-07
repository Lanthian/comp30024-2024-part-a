### Ideas
We want to build a search that uses a heuristic built from counting remaining tokens needed to complete a line that
removes target token. My suggestion, a minimum function between needed tokens on the horizontal and vertical axis 
of target. This will guide our search to massively prioritise completing one of the axes, but only one rather than
splitting between both. We could also use an additional heuristic function prior to this that values how close the 
closest red token is to either axis. So, summary:
* Our bot should prioritise building towards an axis that intersects our target
    * It is possible that it may need to clear other axes first to be able to reach a target axis.
* Once close enough, our bot should work towards filling all the tiles on one of these two axes. 

An A* search is recommended paired with these heuristics, considering each move to be a cost of one (we aim to minimise 
turns played). The search for a solution will be optimal this way - that is, least possible moves found - and complete - 
if there is a solution our program will find it, or an equivalently good solution.

The path played is not important so long as the found solution has minimised turns used - tied solutions are equally 
accepted. If there is no solution, we will exhaust the set of possible moves and output None. A key trick will be 
minimising the calculation required to assure that a board is unsolvable. Ideas regarding this optimisation:
* A list of seen states should be kept - repeat states discovered will not be queued up and instead dropped. (This will 
    add to general processing time, but cut down repeats, so should be quicker in long run and much better space wise)
* Looking at test-vis2.csv, it would be handy to find some clever quick check to see if the target square is blocked off
    from line completion via the formation of blue around it (e.g. red is boxed in). Might be better to frame this trick
    from source POV, rather than target POV.


### Physical code
* Need a way to generate all tetrominoes in all (non duplicate) orientations centred on a tile
    * then, need to validate that placing these on the board is valid (not on top of other existing tokens)
    * hard coding a function to output all these might be the best solution here at the time being
* Need to write a heuristic to evaluate board state
* Need to write a structure to contain each path - current board state, PLACEs made to get here (in order), current 
    board state cost
    * these structures will be kept in a queue, sorted on ascending current state cost


### 2024.03.22
* Tetrominoes are now generatable centred on a tile (hard coded) - now need a way to generate them AROUND a tile
    * board place actions can be now validated and placements can be made (filled axes are cleared)
* Heurestic written - considers an admissible estimate at least possible moves needed to reach and clear a target axis
* "path" structure not yet created, but brainstormed from class content 
    * (STATE, PARENT STATE, path cost so far (g(state)), remaining heuristic cost estimated (h(state)))
    * priority queue still agreed needed. Dictionary or set required for seen board states
## Search()
* Check if current state is goal state - terminate and output current path if so, add to seen if not
* Generate all 'place' actions around existing red tiles
* Check if place actions are valid, generate new board states from them if so
* Insert new board states into priority queue/linked list based on some g(state) + h(state)
* Select new current state from front of queue
* Repeat.


### 2024.03.23
* tetrominoes.py tetrominoes_plus() function added, along with coordinate filter for tetrominoes() - can now be used to 
    generate around a tile as needed
    
### 2024.03.24
* PriorityQueue implementation for state nodes begun
* tetrominoes_plus() duplicate pieces dropped
### Part B thoughts
PART B OF PROJECT BRAINSTORM
* Estimate long term consequences of our moves by evaluating board state with utility function.
    * Some measure of red vs blue squares on the board, with the consideration that not being able to move on your turn 
    is -infinite (big loss!), and opponent not being able to move on their turn is +infinite (big win!!)
* Depth of search ahead is a large consideration as it's exponential to a massive branching factor. Need to prune 
    options EFFICIENTLY to stop this.
* State evaluation only needed at node end, then minimax way back to current state?

* Board state evaluation ideas for tetress:
    * Number of red pieces vs blue vs air
    * Furthest red from furthest red (most reach of the board)
    * +Clearable "mostly blue" lines?
    * -Clearable "mostly red" lines...


### 2024.03.30
SOLVED! Issue was, heuristic was returning true value +11 for the now cleared row whenever it reached a goal state.
  In turn, every possible solution was being queued to the end of the priority queue - we were checking every single 
  node of the graph and stopping shy every time we found a solution to go check others. Bit silly, but glad it's solved
  now.
Solutions CAN now be output - not yet optimal. We should check between equal priority states if any are the goal before
  beginning to expand them all. Plus, a better heuristic can definitely be developed and we can possibly cut down on 
  which tetrominoes are generated for each tile of a board, rather than brute-force generating all of them and queueing
  them differently.


### 2024.04.03
Most time is lost to insertion into priority queue. A better data structure is needed here. 
  Even more important than an improved heuristic I'd wager...
  Alternatively, some kind of putall() for the PQ would also fix this
  Look into perhaps the heapdict module? Or something similar


### 2024.04.06
Insertion fixed, only thing left noticed is that problems of non-straight forward scope struggle massively with solving
  via our heuristic. And problems like test-vis3.csv still remain unsolvable - some trick needed to identify easy 
  way to shorten queue without exploring all nodes - pruning somehow?...
* test-vis4.csv (courtesy of Jack Tong via EDSTEM - https://edstem.org/au/courses/15502/discussion/1861078) terminated
    at "=== Lap 23517, Queue Size: 1277171 ===" - hypothesised not solvable with our current solution.
* test-vis3.csv also ran for a similar amount of time and deemed unsolvable.
