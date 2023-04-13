import simpy
import pandas as pd

class TrainingEvent:
    def __init__(self, env, id, duration):
        self.env = env
        self.id = id
        self.duration = duration
    # request resource function 
class Person:
    def __init__(self, env, id, yrs_exp, rating):
        self.env = env
        self.id = id
        self.yrs_exp = yrs_exp
        self.rating = rating

class TrainingResource:
    def __init__(self, env, asset_id, type, configuration, capacity):
        self.env = env
        self.asset_id = asset_id
        self.type = type
        self.configuration = configuration
        self.capacity = capacity
        self.resource = simpy.Resource(self.env, capacity=capacity)


class Administrator:
    def __init__(self, env):
        self.persons_store = simpy.FilterStore(env) # people currently available for trainings
        self.resources_store = simpy.FilterStore(env) # resources currently available for trainings 
        self.events_store = simpy.FilterStore(env) # training events to be done
        self.fleet_configuration = None # placeholder - to represent our current (and maybe future) fleet configuration
        self.env = env

    # requests necessary resources for an individual training event then simulates that event
    def sim_event(self, env):
        # create new TE object 
        get_event = self.events_store.get()
        get_resource = self.resources_store.get()
        get_person = self.persons_store.get()
        all_requests = [get_event, get_person, get_resource]

        while True:
            print(f"requesting resources at {env.now}")
            yield simpy.AllOf(env, all_requests)
            test_timeout = self.env.timeout(get_event.value.duration)
            print(f"beginning training at {env.now}")
            yield test_timeout
            print(f"completing training at {env.now}")


def define_admin_data(env, pilot_data):

    admin = Administrator(env)

    # fill persons_store with persons
    for index, row in pilot_data.iterrows():
        pilot = Person(env, row['Pilot_ID'], row['Yrs_Exp_Initial'], row['Rating_Initial'])
        admin.persons_store.put(pilot)


    # fill resources_store with a resource
    dmrt = TrainingResource(env, "DMRT_01", "Simulator", "tr3_blk3", 2)
    admin.resources_store.put(dmrt)

    # fill events_store with an event
    event_01 = TrainingEvent(env, "event_01", 8)
    admin.events_store.put(event_01)
    
    return admin
    

pilot_data = pd.read_csv('synthetic_pilot_data.csv')
env = simpy.Environment()
admin = define_admin_data (env, pilot_data)
env.process(admin.sim_event(env))
env.run(until=50)
print("simulation complete")



      



    

    

