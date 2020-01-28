from matplotlib import pyplot as plt
import sys
import matplotlib as mpl
sys.path.append('../')

class Simulator_Debug:
  
  def __init__(self,constants,n_rows,n_cols,title=''):
    self.n_rows = n_rows
    self.n_cols = n_cols
    self.title = title
    
    self.FIGSIZE = constants.get_figsize()
    self.EPS = constants.get_eps()
    self.DELAY = constants.get_delay()
    self.TITLE_SIZE = constants.get_title_size()

    self.particles = {}
    self.scatters = {}

    self.__init_simulation()
   

  def __init_simulation(self):
    
    plt.ion()
    #plt.subplots(figsize=self.FIGSIZE)#figsize=self.FIGSIZE)
    #plt.subplots_adjust(bottom=0.19)
    #fig.canvas.window().statusBar().setVisible(False) # Remove status bar (bottom bar)
    plt.figure(figsize=self.FIGSIZE)
    plt.xticks(range(0, self.n_cols))
    plt.yticks(range(-self.n_rows, 1))
    plt.ylim([-self.n_rows-0.5, 0.5])
    plt.xlim([-0.5, self.n_cols-1+0.5])
    plt.grid()

    #DISEGNA I BORDI!!!
    plt.plot([self.EPS for x in range(self.n_cols)],linestyle="--",color="b")
    plt.plot([-self.n_rows - self.EPS for x in range(self.n_cols)],linestyle="--",color="b")
    plt.plot([-self.EPS for x in range(self.n_rows+1)],[x for x in range(-self.n_rows,1)],linestyle="--",color="b")
    plt.plot([self.n_cols-1 + self.EPS for x in range(self.n_rows+1)],[-x for x in range(self.n_rows+1)],linestyle="--",color="b")
    #plt.tight_layout()

  def plot_particles(self):

    #plt.suptitle('Amazing Stats', size=16)
    plt.suptitle(self.title,size=16)
    for part_id in self.particles.keys():

      print(f'Particles number {part_id}')
      if part_id in self.scatters:
        self.scatters[part_id][0].remove()
        self.scatters[part_id][1].remove()

      x = self.particles[part_id][1]
      y = -self.particles[part_id][0]
      ann = plt.annotate(str(part_id),(x-0.1,y-0.1),size=13)
      s = plt.scatter(x,y,s=600,c="red")

      self.scatters[part_id] = (s,ann)


    print("--------------\n")

  def __update_title(self,title):
    self.title = title

  def update(self,new_positions,new_title=None):
    if new_title:
      self.__update_title(new_title)
      
    for key in new_positions.keys():
      #print(f'Particle number {key}')
      self.particles[key] = new_positions[key]

    self.plot_particles()
    plt.waitforbuttonpress(self.DELAY)
