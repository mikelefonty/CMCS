import sys
sys.path.append('../')
from Clustering.dbscan import DBSCAN
from Util.environment_IO import read_env_from_file,create_environment

#create_environment(12,12,43,'./prova_env.txt')
env = read_env_from_file('./prova_env.txt')
DBSCAN(env.get_env_matrix(),env.get_agents_dict(),3,4)
