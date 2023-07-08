class MazeCell(object):
    def __init__(self, up_wall: bool, right_wall: bool, down_wall: bool, left_wall: bool, visited=False, start=False,
                 end=False):
        """
        :param up_wall: bool
        :param right_wall: bool
        :param down_wall: bool
        :param left_wall: bool

        makes a MazeCell object with the given walls
        """
        self.up_wall = up_wall
        self.right_wall = right_wall
        self.down_wall = down_wall
        self.left_wall = left_wall
        self.visited = visited
        self.start = start
        self.end = end

    def __str__(self):
        return "MazeCell: up_wall = {}, right_wall = {}, down_wall = {}, left_wall = {}".format(self.up_wall,
                                                                                                self.right_wall,
                                                                                                self.down_wall,
                                                                                                self.left_wall)
