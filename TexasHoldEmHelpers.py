import itertools
from Analysis import Analysis


class Card:
    ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
    suits = 'S D C H'.split()

    def __init__(self, rank, suit):
        self.rank = rank
        self.rank_index = Card.ranks.index(self.rank)
        self.suit = suit

    def __repr__(self):
        return 'Card({0}, {1})'.format(self.rank, self.suit)
    

class TexasHoldEmHelpers:

    @staticmethod
    def sort_by_rank(card):
        return card.rank_index

    @staticmethod
    def sort_by_suit(card):
        return Card.suits.index(card.suit)

    @staticmethod
    def is_pair(cards):
        is_pair = False

        if len(cards) >= 2:
            combinations = list(itertools.combinations(cards, 2))

            for combination in combinations:
                if combination[0].rank == combination[1].rank:
                    is_pair = True
                    break

        return is_pair

    @staticmethod
    def is_hidden_pair(cards):
        return TexasHoldEmHelpers.is_pair(cards[:2])

    @staticmethod
    def is_two_pair(cards):
        is_two_pair = False

        if len(cards) >= 4:
            combinations = list(itertools.combinations(cards, 4))

            for combination in combinations:
                combination = sorted(combination, key=TexasHoldEmHelpers.sort_by_rank)

                if combination[0].rank == combination[1].rank and combination[2].rank == combination[3].rank:
                    is_two_pair = True
                    break

        return is_two_pair

    @staticmethod
    def is_three_of_a_kind(cards):
        is_three_of_a_kind = False

        if len(cards) >= 3:
            combinations = list(itertools.combinations(cards, 3))

            for combination in combinations:
                if combination[0].rank == combination[1].rank and combination[0].rank == combination[2].rank:
                    is_three_of_a_kind = True
                    break

        return is_three_of_a_kind

    @staticmethod
    def is_x_card_straight(cards, x):
        is_straight = False

        if len(cards) >= x:
            combinations = list(itertools.combinations(cards, x))

            for combination in combinations:
                combination = sorted(combination, key=TexasHoldEmHelpers.sort_by_rank)

                if combination[x - 1].rank == 'A' and combination[x - 2].rank == '5':
                    combination.pop()

                test_index = Card.ranks.index(combination[0].rank) + 1

                for card in combination[1:]:
                    if Card.ranks.index(card.rank) != test_index:
                        break

                    test_index += 1
                    if card == combination[-1]:
                        is_straight = True

                if is_straight:
                    break

        return is_straight

    @staticmethod
    def is_straight(cards):
        return TexasHoldEmHelpers.is_x_card_straight(cards, 5)

    @staticmethod
    def is_four_card_straight(cards):
        return TexasHoldEmHelpers.is_x_card_straight(cards, 4)

    @staticmethod
    def is_x_card_flush(cards, x):
        is_flush = False

        if len(cards) >= x:
            combinations = list(itertools.combinations(cards, x))

            for combination in combinations:
                combination = sorted(combination, key=TexasHoldEmHelpers.sort_by_suit)

                if combination[0].suit == combination[x - 1].suit:
                    is_flush = True
                    break

        return is_flush

    @staticmethod
    def is_flush(cards):
        return TexasHoldEmHelpers.is_x_card_flush(cards, 5)

    @staticmethod
    def is_four_card_flush(cards):
        return TexasHoldEmHelpers.is_x_card_flush(cards, 4)

    @staticmethod
    def is_straight_flush(cards):
        return TexasHoldEmHelpers.is_straight(cards) and TexasHoldEmHelpers.is_flush(cards)

    @staticmethod
    def is_royal_flush(cards):
        is_royal_flush = False

        if len(cards) >= 5:
            combinations = list(itertools.combinations(cards, 5))

            for combination in combinations:
                combination = sorted(combination, key=TexasHoldEmHelpers.sort_by_rank)

                if TexasHoldEmHelpers.is_straight_flush(combination) and combination[3].rank == 'K':
                    is_royal_flush = True
                    break

        return is_royal_flush

    @staticmethod
    def is_full_house(cards):
        is_full_house = False

        if len(cards) >= 5:
            combinations = list(itertools.combinations(cards, 5))

            for combination in combinations:
                combination = sorted(combination, key=TexasHoldEmHelpers.sort_by_rank)

                xxxyy = (combination[0].rank == combination[1].rank
                         and combination[0].rank == combination[2].rank
                         and combination[3].rank == combination[4].rank)
                xxyyy = (combination[0].rank == combination[1].rank
                         and combination[2].rank == combination[3].rank
                         and combination[2].rank == combination[4].rank)

                if xxxyy or xxyyy:
                    is_full_house = True
                    break

        return is_full_house

    @staticmethod
    def is_four_of_a_kind(cards):
        is_four_of_a_kind = False

        if len(cards) >= 4:
            combinations = list(itertools.combinations(cards, 4))

            for combination in combinations:
                combination = sorted(combination, key=TexasHoldEmHelpers.sort_by_rank)

                if combination[0].rank == combination[3].rank:
                    is_four_of_a_kind = True
                    break

        return is_four_of_a_kind

    @staticmethod
    def is_jacks_or_better(cards):
        is_jacks_or_better = False

        combinations = itertools.combinations(cards, 1)

        for combination in combinations:
            if TexasHoldEmHelpers.is_picture_or_ace(combination):
                is_jacks_or_better = True
                break

        return is_jacks_or_better

    @staticmethod
    def is_picture_or_ace(card):
        return card.rank_index >= 9

    @staticmethod
    def is_picture_or_ace_or_ten(card):
        return card.rank_index >= 8

    @staticmethod
    def is_suited_connector(cards):
        is_suited_connector = False

        if cards[0].suit == cards[1].suit:
            if cards[0].rank_index == cards[1].rank_index + 1 or cards[1].rank_index == cards[0].rank_index + 1:
                is_suited_connector = True

        return is_suited_connector

    hole_ranks = ("32", "42", "62", "52", "72", "43", "32s", "63", "53", "73", "82", "42s", "83", "62s", "52s", "64",
                  "54", "72s", "74", "43s", "92", "84", "63s", "53s", "65", "93", "73s", "82s", "75", "94", "83s",
                  "64s", "85", "54s", "T2", "74s", "76", "92s", "T3", "95", "84s", "65s", "86", "93s", "T4", "75s",
                  "94s", "T5", "J2", "96", "85s", "T2s", "87", "J3", "76s", "T3s", "95s", "T6", "J4", "86s", "97",
                  "T4s", "J5", "T5s", "Q2", "J2s", "96s", "J6", "T7", "87s", "98", "Q3", "J3s", "T6s", "J4s", "97s",
                  "Q4", "J7", "T8", "J5s", "Q5", "Q2s", "22", "K2", "J6s", "T7s", "98s", "Q3s", "Q6", "K3", "J8", "T9",
                  "Q7", "Q4s", "J7s", "K4", "T8s", "Q5s", "K2s", "J9", "K5", "Q8", "Q6s", "33", "J8s", "T9s", "K3s",
                  "K6", "Q7s", "K4s", "A2", "K7", "JT", "Q9", "J9s", "K5s", "A3", "Q8s", "K8", "K6s", "A4", "44", "QT",
                  "A2s", "JTs", "K7s", "Q9s", "A6", "A5", "K9", "QJ", "A3s", "K8s", "A7", "A4s", "QTs", "KT", "A8",
                  "A6s", "A5s", "K9s", "QJs", "55", "KJ", "A9", "A7s", "KQ", "KTs", "A8s", "KJs", "AT", "A9s", "66",
                  "KQs", "AJ", "AQ", "ATs", "AK", "AJs", "AQs", "77", "AKs", "88", "99", "TT", "JJ", "QQ", "KK", "AA")

    @staticmethod
    def to_shorthand_string(cards):
        cards = sorted(cards, key=TexasHoldEmHelpers.sort_by_rank, reverse=True)

        string = cards[0].rank + cards[1].rank

        if cards[0].suit == cards[1].suit:
            string += 's'

        return string

    @staticmethod
    def hole_rank(cards):
        return TexasHoldEmHelpers.hole_ranks.index(TexasHoldEmHelpers.to_shorthand_string(cards))

    Analysis.set_up_hand_ranks()

    @staticmethod
    def hand_rank(cards):
        return Analysis.analyse_hand(cards)

    @staticmethod
    def hand_rank_descriptor(hand_rank):
        return Analysis.hand_rank_descriptors[hand_rank]

if __name__ == '__main__':

    hand = [Card(Card.ranks[12], Card.suits[1]), Card(Card.ranks[11], Card.suits[1]),
            Card(Card.ranks[8], Card.suits[1]), Card(Card.ranks[10], Card.suits[1]),
            Card(Card.ranks[9], Card.suits[1])]

    print(TexasHoldEmHelpers.is_pair(hand))
    print(TexasHoldEmHelpers.is_hidden_pair(hand))
    print(TexasHoldEmHelpers.is_suited_connector(hand))
    print(TexasHoldEmHelpers.is_two_pair(hand))
    print(TexasHoldEmHelpers.is_three_of_a_kind(hand))
    print(TexasHoldEmHelpers.is_straight(hand))
    print(TexasHoldEmHelpers.is_flush(hand))
    print(TexasHoldEmHelpers.is_full_house(hand))
    print(TexasHoldEmHelpers.is_four_of_a_kind(hand))
    print(TexasHoldEmHelpers.is_straight_flush(hand))
    print(TexasHoldEmHelpers.is_royal_flush(hand))
    print(TexasHoldEmHelpers.hand_rank(hand))
    print(TexasHoldEmHelpers.hand_rank_descriptor(TexasHoldEmHelpers.hand_rank(hand)))
