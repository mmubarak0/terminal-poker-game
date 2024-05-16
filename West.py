#!/usr/bin/env python3
"""West Game, by Mohammed Mubarak modymu9@gmail.com
The classic card game.
"""

import random
import colorama
import time


class Card:
    """Poker card class"""

    def __init__(
        self, rank: int, suit: str, owner: "Player" = None, ato: bool = False
    ) -> None:
        self.rank = rank
        self.suit = suit
        self.ato = ato
        self.owner = owner

    def __str__(self) -> str:
        """Simple repersentation of a card!"""
        rows = ["", "", "", "", ""]
        rows[0] += " ___ "
        rows[1] += "|{} | ".format(self.rank.ljust(2))
        rows[2] += "| {} | ".format(self.suit)
        rows[3] += "|_{}| ".format(self.rank.rjust(2, "_"))
        return "\n".join(rows)

    @property
    def order(self) -> int:
        """Return the order of card numeric values."""
        trans = {"J": 11, "Q": 12, "K": 13, "A": 14}
        if self.rank in ("A", "K", "Q", "J"):
            return trans[self.rank]
        return int(self.rank)


class PokerGame:
    """General Poker Game class."""

    HEARTS = chr(9829)  # Character 9829 is '♥'.
    DIAMONDS = chr(9830)  # Character 9830 is '♦'.
    SPADES = chr(9824)  # Character 9824 is '♠'.
    CLUBS = chr(9827)  # Character 9827 is '♣'.

    def __init__(self) -> None:
        self.description = """By Mohammed Mubarak modymu9@gmail.com"""
        self.prompt = "> "
        self.deck = []

    def get_deck(self) -> list[tuple]:
        """Return a list of (rank, suit) tuples for all 52 cards."""
        deck = []
        for suit in (
            PokerGame.HEARTS,
            PokerGame.DIAMONDS,
            PokerGame.SPADES,
            PokerGame.CLUBS,
        ):
            for rank in range(2, 11):
                deck.append(Card(str(rank), suit))
            for rank in ("J", "Q", "K", "A"):
                deck.append(Card(rank, suit))
        # shuffle the newly created deck.
        random.shuffle(deck)
        return deck

    def display_cards(self, cards_join: list[Card]):
        """Display a list of cards in formatted way.

        Args:
            cards_join: List of cards
        """
        cards = cards_join[:]
        # a dict that hold the 4 suit types.
        sorted_cards = {}
        for card in cards:
            if card.suit not in sorted_cards:
                sorted_cards[card.suit] = []
            sorted_cards[card.suit].append(card)
        # sorting each suit.
        for key in sorted_cards.keys():
            sorted_cards[key].sort(key=lambda x: x.order)
        # union all suits together in order where:
        # hearts comes at first then spades, diamonds and clubs at the end.
        result = (
            (sorted_cards[PokerGame.HEARTS] if PokerGame.HEARTS in sorted_cards else [])
            + (
                sorted_cards[PokerGame.SPADES]
                if PokerGame.SPADES in sorted_cards
                else []
            )
            + (
                sorted_cards[PokerGame.DIAMONDS]
                if PokerGame.DIAMONDS in sorted_cards
                else []
            )
            + (sorted_cards[PokerGame.CLUBS] if PokerGame.CLUBS in sorted_cards else [])
        )
        # print the result by converting it to a string.
        print(self.join_cards(result))

    def join_cards(self, cards_join: list) -> str:
        """Format a list of cards

        Args:
            cards_join: a list of Card cards.
        Return: formatted string from the cards list.
        """
        cards = cards_join[:]
        rows = ["", "", "", ""]
        RED, BLUE, RESET = [
            colorama.Fore.LIGHTRED_EX,
            colorama.Fore.BLACK,
            colorama.Fore.RESET,
        ]
        WHITE, BRESET = [colorama.Back.LIGHTWHITE_EX, colorama.Back.RESET]
        red_cards = (PokerGame.HEARTS, PokerGame.DIAMONDS)
        for card in cards:
            rows[0] += "{}{}{}{} {} ".format(
                WHITE,
                (RED if card.suit in red_cards else BLUE),
                card.rank.ljust(2),
                RESET,
                BRESET,
            )
            rows[1] += "{} {}{}{} {} ".format(
                WHITE,
                (RED if card.suit in red_cards else BLUE),
                card.suit,
                RESET,
                BRESET,
            )
            rows[2] += "{} {}{}{}{} ".format(
                WHITE,
                (RED if card.suit in red_cards else BLUE),
                card.rank.rjust(2, " "),
                RESET,
                BRESET,
            )
        return "\n".join(rows)


