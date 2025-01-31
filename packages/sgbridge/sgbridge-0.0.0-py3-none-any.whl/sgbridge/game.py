from dataclasses import dataclass, field

from sgbridge.bid import Bid
from sgbridge.card import Card, Deck, Suit
from sgbridge.entity import Entity
from sgbridge.exception import GameAlready4Players, GameAlreadyDealtException, GameAlreadyFinishedException,\
    GameAuctionAlreadyFinishedException, GameAuctionNotFinishedException, GameDuplicatePlayers, GameInvalidBidException,\
    GameInvalidBidStateException, GameInvalidTrickStateException, GameNotBidWinner, GameNotFinishedYetException,\
    GameNotPlayerBidTurnException, GameNotPlayerTrickTurnException, GameNotReadyForTrickWinnerExcception,\
    GameNotReadyToDealYetException, GamePartnerAlreadyChosenException, GameInvalidPlayerTrickException
from sgbridge.player import PlayerBid, PlayerId, PlayerTrick


@dataclass
class GameId:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class GameTrick:
    player_tricks: list[PlayerTrick]

    def ready_for_trick_winner(self) -> bool:
        return len(self.player_tricks) == 4

    def trick_winner(self, trump_suit: Suit | None) -> PlayerId:
        if not self.ready_for_trick_winner():
            raise GameNotReadyForTrickWinnerExcception()
        first_suit: Suit = self.first_suit()
        no_trump_player_tricks = self.__player_tricks_by_suit(first_suit)
        no_trump_winner_trick = self.__player_trick_winner(no_trump_player_tricks)
        if trump_suit is None:
            return no_trump_winner_trick.player_id
        trump_player_tricks = self.__player_tricks_by_suit(trump_suit)
        if len(trump_player_tricks) == 0:
            return no_trump_winner_trick.player_id
        trump_winner_trick = self.__player_trick_winner(trump_player_tricks)
        return trump_winner_trick.player_id

    def first_suit(self) -> Suit:
        if len(self.player_tricks) == 0:
            raise GameInvalidTrickStateException()
        return self.player_tricks[0].trick.suit
    
    def __player_tricks_by_suit(self, suit: Suit) -> list[PlayerTrick]:
        return [player_trick for player_trick in self.player_tricks if player_trick.trick.suit == suit]
    
    def __player_trick_winner(self, player_tricks: list[PlayerTrick]) -> PlayerTrick:
        return max(player_tricks, key = lambda player_trick: player_trick.trick)

@dataclass
class GamePlayerSnapshot:
    game_id: GameId
    player_id: PlayerId
    player_hand: list[Card]
    bid_turn: bool | None
    bids: list[PlayerBid]
    bid_winner: PlayerId | None
    partner: Card | None
    trick_turn: bool | None
    tricks: list[GameTrick]
    score: dict[PlayerId, int] | None

