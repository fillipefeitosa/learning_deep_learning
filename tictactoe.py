""" 
    A deep  learning algo to learn how to play
    tic tac toe.
    Step 1: Create the tic-tac-toe game board and working environment
    Step 2: Create a Q-lerning agent that can play the game by itself, initialize and store a Q-table
    Step 3: Implement the reward system to improve the exploit behavior
    Step 4: Make the agent play, record and displays statistics
"""

# Winning patterns - Used for check_winning()
import random
import logging
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd


logger = logging.getLogger(__name__)


winning_patterns = [
    [(0, 0), (0, 1), (0, 2)],  # Row 1
    [(1, 0), (1, 1), (1, 2)],  # Row 2
    [(2, 0), (2, 1), (2, 2)],  # Row 3
    [(0, 0), (1, 0), (2, 0)],  # Column 1
    [(0, 1), (1, 1), (2, 1)],  # Column 2
    [(0, 2), (1, 2), (2, 2)],  # Column 3
    [(0, 0), (1, 1), (2, 2)],  # Diagonal 1
    [(0, 2), (1, 1), (2, 0)],  # Diagonal 2
]


class QLearningAgent:

    available_rewards = {"X": 10, "O": -5, "DRAW": -0.1}  # -0.01 is for neutral moves

    def __init__(self, episilon=0.1, alpha=0.1, gamma=0.99):
        self.q_table = {}
        self.active_player = "X"
        self.episilon = episilon
        self.alpha = alpha
        self.gamma = gamma

    def update_q_table(self, state, next_state, action, status):

        if (
            status and status in self.available_rewards.keys()
        ):  # basically when the game finishes
            reward = self.available_rewards[status]
        else:
            reward = 0.01  # encourage winning quickly

        # Let's ensure that current state and following actions exists in Q-table
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0

        current_q_value = self.q_table[state][action]
        # max_q_value_from_state = max(self.q_table[state].values())

        # Max q_value needs to be the highest q-value from the next possible action
        if next_state in self.q_table:
            max_q_value_from_next_state = max(
                self.q_table[next_state].values(), default=0.0
            )
        else:
            max_q_value_from_next_state = (
                0.0  # Default for terminal states, when game ends
            )

        updated_q_value = current_q_value + self.alpha * (
            reward + self.gamma * max_q_value_from_next_state - current_q_value
        )

        self.q_table[state][action] = updated_q_value

    def initialize_q_value(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = {}

        # if action does not exist, add a default value
        # logger.info("action: {}".format(action))
        # print("action {}".format(action))
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0  # default q-value

    def decide_next_move(self, state, valid_actions):

        if random.random() <= self.episilon:  # explore
            move = random.choice(valid_actions)
        else:  # exploit
            # Check if the state exists in the q-table, if not explore
            if state not in self.q_table or not self.q_table[state]:
                move = random.choice(valid_actions)

            max_q_value = max(self.q_table[state].values())
            # get the highest value if a Tie exists
            best_actions = [
                action
                for action, value in self.q_table[state].items()
                if value == max_q_value
            ]
            move = random.choice(best_actions)

        return move
        # return move

    def play_match(self):
        # start a new match
        new_game = Game()

        # and start making valid moves while the still runs (status == False)
        while True:
            # Check empty spaces for valid plays
            valid_actions = [
                (row, col)
                for row in range(3)
                for col in range(3)
                if new_game.game_board[row][col] == " "
            ]

            state = new_game.get_state()

            for action in valid_actions:
                self.initialize_q_value(state, action)

            move = self.decide_next_move(state, valid_actions)

            # self.update_q_table(state)

            status, winner = new_game.make_move(self.active_player, move)

            self.update_q_table(state, new_game.get_state(), move, new_game.status)

            if status:
                # print("Game is over. Final result is: {}".format(winner))
                return winner
            self.active_player = (
                "O" if self.active_player == "X" else "X"
            )  # Switch player
        # new_game.display_board()


class Game:

    def __init__(self):
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]
        self.status = False  # Indicates if game ended
        self.winner = None  # Tracks the winner

    # ---- Q-learning agent specifics
    def get_state(self):
        """Get the Game State, how the board is filled,
        reprenting the moves done so far.

        Returns:
            tuple: A tuple with current state of the game (Eg. (' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' '))
        """
        return tuple(cell for row in self.game_board for cell in row)

    # ---- Game Mechanics -----
    def reset_board(self):
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]
        self.status = False
        self.winner = None

    def check_draw(self):
        if self.status:  # Exit if the game is over. Prevens self.winner from overwrite
            return
        if all(cell != " " for row in self.game_board for cell in row):
            self.winner = "DRAW"
            # print("Game was a {} !!!".format(self.winner))
            self.status = True

    def check_winner(self, player: str):
        for pattern in winning_patterns:
            if all(self.game_board[row][col] == player for row, col in pattern):
                self.winner = player
                # print(f"And we have a winner: {self.winner} !!")
                self.status = True

    def display_board(self):
        for row in self.game_board:
            print("|".join(row))
        print()

    def make_move(self, player: str, coordinates: tuple):
        # Validate input
        if not isinstance(coordinates, tuple) or len(coordinates) != 2:
            raise ValueError("Coordinates must be a tuple with two ints (row, col)")

        row, col = coordinates

        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError("Coordinates must be within range 0 to 2")
        if self.game_board[row][col] != " ":
            raise ValueError("Cell is occupied.")

        self.game_board[row][col] = player
        self.check_winner(player)
        self.check_draw()
        # self.display_board()
        # return is needed for an automated gameplay
        return self.status, self.winner


