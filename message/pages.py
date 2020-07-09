from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import operator

def get_sender_messages(subsession, round):
    """ Retrieves the sender's messages and returns them in a dictionary consisting of a:
    key => The player's participant ID
    value => The sender's message
    """
    messages = {}
    for player in subsession.in_round(round).get_players():
        if player.role == 'sender':
            messages[player.participant.id_in_session] = player.message
    
    return messages

def get_counted_votes(subsession, round):
    """ Retrieves all receiver's votes and counts them. The returned dictionary consists of a:
    key => The ID for the message
    value => The number of times message was voted for.
    """
    votes = {} 
    for player in subsession.in_round(round).get_players():
        if player.role() == 'receiver':
            if player.vote in votes.keys():
                votes[player.vote] += 1 
            else:
                votes[player.vote] = 1
    return votes

class EnterMessagePage(Page):
    form_model = 'player'
    form_fields = ['message']

    def is_displayed(self):
        return self.round_number == 1 and self.player.role() == 'sender'
    
class VotePage(Page):
    form_model = 'player'
    form_fields = ['vote']

    def is_displayed(self):
        return self.round_number == 2 and self.player.role() == 'receiver'
    
    def vars_for_template(self):
        messages = get_sender_messages(self.subsession, 1)
        participant_ids = sorted(list(messages.keys()))
        return {
            'messages': [messages[pid] for pid in participant_ids]
        }

class VoteResultsPage(Page):
    def is_displayed(self):
        return self.round_number == 3

    def vars_for_template(self):
        messages = get_sender_messages(self.subsession, 1)
        participant_ids = sorted(list(messages.keys()))

        votes = get_counted_votes(self.subsession, 2) 
        winning_participant_id = participant_ids[max(votes, key=votes.get)]

        return {
            'winning_message': messages[winning_participant_id]
        }
    

class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True


class Results(Page):
    pass


page_sequence = [EnterMessagePage, ResultsWaitPage, VotePage, ResultsWaitPage, VoteResultsPage]
