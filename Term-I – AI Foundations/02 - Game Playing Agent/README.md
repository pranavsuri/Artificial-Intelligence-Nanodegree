# Build a Game-Playing Agent
> This game-playing agent uses techniques such as Iterative Deepening, Minimax, and Alpha-Beta Pruning to compete in the game of Isolation (a two-player discrete competitive game with perfect information). The different heuristics used are then compared to find the best heuristic.

![Example game of isolation](images/viz.gif)

## About
This project is an adversarial search agent to play the game 'Isolation.' Isolation is a deterministic, two-player board game of perfect information in which the players alternate turns moving a single piece from one cell to another.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.

This project uses a version of Isolation where each agent is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chessboard). The agents can move to an open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. Movements are blocked at the edges of the board (the board does not wrap around). However, the player can "jump" blocked or occupied spaces (just like a knight in chess).

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

## Requirements
This project requires **Python 3**. It is recommended to use [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. Try using the environment provided in this folder.

### Using the Board Visualization
The `isoviz` folder contains a modified version of `chessboard.js` that can animate games played on a 7x7 board.  In order to use the board, you must run a local web server by running `python -m SimpleHTTPServer 8000` from your project directory (you can replace 8000 with another port number if that one is unavailable), then open your browser to `http://localhost:8000` and navigate to the `/isoviz/display.html` page.  Enter the move history of an isolation match (i.e., the array returned by the `Board.play()` method) into the text area and run the match. Refresh the page to run a different game.

## Files
- `game_agent.py` – Contains the code for the game-playing agent (see CustomPlayer class).

- `agent_test.py` - Provided by @udacity to unit test `game_agent.py` implementation.

- `tournament.py` - Provided by the @udacity staff to evaluate the performance of the game-playing agent.

- `heuristic_analysis.pdf` – Contains the analysis of the various heuristics implemented in the game_agent. The metrics are obtained from `tournament.py`.

- `research_review.pdf` – Reviews IBM's Deep Blue's [seminal paper](https://pdfs.semanticscholar.org/ad2c/1efffcd7c3b7106e507396bdaa5fe00fa597.pdf). A detailed blog post can be read on my blog on [this link]()

## Output (`tournament.py`)
```
*************************
 Evaluating: ID_Improved
*************************

Playing Matches:
----------
  Match 1: ID_Improved vs   Random    	Result: 15 to 5
  Match 2: ID_Improved vs   MM_Null   	Result: 14 to 6
  Match 3: ID_Improved vs   MM_Open   	Result: 16 to 4
  Match 4: ID_Improved vs MM_Improved 	Result: 12 to 8
  Match 5: ID_Improved vs   AB_Null   	Result: 14 to 6
  Match 6: ID_Improved vs   AB_Open   	Result: 12 to 8
  Match 7: ID_Improved vs AB_Improved 	Result: 11 to 9

Results:
----------
ID_Improved         67.14%

*************************
   Evaluating: Student   
*************************

Playing Matches:
----------
  Match 1:   Student   vs   Random    	Result: 17 to 3
  Match 2:   Student   vs   MM_Null   	Result: 14 to 6
  Match 3:   Student   vs   MM_Open   	Result: 14 to 6
  Match 4:   Student   vs MM_Improved 	Result: 13 to 7
  Match 5:   Student   vs   AB_Null   	Result: 18 to 2
  Match 6:   Student   vs   AB_Open   	Result: 13 to 7
  Match 7:   Student   vs AB_Improved 	Result: 16 to 4

Results:
----------
Student             75.00%
```

## License
[Modified MIT License © Pranav Suri](/License.txt)
