import simpy
import random

class Pitch():
    def __init__(self, env, batter, pitcher, outcome):
        self.env = env
        self.batter = batter
        self.pitcher = pitcher
        self.outcome = outcome # list of potential outcomes of the pitch (ball, strike, flyout, double, etc.) --> currently just is "STRIKE!" but will have more outcomes in future
        #self.probabilities = probabilities # list of probabilities associated w/ each of those outcomes

    def throw_pitch(self):
        yield self.env.timeout(20) # simulate 20 seconds in between pitches
        outcome_of_pitch = self.outcome
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
            pitch = Pitch(self.env, self.batter, self.pitcher, "STRIKE!")
            yield env.process(pitch.throw_pitch)
            self.pitches.append(pitch)



class HalfInning():
    def __init__(self, env, batting_lineup, pitchers):
        self.env = env
        # necessary information for a half inning to be simulated
        self.batting_lineup = batting_lineup
        self.pitchers = pitchers
        # initialize the inning itself
        self.num_outs = 0
        self.runs_scored = 0
        self.at_bats = []
        self.first_base = simpy.Resource(env, 1)
        self.second_base = simpy.Resource(env, 1)
        self.third_base = simpy.Resource(env, 1)
        self.home_plate = simpy.Resource(env, 1)

    # def increment_hitter(self):

    def sim_half_inning(self):
        while self.num_outs < 4:
            # simulate the next at bat
            batter = self.batting_lineup[0]
            pitcher = self.pitchers[0]
            at_bat = AtBat(self.env, batter, pitcher)
            yield env.process(at_bat.sim_at_bat)

    

class Game():
    def __init__(self, env, home_team_name, away_team_name, batting_lineups, pitchers, score):
        self.env = env
        self.home_team = home_team_name
        self.away_team = away_team_name
        self.batting_lineups = batting_lineups # dictionary where key is the team name and item is a list of the batting order 
        self.pitchers = pitchers # dictionary where key is the team name and item is a list of all available pitchers (first one is the starter)
        self.score = score # dictionary w/ key as Home Team/Away Team and item as their score
        self.half_innings_complete = 0
    
    #def switch_hitting_fielding_teams(self.home_team, self.away_team):
        

    def play_ball(self):
        while self.half_innings_complete < 19:
            # simulate the next half inning
            batting_team = self.away_team # will create a method at some point to set/switch these
            pitching_team = self.home_team
            batting_lineup = self.batting_lineups[batting_team]
            pitchers = self.pitchers[pitching_team]
            yield env.process(self.sim_half_inning(self.env, batting_lineup, pitchers))

    def sim_half_inning(self, batting_lineup, pitchers):
        num_outs = 0 
        while num_outs < 4:
            # simulate the next at bat
            batter = batting_lineup[0]
            pitcher = pitchers[0]
            yield env.process(self.sim_at_bat, batter, pitcher)

    def sim_at_bat(self, batter, pitcher):
        num_strikes = 0
        num_balls = 0
        num_outs = 0
        while num_strikes < 3 and num_balls < 4 and num_outs < 1:
            most_recent_outcome = "Ball"
            # simulate the next pitch
            yield env.process(self.throw_pitch("Ball"))
            if most_recent_outcome == "Ball":
                num_balls += 1
    

    def throw_pitch(self, outcome):
        yield self.env.timeout(20) # simulate 20 seconds in between pitches
        outcome_of_pitch = outcome
        yield outcome_of_pitch

    


lineups = {"Home Team":["Kwan", "Rosario", "Ramirez", "Bell", "Naylor", "Gonzalez", "Gimenez", "Zunino", "Straw"],
            "Away Team":["A", "B", "C", "D", "E", "F", "G", "H", "I"]}

pitchers = {"Home Team":["Bieber", "De Los Santos", "Clase", "Karinchak", "Stephan"],
            "Away Team":["J", "K", "L", "M", "N"]}

score = {"Home Team":0, "Away Team":0}


def start_game(env):
    game = Game(env, "Home Team", "Away Team", lineups, pitchers, score)
    game.play_ball


env = simpy.Environment
start_game(env)
env.run(until=1000)
