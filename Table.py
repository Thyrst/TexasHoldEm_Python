import os
import tkinter
from PIL import Image, ImageTk

CARD_PATH = '64 x 90'

TABLE_WIDTH = 448
TABLE_HEIGHT = 352
TABLE_COLOUR = '#008000'
TABLE_BORDER = 0

CARD_WIDTH = 64
CARD_HEIGHT = 90

CARD_HORIZONTAL_PAD = CARD_WIDTH
CARD_VERTICAL_PAD = CARD_HEIGHT
CARD_INTER_PAD = (TABLE_WIDTH - CARD_HORIZONTAL_PAD - 5 * CARD_WIDTH) / 4

HOLE1_INDEX = 0
HOLE2_INDEX = 1
OP1_INDEX = 2
OP2_INDEX = 3
FLOP1_INDEX = 4
FLOP2_INDEX = 5
FLOP3_INDEX = 6
TURN_INDEX = 7
RIVER_INDEX = 8

TOTAL_CARDS = 9

BOARD_FLOP1_INDEX = 0
BOARD_FLOP2_INDEX = 1
BOARD_FLOP3_INDEX = 2
BOARD_TURN_INDEX = 3
BOARD_RIVER_INDEX = 4

PRE_FLOP = 0
FLOP = 1
TURN = 2
RIVER = 3
SHOWDOWN = 4

HOLE1_X, HOLE1_Y = (CARD_HORIZONTAL_PAD, TABLE_HEIGHT - CARD_VERTICAL_PAD)
HOLE2_X, HOLE2_Y = (HOLE1_X + CARD_WIDTH + CARD_INTER_PAD, HOLE1_Y)

OP2_X, OP2_Y = (TABLE_WIDTH - CARD_HORIZONTAL_PAD, HOLE1_Y)
OP1_X, OP1_Y = (OP2_X - CARD_WIDTH - CARD_INTER_PAD, HOLE1_Y)

FLOP1_X, FLOP1_Y = (HOLE1_X, CARD_VERTICAL_PAD)
FLOP2_X, FLOP2_Y = (HOLE2_X, FLOP1_Y)
FLOP3_X, FLOP3_Y = (HOLE2_X + CARD_WIDTH + CARD_INTER_PAD, FLOP1_Y)

TURN_X, TURN_Y = (OP1_X, FLOP1_Y)

RIVER_X, RIVER_Y = (OP2_X, FLOP1_Y)

PLAYER_INDEX = 0
OP_INDEX = 1

STACK_STRING = 'Stack: {0}'

STACK_VERTICAL_PAD = 32

PLAYER_STACK_X, PLAYER_STACK_Y = ((HOLE1_X + HOLE2_X) / 2, TABLE_HEIGHT - STACK_VERTICAL_PAD)
OP_STACK_X, OP_STACK_Y = ((OP1_X + OP2_X) / 2, TABLE_HEIGHT - STACK_VERTICAL_PAD)

BET_STRING = 'Bet: {0}'

BET_VERTICAL_PAD = 3 / 4 * CARD_HEIGHT

PLAYER_BET_X, PLAYER_BET_Y = ((HOLE1_X + HOLE2_X) / 2, HOLE1_Y - BET_VERTICAL_PAD)
OP_BET_X, OP_BET_Y = ((OP1_X + OP2_X) / 2, PLAYER_BET_Y)

WON_STRING = 'Won'
LOST_STRING = 'Lost'
DRAW_STRING = 'Draw'

PLAYER_W0N = 0
PLAYER_LOST = 1
PLAYER_DRAW = 2

DEALER_CHIP_WIDTH = 24
DEALER_CHIP_HEIGHT = 24
DEALER_CHIP_COLOUR = '#ffffff'

DEALER_CHIP_HORIZONTAL_PAD = 64

DEALER_CHIP_VERTICAL_PAD = 16

DEALER_CHIP_PLAYER_X1, DEALER_CHIP_PLAYER_Y1 = (PLAYER_BET_X - DEALER_CHIP_HORIZONTAL_PAD,
                                                PLAYER_BET_Y - DEALER_CHIP_VERTICAL_PAD)
DEALER_CHIP_PLAYER_X2, DEALER_CHIP_PLAYER_Y2 = (DEALER_CHIP_PLAYER_X1 + DEALER_CHIP_WIDTH,
                                                DEALER_CHIP_PLAYER_Y1 + DEALER_CHIP_HEIGHT)

DEALER_CHIP_OP_X1, DEALER_CHIP_OP_Y1 = (OP_BET_X - DEALER_CHIP_HORIZONTAL_PAD,
                                        DEALER_CHIP_PLAYER_Y1)
DEALER_CHIP_OP_X2, DEALER_CHIP_OP_Y2 = (DEALER_CHIP_OP_X1 + DEALER_CHIP_WIDTH,
                                        DEALER_CHIP_OP_Y1 + DEALER_CHIP_HEIGHT)

POT_STRING = 'Pot: {0}'

POT_X, POT_Y = ((PLAYER_BET_X + OP_BET_X) / 2, FLOP1_Y + CARD_HEIGHT)