@dataclass
class Game(Entity[GameId]):
    player_ids: list[PlayerId]
    player_hands: dict[PlayerId, list[Card]] = field(default_factory = dict)
    bids: list[PlayerBid] = field(default_factory = list)
    partner: Card | None = None
    tricks: list[GameTrick] = field(default_factory = list)

    def player_snapshot(self, player_id: PlayerId) -> GamePlayerSnapshot:
        dealt: bool = self.dealt()
        game_bid_ready: bool = self.game_bid_ready()
        game_finished: bool = self.game_finished()
        return GamePlayerSnapshot(
            game_id = self.id,
            player_id = player_id,
            player_hand = self.player_hands.get(player_id),
            bid_turn = self.next_bid_player_id() == player_id if dealt and not game_bid_ready else None,
            bids = self.bids,
            bid_winner = self.bid_winner() if dealt and game_bid_ready else None,
            partner = self.partner,
            trick_turn = self.next_trick_player_id() == player_id if dealt and game_bid_ready and not game_finished else None,
            tricks = self.tricks,
            score = self.score() if game_finished else None
        )

    def add_player(self, player_id: PlayerId) -> None:
        if len(self.player_ids) >= 4:
            raise GameAlready4Players()
        if len(set(self.player_ids + [player_id])) != len(self.player_ids + [player_id]):
            raise GameDuplicatePlayers()
        self.player_ids.append(player_id)

    def ready_to_deal(self) -> bool:
        return len(self.player_ids) == 4
    
    def dealt(self) -> bool:
        return len(self.player_hands) == 4
    
    def deal(self) -> None:
        if not self.ready_to_deal():
            raise GameNotReadyToDealYetException()
        if self.dealt():
            raise GameAlreadyDealtException()
        deck = Deck()
        n_cards_per_player = len(deck.cards) // len(self.player_ids)
        for i in range(len(self.player_ids)):
            player_id: PlayerId = self.player_ids[i]
            cards = deck.cards[i * n_cards_per_player : (i + 1) * n_cards_per_player]
            self.player_hands[player_id] = sorted(cards, reverse = True)

    def next_bid_player_id(self) -> PlayerId:
        return self.player_ids[(len(self.bids) + 1) % 4]

    def game_bid_ready(self) -> bool:
        for player_bid in reversed(self.bids):
            if player_bid.bid is None:
                continue
            if player_bid.bid == Bid(level = 7, suit = None):
                return True
        return len(self.bids) >= 3 and all(player_bid.bid is None for player_bid in self.bids[-3:])

    def valid_bid(self, bid: Bid | None) -> bool:
        if len(self.bids) == 0:
            if bid is None:
                return False
            return bid.level >= 1 and bid.level <= 7
        if bid is None:
            return True
        return bid.level >= 1 and bid.level <= 7 and bid > self.last_player_bid().bid

    def last_player_bid(self) -> PlayerBid:
        for player_bid in reversed(self.bids):
            if player_bid.bid is not None:
                return player_bid
        raise GameInvalidBidStateException()
    
    def bid(self, player_bid: PlayerBid) -> None:
        if self.next_bid_player_id() != player_bid.player_id:
            raise GameNotPlayerBidTurnException()
        if self.game_bid_ready():
            raise GameAuctionAlreadyFinishedException()
        if not self.valid_bid(player_bid.bid):
            raise GameInvalidBidException()
        self.bids.append(player_bid)

    def bid_winner(self) -> PlayerId:
        return self.__bid_winner().player_id

    def __bid_winner(self) -> PlayerBid:
        if not self.game_bid_ready():
            raise GameAuctionNotFinishedException()
        return self.last_player_bid()
    
    def choose_partner(self, player_id: PlayerId, partner: Card) -> None:
        if self.bid_winner() != player_id:
            raise GameNotBidWinner()
        if self.partner is not None:
            raise GamePartnerAlreadyChosenException()
        self.partner = partner

    def trump_suit(self) -> Suit:
        return self.__bid_winner().bid.suit

    def game_finished(self) -> bool:
        return len(self.tricks) == 13 and self.tricks[-1].ready_for_trick_winner()
    
    def next_trick_player_id(self) -> PlayerId:
        if self.game_finished():
            raise GameAlreadyFinishedException()
        trump_suit: Suit = self.trump_suit()
        if len(self.tricks) == 0:
            bid_winner_player_id: PlayerId = self.bid_winner()
            return self.next_player(bid_winner_player_id) if trump_suit is not None else bid_winner_player_id
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
            trick_winner_player_id: PlayerId = game_trick.trick_winner(trump_suit)
            return trick_winner_player_id
        last_player_trick: PlayerTrick = game_trick.player_tricks[-1]
        last_player_trick_player_id: PlayerId = last_player_trick.player_id
        return self.next_player(last_player_trick_player_id)

    def next_player(self, player_id: PlayerId) -> PlayerId:
        i = self.player_ids.index(player_id)
        return self.player_ids[(i + 1) % 4]

    def trick(self, player_trick: PlayerTrick) -> None:
        if self.next_trick_player_id() != player_trick.player_id:
            raise GameNotPlayerTrickTurnException()
        if not self.__valid_player_trick(player_trick):
            raise GameInvalidPlayerTrickException()
        self.player_hands[player_trick.player_id].remove(player_trick.trick)
        if len(self.tricks) == 0:
            self.tricks.append(GameTrick(player_tricks = [player_trick]))
            return
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
           self.tricks.append(GameTrick(player_tricks = [player_trick]))
           return
        game_trick.player_tricks.append(player_trick)

    def __valid_player_trick(self, player_trick: PlayerTrick) -> bool:
        if self.player_hands.get(player_trick.player_id) is None:
            return False
        trick_from_player_hand = player_trick.trick in self.player_hands[player_trick.player_id]
        if not trick_from_player_hand:
            return False
        trump_trick: bool = player_trick.trick.suit == self.trump_suit()
        if trump_trick:
            return self.__can_trump(player_trick.player_id)
        if len(self.tricks) == 0:
            return True
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
            return True
        first_suit: Suit = game_trick.first_suit()
        if player_trick.trick.suit == first_suit:
            return True
        first_suit_cards = [card for card in self.player_hands[player_trick.player_id] if card.suit == first_suit]
        return len(first_suit_cards) == 0
        
    def __can_trump(self, player_id: PlayerId) -> bool:
        trump_suit: Suit = self.trump_suit()
        trump_cards = [card.suit == trump_suit for card in self.player_hands[player_id]]
        if len(trump_cards) == 0:
            return False
        if len(self.tricks) == 0:
            return all(trump_cards)
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
            return self.__trump_broken() or all(trump_cards)
        first_suit: Suit = game_trick.first_suit()
        if first_suit == trump_suit:
            return True
        first_suit_cards = [card for card in self.player_hands[player_id] if card.suit == first_suit]
        return len(first_suit_cards) == 0

    def __trump_broken(self) -> bool:
        for game_trick in reversed(self.tricks):
            for player_trick in reversed(game_trick.player_tricks):
                if player_trick.trick.suit == self.trump_suit():
                    return True
        return False
    
    def score(self) -> dict[PlayerId, int]:
        if not self.game_finished():
            raise GameNotFinishedYetException()
        score: dict[PlayerId, int] = {}
        for game_trick in self.tricks:
            trick_winner_player_id: PlayerId = game_trick.trick_winner(self.trump_suit())
            score[trick_winner_player_id] = score.get(trick_winner_player_id, 0) + 1
        return score
