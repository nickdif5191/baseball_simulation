import simpy
import random

class Pitch():
    def __init__(self, env, batter, pitcher, outcomes, probabilities):
        self.env = env
        self.batter = batter
        self.pitcher = pitcher
        self.outcomes = outcomes # list of potential outcomes of the pitch (ball, strike, flyout, double, etc.)
        self.probabilities = probabilities # list of probabilities associated w/ each of those outcomes

    def throw_pitch(self):
        yield self.env.timeout(20) # simulate 20 seconds in between pitches
        outcome_of_pitch = random.choices(self.outcomes, weights = self.probabilities)[0] # determine the outcome of the pitch 
        yield outcome_of_pitch
        

class AtBat():
    def __init__(self, env, batter, pitcher):
        self.env = env
        self.batter = batter
        self.pitcher = pitcher
        self.num_strikes = 0 # incremented if outcome of pitch is strike
        self.num_balls = 0 # incremented if outcome of pitch is ball
        self.num_outs = 0 # incremented if outcome of pitch is out
        self.pitches = []

    def sim_at_bat(self):
        while self.num_strikes < 3 and self.num_balls < 4 and self.num_outs < 1:
            # simulate the next pitch




class HalfInning():
    def __init__(self, env, batting_team, pitching_team):
        self.env = env
        self.batting_team = batting_team
        self.pitching_team = pitching_team
        self.num_outs = 0
        self.runs_scored = 0
        self.at_bats = []
        self.first_base = simpy.Resource(env, 1)
        self.second_base = simpy.Resource(env, 1)
        self.third_base = simpy.Resource(env, 1)

    def sim_half_inning(self):
        while self.num_outs < 4:
            # simulate the next at bat
    

class Game():
    def __init__(self, env, team_names, batting_lineups, pitchers, score):
        self.env = env
        self.team_names = team_names
        self.batting_lineups = batting_lineups 
        self.pitchers = pitchers
        self.score = score
        self.half_innings_complete = 0
    
    def sim_game(self):
        while self.half_innings_complete < 19:
            # simulate the next half inning





