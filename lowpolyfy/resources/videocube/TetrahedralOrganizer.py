from numpy import empty

class TetrahedralOrganizer():
    def __init__(self, length):
        self.bins = list(empty(length))

    def insert(self, tetrahedrals):
        # Insert each tetrahedral into the frame bins that they overlap
        for tetrahedral in tetrahedrals:
            # Find the frames which they overlap
            frame_numbers = tetrahedral.frames_intersected()   

            for frame_number in frame_numbers:
                if (type(self.bins[frame_number]) is not list):
                    self.bins[frame_number] = []
                self.bins[frame_number].append(tetrahedral)   
        return