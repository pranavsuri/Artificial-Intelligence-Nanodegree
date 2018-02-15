"""This file contains all the classes you must complete for this project.

You can use the test cases in `agent_test.py` to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known relative
strength using `tournament.py` and include the results in your report.
"""

import random
import math

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

# Heuristic Definitions
def penalize_corners(game, player):
    """Heuristic which penalizes the player for moving to a corner and returns
    a float value of the difference in legal moves of the two players.

    PARAMETERS:
        game :: `isolation.Board`
            An instance of `isolation.Board` encoding the current state of
            the game (e.g. player locations and blocked cells).

        player :: object
            A player instance in the current game.

    RETURNS:
        float :: The heuristic value of the current game state to a specified
        player.
    """

    # Check if game is already over
    if game.is_loser(player):
        return float('-inf')
    if game.is_winner(player):
        return float('inf')

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # Penalize for moving to corner
    corner_weight = 4
    if is_corner(game, game.get_player_location(player)):
        own_moves -= corner_weight

    return float(own_moves - opp_moves)

def is_corner(game, player_location):
    """Returns 'True' if player's current location is a board corner.
    """
    corner_positions = [(0, 0), (0, game.height - 1), \
                        (game.width - 1, 0), \
                        (game.width - 1, game.height - 1)]
    return player_location in corner_positions

def run_away(game, player):
    """Heuristic to credit player moves that are farther from the opponent and
    returns a float value of the difference in legal moves of the two players.

    PARAMETERS:
        game :: `isolation.Board`
            An instance of `isolation.Board` encoding the current state of
            the game (e.g. player locations and blocked cells).

        player :: object
            A player instance in the current game.

    RETURNS:
        float :: The heuristic value of the current game state to a specified
        player.
    """

    # Check if game is already over
    if game.is_loser(player):
        return float('-inf')
    if game.is_winner(player):
        return float('inf')

    opp_player = game.get_opponent(player)
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # Reward player for choosing moves farther from opponent
    distance = euclid_distance(game, player, opp_player)
    own_moves += distance

    return((own_moves - opp_moves))

def euclid_distance(game, player, opp_player):
    """Returns distance between current positions of two players.
    """
    player_location = game.get_player_location(player)
    opp_location = game.get_player_location(opp_player)
    x_dist = math.pow(player_location[0] - opp_location[0], 2)
    y_dist = math.pow(player_location[1] - opp_location[1], 2)
    return math.sqrt(x_dist + y_dist)

def foresee_moves(game, player):
    """Heuristic that returns a float of the difference in the number of legal
    moves in the current game state plus the number of possible moves.

    PARAMETERS:
        game :: `isolation.Board`
            An instance of `isolation.Board` encoding the current state of
            the game (e.g. player locations and blocked cells).

        player :: object
            A player instance in the current game.

    RETURNS
        float :: The heuristic value of the current game state to a specified
        player.
    """

    # Check if game is already over
    if game.is_loser(player):
        return float('-inf')
    if game.is_winner(player):
        return float('inf')

    own_legal_moves = game.get_legal_moves(player)
    own_moves = len(own_legal_moves)
    for m in own_legal_moves:
        own_moves += len(game.get_moves(m))

    opp_legal_moves = game.get_legal_moves(game.get_opponent(player))
    opp_moves = len(opp_legal_moves)
    for m in opp_legal_moves:
        opp_moves += len(game.get_moves(m))

    return float(own_moves - opp_moves)

