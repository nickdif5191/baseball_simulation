import simpy 


class Pilot():
    def __init__(self, env, id, yrs_exp, delta_trainings, curr_proficiency, target_proficiency, training_resources):
        self.env = env
        self.id = id
        self.yrs_exp = yrs_exp
        self.delta_trainings = delta_trainings
        self.curr_proficiency = curr_proficiency
        self.target_proficiency = target_proficiency
        self.training_resources = training_resources # the training resources available to this pilot

    def request_training_resource(self, env, resource, training_event):
        with resource.request() as req:
            print(f"{self.id} requesting {resource.name} at {env.now}")
            yield req
            print(f"{self.id} beginning {training_event.name} at {env.now}")
            yield env.timeout(training_event.duration)
            print(f"{self.id} completed {training_event.name} at {env.now}")

class FMS(simpy.Resource):
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
    training_01 = TrainingEvent(env, "training_01", 3)
    training_02 = TrainingEvent(env, "training_02", 5)
    delta_trainings = [training_01, training_02] # trainings the pilot still needs to do
    # create our pilot
    pilot_1 = Pilot(env, "Pilot 01", 8.8, delta_trainings, "tr2_blk3", "tr3_blk4", training_resources)
    pilot_2 = Pilot(env, "Pilot 02", 9.0, delta_trainings, "tr2_blk3", "tr3_blk4", training_resources)
    # have the pilot request to use the FMS 
    env.process(pilot_1.request_training_resource(env, training_resources.fms_1, delta_trainings[0]))
    env.process(pilot_2.request_training_resource(env, training_resources.fms_1, delta_trainings[0]))


env = simpy.Environment() # create the environment
use_resources(env) # define the environment
env.run(until=1000) # run the environment






