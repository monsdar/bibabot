
from bibabot.ICommand import ICommand

import datetime
from typing import List
from espn_api.basketball import League #Ref: https://github.com/cwendt94/espn-api/wiki/League-Class-Basketball

class RecentActivityCommand(ICommand):
    def __init__(self, league: League, activity_since_secs=1*60*60):
        self.league = league
        self.activity_since_secs = activity_since_secs
        
        self.action_types = {}
        self.action_types['DROPPED'] = 'dropped'
        self.action_types['FA ADDED'] = 'added FA'
        self.action_types['WAIVER ADDED'] = 'added Waiver'
        self.action_types['TRADED'] = 'traded'
        
        self.cats = ["PTS", "BLK", "STL", "AST", "REB", "TO", "3PTM", "FG%", "FT%"]
        
        self.diff_timeframe = "2025_total"

    def is_valid_command(self, command: str) -> bool:
        return command.startswith('/activity')

    def get_messages_from_command(self, command: str) -> List[str]:
        activities = self.league.recent_activity(size=10) # TODO: Is max 10 enough?
        messages = []
        for activity in activities:
            act_timepoint = datetime.datetime.fromtimestamp(activity.date/1000.0)
            act_check_period = datetime.datetime.now() - datetime.timedelta(seconds=self.activity_since_secs)
            if act_timepoint < act_check_period: # if activity is older than what we want to work with
                continue

            message = "_" + act_timepoint.strftime("%H:%M:%S") + "_ New Activity:\n"
            plus_players = []
            minus_players = []
            for action in activity.actions:
                team = action[0].team_name
                type = self.action_types[action[1]]
                player = action[2]
                message += f"\* *{team}* {type} *{player}*\n"

                if "added" in type:
                    plus_players.append(player)
                elif "dropped" in type:
                    minus_players.append(player)
            
            if plus_players and minus_players:
                message += f"\nDifference ({self.diff_timeframe}):"
                message += self.get_player_diff_message(plus_players, minus_players)
            messages.append(message)
        return messages

    def get_player_diff(self, plus_players: list[str], minus_players: list[str]):
        cat_diff = {}
        for player in plus_players:
            player_full = self.league.player_info(name=player)
            for cat in self.cats:
                if not cat in cat_diff:
                    cat_diff[cat] = 0.0
                cat_diff[cat] += player_full.stats[self.diff_timeframe]['avg'][cat]
        
        for player in minus_players:
            player_full = self.league.player_info(name=player)
            for cat in self.cats:
                if not cat in cat_diff:
                    cat_diff[cat] = 0.0
                cat_diff[cat] -= player_full.stats[self.diff_timeframe]['avg'][cat]

        return cat_diff

    def get_player_diff_message(self, plus_players: list[str], minus_players: list[str]):
        diff = self.get_player_diff(self.league, plus_players, minus_players)
        message = ""
        for cat, value in diff.items():
            message += f"\n  \* *{cat}:* {value:.2f}"
        return message
    