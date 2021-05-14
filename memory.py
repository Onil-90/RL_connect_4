# Class Memory
class Memory:
    def __init__(self, size, batchSize):
        self.size = size
        self.batchSize = batchSize

    def get_batch(self):
        # TO WRITE
        pass

    def update(self):
        # TO WRITE
        pass


    def create_x_train(experience):
        # TO FIX
        len_experience = len(experience)
        n_rows = np.shape(experience[0][0])[0]
        n_columns = np.shape(experience[0][0])[1]
        S = []
        for exp in range(len_experience):
           S.append(experience[exp][0])
        S = np.array(S)
        S = S.reshape(len_experience, n_rows, n_columns, 1)
        return S
