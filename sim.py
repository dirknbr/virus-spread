
import matplotlib.pyplot as plt
import numpy as np

def inv_logit(x):
  return np.exp(x) / (1 + np.exp(x))

def change(x):
  chg = [np.nan]
  for i in range(1, len(x)):
    chg.append(x[i] - x[i - 1])
  return chg

class Human:
  def __init__(self, _id=0, tot=1000):
    self.id = _id
    self.age = np.random.randint(1, 99)
    self.gender = 'female' if np.random.random() < .5 else 'male'
    self.infected = False
    self.days_infected = True
    self.immune = False
    self.alive = True
    self.isolated = False
    self.n_friends = np.random.randint(1, 5)
    self.friends = np.random.choice(tot, size=self.n_friends, replace=False)

  def get_infected(self, prob=.4):
    # check if will be infected by friends
    if not self.infected and not self.isolated and not self.immune:
      infected_friends = sum([1 for i in self.friends if humans[i].infected])
      notinfected = 1 - prob ** infected_friends
      if notinfected > np.random.random():
        self.infected = True

  def die_if_infected(self):
    if self.alive and self.infected and not self.immune:
      prob = inv_logit(-5 + self.days_infected / 10 + self.age / 100 + 1 * (self.gender == 'male'))
      # print(prob)
      if np.random.random() < prob:
        self.alive = False

  def recover_if_infected(self, days=10):
    if self.infected and self.alive:
      if self.days_infected > days:
        self.infected = False
        self.immune = True

  def add_day(self):
    if self.infected and self.alive:
      self.days_infected += 1

  def isolate(self):
    self.isolated = True


N = 2000
T = 30 # periods

# initialise population

humans = [Human(i) for i in range(N)]

# infect a few people

rand = np.random.choice(N, 10, replace=False)

for r in rand:
  humans[r].infected = True

# now evolve

data_cases = []
data_dead = []

for period in range(T):
  for i in range(N):
    humans[i].add_day()
    humans[i].get_infected()
    humans[i].die_if_infected()
    humans[i].recover_if_infected()
    # some people isolate
    if np.random.random() < .01:
      humans[i].isolate()

  n_cases = sum([1 for i in range(N) if humans[i].infected])
  n_dead = sum([1 for i in range(N) if humans[i].alive == False])
  n_immune = sum([1 for i in range(N) if humans[i].immune])
  n_cases += n_immune

  print(period, n_cases, n_dead, n_immune)
  data_cases.append(n_cases)
  data_dead.append(n_dead)

p1, = plt.plot(data_cases, label='Total Infected')
chg = change(data_cases)
p2, = plt.plot(chg, label='Change in infected')
p3, = plt.plot(data_dead, label='Dead')
plt.legend(handles=[p1, p2, p3])
# plt.show()
plt.savefig('change.png')






