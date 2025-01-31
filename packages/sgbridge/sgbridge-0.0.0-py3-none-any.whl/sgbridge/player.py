from dataclasses import dataclass

from sgbridge.bid import Bid
from sgbridge.card import Card

@dataclass
class PlayerId:
    value: str

    def __hash__(self) -> int:
        return hash(self.value)
    
    def __repr__(self) -> str:
        return self.value

@dataclass
class PlayerBid:
    player_id: PlayerId
    bid: Bid | None

@dataclass
class PlayerTrick:
    player_id: PlayerId
    trick: Card
