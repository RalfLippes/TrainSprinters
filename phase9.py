import matplotlib.pyplot as plt
import math
import random

class Creature():
    """
    Create Creature object with position in a 1 x 1 field, with an angle to move
    toward, speed and color. Can use step method to move in the direction of the
    angle.
    """
    def __init__(self, pos_x, pos_y, angle, birthrate = 0, alive = True, reproduce = False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle
        self.alive = alive
        self.birthrate = birthrate
        self.reproduce = reproduce

    def step(self):
        """
        Changes the creature's position by calculation the rate of change, then
        updating the position using that rate of change.
        """
        # calculate rate of change
        change_x = math.cos(self.angle) * self.speed
        change_y = math.sin(self.angle) * self.speed

        # add rate of change to current position
        self.pos_x += change_x
        self.pos_y += change_y

        # if the creature is out of bounds, change angle
        if self.pos_x < 0 or self.pos_x > 1 or self.pos_y < 0 or self.pos_y > 1:
            self.angle += math.pi

    def distance(self, other):
        """
        Calculates the Euclidean distance between the creature and another creature.
        """
        return math.sqrt((self.pos_x - other.pos_x) ** 2 + (self.pos_y - other.pos_y) ** 2)

    def interact(self, other):
        """
        Handles the interactions for all creatures. It sets reproduce to True when
        two creatures of the same type meet (with a success probability of birthrate).
        """
        if type(self) == type(other) and random.random() < self.birthrate:
            self.reproduce = True

class Rabbit(Creature):
    """
    Subclass from Creature. Inherits position and angle, and can set speed and
    color seperately. Uses superclass step method, but also introduces variability
    in moving direction.
    """
    def __init__(self, pos_x, pos_y, angle, birthrate = 0, alive = True):
        super().__init__(pos_x, pos_y, angle, alive)
        self.speed = 0.01
        self.color = "blue"
        self.birthrate = birthrate

    def step(self):
        """
        Changes the rabbits position when it goes out of bounds, or randomly
        with a 20 percent change before each step.
        """
        # create a 20 percent change to change direction
        if random.random() >= 0.8:
            self.angle += random.uniform(-math.pi / 2, math.pi / 2)

        super().step()

class Fox(Creature):
    """
    Subclass from Creature. Inherits position and angle, and can set speed and
    color seperately. Uses superclass step method, but also introduces variability
    in moving direction.
    """
    def __init__(self, pos_x, pos_y, angle, birthrate = 0, alive = True, hunger = 0):
        super().__init__(pos_x, pos_y, angle, alive)
        self.speed = 0.03
        self.color = "red"
        self.hunger = hunger
        self.birthrate = birthrate

    def step(self):
        """
        Changes the fox' position when it goes out of bounds, or randomly
        with a 20 percent change before each step.
        """
        # add 1 to hunger and kill if hunger gets too high
        self.hunger += 1
        if self.hunger >= 80:
            self.alive = False

        # create a 20 percent change to change direction
        if random.random() > 0.8:
            self.angle += random.uniform(-math.pi / 4, math.pi / 4)

        super().step()

    def interact(self, other):
        """
        This function handles the interactions the fox has when close enough to
        other creatures.
        """
        # inherit interactions from superclass
        super().interact(other)

        # check if the other creature is a rabbit
        if type(other) == Rabbit:
            # reset hunger
            self.hunger = 0

            # kill rabbit
            other.alive = False

class Experiment():
    """
    Sets up the 'playing field' for the experiment. Creates the appropriate
    number of foxes and rabbits, and performs the experiment the chosen amount
    of times.
    """
    def __init__(self, iterations, number_of_rabbits, number_of_foxes, birthrate_rabbits, birthrate_foxes, interaction_distance = 0.05, max_creatures = 50, visualize = False):
        """
        Initializes the experiment with a number of iterations, number of rabbits
        and a number of foxes.
        """
        self.iterations = iterations
        self.interaction_distance = interaction_distance
        self.birthrate_rabbits = birthrate_rabbits
        self.birthrate_foxes = birthrate_foxes
        self.max_creatures = max_creatures
        self.visualize = visualize

        # only plot when self.visualize is true
        if self.visualize == True:
            self.setup_plot()
        self.creatures = []

        # create the correct amount of rabbits and foxes
        self.add_creatures(number_of_rabbits, number_of_foxes)

    def add_creatures(self, number_of_rabbits, number_of_foxes):
        """
        Creates the chosen amount of rabbits and foxes by looping over the amount
        and storing each new object in the list that was made before. Warning: The
        amount of creatures can go slightly over the max_creatures limit when
        multiple creatures are added in a single iteration.
        """
        # only run if there is less than the maximum amount of creatures
        if len(self.creatures) < self.max_creatures:
            for rabbit in range(number_of_rabbits):
                # create new random rabbit each iteration and append to list
                rabbit = Rabbit(random.random(), random.random(), random.random() * math.pi, self.birthrate_rabbits)
                self.creatures.append(rabbit)

            # do the same for the foxes
            for fox in range(number_of_foxes):
                fox = Fox(random.random(), random.random(), random.random() * math.pi, self.birthrate_foxes)
                self.creatures.append(fox)

    def run(self, iterations=None):
        """
        Sets up the amount of iterations, with a default of None. Then draws the
        1 x 1 experiment field and performs the steps every iteration.
        """
        if iterations == None:
            iterations = self.iterations

        for i in range(iterations):
            self.step()

            if self.visualize == True:
                self.draw()

    def step(self):
        """
        Performs a step for every creature in the list. This function gets
        repeated every iteration by the run() method. This means every iteration
        each creature moves. It also removes creatures that have died.
        """
        for creature in self.creatures:
            creature.step()

        # handle interactions and resolve reproduction and deaths
        self.handle_interaction()
        self.resolve_deaths()
        self.resolve_reproduction()

    def resolve_deaths(self):
        """
        Removes creatures that have died of hunger from the creatures list.
        """
        for creature in self.creatures[:]:
            if creature.alive == False:
                self.creatures.remove(creature)

    def resolve_reproduction(self):
        """
        Spawns new creatures when reproduce attribute has been set to True after
        the two creatures have met.
        """
        # create count of how many creatures to spawn
        rabbit_number = 0
        foxes_number = 0

        # check for every creature if they can reproduce
        for creature in self.creatures[:]:
            # and add 1 to counter of the correct creature
            if creature.reproduce == True and type(creature) == Rabbit:
                rabbit_number += 1
            elif creature.reproduce == True and type(creature) == Fox:
                foxes_number += 1

            # reset the creature's reproduction status
            creature.reproduce = False

        # now add the correct amount of creatures
        self.add_creatures(rabbit_number, foxes_number)

    def handle_interaction(self):
        """
        Checks the distances between all the creatures and calls the interact
        function when the distance is in interaction range.
        """
        for creature1 in self.creatures:
            for creature2 in self.creatures:
                if creature1 is not creature2 and creature1.distance(creature2) < self.interaction_distance:
                    creature1.interact(creature2)

    def count_creatures(self):
        """
        Counts the creatures of each class and returns their count.
        """
        rabbits_number = 0
        foxes_number = 0

        # loop over creature list and add creature to correct count
        for creature in self.creatures:
            if type(creature) == Fox:
                foxes_number += 1
            else:
                rabbits_number += 1

        return rabbits_number, foxes_number

    def draw(self):
        """
        Plots the current position of the creatures in the 1 x 1 space.
        """
        self.ax1.axis([0, 1, 0, 1])

        # create list to collect positions of all creatures and their colors
        self.creature_x = []
        self.creature_y = []
        self.color_list = []

        # append positions and colors of the creatures to the lists
        for creature in self.creatures:
            self.creature_x.append(creature.pos_x)
            self.creature_y.append(creature.pos_y)
            self.color_list.append(creature.color)

        # plot all positions in correct color
        self.ax1.scatter(self.creature_x, self.creature_y, c = self.color_list)

        plt.draw()
        plt.pause(0.01)
        self.ax1.cla()

    def setup_plot(self):
        self.fig, self.ax1 = plt.subplots(1)
        self.ax1.set_aspect('equal')
        self.ax1.axes.get_xaxis().set_visible(False)
        self.ax1.axes.get_yaxis().set_visible(False)

if __name__ == "__main__":
    my_experiment = Experiment(200, 10, 3, 0.15, 0.10, visualize = True)
    my_experiment.run()
    print(my_experiment.count_creatures())
