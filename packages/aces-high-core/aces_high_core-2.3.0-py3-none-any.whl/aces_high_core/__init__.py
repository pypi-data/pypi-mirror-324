r'''
# aces-high-core
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *


class Card(metaclass=jsii.JSIIMeta, jsii_type="aces-high-core.Card"):
    def __init__(
        self,
        suit: "Suits",
        face: "Faces",
        _index: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param suit: -
        :param face: -
        :param _index: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c600145f344538583c58a9fd5bfa6bee510ad7396318c460b86033eb6cb6efd)
            check_type(argname="argument suit", value=suit, expected_type=type_hints["suit"])
            check_type(argname="argument face", value=face, expected_type=type_hints["face"])
            check_type(argname="argument _index", value=_index, expected_type=type_hints["_index"])
        jsii.create(self.__class__, self, [suit, face, _index])

    @jsii.member(jsii_name="isAce")
    def is_ace(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isAce", []))

    @jsii.member(jsii_name="isInDeck")
    def is_in_deck(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isInDeck", []))

    @jsii.member(jsii_name="isKing")
    def is_king(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isKing", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "index"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="face")
    def face(self) -> "Faces":
        return typing.cast("Faces", jsii.get(self, "face"))

    @face.setter
    def face(self, value: "Faces") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd8c9c85bb2e6159f2fde53221180a94bdcb314551ceccd6319e90052b4a33a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "face", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suit")
    def suit(self) -> "Suits":
        return typing.cast("Suits", jsii.get(self, "suit"))

    @suit.setter
    def suit(self, value: "Suits") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1beccdd6c3c51e6cfaa0bf7090da0e3935bed8af80f3d3e5b6d05a147b493e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suit", value) # pyright: ignore[reportArgumentType]


class CardHand(metaclass=jsii.JSIIAbstractClass, jsii_type="aces-high-core.CardHand"):
    def __init__(self, _cards: typing.Sequence[Card]) -> None:
        '''
        :param _cards: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86899751380a331f1888b637cbbb4ebe95ae713e53a87b31e6b6d3bfe9ecb129)
            check_type(argname="argument _cards", value=_cards, expected_type=type_hints["_cards"])
        jsii.create(self.__class__, self, [_cards])

    @jsii.member(jsii_name="addCards")
    def add_cards(self, cards: typing.Sequence[Card]) -> None:
        '''
        :param cards: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388fa00c1a9a5440855218196e5d18425287bdfb2a988e5b6dfe39811d3982d8)
            check_type(argname="argument cards", value=cards, expected_type=type_hints["cards"])
        return typing.cast(None, jsii.invoke(self, "addCards", [cards]))

    @jsii.member(jsii_name="calculateScore")
    @abc.abstractmethod
    def calculate_score(self) -> jsii.Number:
        ...

    @builtins.property
    @jsii.member(jsii_name="cards")
    def cards(self) -> typing.List[Card]:
        return typing.cast(typing.List[Card], jsii.get(self, "cards"))


class _CardHandProxy(CardHand):
    @jsii.member(jsii_name="calculateScore")
    def calculate_score(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.invoke(self, "calculateScore", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CardHand).__jsii_proxy_class__ = lambda : _CardHandProxy


class CardPlayer(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aces-high-core.CardPlayer",
):
    def __init__(self, _hand: CardHand) -> None:
        '''
        :param _hand: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed655a58e0b7fe623a83b5ecee5c5ec87663a6a7ec10c0f5ae6c951f2d2a090)
            check_type(argname="argument _hand", value=_hand, expected_type=type_hints["_hand"])
        jsii.create(self.__class__, self, [_hand])

    @jsii.member(jsii_name="scoreHand")
    @abc.abstractmethod
    def score_hand(self) -> None:
        ...

    @jsii.member(jsii_name="takeCards")
    def take_cards(self, cards: typing.Sequence[Card]) -> None:
        '''
        :param cards: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b83549474dde51c8ec0c760cecf133c98eae7e6c516f49443e24b467555a3a6)
            check_type(argname="argument cards", value=cards, expected_type=type_hints["cards"])
        return typing.cast(None, jsii.invoke(self, "takeCards", [cards]))

    @builtins.property
    @jsii.member(jsii_name="hand")
    def hand(self) -> CardHand:
        return typing.cast(CardHand, jsii.get(self, "hand"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "score"))


class _CardPlayerProxy(CardPlayer):
    @jsii.member(jsii_name="scoreHand")
    def score_hand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "scoreHand", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CardPlayer).__jsii_proxy_class__ = lambda : _CardPlayerProxy


class DeckOfCards(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aces-high-core.DeckOfCards",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="cardAt")
    def card_at(self, index: jsii.Number) -> Card:
        '''
        :param index: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb6ef5364392a714c3d26d5f5ac16c1915c8e4c5654333db8dbd22ac1c42c73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(Card, jsii.invoke(self, "cardAt", [index]))

    @jsii.member(jsii_name="coinFlip")
    def _coin_flip(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.invoke(self, "coinFlip", []))

    @jsii.member(jsii_name="deal")
    @abc.abstractmethod
    def deal(self) -> typing.Union[Card, typing.List[Card]]:
        ...

    @jsii.member(jsii_name="faroShuffle")
    def faro_shuffle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "faroShuffle", []))

    @jsii.member(jsii_name="fullShuffle")
    def full_shuffle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "fullShuffle", []))

    @jsii.member(jsii_name="getRandomIndex")
    def _get_random_index(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        '''
        :param min: -
        :param max: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de410997d8fa0e7d4cceed697d1ef77be5b9d768d2827bf0f36c284c006c5ec1)
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getRandomIndex", [min, max]))

    @jsii.member(jsii_name="isEmpty")
    def _is_empty(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.invoke(self, "isEmpty", []))

    @jsii.member(jsii_name="numberOfCards")
    def number_of_cards(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.invoke(self, "numberOfCards", []))

    @jsii.member(jsii_name="randomShuffle")
    def random_shuffle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "randomShuffle", []))

    @jsii.member(jsii_name="riffleShuffle")
    def riffle_shuffle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "riffleShuffle", []))

    @jsii.member(jsii_name="runningCutsShuffle")
    def running_cuts_shuffle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "runningCutsShuffle", []))

    @jsii.member(jsii_name="splitDeck")
    def _split_deck(self) -> typing.List[typing.List[Card]]:
        return typing.cast(typing.List[typing.List[Card]], jsii.invoke(self, "splitDeck", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="cards")
    def cards(self) -> typing.List[Card]:
        return typing.cast(typing.List[Card], jsii.get(self, "cards"))

    @cards.setter
    def cards(self, value: typing.List[Card]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79e96eb052f0543fd0d6ba3dec1f513acc63a3625909b50c0865decf3aa80c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cards", value) # pyright: ignore[reportArgumentType]


class _DeckOfCardsProxy(DeckOfCards):
    @jsii.member(jsii_name="deal")
    def deal(self) -> typing.Union[Card, typing.List[Card]]:
        return typing.cast(typing.Union[Card, typing.List[Card]], jsii.invoke(self, "deal", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DeckOfCards).__jsii_proxy_class__ = lambda : _DeckOfCardsProxy


@jsii.enum(jsii_type="aces-high-core.Faces")
class Faces(enum.Enum):
    ACE = "ACE"
    TWO = "TWO"
    THREE = "THREE"
    FOUR = "FOUR"
    FIVE = "FIVE"
    SIX = "SIX"
    SEVEN = "SEVEN"
    EIGHT = "EIGHT"
    NINE = "NINE"
    TEN = "TEN"
    JACK = "JACK"
    QUEEN = "QUEEN"
    KING = "KING"


class StandardDeck(
    DeckOfCards,
    metaclass=jsii.JSIIMeta,
    jsii_type="aces-high-core.StandardDeck",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="deal")
    def deal(self) -> typing.Union[Card, typing.List[Card]]:
        return typing.cast(typing.Union[Card, typing.List[Card]], jsii.invoke(self, "deal", []))


@jsii.enum(jsii_type="aces-high-core.Suits")
class Suits(enum.Enum):
    CLUBS = "CLUBS"
    HEARTS = "HEARTS"
    SPADES = "SPADES"
    DIAMONDS = "DIAMONDS"


__all__ = [
    "Card",
    "CardHand",
    "CardPlayer",
    "DeckOfCards",
    "Faces",
    "StandardDeck",
    "Suits",
]

publication.publish()

def _typecheckingstub__1c600145f344538583c58a9fd5bfa6bee510ad7396318c460b86033eb6cb6efd(
    suit: Suits,
    face: Faces,
    _index: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd8c9c85bb2e6159f2fde53221180a94bdcb314551ceccd6319e90052b4a33a(
    value: Faces,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1beccdd6c3c51e6cfaa0bf7090da0e3935bed8af80f3d3e5b6d05a147b493e2b(
    value: Suits,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86899751380a331f1888b637cbbb4ebe95ae713e53a87b31e6b6d3bfe9ecb129(
    _cards: typing.Sequence[Card],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388fa00c1a9a5440855218196e5d18425287bdfb2a988e5b6dfe39811d3982d8(
    cards: typing.Sequence[Card],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed655a58e0b7fe623a83b5ecee5c5ec87663a6a7ec10c0f5ae6c951f2d2a090(
    _hand: CardHand,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b83549474dde51c8ec0c760cecf133c98eae7e6c516f49443e24b467555a3a6(
    cards: typing.Sequence[Card],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb6ef5364392a714c3d26d5f5ac16c1915c8e4c5654333db8dbd22ac1c42c73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de410997d8fa0e7d4cceed697d1ef77be5b9d768d2827bf0f36c284c006c5ec1(
    min: jsii.Number,
    max: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79e96eb052f0543fd0d6ba3dec1f513acc63a3625909b50c0865decf3aa80c6(
    value: typing.List[Card],
) -> None:
    """Type checking stubs"""
    pass
