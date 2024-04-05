# Team: BeatBytes
### Contributors:
* Anthony Hill
* Liam Anthian

Tetress game demo found here - https://comp30024.pages.gitlab.unimelb.edu.au/2024s1/project-playground/

---
# Due Dates
### Part A: 8th of April, 11pm

Places red tiles on a board, stemming off other red tokens, until an axis is filled in such a way that a target cell "B"
is cleared in turn. Searches for a possible solution in all following board states via A*.

To run our code, clone 'search' directory and via terminal input:       python -m search < [game csv file]      
e.g.
* python -m search < test-vis1.csv
* python -m search < tung-csvs/1.csv