def normalized_moves(game, player):
    """
    Heuristic that returns the difference of player's and opponent's move(s),
    divided by total of all remaining legal moves.

    PARAMETERS:
        game :: `isolation.Board`
            An instance of `isolation.Board` encoding the current state of
            the game (e.g. player locations and blocked cells).

        player :: object
            A player instance in the current game.

    RETURNS:
        float :: The heuristic value of the current game state to a specified
        player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    score = float((own_moves - opp_moves) / (own_moves + opp_moves))
    return score

def custom_score(game, player):
    """Calclate the heuristic value of a game state from the point of view of
    the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` - you should not need to call this function directly.

    PARAMETERS:
        game :: `isolation.Board`
            An instance of `isolation.Board` encoding the current state of
            the game (e.g. player locations and blocked cells).

        player :: object
            A player instance in the current game.

    RETURNS:
        float :: The heuristic value of the current game state to a specified
        player.
    """

    # return penalize_corners(game, player)
    # return run_away(game, player)
    return foresee_moves(game, player)
    # return normalized_moves(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    PARAMETERS:
        search_depth :: int (optional)
            A strictly positive integer (i.e., 1, 2, 3,...) for the number of
            layers in the game tree to explore for fixed-depth search i.e., a
            depth of one (1) would only explore the immediate sucessors of the
            current state. This parameter should be ignored when
            iterative = True.

        score_fn :: callable (optional)
            A function to use for heuristic evaluation of game states.

        iterative :: boolean (optional)
            Flag indicating whether to perform fixed-depth search (False) or
            iterative deepening search (True). When True, search_depth should
            be ignored and no limit to search depth.

        method :: {'minimax', 'alphabeta'} (optional)
            The name of the search method to use in get_move().

        timeout :: float (optional)
            Time remaining (in milliseconds) when search is aborted. Should be
            a positive value large enough to allow the function to return
            before the timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        PARAMETERS:
            game :: `isolation.Board`
                An instance of `isolation.Board` encoding the current state of
                the game (e.g., player locations and blocked cells).

            legal_moves :: list<(int, int)>
                A list containing legal moves. Moves are encoded as tuples of
                pairs of ints defining the next (row, col) for the agent to
                occupy.

            time_left :: callable
                A function that returns the number of milliseconds left in the
                current turn. Returning with any less than 0 ms remaining
                forfeits the game.

        RETURNS:
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        if not legal_moves:
            return (-1, -1)

        move = None
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring.
            algorithm_name = getattr(self, self.method)
            if self.iterative:
                depth = 1 # Depth used for iterative deepening.
                while True:
                    _, move = algorithm_name(game, depth)
                    depth += 1
            else:
                _, move = algorithm_name(game, self.search_depth)
        except Timeout:
            # Return the best move so far in-case of time-out.
            return move
        return move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        PARAMETERS:
            game :: isolation.Board
                An instance of the Isolation game `Board` class representing
                the current game state.

            depth :: int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting.

            maximizing_player :: bool
                Flag indicating whether the current search depth corresponds to
                a maximizing layer (True) or a minimizing layer (False).

        RETURNS:
            float :: The score for the current search branch

            tuple(int, int) :: The best move for the current branch;
            (-1, -1) for no legal moves
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Return heuristic value of game when search has reached max depth
        if depth == 0:
            # Note: No need to return the move.
            # The max/min players keep a track of them.
            return (self.score(game, self), None)

        # Verify if there are any available legal moves
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (game.utility(self), (-1, -1))

        # Maximize/minimize play accordingly
        if maximizing_player:
            return self.minimax_maximize(game, legal_moves, depth)
        else:
            return self.minimax_minimize(game, legal_moves, depth)

    def minimax_maximize(self, game, legal_moves, depth):
        """Minimax maximizer player. Returns the highest (score, move)
        tuple found in the game."""
        highest_score, selected_move = (float('-inf'), (-1, -1))
        for move in legal_moves:
            score, _ = self.minimax(game.forecast_move(move), \
            depth - 1, False)
            highest_score, selected_move = max((highest_score, \
            selected_move), (score, move))
        return (highest_score, selected_move)

    def minimax_minimize(self, game, legal_moves, depth):
        """Minimax maximizer player. Returns the lowest (score, move)
        tuple found in the game."""
        lowest_score, selected_move = (float('inf'), (-1, -1))
        for move in legal_moves:
            score, _ = self.minimax(game.forecast_move(move), depth - 1)
            lowest_score, selected_move = min((lowest_score, \
            selected_move), (score, move))
        return (lowest_score, selected_move)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"),
    maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        PARAMETERS:
            game :: `isolation.Board`
                An instance of the Isolation game 'Board' class representing
                the current game state.

            depth :: int
                Depth is an integer representing the maximum number of plies
                to search in the game tree before aborting.

            alpha :: float
                Alpha limits the lower bound of search on minimizing layers.

            beta :: float
                Beta limits the upper bound of search on maximizing layers.

            maximizing_player :: bool
                Flag indicating whether the current search depth corresponds
                to a maximizing layer (True) or a minimizing layer (False).

        RETURNS:
            float
                The score for the current search branch.

            tuple(int, int)
                The best move for the current branch; (-1, -1) for no legal
                moves.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Return heuristic value of game when search has reached max-depth
        if depth == 0:
            # Move need not be returned.
            # Min/Max players keep a track of them.
            return (self.score(game, self), None)

        # Verify if there are any available legal moves
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (game.utility(self), (-1, -1))

        # Maximize/minimize play accordingly
        if maximizing_player:
            return self.ab_maximize_play(game, legal_moves, depth, alpha, beta)
        else:
            return self.ab_minimize_play(game, legal_moves, depth, alpha, beta)

    def ab_maximize_play(self, game, legal_moves, depth, alpha, beta):
        """Alphabeta maximizer player. Returns the highest score/move
        tuple found in game, pruning the search tree."""
        highest_score, selected_move = (float('-inf'), (-1, -1))
        for move in legal_moves:
            score, _ = self.alphabeta(game.forecast_move(move), \
            depth - 1, alpha, beta, False)
            if score > alpha:
                alpha = score
                highest_score, selected_move = score, move
            if alpha >= beta:
                break
        return (highest_score, selected_move)

    def ab_minimize_play(self, game, legal_moves, depth, alpha, beta):
        """Alphabeta minimizer player. Returns the lowest score/move
        tuple found in game, pruning the search tree."""
        lowest_score, selected_move = (float('inf'), (-1, -1))
        for move in legal_moves:
            score, _ = self.alphabeta(game.forecast_move(move), \
            depth - 1, alpha, beta, True)
            if score < beta:
                beta = score
                lowest_score, selected_move = score, move
            if beta <= alpha:
                break
        return (lowest_score, selected_move)