class Player:
    """Players and AI class"""

    count = 1

    def __init__(self, cards: Card, teammate: "Player" = None) -> None:
        self.name = Player.count
        self.turn = Player.count - 1
        Player.count += 1
        self.cards = cards
        self.teammate = teammate
        for card in self.cards:
            card.owner = self

    def __str__(self) -> str:
        return f"{self.name}"

    def get_card(self, rank: int, suit: str) -> Card:
        """Get a card from the player deck if it exists."""
        for card in self.cards:
            if card.rank == rank.upper() and card.suit == suit:
                return card
        return None

    def get_suit(self, suit: str) -> list[Card]:
        """Get a list of card of the same suit if it exists."""
        return sorted(
            [card for card in self.cards if card.suit == suit],
            key=lambda x: x.order,
        )

    def has(self, suit: str) -> bool:
        """Check if player has a suit"""
        for card in self.cards:
            if card.suit == suit:
                return True
        return False

    def player_select(self) -> Card:
        """Human player selection process."""
        while True:
            try:
                rank, suit = input("> ").split(",")
                suit = West.trans[suit.upper()]
                played_card = self.get_card(rank, suit)
                if played_card:
                    break
                else:
                    print("card doesn't exists")
            except Exception:
                print("Incorrect format.")
        if played_card:
            self.cards.remove(played_card)
            return played_card
        return None

    def ai_select(self, table: list[Card]) -> Card:
        """Ai player selection process."""
        if table:
            # find the first card suit.
            suit = table[0].suit
            # initial guess that the winning card is the first card.
            winning_card = table[0]
        else:
            # FIXME: change card suit to a random card suit.
            winning_card = Card(-1, PokerGame.HEARTS, self)
            suit = winning_card.suit
        # initial guess that smallest card in hand is the first.
        smallest_card = self.cards[0]

        # find the winning card from all cards in the table.
        for card in table:
            if card.order > winning_card.order and card.suit == winning_card.suit:
                winning_card = card
            elif card.ato:
                if winning_card.ato:
                    if card.order > winning_card.order:
                        winning_card = card
                else:
                    winning_card = card

        # when the player has the first card suit play the same suit.
        if self.has(suit):
            gr_card = None
            sm_card = None

            # select a card greater than winning card.
            for card in self.get_suit(suit):
                if card.order < winning_card.order:
                    sm_card = card
                    break
            # selct a card smaller than winning card.
            for card in self.get_suit(suit):
                if card.order > winning_card.order:
                    gr_card = card
                    break

            # it's important to check if the winning card owner is not teammate.
            if (
                gr_card
                and winning_card.owner is not self.teammate
                and gr_card.suit == winning_card.suit
            ):
                self.cards.remove(gr_card)
                return gr_card
            else:
                if sm_card:
                    self.cards.remove(sm_card)
                    return sm_card
                else:
                    self.cards.remove(gr_card)
                    return gr_card

        # selection of smallest card when the player don't have the first card suit.
        for card in self.cards:
            # check if it has the ato suit.
            if card.ato and winning_card.owner is not self.teammate:
                if card.suit == winning_card.suit:
                    if card.order > winning_card.order:
                        smallest_card = card
                        break
                else:
                    smallest_card = card
                    break
            # TODO: select a random smallest card from a list.
            if card.order <= smallest_card.order:
                if card.order == smallest_card.order:
                    if len(self.get_suit(card.suit)) >= len(
                        self.get_suit(smallest_card.suit)
                    ):
                        smallest_card = card
                else:
                    smallest_card = card
        self.cards.remove(smallest_card)
        return smallest_card


