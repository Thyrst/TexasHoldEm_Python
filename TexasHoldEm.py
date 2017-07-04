import random
from TexasHoldEmHelpers import Card
from TexasHoldEmHelpers import TexasHoldEmHelpers


def calculate_move(game_state):
    # This method is called inside of the auto_play method each time a new move is required. This is where
    # we should implement some poker logic for our bot! The start of this methods grabs a load of information
    # from the game_state returned by the server and stores them in helper values. This method should demonstrate
    # how we can interact with the TexasHoldEmHelpers class to asses the strength of our hand

    # helper values
    opponent_id = game_state['OpponentId']
    board_cards = [Card(c[0], c[1]) for c in game_state['BoardCards']]
    board_cards_count = len(board_cards)

    player_hand = [Card(c[0], c[1]) for c in game_state['PlayerHand']]

    hole1 = player_hand[0]
    hole2 = player_hand[1]

    round = game_state['Round']

    big_blind = game_state['BigBlind']
    small_blind = game_state['SmallBlind']
    deal_count = game_state['DealCount']
    deal_number = game_state['DealNumber']
    is_dealer = game_state['IsDealer']
    opponent_round_bet_total = game_state['OpponentRoundBetTotal']
    opponent_stack = game_state['OpponentStack']
    player_round_bet_total = game_state['PlayerRoundBetTotal']
    player_stack = game_state['PlayerStack']
    pot_after_previous_round = game_state['PotAfterPreviousRound']
    response_deadline = game_state['ResponseDeadline']

    min_bet = opponent_round_bet_total - player_round_bet_total
    max_bet = min_bet + opponent_stack
    if max_bet > player_stack:
        max_bet = player_stack

    # random helpers
    random10 = random.randrange(1, 11)
    random219 = random.randrange(1, 220, 20)

    # is_picture helpers
    is_picture_hole1 = TexasHoldEmHelpers.is_picture_or_ace(hole1)
    is_picture_hole2 = TexasHoldEmHelpers.is_picture_or_ace(hole2)
    is_picture_or_ten_hole1 = TexasHoldEmHelpers.is_picture_or_ace_or_ten(hole1)
    is_picture_or_ten_hole2 = TexasHoldEmHelpers.is_picture_or_ace_or_ten(hole2)

    # is_pair helpers
    is_pair_player_hand = TexasHoldEmHelpers.is_pair(player_hand)
    is_pair = TexasHoldEmHelpers.is_pair(player_hand + board_cards)

    # is_two_pair helpers
    is_two_pair_board_cards = TexasHoldEmHelpers.is_two_pair(board_cards)
    is_two_pair = TexasHoldEmHelpers.is_two_pair(player_hand + board_cards)

    # is_three_of_a_kind helpers
    is_three_of_a_kind_board_cards = TexasHoldEmHelpers.is_three_of_a_kind(board_cards)
    is_three_of_a_kind = TexasHoldEmHelpers.is_three_of_a_kind(player_hand + board_cards)

    # is_straight_helpers
    is_straight_board_cards = TexasHoldEmHelpers.is_straight(board_cards)
    is_straight = TexasHoldEmHelpers.is_straight(player_hand + board_cards)

    # is_flush helpers
    is_flush_board_cards = TexasHoldEmHelpers.is_flush(board_cards)
    is_flush = TexasHoldEmHelpers.is_flush(player_hand + board_cards)

    # is_full_house helpers
    is_full_house_board_cards = TexasHoldEmHelpers.is_full_house(board_cards)
    is_full_house = TexasHoldEmHelpers.is_full_house(player_hand + board_cards)

    # is_four_of_a_kind helpers
    is_four_of_a_kind_board_cards = TexasHoldEmHelpers.is_four_of_a_kind(board_cards)
    is_four_of_a_kind = TexasHoldEmHelpers.is_four_of_a_kind(player_hand + board_cards)

    # is_straight_flush helpers
    is_straight_flush_board_cards = TexasHoldEmHelpers.is_straight_flush(board_cards)
    is_straight_flush = TexasHoldEmHelpers.is_straight_flush(player_hand + board_cards)

    # is_four_card_flush helpers
    is_four_card_flush_board_cards = TexasHoldEmHelpers.is_four_card_flush(board_cards)
    is_four_card_flush = TexasHoldEmHelpers.is_four_card_flush(player_hand + board_cards)

    # is_four_card_straight helpers
    is_four_card_straight_board_cards = TexasHoldEmHelpers.is_four_card_straight(board_cards)
    is_four_card_straight = TexasHoldEmHelpers.is_four_card_straight(player_hand + board_cards)

    # is_suited_connector helper
    is_suited_connector = TexasHoldEmHelpers.is_suited_connector(player_hand)

    # is_hidden_pair helper
    is_hidden_pair = TexasHoldEmHelpers.is_hidden_pair(player_hand)

    # to_shorthand_string helper
    shorthand = TexasHoldEmHelpers.to_shorthand_string(player_hand)

    # hole_rank helper
    hole_rank = TexasHoldEmHelpers.hole_rank(player_hand)

    # hand rank helpers
    board_rank = TexasHoldEmHelpers.hand_rank(board_cards)
    hand_rank = TexasHoldEmHelpers.hand_rank(player_hand + board_cards)

    # here we make our move! our strategy is to make a minimum bet
    # raising by 20, 30, or 40 one in every three bets
    bet_size = min_bet
    if random.randrange(0, 3) == 1:
        bet_size += 10 * random.randrange(2, 5)
    fold = False

    return bet_size, fold
