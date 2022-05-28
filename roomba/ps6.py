# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

from cProfile import label
import math
import random
from turtle import color, position

import ps6_visualize
import pylab

# === Provided classes


class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """

    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getXY(self):
        return [self.x, self.y]

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """

    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        assert width > 0 and height > 0
        self.width = width
        self.height = height
        self.tiles = []
        for i in range(width):
            self.tiles.append([False]*len(range(height)))
            for j in range(height):
                self.tiles[i][j] = False

    def cleanTileAtPosition(self, pos: Position):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        if self.isPositionInRoom(pos):
            x, y = int(pos.getX()), int(pos.getY())
            self.tiles[x][y] = True
        else:
            print("Requested position out of bounds.")

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if m >= self.width or n >= self.height or (m < 0 or n < 0):
            print("Indices out of bounds!")
            return None

        return self.tiles[m][n]

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        total = 0
        for row in self.tiles:
            for col in row:
                if col:
                    total += 1

        return total

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.random() * self.width, random.random() * self.height)

    def isPositionInRoom(self, pos: Position):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """

        return ((0 <= pos.getX() < self.width)
                and (0 <= pos.getY() < self.height))


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """

    def __init__(self, room: RectangularRoom, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.dir = random.randrange(360)
        self.pos = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.pos)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.pos.getNewPosition(self.dir, self.speed)

        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(self.getRobotPosition())
        else:
            self.setRobotDirection(random.randrange(360))


# === Problem 3


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type: Robot, animate=False):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """

    clockTicks = 0
    for i in range(num_trials):
        if animate:
            anim = ps6_visualize.RobotVisualization(1, width, height)

        room = RectangularRoom(width, height)
        robots = []
        for i in range(num_robots):
            robots.append(robot_type(room, speed))

        while not isAboveCoverage(min_coverage, room):
            if animate:
                anim.update(room, robots)

            for robot in robots:
                robot.updatePositionAndClean()

            clockTicks += 1

        if animate:
            anim.done()

    return math.ceil(clockTicks / num_trials)


def isAboveCoverage(min_coverage, room: RectangularRoom):
    return min_coverage <= room.getNumCleanedTiles() / room.getNumTiles()


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20�20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions
#	 20�20, 25�16, 40�10, 50�8, 80�5, and 100�4?


def showPlot1(num_robots, robot_type=StandardRobot, room_size=(50, 50)):
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    t = []
    r = range(1, num_robots + 1)

    for i in r:
        t.append(runSimulation(
            i, 1.0, room_size[0], room_size[1], 0.8, 10, robot_type))

    pylab.plot(t, r)
    pylab.xlabel('Cleaning time (s)')
    pylab.ylabel('Number of robots')
    pylab.title('Dependence of cleaning time on number of robots')
    pylab.show()


# showPlot1(20)


def showPlot2(room_sizes):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    t = []
    tiles = []

    for w, h in room_sizes:
        print(w, h)
        print(tiles)
        print(t)
        tiles.append(w*h)
        t.append(runSimulation(10, 1.0, w, h, 0.8, 10, StandardRobot))

    pylab.plot(t, tiles)
    pylab.xlabel('Cleaning time (s)')
    pylab.ylabel('Number of tiles')
    pylab.title('Dependence of cleaning time on room size (10 robots)')
    pylab.show()


# room_sizes = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
# showPlot2(room_sizes)

# === Problem 5


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos = self.getRobotPosition()
        direction = self.getRobotDirection()
        self.setRobotDirection(random.randrange(360))
        new_pos = pos.getNewPosition(direction, self.speed)
        if self.room.isPositionInRoom(new_pos):
            self.setRobotPosition(new_pos)
            self.room.cleanTileAtPosition(new_pos)


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    t_standard = []
    t_random = []
    r = range(1, 10 + 1)

    for i in r:
        t_standard.append(runSimulation(
            i, 1.0, 20, 20, 0.8, 10, StandardRobot))
        t_random.append(runSimulation(
            i, 1.0, 20, 20, 0.8, 10, RandomWalkRobot))

    pylab.plot(t_standard, r, color='pink', label="Standard robot")
    pylab.plot(t_random, r, color='green', label="Random walk robot")
    pylab.xlabel('Cleaning time (s)')
    pylab.ylabel('Number of robots')
    pylab.title('Dependence of cleaning time on number of robots')
    pylab.legend()
    pylab.show()


# showPlot3()
# avg_std = runSimulation(5, 1, 20, 20, 0.8, 10, RandomWalkRobot, False)
avg_std = runSimulation(10, 2, 50, 50, 0.8, 10, StandardRobot, True)