DEAL_NUMBER_X, DEAL_NUMBER_Y = (TABLE_WIDTH / 2, PLAYER_STACK_Y)

DEAL_NUMBER_STRING = '{0} / {1}'

TEXT_COLOUR = '#ffffff'
TEXT_FONT = 'Helvetica 12 bold'

HIDDEN = 'hidden'
NORMAL = 'normal'


class Table(tkinter.Canvas):

    def __init__(self, root):

        super().__init__(root, width=TABLE_WIDTH, height=TABLE_HEIGHT, bg=TABLE_COLOUR, bd=TABLE_BORDER)

        self.card_images = [None] * TOTAL_CARDS
        self.card_photos = [None] * TOTAL_CARDS
        self.card_ids = [None] * TOTAL_CARDS

        self.dealer_chip_id = self.create_oval(DEALER_CHIP_PLAYER_X1, DEALER_CHIP_PLAYER_Y1,
                                               DEALER_CHIP_PLAYER_X2, DEALER_CHIP_PLAYER_Y2,
                                               fill=DEALER_CHIP_COLOUR)

        self.stack_ids = [None, None]
        self.stack_ids[PLAYER_INDEX] = self.create_text(PLAYER_STACK_X, PLAYER_STACK_Y, text=STACK_STRING)
        self.stack_ids[OP_INDEX] = self.create_text(OP_STACK_X, OP_STACK_Y, text=STACK_STRING)

        self.bet_ids = [None, None]
        self.bet_ids[PLAYER_INDEX] = self.create_text(PLAYER_BET_X, PLAYER_BET_Y, text=BET_STRING)
        self.bet_ids[OP_INDEX] = self.create_text(OP_BET_X, OP_BET_Y, text=BET_STRING)

        self.pot_id = self.create_text(POT_X, POT_Y, text=POT_STRING)

        self.deal_number_id = self.create_text(DEAL_NUMBER_X, DEAL_NUMBER_Y, text=DEAL_NUMBER_STRING)

        self.player_outcome_id = self.create_text(PLAYER_BET_X, PLAYER_BET_Y, text=DRAW_STRING)
        self.op_outcome_id = self.create_text(OP_BET_X, OP_BET_Y, text=DRAW_STRING)

        self.reset_for_new_game()

    def add_card(self, card, x, y, index):
        card_path = os.path.join(CARD_PATH, card.lower() + '.png')

        card_image = Image.open(card_path)
        card_photo = ImageTk.PhotoImage(card_image)

        self.card_ids[index] = self.create_image(x, y, image=card_photo)

        self.card_images[index] = card_image
        self.card_photos[index] = card_photo

    def add_player_hand(self, player_hand):
        hole1, hole2 = player_hand
        self.add_card(hole1, HOLE1_X, HOLE1_Y, HOLE1_INDEX)
        self.add_card(hole2, HOLE2_X, HOLE2_Y, HOLE2_INDEX)

    def add_opponent_hand(self, opponent_hand):
        op1, op2 = opponent_hand
        self.add_card(op1, OP1_X, OP1_Y, OP1_INDEX)
        self.add_card(op2, OP2_X, OP2_Y, OP2_INDEX)

    def add_flop(self, flop):
        flop1, flop2, flop3 = flop
        self.add_card(flop1, FLOP1_X, FLOP1_Y, FLOP1_INDEX)
        self.add_card(flop2, FLOP2_X, FLOP2_Y, FLOP2_INDEX)
        self.add_card(flop3, FLOP3_X, FLOP3_Y, FLOP3_INDEX)

    def add_turn(self, turn):
        self.add_card(turn, TURN_X, TURN_Y, TURN_INDEX)

    def add_river(self, river):
        self.add_card(river, RIVER_X, RIVER_Y, RIVER_INDEX)

    def remove_card(self, index):
        if self.card_ids[index] is not None:
            self.delete(self.card_ids[index])

            self.card_images[index] = None
            self.card_photos[index] = None
            self.card_ids[index] = None

    def remove_player_hand(self):
        self.remove_card(HOLE1_INDEX)
        self.remove_card(HOLE2_INDEX)

    def remove_opponent_hand(self):
        self.remove_card(OP1_INDEX)
        self.remove_card(OP2_INDEX)

    def remove_flop(self):
        self.remove_card(FLOP1_INDEX)
        self.remove_card(FLOP2_INDEX)
        self.remove_card(FLOP3_INDEX)

    def remove_turn(self):
        self.remove_card(TURN_INDEX)

    def remove_river(self):
        self.remove_card(RIVER_INDEX)

    def remove_all_cards(self):
        self.remove_player_hand()
        self.remove_opponent_hand()
        self.remove_flop()
        self.remove_turn()
        self.remove_river()

    def set_dealer(self, player_is_dealer):
        if player_is_dealer:
            x1, y1, x2, y2 = (DEALER_CHIP_PLAYER_X1, DEALER_CHIP_PLAYER_Y1,
                              DEALER_CHIP_PLAYER_X2, DEALER_CHIP_PLAYER_Y2)
        else:
            x1, y1, x2, y2 = (DEALER_CHIP_OP_X1, DEALER_CHIP_OP_Y1,
                              DEALER_CHIP_OP_X2, DEALER_CHIP_OP_Y2)
        self.delete(self.dealer_chip_id)
        self.dealer_chip_id = self.create_oval(x1, y1, x2, y2, fill=DEALER_CHIP_COLOUR)

    def set_text(self, widget_id, text):
        self.itemconfigure(widget_id, text=text, fill=TEXT_COLOUR, font=TEXT_FONT, state=NORMAL)

    def set_player_stack(self, stack):
        self.set_text(self.stack_ids[PLAYER_INDEX], text=STACK_STRING.format(stack))

    def set_opponent_stack(self, stack):
        self.set_text(self.stack_ids[OP_INDEX], text=STACK_STRING.format(stack))

    def set_player_bet(self, bet):
        self.set_text(self.bet_ids[PLAYER_INDEX], text=BET_STRING.format(bet))

    def set_opponent_bet(self, bet):
        self.set_text(self.bet_ids[OP_INDEX], text=BET_STRING.format(bet))

    def set_pot(self, pot):
        self.set_text(self.pot_id, text=POT_STRING.format(pot))

    def set_deal_number(self, current, total):
        self.set_text(self.deal_number_id, DEAL_NUMBER_STRING.format(current, total))

    def hide_widget(self, widget_id):
        self.itemconfigure(widget_id, state='hidden')

    def hide_all_text(self):
        self.hide_widget(self.stack_ids[PLAYER_INDEX])
        self.hide_widget(self.stack_ids[OP_INDEX])
        self.hide_widget(self.bet_ids[PLAYER_INDEX])
        self.hide_widget(self.bet_ids[OP_INDEX])
        self.hide_widget(self.pot_id)
        self.hide_widget(self.deal_number_id)
        self.hide_widget(self.player_outcome_id)
        self.hide_widget(self.op_outcome_id)

    def hide_dealer_chip(self):
        self.hide_widget(self.dealer_chip_id)

    def show_widget(self, widget_id):
        self.itemconfigure(widget_id, state='normal')

    def show_all_text(self):
        self.show_widget(self.stack_ids[PLAYER_INDEX])
        self.show_widget(self.stack_ids[OP_INDEX])
        self.show_widget(self.bet_ids[PLAYER_INDEX])
        self.show_widget(self.bet_ids[OP_INDEX])
        self.show_widget(self.pot_id)
        self.show_widget(self.deal_number_id)

    def show_dealer_chip(self):
        self.show_widget(self.dealer_chip_id)

    def draw_game_state(self, game_state):

        game_round = game_state['Round']
        board_cards = game_state['BoardCards']

        if self.card_ids[HOLE1_INDEX] is None:
            self.add_player_hand(game_state['PlayerHand'])
            self.add_opponent_hand(game_state['OpponentHand'])

            self.hide_widget(self.player_outcome_id)
            self.hide_widget(self.op_outcome_id)

        elif game_round == FLOP and self.card_ids[FLOP1_INDEX] is None:
            self.add_flop((board_cards[BOARD_FLOP1_INDEX],
                           board_cards[BOARD_FLOP2_INDEX],
                           board_cards[BOARD_FLOP3_INDEX]))

        elif game_round == TURN and self.card_ids[TURN_INDEX] is None:
            self.add_turn(board_cards[BOARD_TURN_INDEX])

        elif game_round == RIVER and self.card_ids[RIVER_INDEX] is None:
            self.add_river(board_cards[BOARD_RIVER_INDEX])

        elif game_round == SHOWDOWN:
            self.remove_opponent_hand()
            self.add_opponent_hand(game_state['OpponentHand'])

        self.set_player_bet(game_state['PlayerRoundBetTotal'])
        self.set_player_stack(game_state['PlayerStack'])

        self.set_opponent_bet(game_state['OpponentRoundBetTotal'])
        self.set_opponent_stack(game_state['OpponentStack'])

        self.set_pot(game_state['PotAfterPreviousRound'])
        self.set_dealer(game_state['IsDealer'])
        self.set_deal_number(game_state['DealNumber'], game_state['DealCount'])

    def reset_for_new_round(self):
        self.set_player_bet(0)
        self.set_opponent_bet(0)

    def reset_for_new_deal(self, outcome):
        self.remove_all_cards()
        self.hide_dealer_chip()

        if outcome == PLAYER_W0N:
            self.set_text(self.player_outcome_id, WON_STRING)
            self.set_text(self.op_outcome_id, LOST_STRING)
        elif outcome == PLAYER_LOST:
            self.set_text(self.player_outcome_id, LOST_STRING)
            self.set_text(self.op_outcome_id, WON_STRING)
        else:
            self.set_text(self.player_outcome_id, DRAW_STRING)
            self.set_text(self.op_outcome_id, DRAW_STRING)

        self.hide_widget(self.bet_ids[PLAYER_INDEX])
        self.hide_widget(self.bet_ids[OP_INDEX])

    def reset_for_new_game(self):
        self.remove_all_cards()
        self.hide_all_text()
        self.hide_dealer_chip()
