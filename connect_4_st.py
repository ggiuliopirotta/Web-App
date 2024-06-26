from    connect_4_minimax import *
from    time import sleep
import  streamlit as st
import  pickle


### ---------------------------------------------------------------------------------------------------- ###
### INITIALIZE SESSION STATE


if "connect4" not in st.session_state:

    st.session_state["connect4"] = {
        "bot_sigma"     : dict(),
        "end_game"      : None,
        "n_rows"        : 2,
        "n_cols"        : 2,
        "game_on"       : False,
        "game_hist"     : [],
        "game_state"    : Connect4State(2, 2),
        "user"          : "1"
    }


# define game column
connect4_col = {
    2: 0.143,
    3: 0.24,
    4: 0.35,
    5: 0.485,
    6: 0.65,
    7: 0.855,
}


### ---------------------------------------------------------------------------------------------------- ###
### STATE FUNCTIONS


def set_connect4_state(key, val):
    st.session_state.connect4[key] = st.session_state[val]
    
    # reset board if height or width are changed and instantiate new root
    if key == "n_rows" or key == "n_cols":
        st.session_state.connect4["game_state"] = Connect4State(
            n_rows = st.session_state.connect4["n_rows"],
            n_cols = st.session_state.connect4["n_cols"],
        )


### ---------------------------------------------------------------------------------------------------- ###
### GAME FUNCTIONS


def play():

    # start game
    st.session_state.connect4["game_on"] = True
    st.session_state.connect4["game_hist"].append("The game is started")

    # # compute optimal strategy and store it in session state
    # _, _, sigma = negamax(st.session_state.connect4["game_state"])
    # st.session_state.connect4["bot_sigma"] = sigma

    # get optimal strategy and store it in session state
    with open(f"assets/connect 4/solution{st.session_state.connect4["n_rows"]}x{st.session_state.connect4["n_rows"]}.pkl", "rb") as f:
        sigma = pickle.load(f)
    st.session_state.connect4["bot_sigma"] = sigma

    # if user is in position 2, then let bot make its first move
    if st.session_state.connect4["user"] == 2:
        sleep(1)
        bot_move = bot_action(
            bot_sigma   = st.session_state.connect4["bot_sigma"],
            state       = st.session_state.connect4["game_state"],
        )

        # append it to history
        st.session_state.connect4["game_state"] = st.session_state.connect4["game_state"].add_disc(*bot_move)
        st.session_state.connect4["game_hist"].append("Player 1 places disc at column {}".format(*bot_move))


def move(*col):

    # get current state
    state = st.session_state.connect4["game_state"]

    # apply move and append it to history
    state_n = state.add_disc(*col)
    st.session_state.connect4["game_state"] = state_n
    st.session_state.connect4["game_hist"].append("Player {} places disc at column {}".format(st.session_state.connect4["user"], *col))
    
    # if move leads to terminal state, then terminate game with a win or a draw accordingly
    if state_n.is_terminal():
        if state_n.check_win():
            end_game("user wins")
        else:
            end_game("draw")
    else:

        # otherwise, let bot make its move
        # this sleep command is actually not perceived because the page is only updated at the end of the function
        sleep(1)
        bot_move    = bot_action(
            bot_sigma   = st.session_state.connect4["bot_sigma"],
            state       = state_n
        )
        state_n     = state_n.add_disc(*bot_move)

        # append it to history
        st.session_state.connect4["game_state"] = state_n
        st.session_state.connect4["game_hist"].append("Player {} places disc at column {}".format(3-int(st.session_state.connect4["user"]), *bot_move))
    
        # if move leads to terminal state, then terminate game with a lose or a draw accordingly
        if state_n.is_terminal():
            if state_n.check_win():
                end_game("game over")
            else:
                end_game("draw")


def bot_action(bot_sigma, state):
    # return bot's strategy at the given state
    return (bot_sigma[str(state)]["move"], )


def end_game(status):
    
    # append status to history
    st.session_state.connect4["game_hist"].append("Game over")

    # update game variables
    # according to end game status, different messages will be displayed
    st.session_state.connect4["end_game"]  = status
    st.session_state.connect4["game_on"]   = False


def reset():
    
    # reset board and instantiate new root
    st.session_state.connect4["game_state"] = Connect4State(
            n_rows = st.session_state.connect4["n_rows"],
            n_cols = st.session_state.connect4["n_cols"],
        )
    
    # reset game variables
    st.session_state.connect4["game_hist"] = []
    st.session_state.connect4["end_game"]  = None
