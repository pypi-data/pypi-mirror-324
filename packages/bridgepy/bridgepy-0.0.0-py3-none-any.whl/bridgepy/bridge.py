from bridgepy.bid import Bid
from bridgepy.card import Card
from bridgepy.datastore import Datastore
from bridgepy.game import Game, GameId, GamePlayerSnapshot
from bridgepy.player import PlayerBid, PlayerId, PlayerTrick


class BridgeClient:

    def __init__(self, game_datastore: Datastore[GameId, Game]) -> None:
        self.game_datastore = game_datastore

    def create_game(self, player_id: PlayerId, game_id: GameId) -> None:
        game = self.game_datastore.query(game_id)
        if game is not None:
            return
        self.game_datastore.insert(Game(id = game_id, player_ids = [player_id]))

    def join_game(self, player_id: PlayerId, game_id: GameId) -> None:
        game = self.game_datastore.query(game_id)
        if game is None:
            return
        game.add_player(player_id)
        if game.ready_to_deal():
            game.deal()
        self.game_datastore.update(game)
    
    def view_game(self, player_id: PlayerId, game_id: GameId) -> GamePlayerSnapshot | None:
        game = self.game_datastore.query(game_id)
        if game is None:
            return None
        return game.player_snapshot(player_id)
    
    def bid(self, player_id: PlayerId, game_id: GameId, bid: Bid) -> None:
        game = self.game_datastore.query(game_id)
        if game is None:
            return
        game.bid(PlayerBid(player_id = player_id, bid = bid))
        self.game_datastore.update(game)
    
    def choose_partner(self, player_id: PlayerId, game_id: GameId, partner: Card) -> None:
        game = self.game_datastore.query(game_id)
        if game is None:
            return
        game.choose_partner(player_id, partner)
        self.game_datastore.update(game)
    
    def trick(self, player_id: PlayerId, game_id: GameId, trick: Card) -> None:
        game = self.game_datastore.query(game_id)
        if game is None:
            return
        game.trick(PlayerTrick(player_id = player_id, trick = trick))
        self.game_datastore.update(game)
