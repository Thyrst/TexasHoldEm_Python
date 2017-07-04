import tkinter
import tkinter.messagebox
import requests
import time
import threading
from Table import Table
from TexasHoldEm import calculate_move

TITLE_TEXT = 'Texas Hold \'EM Demo Client'

BUTTON_WIDTH = 16

BOT_ID_LABEL_ROW, BOT_ID_LABEL_COLUMN = (0, 0)
BOT_ID_LABEL_TEXT = 'Bot ID:'
BOT_ID_ENTRY_ROW, BOT_ID_ENTRY_COLUMN = (BOT_ID_LABEL_ROW, BOT_ID_LABEL_COLUMN + 1)

BOT_PASSWORD_LABEL_ROW, BOT_PASSWORD_LABEL_COLUMN = (0, BOT_ID_ENTRY_COLUMN + 1)
BOT_PASSWORD_LABEL_TEXT = 'Password:'
BOT_PASSWORD_ENTRY_ROW, BOT_PASSWORD_ENTRY_COLUMN = (BOT_PASSWORD_LABEL_ROW, BOT_PASSWORD_LABEL_COLUMN + 1)

LOG_IN_OUT_BUTTON_ROW, LOG_IN_OUT_BUTTON_COLUMN = (0, BOT_PASSWORD_ENTRY_COLUMN + 1)
LOG_IN_TEXT = 'Login'
LOG_OUT_TEXT = 'Logout'

SPECIFY_OPPONENT_LABEL_ROW, SPECIFY_OPPONENT_LABEL_COLUMN = (BOT_PASSWORD_ENTRY_ROW + 1, 0)
SPECIFY_OPPONENT_LABEL_TEXT = 'Specify Opponent:'
SPECIFY_OPPONENT_ENTRY_ROW, SPECIFY_OPPONENT_ENTRY_COLUMN = (SPECIFY_OPPONENT_LABEL_ROW,
                                                             SPECIFY_OPPONENT_LABEL_COLUMN + 1)

GAME_STYLE_LABEL_ROW, GAME_STYLE_LABEL_COLUMN = (SPECIFY_OPPONENT_LABEL_ROW + 1, 0)
GAME_STYLE_LABEL_TEXT = 'Game Styles'

GAME_STYLE_LISTBOX_ROW, GAME_STYLE_LISTBOX_COLUMN = (GAME_STYLE_LABEL_ROW + 1, 0)
GAME_STYLE_LISTBOX_COLUMN_SPAN = 3

GAME_STYLE_LISTBOX_TEXT = 'ID: {0}, STAKE: {1}, TIME: {2}, PLAYING: {3}, WAITING: {4}'
GAME_STYLE_LISTBOX_TEXT_BUFFER = 4
GAME_STYLE_LISTBOX_TEXT_LEN = len(GAME_STYLE_LISTBOX_TEXT) + GAME_STYLE_LISTBOX_TEXT_BUFFER

GAME_STYLE_LISTBOX_ACTIVE_STYLE = 'none'

GAME_STYLE_LISTBOX_DEFAULT_SELECTION = 0

REFRESH_GAME_STYLES_ROW, REFRESH_GAME_STYLES_COLUMN = (GAME_STYLE_LISTBOX_ROW + 1, 0)
REFRESH_GAME_STYLES_TEXT = 'Refresh Game Styles'

FIND_GAME_BUTTON_ROW, FIND_GAME_BUTTON_COLUMN = (REFRESH_GAME_STYLES_ROW + 1, 0)
FIND_GAME_BUTTON_TEXT = 'Find Game'

AUTO_FIND_NEXT_GAME_CHECK_ROW, AUTO_FIND_NEXT_GAME_CHECK_COL = (FIND_GAME_BUTTON_ROW, FIND_GAME_BUTTON_COLUMN + 1)
AUTO_FIND_NEXT_GAME_CHECK_TEXT = 'Automatically find next game'

CANCEL_STOP_GAME_BUTTON_ROW, CANCEL_STOP_GAME_BUTTON_COLUMN = (FIND_GAME_BUTTON_ROW + 1, 0)
CANCEL_GAME_TEXT = 'Cancel'
STOP_GAME_TEXT = 'Cancel'

THINKING_TIME_LABEL_ROW, THINKING_TIME_LABEL_COLUMN = (CANCEL_STOP_GAME_BUTTON_ROW + 1, 0)
THINKING_TIME_LABEL_TEXT = 'Thinking time:'

