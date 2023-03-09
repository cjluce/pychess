"""."""


class Move:
    """."""

    FileCharToNum = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5,
                     "G": 6, "H": 7}
    RankCharToNum = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5,
                     "7": 6, "8": 7}

    def __init__(self, moveinput):
        """."""
        self.moveinput = moveinput
        self.string = self.get_movestring()
        self.index = self.get_moveindex()

    def __str__(self):
        """."""
        return self.string

    def __repr__(self):
        """."""
        return self.__str__()

    def _handle_stringinput(self, stringinput):
        """."""
        if len(stringinput) != 2:
            print(f"Invalid move input: {stringinput}")
            raise ValueError

        movefile, moverank = stringinput[0], stringinput[1]

        if movefile not in self.FileCharToNum:
            print(f"Invalid file: {movefile}")
            raise KeyError

        if moverank not in self.RankCharToNum:
            print(f"Invalid rank: {moverank}")
            raise KeyError

        return ((self.RankCharToNum[moverank] * 8) +
                self.FileCharToNum[movefile])

    def _index_to_coord(self, index):
        """."""
        alphabet = "ABCDEFGH"
        if index < 0 or index > 63:
            print(f"The given index is invalid: {index}")
            raise IndexError
        coord_file = index % 8
        coord_rank = (index // 8) + 1
        return f"{alphabet[coord_file]}{coord_rank}"

    def get_movestring(self):
        """."""
        if isinstance(self.moveinput, str):
            return self.moveinput
        else:
            return self._index_to_coord(self.moveinput)

    def get_moveindex(self):
        """."""
        if isinstance(self.moveinput, int):
            return self.moveinput
        else:
            return self._handle_stringinput(self.moveinput)

    def parse_moveinput(self, moveinput):
        """."""
        if isinstance(moveinput, int):
            return moveinput
        if isinstance(moveinput, str):
            return self._handle_stringinput(moveinput)
