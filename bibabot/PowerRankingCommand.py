
from bibabot.ICommand import ICommand

import datetime
import logging
from typing import List
from espn_api.basketball import League #Ref: https://github.com/cwendt94/espn-api/wiki/League-Class-Basketball

class PowerRankingCommand(ICommand):
    def __init__(self, league: League):
        self.league = league
        self.num_weeks_to_calc = 1
        self.start_week = self.get_weeks_since_season_start() - self.num_weeks_to_calc
        if self.start_week < 1:
            self.start_week = 1 # ESPN starts counting at 1

        self.cats = ["PTS", "BLK", "STL", "AST", "REB", "TO", "3PM", "FG%", "FT%"]
        
        self.diff_timeframe = "2025_total"

    def get_weeks_since_season_start(self) -> int:
        now = datetime.datetime.now()
        season_start = datetime.datetime(year=2024, month=10, day=21)
        full_weeks_since_start = int((now - season_start).days / 7)
        christmas = datetime.datetime(year=2024, month=12, day=24)
        allstar = datetime.datetime(year=2025, month=2, day=14)
        # TODO: The following code probably won't work as expected...
        if now > christmas: # christmas is a longer week than usual
            full_weeks_since_start -= 1
        if now > allstar: # allstar weekend is a longer week than usual
            full_weeks_since_start -= 1
        return full_weeks_since_start
    
    def is_same_boxscore(self, left, right):
        is_same = True
        for index in range(len(left)):
            is_same_home = left[index].home_team.team_name == right[index].home_team.team_name
            is_same_away = left[index].away_team.team_name == right[index].away_team.team_name
            if (not is_same_home) and (not is_same_away):
                is_same = False
        return is_same

    def get_boxscores_for_all_weeks(self, league: League):
        boxscores = {}
        curr_week = self.start_week
        curr_boxscores = league.box_scores(matchup_period=curr_week)
        while(curr_boxscores[0].winner != 'UNDECIDED'):
            boxscores[curr_week] = []
            for boxscore in curr_boxscores:
                boxscores[curr_week].append({'team': boxscore.home_team.team_name, 'stats': boxscore.home_stats})
                boxscores[curr_week].append({'team': boxscore.away_team.team_name, 'stats': boxscore.away_stats})
            curr_week += 1
            new_boxscores = league.box_scores(curr_week)
            if self.is_same_boxscore(curr_boxscores, new_boxscores):
                break
            curr_boxscores = new_boxscores
        return boxscores

    def get_sorted_rankings(self, boxscores, week_offset=0):
        calc_weeks = self.num_weeks_to_calc+week_offset
        if len(boxscores) < (calc_weeks):
            logging.info(f"Cannot query for {calc_weeks} weeks, there aren't enough matchups yet")
            calc_weeks = len(boxscores)
            if week_offset > 0:
                if calc_weeks > 1:
                    week_offset = calc_weeks-1
        
        team_ranking = {}
        if week_offset == 0:
            boxscore_splice = list(boxscores.values())[-calc_weeks:]
        else:
            boxscore_splice = list(boxscores.values())[-calc_weeks:-week_offset]
        for score_list in boxscore_splice:
            for cat in self.cats:
                ordered_results = sorted(score_list, key=lambda item: item['stats'][cat]['value'])
                if cat == 'TO':
                    ordered_results.reverse()
                logging.info(f"[{cat}]")
                for num, result in enumerate(ordered_results, start=1):
                    team = result['team']
                    logging.info(f"  {num}. {team}")
                    if not team in team_ranking:
                        team_ranking[team] = 0
                    team_ranking[team] += num
        sorted_rankings = sorted(team_ranking.items(), key=lambda item: item[1], reverse=True)
        return sorted_rankings

    def get_ranking_messages(self, current_rankings, last_rankings=[]):
        if self.num_weeks_to_calc == 1:
            woche_name = "Woche"
        else:
            woche_name = "Wochen"
        message = f"*Power Rankings*\n_{self.num_weeks_to_calc} {woche_name}_"
        for index, rank in enumerate(current_rankings, start=1):
            if last_rankings:
                pos_diff = self.get_index_of_team(rank[0], last_rankings) - index
            else:
                pos_diff = 0
            team_name = rank[0]
            pos_diff = f"{pos_diff:+}".replace('-', '\-').replace('+', '\+')
            message += f"\n*{index}\.* \({pos_diff}\) {team_name}: *{rank[1]} Power*"
        return [message]

    def get_index_of_team(self, team_name, ranking):
        for index, item in enumerate(ranking, start=1):
            if item[0] == team_name:
                return index
        return 0

    def is_valid_command(self, command: str) -> bool:
        return command.startswith('/power')

    def get_messages_from_command(self, command: str) -> List[str]:
        boxscores = self.get_boxscores_for_all_weeks(self.league)
        
        # This takes the results of the last weeks and calculates the rankings
        last_rankings = self.get_sorted_rankings(boxscores, week_offset=1)
        current_rankings = self.get_sorted_rankings(boxscores)

        # Post everything to telegram in the end
        return self.get_ranking_messages(current_rankings, last_rankings)
    