THINKING_TIME_ENTRY_ROW, THINKING_TIME_ENTRY_COLUMN = (THINKING_TIME_LABEL_ROW, THINKING_TIME_LABEL_COLUMN + 1)
THINKING_TIME_DEFAULT = 1500

TABLE_ROW, TABLE_COLUMN = (GAME_STYLE_LISTBOX_ROW, GAME_STYLE_LISTBOX_COLUMN + GAME_STYLE_LISTBOX_COLUMN_SPAN)
TABLE_ROW_SPAN = 10
TABLE_COLUMN_SPAN = 10

BASE_URL = 'http://beta.aigaming.com/Api/'
GET_LIST_OF_GAME_STYLES_EXTENSION = 'GetListOfGameStyles'
OFFER_GAME_EXTENSION = 'OfferGame'
POLL_FOR_GAME_STATE_EXTENSION = 'PollforGameState'
MAKE_MOVE_EXTENSION = 'MakeMove'
CANCEL_GAME_OFFER_EXTENSION = 'CancelGameOffer'

API_CALL_HEADERS = {'Content-Type': 'application/json'}

POKER_GAME_TYPE_ID = 3

DISABLED = 'disable'
ENABLED = 'normal'

PLAYER_W0N = 0
PLAYER_LOST = 1
PLAYER_DRAW = 2


