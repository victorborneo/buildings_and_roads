Buildings and Roads
===================

Given an 2d matrix, build a graph representing such matrix.

# Running the code
- **It is necessary to have Graphviz installed.** Download it [here](https://graphviz.org/download/) and **make sure to add it to your environment variables (PATH).**

- Copy this repository and use the following commands:
  - `python -m venv .venv`;
  - Activate the virtual environment with `.\.venv\Scripts\activate` on Windows, or `source .venv/bin/activate` on Linux;
  - `python -m pip install -r requirements.txt`;
  - Run the `main.py` script.

# Inputs
In the inputs file, setup the 2d matrix in the `grid` variable.
 - Use the character `R` to represent roads;
 - Anything that is not an `R` or empty space will be considered a building ID;
 - Specify the storages in the `storage_ids` list.

# Logic
First, iterate over the grid and keep track of:
 - The buildings, by simply checking if the current cell is not an `R` or empty space;
 - The intersections, by counting each `R` cell's neighbors. If there are more than 2 `R` cells around the current cell (orthogonally), then it is an interception;
 - The deadends, by counting if the current `R` cell has either:
   - No `R` neighbors, or;
   - Exactly one `R` neighbor but no building neighbor.

Second, iterate through the buildings and perform an Depth-First Search (DFS) on the `R` cells, stopping whenever it finds another graph node (like interceptions or other buildings).

Third, iterate through the interceptions and deadends just like the second step, connecting between themselves.

# Considerations
To avoid duplicated nodes (X -- Y and Y -- X), it's necessary to keep track of the edges (in this case, using a set).

To avoid buildings poiting to themselves because of roads tangencing them, only add edges if `origin != current_cell`.

Using dictionaries and sets whenever possible to speedup lookups with O(1) time.

## Keeping track of road width and adding a node whenever it changes.
This step has proven to be quite a challenge.

Basic examples are easy to get around but there are way too many edge cases.

I wonder if there's a more robust way of doing it that I can't think of, or if it really is just very complicated.
