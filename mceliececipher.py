from mathutils import *


class McElieceCipher:
    def __init__(self, t, k, n):
        self.t = t
        self.k = k
        self.n = n
        self.G = None
        self.S = None
        self.P = None
        self.P_inv = None
        self.S_inv = None
        self.Gp = None
        self.Gp_row = None
        self.Gp_col = None
        self.e = None
        self.y = None
        self.x = None
        self.xS = None
        self.y_ = None
        self.Cp = None


    def generate_create_keys(self):
        self.G = create_generation_G(self.n, self.k*3)
        self.S, self.S_inv = create_invertible_S_inverse_S_inv(self.G.shape[0])
        self.P = create_permutation_P(self.G.shape[1])
        self.Gp = create_matrix_Gp(self.G, self.S, self.P)
        self.Gp_row = self.Gp.shape[0]
        self.Gp_col = self.Gp.shape[1]
        self.P_inv = create_inverse_P(self.P)


    def encrypt(self, x, Gp, Gp_col, t):
        if Gp is not None and x is not None:
            self.Cp = multi_matrix(x, Gp)
            print(f"\t   --> Successfully create generated ciphertext vector Cp[{self.Cp.shape[0]}, {self.Cp.shape[1]}] = x[{x.shape[0]},{x.shape[1]}] * Gp[{Gp.shape[0]}, {Gp.shape[1]}]")

            self.e = random_matrix(t, Gp_col)
            self.y = cipherText(self.Cp, self.e)


    def decrypt(self, matrix, y, P_inv, S_inv, S):
        if P_inv is not None and S_inv is not None:
            print(f"\n\t- Creating multiply matrix .....")
            # self.y_ = multi_matrix(y, P_inv)
            # print(f"\t   --> Successfully create generated ciphertext vector y' = y * P^-1")

            self.xS = multi_matrix(matrix, S)
            print(f"\t   --> Successfully create value xS")

            self.x = multi_matrix(self.xS, S_inv)
            print(f"\t   --> Successfully restore the original matrix x = xS * S^-1")

