class PokPokError(Exception):
    """Base exception for PokPok SDK"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)