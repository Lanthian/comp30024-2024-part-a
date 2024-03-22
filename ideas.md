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