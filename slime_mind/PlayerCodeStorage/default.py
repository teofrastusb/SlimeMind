from slime_mind.models.player_base import PlayerBase

class Player(PlayerBase):
    def __init__(self, player_id):
        super().__init__(id, "Default AI", 'default', 'default')
        self.id = player_id

    # use default command_slime