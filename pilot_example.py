import simpy 
import pandas as pd


class Pilot():
    def __init__(self, env, id, yrs_exp, curr_proficiency, target_proficiency, training_resources):
        self.env = env
        self.id = id
        self.yrs_exp = yrs_exp
        self.curr_proficiency = curr_proficiency
        self.target_proficiency = target_proficiency
        self.delta_training = TrainingEvent(env, "training_01", 3) # trainings needed to get to next proficiency level
        self.training_resources = training_resources # the training resources available to this pilot
        env.process(self.request_training_resource(env, training_resources.fms_1, self.delta_training))

    def request_training_resource(self, env, resource, training_event):
        print(f"{self.id}: requesting resource at {env.now}")
        with resource.request(priority=self.yrs_exp*-1) as req:
            yield req
            print(f"{self.id}: granted resource at {env.now}")
            '''print(dir(resource))
            print(resource.users)
            print(resource.get_queue)'''
            print(f"{self.id} beginning {training_event.name} at {env.now}")
            yield env.timeout(training_event.duration)
            print(f"{self.id} completed {training_event.name} at {env.now}")

class FMS(simpy.PriorityResource):
    def __init__(self, env, capacity, name):
        super().__init__(env, capacity=capacity)
        self.name = name

    def do_training(self, training_event):
        print(f"{training_event.name} starting at {self.env.now}")
        yield self.env.timeout(training_event.duration)
        print(f"{training_event.name} completed at {self.env.now}")

class TrainingEvent():
    def __init__(self, env, name, duration):
        self.env = env
        self.name = name
        self.duration = duration

class TrainingResources():
    def __init__(self, env):
        self.env = env
        self.fms_1 = FMS(env, 1, "FMS 01")

def use_resources(env):
    training_resources = TrainingResources(env) # define training resources available
    # basic simulation info
    # training_01 = TrainingEvent(env, "training_01", 3)
    # delta_trainings = [training_01] # trainings the pilot still needs to do

    pilots_synthetic = pd.read_csv("synthetic_pilot_data.csv")
    pilots_synthetic = pilots_synthetic.sort_values(by='Yrs_Exp_Initial', ascending=False)

    for index, row in pilots_synthetic.iterrows():
        pilot = Pilot(env, row['Pilot_ID'], row['Yrs_Exp_Initial'], row['Rating_Initial'], 'tr3_blk4', training_resources)



env = simpy.Environment() # create the environment
use_resources(env) # define the environment
env.run(until=1000) # run the environment






