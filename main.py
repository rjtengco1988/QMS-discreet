import simpy  # Import the SimPy library for discrete event simulation
import random  # Import the random module for generating random values

arrival_rate = 1/3   # Customers arrive approximately every 3 time units
service_rate = 1/3   # The average service time per customer is 3 time units

# To test for 1 hour, change env.run(until=60).
# To change service time, modify service_rate = 1/x.
# To allow more customers to be served at once, increase capacity=2 or more.

def customer(env, name, server):
    print(f"{name} arrives at {env.now: .2f}") # Print the arrival time of the customer
    with server.request() as req:  # Request access to the server (resource)
        yield req # Wait until the request is granted
        print(f"{name} starts service at {env.now: .2f}") # Print when service starts
        yield env.timeout(random.expovariate(service_rate))  # Simulate service time based on exponential distribution
        print(f"{name} leaves at {env.now: .2f}") # Print when the customer leaves


def generate_customer(env, server):
    for i in range(10): # Generate 10 customers
        env.process(customer(env, f"customer {i + 1}", server))  # Start the customer process
        yield env.timeout(random.expovariate(arrival_rate)) # Wait for the next customer to arrive


env = simpy.Environment()  # Create a SimPy simulation environment
server = simpy.Resource(env, capacity=1)  # Create a server with a capacity of 1 (single server)
env.process(generate_customer(env, server))  # Start the customer generation process
env.run(until=30)  # Run the simulation for 30 time units
