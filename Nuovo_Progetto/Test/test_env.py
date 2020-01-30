import sys
sys.path.append('../')
from Environment.environment import Environment
from Util.environment_IO import read_env_from_file,create_environment

n_row = 5
n_col = 5

agents = {
    1:(0,0),
    4:(3,3),
    5:(4,4)
}

env = Environment(n_row,n_col)
print('Initial Matrix :\n',env.get_env_matrix())
print()
env.add_agents(agents)

print('After first insertions:\n',env.get_env_matrix())

assert env.get_agent_position(1) == (0,0)
assert env.get_agent_position(4) == (3,3)
assert env.get_agent_position(5) == (4,4)
print('First test passed!!\n')
print()
agents = {
    1:(2,2),
    4:(4,3)
}

env.add_agents(agents)
print('After second insertions:\n',env.get_env_matrix())
assert env.get_agent_position(1) == (0,0)
assert env.get_agent_position(4) == (3,3)
assert env.get_agent_position(5) == (4,4)
print('Second test passed!!\n')


env.remove_agent(4)
print('After removing 4:\n',env.get_env_matrix())
assert env.get_agent_position(1) == (0,0)
assert env.get_agent_position(5) == (4,4)

try:
    env.get_agent_position(4)
except:
    print('Third test passed!!\n')

n_agents = env.get_number_of_agents()
assert n_agents == 2
agents_list = env.get_agents_id_list()
print(f'In the env there are the following agents\n{agents_list}\n')
print("Fourth test passed")

print('Moving 1 from (0,0) to (2,1)')
env.move_agent(1,(2,1))
print(env.get_env_matrix())
assert env.get_agent_position(1) == (2,1)
print("5th test passed!")

print(100*"-")
print()
print("Test env IO....")

env = create_environment(5,7,10,"./env_prova.txt",)
env = read_env_from_file('./env_prova.txt',verbose=True)

print("Ambiente letto dal file:\n",env.get_env_matrix())