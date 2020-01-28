"""
Questo file contiene l'implementazione della classe Simulator_Debug, che  
si occupa di trasmettere a video l'evoluzione della simulazione, animando uno scatter plot.
"""

from matplotlib import pyplot as plt
import sys
import matplotlib as mpl
sys.path.append('../')

class Simulator_Debug:
  
  """
  Costruttore della classe.

  params:

  - constants: Oggetto di tipo Constant_Reader. Contiene al suo interno i metodi per recuperare i valori delle costanti
  - n_rows: Numero di righe della matrice che rappresenta l'ambiente
  - n_cols : Numero di colonne della matrice che rappresenta l'ambiente
  - title : Titolo dell'animazione.
  """
  def __init__(self,constants,n_rows,n_cols,title=''):
    self.n_rows = n_rows
    self.n_cols = n_cols
    self.title = title
    
    self.FIGSIZE = constants.get_figsize()
    self.EPS = constants.get_eps()
    self.DELAY = constants.get_delay()
    self.TITLE_SIZE = constants.get_title_size()
    self.MARKER_SIZE = constants.get_marker_size()
    self.TEXT_SIZE = constants.get_text_size()
    self.particles = {}
    self.scatters = {}

    self.__init_simulation()
   

  """
  Inizializza le strutture necessarie per la visualizzazione della simulazione.
  """

  def __init_simulation(self):
    
    plt.ion()
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
 

  """
  Mostra a schermo lo stato della simulazione.
  """
  def __plot_particles(self):

    plt.suptitle(self.title,size=self.TITLE_SIZE)
    for part_id in self.particles.keys():
      if part_id in self.scatters:
        self.scatters[part_id][0].remove()
        self.scatters[part_id][1].remove()

      x = self.particles[part_id][1]
      y = -self.particles[part_id][0]
      ann = plt.annotate(str(part_id),(x-0.1,y-0.1),size=self.TEXT_SIZE)
      s = plt.scatter(x,y,s=self.MARKER_SIZE,c="red")

      self.scatters[part_id] = (s,ann)


  """
  Aggiorna il titolo della simulazione. Tale valore non viene però mostrato a schermo.
  """
  def __update_title(self,title):
    self.title = title

  """
  Aggiorna lo stato della simulazione. Aggiorna sia titolo sia la posizione degli agenti. Mostra a schermo i risultati ottenuti.

  params:

  - new_positions: Dizionario di elementi key:(x',y'). La particella di ID uguale a key si trova in (x',y').
  - new_title : Se diverso da None, corrisponde al nuovo titolo da assegnare all'animazione.
  """
  def update(self,new_positions,new_title=None):
    if new_title:
      self.__update_title(new_title)

    for key in new_positions.keys():
      self.particles[key] = new_positions[key]

    self.__plot_particles()
    plt.waitforbuttonpress(self.DELAY)
