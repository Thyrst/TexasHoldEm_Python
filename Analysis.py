import itertools


class Analysis:

    hand_ranks = [[[[[[0 for _ in range(13)]
                      for _ in range(13)]
                     for _ in range(13)]
                    for _ in range(13)]
                   for _ in range(13)]
                  for _ in range(2)]

    hand_rank_descriptors = [None for _ in range(8000)]

    card_ranks = [str(n) for n in range(2, 10)] + list('TJQKA')

    @staticmethod
    def set_up_combination(suited, cards, hand_rank, hand_rank_descriptor):
        for (i0, i1, i2, i3, i4) in itertools.permutations(cards):
            Analysis.hand_ranks[suited][i0][i1][i2][i3][i4] = hand_rank

        Analysis.hand_rank_descriptors[hand_rank] = hand_rank_descriptor + Analysis.card_ranks[i0]\
                                                    + Analysis.card_ranks[i1] + Analysis.card_ranks[i2]\
                                                    + Analysis.card_ranks[i3] + Analysis.card_ranks[i4]

    @staticmethod
    def set_up_hand_ranks():
        rank = 1

        # set up high cards
        for i0 in range(5, 13):  # high card can be 7 through ace
            for i1 in range(3, i0):  # second card can go from 5 to i0 - 1
                for i2 in range(2, i1):  # third card can go from 4 to i1 - 1
                    for i3 in range(1, i2):  # fourth card can go from 3 to i2 - 1
                        for i4 in range(0, i3):  # fifth card can go from 2 to i3 - 1
                            is_not_five_high_straight = i0 != 12 or i1 != 3 or i2 != 2 or i3 != 1 or i4 != 0
                            is_not_regular_straight = i0 - i4 != 4
                            is_not_straight = is_not_five_high_straight and is_not_regular_straight
                            if is_not_straight:
                                Analysis.set_up_combination(False, (i0, i1, i2, i3, i4), rank, 'high card: ')
                                rank += 1

        # set up pairs
        for i0 in range(0, 13):  # the pair can be 2s through aces
            for i1 in range(2, 13):  # first kicker can be 4 through ace
                for i2 in range(1, i1):  # second kicker can be 3 through i1 - 1
                    for i3 in range(0, i2):  # third kicker can be 2 through i2 - 1
                        if i0 != i1 and i0 != i2 and i0 != i3:  # if this isn't true, we have a three of a kind!
                            Analysis.set_up_combination(False, (i0, i0, i1, i2, i3), rank, 'a pair: ')
                            rank += 1

        # set up two pair
        for i0 in range(1, 13):  # first pair can be 3s through aces
            for i1 in range(0, i0):  # second pair can be 2s through i0s - 1
                for i2 in range(0, 13):  # kicker can be 2 through ace
                        if i0 != i2 and i1 != i2:  # if this isn't true, we have a full house!
                            Analysis.set_up_combination(False, (i0, i0, i1, i1, i2), rank, 'two pair: ')
                            rank += 1

        # set up three of a kind
        for i0 in range(0, 13):  # three of a kind can be 2s through aces
            for i1 in range(1, 13):  # first kicker can be 3 through ace
                for i2 in range(0, i1):  # second kicker can be 2 through i1 - 1
                    if i0 != i1 and i0 != i2:  # make sure neither kicker is equal to the three of a kind
                        Analysis.set_up_combination(False, (i0, i0, i0, i1, i2), rank, 'three of a kind: ')
                        rank += 1

        # set up special case straight
        Analysis.set_up_combination(False, (12, 0, 1, 2, 3), rank, 'a straight: ')
        rank += 1

        # set up all the other straights
        for i0 in range(4, 13):
            Analysis.set_up_combination(False, (i0, i0-1, i0-2, i0-3, i0-4), rank, 'a straight: ')
            rank += 1

        # set up flushes (same as high card, but suited)
        for i0 in range(5, 13):  # 7 high through ace high
            for i1 in range(3, i0):  # second card can go from 5 to i0 - 1
                for i2 in range(2, i1):  # third card can go from 4 to i1 - 1
                    for i3 in range(1, i2):  # fourth card can go from 3 to i2 - 1
                        for i4 in range(0, i3):  # fifth card can go from 2 to i3 - 1
                            is_not_five_high_straight_flush = i0 != 12 or i1 != 3 or i2 != 2 or i3 != 1 or i4 != 0
                            is_not_regular_straight_flush = i0 - i4 != 4
                            is_not_straight_flush = is_not_five_high_straight_flush and is_not_regular_straight_flush
                            if is_not_straight_flush:
                                Analysis.set_up_combination(True, (i0, i1, i2, i3, i4), rank, 'a flush: ')
                                rank += 1

        # set up full houses
        for i0 in range(0, 13):  # the triple can be 2 through ace
            for i1 in range(0, 13):  # as can the pair
                if i0 != i1:  # make sure we don't have the elusive five of a kind...
                    Analysis.set_up_combination(False, (i0, i0, i0, i1, i1), rank, 'a full house: ')
                    rank += 1

        # set up 4 of a kinds
        for i0 in range(0, 13):  # four of a kind can be 2 through ace
            for i1 in range(0, 13):  # as can the kicker
                if i0 != i1:  # again, no 5 of a kinds though
                    Analysis.set_up_combination(False, (i0, i0, i0, i0, i1), rank, 'four of a kind: ')
                    rank += 1

        # set up special case straight flush
        Analysis.set_up_combination(True, (12, 0, 1, 2, 3), rank, 'a straight flush: ')
        rank += 1

        # set up all the other straight flushes
        for i0 in range(4, 13):
            Analysis.set_up_combination(True, (i0, i0 - 1, i0 - 2, i0 - 3, i0 - 4), rank, 'a straight flush: ')
            rank += 1

    @staticmethod
    def analyse_five_cards(cards):
        (c0, c1, c2, c3, c4) = cards

        suited = False
        if c0.suit == c1.suit and c0.suit == c2.suit and c0.suit == c3.suit and c0.suit == c4.suit:
            suited = True

        return Analysis.hand_ranks[suited][c0.rank_index][c1.rank_index][c2.rank_index][c3.rank_index][c4.rank_index]

    @staticmethod
    def analyse_hand(cards):
        best_hand_rank = 0

        combinations = list(itertools.combinations(cards, 5))

        for combination in combinations:
            test_hand_rank = Analysis.analyse_five_cards(combination)

            if test_hand_rank > best_hand_rank:
                best_hand_rank = test_hand_rank

        return best_hand_rank
