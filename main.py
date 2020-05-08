from random import random
import pandas as pd


class QLearner:
    _q_matrix = None
    _learn_rate = None
    _discount_factor = None

    def __init__(self,
                 possible_states,
                 possible_actions,
                 initial_reward,
                 learning_rate,
                 discount_factor):
        """
        Initialise the q learning class with an initial matrix and the parameters for learning.

        :param possible_states: list of states the agent can be in
        :param possible_actions: list of actions the agent can perform
        :param initial_reward: the initial Q-values to be used in the matrix
        :param learning_rate: the learning rate used for Q-learning
        :param discount_factor: the discount factor used for Q-learning
        """
        # Initialize the matrix with Q-values
        init_data = [[float(initial_reward) for _ in possible_states]
                     for _ in possible_actions]
        self._q_matrix = pd.DataFrame(data=init_data,
                                      index=possible_actions,
                                      columns=possible_states)

        # Save the parameters
        self._learn_rate = learning_rate
        self._discount_factor = discount_factor

    def get_best_action(self, state):
        """
        Retrieve the action resulting in the highest Q-value for a given state.

        :param state: the state for which to determine the best action
        :return: the best action from the given state
        """
        # Return the action (index) with maximum Q-value
        return self._q_matrix[[state]].idxmax().iloc[0]

    def update_model(self, state, action, reward, next_state):
        """
        Update the Q-values for a given observation.

        :param state: The state the observation started in
        :param action: The action taken from that state
        :param reward: The reward retrieved from taking action from state
        :param next_state: The resulting next state of taking action from state
        """
        # Update q_value for a state-action pair Q(s,a):
        # Q(s,a) = Q(s,a) + α( r + γmaxa' Q(s',a') - Q(s,a) )
        q_sa = self._q_matrix.ix[action, state]
        max_q_sa_next = self._q_matrix.ix[self.get_best_action(next_state), next_state]
        r = reward
        alpha = self._learn_rate
        gamma = self._discount_factor

        # Do the computation
        new_q_sa = q_sa + alpha * (r + gamma * max_q_sa_next - q_sa)
        self._q_matrix.set_value(action, state, new_q_sa)



class Board:
    def __init__(self, string):
        # board = [0, 0, 0, 0,
        #          0, 0, 0, 0,
        #          0, 0, 0, 0,
        #          0, "A", 0, 0]

        # board = [0, 1, 2, 3,
        #          4, 5, 6, 7,
        #          8, 9, 10, 11,
        #          12, 13, 14, 15]

        input_list = string.split(" ")
        # print(input_list)

        self.agent = 13
        self.goal_1 = transform_matrix_point(input_list[0])
        self.goal_2 = transform_matrix_point(input_list[1])
        self.trap = transform_matrix_point(input_list[2])
        self.wall = transform_matrix_point(input_list[3])

        # “p” refers to printing the optimal policy (Π*), and “q” refers to the optimal Q-values (Q*).
        # if input_list[4] is not None:
        #     output_format = input_list[4]  # p or q
        #
        # # if output_format is “q”, there will be an additional number at the end.
        # if input_list[5] is not None:
        #     options = input_list[5]

        # print("goal1: {} | goal2: {} | forbidden: {} | wall: {}".format(goal1, goal2, forbidden, wall))

        # board[goal1] = "G"
        # board[goal2] = "G"
        # board[forbidden] = "F"
        # board[wall] = "W"

        # board = Board(13, goal1, goal2, forbidden, wall)

        # self.board_print()

    # def __init__(self, agent, goal_1, goal_2, trap, wall):
    #     self.agent = agent  # type: int
    #     self.goal_1 = goal_1  # type: int
    #     self.goal_2 = goal_2  # type: int
    #     self.trap = trap  # type: int
    #     self.wall = wall  # type: int

    def board_print(self):
        display_board = [" ", " ", " ", " ",
                         " ", " ", " ", " ",
                         " ", " ", " ", " ",
                         " ", " ", " ", " "]

        display_board[self.wall] = "W"
        display_board[self.trap] = "X"
        display_board[self.goal_1] = "O"
        display_board[self.goal_2] = "O"

        display_board[self.agent] = "A"

        print("-----------------")
        print("| {} | {} | {} | {} |".format(display_board[0], display_board[1], display_board[2], display_board[3]))
        print("| {} | {} | {} | {} |".format(display_board[4], display_board[5], display_board[6], display_board[7]))
        print("| {} | {} | {} | {} |".format(display_board[8], display_board[9], display_board[10], display_board[11]))
        print(
            "| {} | {} | {} | {} |".format(display_board[12], display_board[13], display_board[14], display_board[15]))
        print("-----------------")


