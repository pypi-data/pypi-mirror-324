class BizException(Exception):
    pass

class GameAlready4Players(BizException):
    def __init__(self):
        self.message = "Game already has 4 players!"
        super().__init__(self.message)

class GameDuplicatePlayers(BizException):
    def __init__(self):
        self.message = "Game has duplicate players!"
        super().__init__(self.message)

class GamePartnerAlreadyChosenException(BizException):
    def __init__(self):
        self.message = "Partner already chosen!"
        super().__init__(self.message)

class GameNotReadyToDealYetException(BizException):
    def __init__(self):
        self.message = "Game not ready to deal yet!"
        super().__init__(self.message)

class GameAlreadyDealtException(BizException):
    def __init__(self):
        self.message = "Game already dealt the cards!"
        super().__init__(self.message)

class GameInvalidBidStateException(BizException):
    def __init__(self):
        self.message = "Game invalid bid state!"
        super().__init__(self.message)    

class GameNotPlayerBidTurnException(BizException):
    def __init__(self):
        self.message = "Game not player's turn to bid!"
        super().__init__(self.message)

class GameAuctionNotFinishedException(BizException):
    def __init__(self):
        self.message = "Game auction not finished yet!"
        super().__init__(self.message)

class GameAuctionAlreadyFinishedException(BizException):
    def __init__(self):
        self.message = "Game auction already finished!"
        super().__init__(self.message)

class GameInvalidBidException(BizException):
    def __init__(self):
        self.message = "Game invalid bid!"
        super().__init__(self.message)

class GameNotBidWinner(BizException):
    def __init__(self):
        self.message = "Game not bid winner!"
        super().__init__(self.message)

class GameNotReadyForTrickWinnerExcception(BizException):
    def __init__(self):
        self.message = "Game not ready for trick winner!"
        super().__init__(self.message)

class GameInvalidTrickStateException(BizException):
    def __init__(self):
        self.message = "Game invalid trick state!"
        super().__init__(self.message)

class GameAlreadyFinishedException(BizException):
    def __init__(self):
        self.message = "Game already finished!"
        super().__init__(self.message)

class GameNotFinishedYetException(BizException):
    def __init__(self):
        self.message = "Game not finished yet!"
        super().__init__(self.message)

class GameNotPlayerTrickTurnException(BizException):
    def __init__(self):
        self.message = "Game not player's turn to trick!"
        super().__init__(self.message)

class GameInvalidPlayerTrickException(BizException):
    def __init__(self):
        self.message = "Game player tricks with invalid card!"
        super().__init__(self.message)
