import sys
sys.path.append('../')
from Util.data_structures import Direction
from Decide_Direction.decide_direction import choose_direction

class Agent:

    def __init__(self,agent_id,x,y):
        self.id = agent_id
        self.x = x
        self.y = y
    
    def get_id(self):
        return self.id
    
    def get_current_position(self):
        return (self.x,self.y)
        
    def move(self,direction,env):    
        assert isinstance(direction,Direction)

        n_rows = env.shape[0]
        n_cols = env.shape[1] 

        dx,dy = direction.direction2pair()
        self.x = (self.x + dx) % n_rows
        self.y = (self.y + dy) % n_cols
    
    def next_direction(self,env,k,verbose=False):
        return choose_direction(env,self.x,self.y,k,verbose)
       