# Process stats for plotting and analysis
def process_stats_for_plot(stats_for_plot):
    # Convert stats to a DataFrame for easier processing
    stats_df = pd.DataFrame.from_dict(
        stats_for_plot, orient="index", columns=["Winner"]
    )
    stats_df.index.name = "Episode"

    # Count cumulative wins for each player

    cumulative_wins = pd.DataFrame(0, index=stats_df.index, columns=["X", "O", "DRAW"])

    # Calculate percentages
    for episode, winner in stats_df["Winner"].items():
        if winner in cumulative_wins.columns:
            cumulative_wins.loc[episode:, winner] += 1

    # Calculate percentages
    cumulative_wins["Total"] = cumulative_wins.sum(axis=1)
    percentages = cumulative_wins.div(cumulative_wins["Total"], axis=0) * 100
    percentages.drop(columns=["Total"], inplace=True)

    return percentages


stats_for_plot = {}


# Trainning flow logic
def train_agent(agent: QLearningAgent, episodes=10000):
    track_wins = {"X": 0, "O": 0, "DRAW": 0}

    for episode in tqdm(range(episodes), desc="Trainning Agent"):
        winner = agent.play_match()
        if winner in track_wins:
            stats_for_plot[episode] = winner
            track_wins[winner] += 1

    print("\nTrainning Complete!")
    print("\nFinal Stats: {}".format(track_wins))


# Main execution
if __name__ == "__main__":
    print("Let's start playing TicTacToe!")
    my_agent = QLearningAgent()

    train_agent(my_agent, 100000)

    percentages = process_stats_for_plot(stats_for_plot)

    plt.figure(figsize=(10, 6))

    colors = {"X": "blue", "O": "red", "DRAW": "green"}

    for player in percentages.columns:
        plt.plot(
            percentages.index,
            percentages[player],
            label=f"{player} Win %",
            color=colors[player],
        )

    # Add a horizontal line for 50% as a reference
    plt.axhline(50, color="gray", linestyle="--", label="50% Line")

    # Add titles and labels
    plt.title("Training Convergence of Tic-Tac-Toe Agent", fontsize=14)
    plt.xlabel("Episodes", fontsize=12)
    plt.ylabel("Win Percentage (%)", fontsize=12)

    # Add legend and grid
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()