class West(PokerGame):
    """West poker game class."""

    trans = {
        "H": PokerGame.HEARTS,
        "S": PokerGame.SPADES,
        "D": PokerGame.DIAMONDS,
        "C": PokerGame.CLUBS,
    }

    def __init__(self) -> None:
        super().__init__()
        (
            self.player_1,
            self.player_2,
            self.player_3,
            self.player_4,
        ) = self.prepare_cards()
        self.t1_points = 0
        self.t2_points = 0

    def winner_card(self, table: list[Card]) -> Card:
        """Return the winning card."""
        winning_card = table[0]
        for card in table:
            if card.order > winning_card.order and card.suit == winning_card.suit:
                winning_card = card
            elif card.ato:
                if winning_card.ato:
                    if card.order > winning_card.order:
                        winning_card = card
                else:
                    winning_card = card
        return winning_card

    def winner_team(self, table: list[Card]) -> Player:
        """Decide winner team on each round."""
        return self.winner_card(table).owner

    def prepare_cards(self):
        """Prepare the deck for a new game"""
        self.deck = self.get_deck()
        k = 13
        player_1 = Player(self.deck[0:k])
        player_2 = Player(self.deck[k : k * 2])
        player_3 = Player(self.deck[k * 2 : k * 3], player_1)
        player_4 = Player(self.deck[k * 3 : k * 4], player_2)
        player_1.teammate = player_3
        player_2.teammate = player_4
        return [player_1, player_2, player_3, player_4]

    def player_turn(self, player: Player, table: list[Card], ai: bool = False) -> None:
        """Player turn actions."""
        time_between = 1
        if not ai:
            print(f"Player {player.name} turn:")
            self.display_cards(player.cards)
            if len(player.cards) == 13:
                played_card = player.player_select()
                for card in self.deck:
                    if card.suit == played_card.suit:
                        card.ato = True
            else:
                played_card = player.player_select()
            table.append(played_card)
            self.display_cards([table[-1]])
            time.sleep(time_between)
        else:
            print(f"Player {player.name} turn:")
            table.append(player.ai_select(table))
            self.display_cards([table[-1]])
            time.sleep(time_between)

    def start(self) -> None:
        """The beginning of the game."""
        print(self.description)
        print()

        # last round winning player.
        t_win = self.player_1
        # game round counter.
        game_r = 1
        while True:
            # No card left in hand.
            if game_r == 14:
                if self.t1_points > self.t2_points:
                    print("First Team Won!🎉")
                elif self.t2_points > self.t2_points:
                    print("Second Team Won!🎉")
                else:
                    print("TIE !!!!")
                break
            table = []
            w = [self.player_1, table, False]
            x = [self.player_2, table, True]
            y = [self.player_1.teammate, table, True]
            z = [self.player_2.teammate, table, True]
            players = [w, x, y, z]
            turns = t_win.turn
            # define players turns order based on the winner player of last round.
            [self.player_turn(*p) for p in players[turns:] + players[:turns]]
            # select winner player
            t_win = self.winner_team(table)
            if t_win in (self.player_1, self.player_1.teammate):
                self.t1_points += 1
            else:
                self.t2_points += 1
            print(
                f"""
                Team 1 \t\t\t TEAM 2
                {self.t1_points} \t\t\t {self.t2_points}
                """
            )
            game_r += 1


# A new game instance of the west poker game.
new_game = West()
new_game.start()