class State:
    def __init__(self, board, q_value):
        self.board = board  # type: Board
        # self.action = action
        self.q_value = q_value


def q_learn(input_string):
    print(input_string)
    board = Board(input_string)
    # TODO
    #  learner = QLearning()
    # state = State(board)
    # explore_state(state)
    # board_print(board)
    initial_state = State(board, 0)


# def set_q(state, action):
#     reward = -.1
#     discount_factor = .2
#     learning_rate = .1
#     return set_q(state, action) + learning_rate * (reward + discount_factor * np.max(set_q()))


def explore_state(state):
    print(state.board)
    state = state  # type: State
    agent = ""
    for i in range(0, 15):
        if state.board[i] == "A":
            agent += i
            # print("Agent at {}".format(i))


def perform_action(state, action):
    state = state  # type: State
    new_agent_location = state.board.agent
    action_string = ""
    if action == 0:
        # print("↑")
        action_string += "↑"
        if new_agent_location > 4:
            new_agent_location = new_agent_location - 4
        else:
            print("Can't move up")
    if action == 1:
        # print("↓")
        action_string += "↓"
        if new_agent_location < 12:
            new_agent_location = new_agent_location + 4
        else:
            print("Can't move down")
    if action == 2:
        # print("←")
        action_string += "←"
        if new_agent_location != 0 | 4 | 8 | 12:
            new_agent_location = new_agent_location - 1
        else:
            print("Can't move left")
    if action == 3:
        # print("→")
        action_string += "→"
        if new_agent_location != 3 | 7 | 11 | 15:
            new_agent_location = new_agent_location + 1
        else:
            print("Can't move right")

    # Check if move is valid
    if new_agent_location == state.board.wall:
        print("Moved into wall, move invalid")
    elif 0 > new_agent_location | new_agent_location > 15:
        print("Out of bounds")
    else:
        board_print_action(state.board, new_agent_location, action_string)
        state.board.agent = new_agent_location

    state.board.agent = int(state.board.agent)

    # Check for goals and traps
    if state.board.agent == int(state.board.goal_1):
        print("Reached goal!")
        state.board.board_print()
    elif state.board.agent == int(state.board.goal_2):
        print("Reached goal!")
        state.board.board_print()
    elif state.board.agent == int(state.board.trap):
        print("Reached trap!")
        state.board.board_print()
    # else:
    # print("didnt' find anything | {} {} {}".format(state.board.agent, state.board.goal_1, state.board.goal_2))

    # board_print(state.board)
    return state


def choose_action():
    action_to_choose = 0
    greed_factor = .1

    if random(1 - greed_factor) > greed_factor:
        action_to_choose = 0
    # pick_highest_q_value
    else:
        action_to_choose = random.uniform(0, 4)
    return action_to_choose


def transform_matrix_point(number):
    number = int(number)  # type: int
    # print("taking in {}".format(number))
    if number == 1:
        return 12
    elif number == 2:
        return 13
    elif number == 3:
        return 14
    elif number == 4:
        return 15
    elif number == 5:
        return 8
    elif number == 6:
        return 9
    elif number == 7:
        return 10
    elif number == 8:
        return 11
    elif number == 9:
        return 4
    elif number == 10:
        return 5
    elif number == 11:
        return 6
    elif number == 12:
        return 7
    elif number == 13:
        return 0
    elif number == 14:
        return 1
    elif number == 15:
        return 2
    elif number == 16:
        return 3


def board_print_action(input_board, action_coord, action_string):
    display_board = [" ", " ", " ", " ",
                     " ", " ", " ", " ",
                     " ", " ", " ", " ",
                     " ", " ", " ", " "]
    display_board[input_board.wall] = "W"
    display_board[input_board.trap] = "X"
    display_board[input_board.goal_1] = "O"
    display_board[input_board.goal_2] = "O"
    display_board[action_coord] = action_string
    display_board[input_board.agent] = "A"

    print("-----------------")
    print("| {} | {} | {} | {} |".format(display_board[0], display_board[1], display_board[2], display_board[3]))
    print("| {} | {} | {} | {} |".format(display_board[4], display_board[5], display_board[6], display_board[7]))
    print("| {} | {} | {} | {} |".format(display_board[8], display_board[9], display_board[10], display_board[11]))
    print("| {} | {} | {} | {} |".format(display_board[12], display_board[13], display_board[14], display_board[15]))
    print("-----------------")


def tests():
    inputa = "15 12 8 6"
    inputb = "13 4 5 3"
    q_learn(inputa)
    q_learn(inputb)


tests()