class TexasHoldEmDemoClient(tkinter.Tk):
    """User demo client for playing and watching games of Texas Hold 'Em."""

    def __init__(self):
        # This is the constructor. This method is called when we create an instance of the TexasHoldEmDemoClient class.
        # It is responsible for creating all of the UI widgets. There isn't any code here that actually interacts with
        # the REST API. Feel free to play around with this portion of the code if you want to make the UI a bit
        # prettier, but if you are just interested in learning the API you can ignore this method completely!
        # If you are interested in fiddling with the GUI, we use the tkinter python package. Find out more at
        # https://docs.python.org/3/library/tk.html

        # Call super class constructor as we inherit from the top level tkinter.TK class
        super().__init__()

        # Init class data fields that we use for storing info that we need for using the API
        self.bot_id = None
        self.bot_password = None
        self.logged_in = False
        self.game_style_ids = []
        self.player_key = None
        self.play_again = tkinter.BooleanVar()

        self.game_cancelled = False

        # Set title
        self.title(TITLE_TEXT)

        # Bot ID label and entry
        tkinter.Label(self, text=BOT_ID_LABEL_TEXT).grid(row=BOT_ID_LABEL_ROW,
                                                         column=BOT_ID_LABEL_COLUMN,
                                                         sticky=tkinter.W)
        self.bot_id_entry = tkinter.Entry(self)
        self.bot_id_entry.grid(row=BOT_ID_ENTRY_ROW, column=BOT_ID_ENTRY_COLUMN, sticky=tkinter.W)

        # Bot Password label and entry
        tkinter.Label(self, text=BOT_PASSWORD_LABEL_TEXT).grid(row=BOT_PASSWORD_LABEL_ROW,
                                                               column=BOT_PASSWORD_LABEL_COLUMN,
                                                               sticky=tkinter.W)
        self.bot_password_entry = tkinter.Entry(self, show='*')
        self.bot_password_entry.grid(row=BOT_PASSWORD_ENTRY_ROW, column=BOT_PASSWORD_ENTRY_COLUMN, sticky=tkinter.W)

        # Login/Logout button
        self.log_in_out_button = tkinter.Button(self,
                                                text=LOG_IN_TEXT,
                                                width=BUTTON_WIDTH,
                                                command=self.log_in_out_clicked)
        self.log_in_out_button.grid(row=LOG_IN_OUT_BUTTON_ROW, column=LOG_IN_OUT_BUTTON_COLUMN, sticky=tkinter.W)

        # Specify Opponent label + entry
        tkinter.Label(self, text=SPECIFY_OPPONENT_LABEL_TEXT).grid(row=SPECIFY_OPPONENT_LABEL_ROW,
                                                                   column=SPECIFY_OPPONENT_LABEL_COLUMN,
                                                                   sticky=tkinter.W)
        self.specify_opponent_entry = tkinter.Entry(self)
        self.specify_opponent_entry.grid(row=SPECIFY_OPPONENT_ENTRY_ROW,
                                         column=SPECIFY_OPPONENT_ENTRY_COLUMN,
                                         sticky=tkinter.W)
        self.specify_opponent_entry.config(state=DISABLED)

        # Game Styles label and listbox
        tkinter.Label(self, text=GAME_STYLE_LABEL_TEXT).grid(row=GAME_STYLE_LABEL_ROW,
                                                             column=GAME_STYLE_LABEL_COLUMN,
                                                             sticky=tkinter.W)

        self.game_styles_listbox = tkinter.Listbox(self,
                                                   width=GAME_STYLE_LISTBOX_TEXT_LEN,
                                                   activestyle=GAME_STYLE_LISTBOX_ACTIVE_STYLE)

        self.game_styles_listbox.grid(row=GAME_STYLE_LISTBOX_ROW,
                                      column=GAME_STYLE_LISTBOX_COLUMN,
                                      columnspan=GAME_STYLE_LISTBOX_COLUMN_SPAN,
                                      sticky=tkinter.W)

        # Refresh Game Styles button
        self.refresh_game_styles_button = tkinter.Button(self,
                                                         text=REFRESH_GAME_STYLES_TEXT,
                                                         width=BUTTON_WIDTH,
                                                         command=self.refresh_game_styles_clicked)
        self.refresh_game_styles_button.grid(row=REFRESH_GAME_STYLES_ROW,
                                             column=REFRESH_GAME_STYLES_COLUMN,
                                             sticky=tkinter.W)
        self.refresh_game_styles_button.config(state=DISABLED)

        # Find Game button
        self.find_game_button = tkinter.Button(self,
                                               text=FIND_GAME_BUTTON_TEXT,
                                               width=BUTTON_WIDTH,
                                               command=self.find_game_clicked)

        self.find_game_button.grid(row=FIND_GAME_BUTTON_ROW,
                                   column=FIND_GAME_BUTTON_COLUMN,
                                   sticky=tkinter.W)

        self.find_game_button.config(state=DISABLED)

        # Auto find next game checkbutton
        self.auto_play_next_game_check = tkinter.Checkbutton(self,
                                                             text=AUTO_FIND_NEXT_GAME_CHECK_TEXT,
                                                             var=self.play_again)
        self.auto_play_next_game_check.grid(row=AUTO_FIND_NEXT_GAME_CHECK_ROW,
                                            column=AUTO_FIND_NEXT_GAME_CHECK_COL,
                                            sticky=tkinter.W)
        self.auto_play_next_game_check.config(state=DISABLED)

        # Cancel/Stop game button
        self.cancel_stop_game_button = tkinter.Button(self,
                                                      text=CANCEL_GAME_TEXT,
                                                      width=BUTTON_WIDTH,
                                                      command=self.cancel_stop_game_clicked)
        self.cancel_stop_game_button.grid(row=CANCEL_STOP_GAME_BUTTON_ROW,
                                          column=CANCEL_STOP_GAME_BUTTON_COLUMN,
                                          sticky=tkinter.W)
        self.cancel_stop_game_button.config(state=DISABLED)

        # Table
        self.table = Table(self)
        self.table.grid(row=TABLE_ROW, column=TABLE_COLUMN, rowspan=TABLE_ROW_SPAN, columnspan=TABLE_COLUMN_SPAN)

        # Thinking time label + entry
        tkinter.Label(self, text=THINKING_TIME_LABEL_TEXT).grid(row=THINKING_TIME_LABEL_ROW,
                                                                column=THINKING_TIME_LABEL_COLUMN,
                                                                stick=tkinter.W)

        self.thinking_time_entry = tkinter.Entry(self)
        self.thinking_time_entry.grid(row=THINKING_TIME_ENTRY_ROW, column=THINKING_TIME_ENTRY_COLUMN, sticky=tkinter.W)
        self.thinking_time_entry.insert(0, THINKING_TIME_DEFAULT)
        self.thinking_time_entry.config(state=DISABLED)

    def log_in_out_clicked(self):
        """Click handler for the 'Login'/'Logout' button."""

        # This means we're logging out
        if self.logged_in:
            self.bot_id = None
            self.bot_password = None

            self.bot_id_entry.config(state=ENABLED)
            self.bot_password_entry.config(state=ENABLED)
            self.specify_opponent_entry.config(state=DISABLED)
            self.find_game_button.config(state=DISABLED)
            self.refresh_game_styles_button.config(state=DISABLED)
            self.auto_play_next_game_check.config(state=DISABLED)
            self.thinking_time_entry.config(state=DISABLED)

            self.log_in_out_button.config(text=LOG_IN_TEXT)

            self.reset_game_styles_listbox()

            self.logged_in = False

        # This means we're logging in
        else:
            self.bot_id = self.bot_id_entry.get()
            self.bot_password = self.bot_password_entry.get()

            res = self.get_list_of_game_styles()
            if res['Result'] == 'SUCCESS':
                game_styles = res['GameStyles']
                self.set_game_styles_listbox(game_styles)

                self.bot_id_entry.config(state=DISABLED)
                self.bot_password_entry.config(state=DISABLED)
                self.specify_opponent_entry.config(state=ENABLED)
                self.find_game_button.config(state=ENABLED)
                self.refresh_game_styles_button.config(state=ENABLED)
                self.auto_play_next_game_check.config(state=ENABLED)
                self.thinking_time_entry.config(state=ENABLED)

                self.log_in_out_button.config(text=LOG_OUT_TEXT)

                self.logged_in = True

            else:
                tkinter.messagebox.showinfo('Error', 'Invalid login or password')

    def get_list_of_game_styles(self):
        """Get list of game styles from the server."""

        # Here we interact with the GetListOfGameStyles portion of the REST API. For more details, check
        # http://help.aigaming.com/rest-api-manual#GetListOfGameStyles. We build a python dict to hold all of the
        # data that we need to send to the server. Then we build the URL we need to post to. Then we make the call.
        # Finally, we return the list of GameStyles returned by the server.

        req = {'BotId': self.bot_id,
               'BotPassword': self.bot_password,
               'GameTypeId': POKER_GAME_TYPE_ID}

        url = BASE_URL + GET_LIST_OF_GAME_STYLES_EXTENSION

        return TexasHoldEmDemoClient.make_api_call(url, req)

    def set_game_styles_listbox(self, game_styles):
        """Set the content of the game styles listbox with a list of GameStyle dictionaries.

        Keyword Arguments:
        game_styles -- The list of GameStyle dictionaries, this should be obtained through get_list_of_game_styles().
        """

        self.reset_game_styles_listbox()
        for index, game_style in enumerate(game_styles):
            self.game_styles_listbox.insert(index, GAME_STYLE_LISTBOX_TEXT.format(game_style['GameStyleId'],
                                                                                  game_style['Stake'],
                                                                                  game_style['MoveTime'],
                                                                                  game_style['Playing'],
                                                                                  game_style['Waiting']))
            self.game_style_ids.append(game_style['GameStyleId'])

        self.game_styles_listbox.select_set(GAME_STYLE_LISTBOX_DEFAULT_SELECTION)

    def reset_game_styles_listbox(self):
        """Reset the content of the game styles listbox."""

        if self.game_styles_listbox.size() != 0:
            self.game_styles_listbox.delete(0, tkinter.END)

            self.game_style_ids = []

    def refresh_game_styles_clicked(self):
        """Click handler for the 'Refresh Game Styles' button."""

        res = self.get_list_of_game_styles()
        game_styles = res['GameStyles']
        self.set_game_styles_listbox(game_styles)

    def find_game_clicked(self):
        """Click handler for the 'Find Game' button"""

        self.find_game_button.config(state=DISABLED)
        self.cancel_stop_game_button.config(state=ENABLED)

        # Here we dispatch the work to a separate thread, to keep the GUI responsive.
        threading.Thread(target=self.game_loop).start()

    def game_loop(self):
        """Loop through finding and playing games."""

        while True:
            self.find_game()

            if self.game_cancelled:
                break

            self.play_game()

            if self.game_cancelled:
                break

            if not self.play_again.get():
                break

        self.find_game_button.config(state=ENABLED)
        self.cancel_stop_game_button.config(state=DISABLED, text=CANCEL_GAME_TEXT)
        self.game_cancelled = False

    def find_game(self):
        """Find a game."""

        offer_game_res = self.offer_game()

        self.player_key = offer_game_res['PlayerKey']

        if offer_game_res['Result'] == 'WAITING_FOR_GAME':
            self.wait_for_game()

    def offer_game(self):
        """Offer a game."""

        # Here we are interacting with the OfferGame portion of the REST API, see
        # http://help.aigaming.com/rest-api-manual#OfferGame for more details. We build a python dict to hold all of the
        # data that we need to send to the server. Then we build the URL we need to post to. Then we make the call.
        # Finally, we return the result of the call.

        opponent_id = self.specify_opponent_entry.get()
        if len(opponent_id) == 0:
            opponent_id = None

        req = {'BotId': self.bot_id,
               'BotPassword': self.bot_password,
               'MaximumWaitTime': 1000,
               'GameStyleId': self.game_style_ids[int(self.game_styles_listbox.curselection()[0])],
               'DontPlayAgainstSameUser': False,
               'DontPlayAgainstSameBot': False,
               'OpponentId': opponent_id}
        url = BASE_URL + OFFER_GAME_EXTENSION

        return TexasHoldEmDemoClient.make_api_call(url, req)

    def wait_for_game(self):
        """Wait for game to start."""

        while True:
            if self.game_cancelled:
                self.cancel_game()
                break

            poll_results = self.poll_for_game_state()

            if poll_results['Result'] == 'SUCCESS':
                break

    def play_game(self):
        """Play a game."""

        self.in_game = True

        poll_results = self.poll_for_game_state()

        game_state = poll_results['GameState']
        current_deal = game_state['DealNumber']
        current_round = game_state['Round']

        # info to determine who won the pot
        player_stack = game_state['PlayerStack']
        opponent_stack = game_state['OpponentStack']
        pot = game_state['PotAfterPreviousRound']

        self.table.draw_game_state(game_state)
        self.update()

        while True:
            if self.game_cancelled:
                break

            if game_state['IsMover']:
                bet_size, fold = calculate_move(game_state)
                move_results = self.make_move(fold, bet_size)

                if move_results['Result'] != 'SUCCESS':
                    break

                game_state = move_results['GameState']

            else:
                poll_results = self.poll_for_game_state()

                if poll_results['Result'] != 'SUCCESS':
                    break
                game_state = poll_results['GameState']

            if game_state['GameStatus'] != 'RUNNING':
                break

            self.table.draw_game_state(game_state)

            prev_round = current_round
            current_round = game_state['Round']

            # This means a new round is being played
            if current_round != prev_round:
                self.table.reset_for_new_round()

            prev_deal = current_deal
            current_deal = game_state['DealNumber']

            # This means a new hand is being played
            if current_deal != prev_deal:
                # Figure out who won
                current_player_bet = game_state['PlayerRoundBetTotal']
                current_opponent_bet = game_state['OpponentRoundBetTotal']

                current_player_stack = game_state['PlayerStack']
                current_opponent_stack = game_state['OpponentStack']

                # player won
                if current_player_stack + current_player_bet > player_stack:
                    self.table.reset_for_new_deal(PLAYER_W0N)
                # opponent won
                elif current_opponent_stack + current_opponent_bet > opponent_stack:
                    self.table.reset_for_new_deal(PLAYER_LOST)
                # draw
                else:
                    self.table.reset_for_new_deal(PLAYER_DRAW)

                player_stack = current_player_stack
                opponent_stack = current_opponent_stack

            self.update()

            time.sleep(int(self.thinking_time_entry.get())/1000)

        self.table.reset_for_new_game()

        self.in_game = False

    def make_move(self, fold, bet_size):
        """Make a move."""

        # Here we are interacting with the Make Move portion of the REST API, see
        # http://help.aigaming.com/rest-api-manual#MakeMove for more details. We build a python dict to hold all
        # of the data that we need to send to the server. Then we build the URL we need to post to.
        # Then we make the call. Finally, we return the result of the call.

        req = {'BotId': self.bot_id,
               'BotPassword': self.bot_password,
               'PlayerKey': self.player_key,
               'Move': {'Fold': fold,
                        'BetSize': bet_size}}
        url = BASE_URL + MAKE_MOVE_EXTENSION

        return TexasHoldEmDemoClient.make_api_call(url, req)

    def poll_for_game_state(self):
        """Poll the server for the latest GameState."""

        # Here we are interacting with the Poll For Game State portion of the REST API, see
        # http://help.aigaming.com/rest-api-manual#PollForGameState for more details. We build a python dict to hold all
        # of the data that we need to send to the server. Then we build the URL we need to post to.
        # Then we make the call. Finally, we return the result of the call.

        req = {'BotId': self.bot_id,
               'BotPassword': self.bot_password,
               'MaximumWaitTime': 1000,
               'PlayerKey': self.player_key}
        url = BASE_URL + POLL_FOR_GAME_STATE_EXTENSION

        return TexasHoldEmDemoClient.make_api_call(url, req)

    def cancel_stop_game_clicked(self):
        self.game_cancelled = True

    def cancel_game(self):
        req = {'BotId': self.bot_id,
               'BotPassword': self.bot_password,
               'PlayerKey': self.player_key}

        url = BASE_URL + CANCEL_GAME_OFFER_EXTENSION

        TexasHoldEmDemoClient.make_api_call(url, req)

    @staticmethod
    def make_api_call(url, req):
        """Make an API call."""

        res = requests.post(url, json=req, headers=API_CALL_HEADERS)
        return res.json()

if __name__ == '__main__':
    client = TexasHoldEmDemoClient()
    client.mainloop()


