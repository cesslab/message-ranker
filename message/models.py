from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import math


author = 'Anwar A. Ruff'

doc = """"""


class Constants(BaseConstants):
    name_in_url = 'message'
    players_per_group = 2
    num_rounds = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    message = models.LongStringField()
    vote = models.IntegerField(blank=False)

    def role(self):
        if self.id_in_group == 1:
            return 'sender'
        else:
            return 'receiver'

    def vote_choices(self):
        return [i for i in range(math.floor(self.session.num_participants/2))]

    