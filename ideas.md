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
