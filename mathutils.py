import numpy as np
from joblib import Parallel, delayed


def brute_force(A, B):
    n, m, p = A.shape[0], A.shape[1], B.shape[1]
    C = np.zeros((n, p))
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k]*B[k][j]
    return C


def split(matrix):
    n = len(matrix)
    return matrix[:n//2, :n//2], matrix[:n//2, n//2:], matrix[n//2:, :n//2], matrix[n//2:, n//2:]


def strassen_nxn(A, B, m):
    if len(A) <= 2:
        return brute_force(A, B)

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    arg_list = [(np.add(A11,A22), np.add(B11,B22), m), 
                 (np.add(A21,A22), B11, m), (A11, np.subtract(B12,B22), m), 
                 (A22, np.subtract(B21,B11), m), (np.add(A11,A12), B22, m), 
                 (np.subtract(A11,A21), np.add(B11,B12), m), 
                 (np.subtract(A12,A22), np.add(B21,B22), m)]
    
    results = Parallel(n_jobs=7)(delayed(strassen_nxn)(A, B, m) for A, B, m in arg_list)
    p1, p2, p3, p4, p5, p6, p7 = get_strassen(results)

    C11 = np.add(np.subtract(np.add(p1,p4), p5),p7) 
    C12 = np.add(p3,p5)
    C21 = np.add(p2,p4) 
    C22 = np.subtract(np.subtract(np.add(p3, p1), p2), p6)

    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    C = C[:m, :m]
    return C


def strassen_nxm(A, B, n, m):
    if len(A) <= 2:
        return brute_force(A, B)

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    arg_list = [(np.add(A11,A22), np.add(B11,B22), n, m), 
                 (np.add(A21,A22), B11, n, m), (A11, np.subtract(B12,B22), n, m), 
                 (A22, np.subtract(B21,B11), n, m), (np.add(A11,A12), B22, n, m), 
                 (np.subtract(A11,A21), np.add(B11,B12), n, m), 
                 (np.subtract(A12,A22), np.add(B21,B22), n, m)]
    
    results = Parallel(n_jobs=7)(delayed(strassen_nxm)(A, B, n, m) for A, B, n, m in arg_list)
    p1, p2, p3, p4, p5, p6, p7 = get_strassen(results)

    C11 = np.add(np.subtract(np.add(p1,p4), p5),p7) 
    C12 = np.add(p3,p5)
    C21 = np.add(p2,p4) 
    C22 = np.subtract(np.subtract(np.add(p3, p1), p2), p6)

    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    C = C[:n, :m]
    return C


def can_create_matrix(X):
    try:
        num_cols = len(X[0])
        same_num_cols = True
        for row in X:
            if len(row) != num_cols:
                same_num_cols = False
                break

        return same_num_cols
    
    except ValueError as e:
        print(f"Error from 'can_create_matrix_?': {e}")

    return None 


def paddingMatrix(X):
    try:
        max_length = max([len(row) for row in X])
        input = np.full((len(X), max_length), -1)

        already_assigned = np.zeros_like(input, dtype=bool)

        for i, row in enumerate(X):
            input[i, :len(row)] = row
            already_assigned[i, :len(row)] = True

        return input.astype(int), already_assigned
    
    except ValueError as e:
        print(f"Error from 'padding to matrix': {e}")

    return None 


def create_generation_G(k, n):
    try:
        print(f"\n\t- Creating Generation matrix G .....")
        G = np.random.randint(0, 2, size=(k, n))
        print(f"\t   --> Successfully create Generation matrix G[{k},{n}]")
        return G
    
    except ValueError as e:
        print(f"Error from 'create_G[{k},{n}]': {e}")

    return None


def create_invertible_S_inverse_S_inv(k):
    try:
        I = np.eye(k) 
        print(f"\t- Creating Invertible matrix S .....")
        count = 0
        while True:
            S = np.random.randint(2, size=(k, k))
            count+=1
            test = np.linalg.det(S)
            if test != 0:
                S_inv = np.linalg.inv(S).astype(int)
                n = len(S)
                m = 2 ** int(np.ceil(np.log2(max(len(S), len(S_inv), len(S[0]), len(S_inv[0])))))  
                A_new = np.zeros((m, m))
                A_new[:len(S), :len(S[0])] = S
                B_new = np.zeros((m, m))
                B_new[:len(S_inv), :len(S_inv[0])] = S_inv
                SS_inv = strassen_nxn(A_new, B_new, n)

                if np.allclose(SS_inv, I):
                    print(f"\t   --> Successfully create Invertible matrix S[{k},{k}]") 
                    print(f"\t   --> Number time of random S: ", count)
                    print(f"\t   --> Successfully create Inverse matrix S^-1")
                    return S, S_inv
                
    except ValueError as e:
        print(f"Error from 'create_S_S^-1[{k},{k}]': {e}")

    return None


def create_permutation_P(n):
    try:
        print(f"\t- Creating Permutation matrix P .....")
        arr = np.arange(n)

        for i in range(n-1):
            j = np.random.randint(i, n)
            arr[i], arr[j] = arr[j], arr[i]

        P = np.zeros((n, n))
        for i in range(n):
            P[i, arr[i]] = 1

        P = P.astype(int)
        if np.linalg.det(P) != 0:
            print(f"\t   --> Successfully create Permutation matrix P[{n},{n}]")
            return P 

    except ValueError as e:
        print(f"Error from 'create_P[{n},{n}]': {e}")

    return None


def create_matrix_Gp(G, S, P):
    try:
        print(f"\t- Creating matrix Gp .....")
        n = len(G)
        m = len(P)
        q = 2 ** int(np.ceil(np.log2(max(len(G), len(P), len(S), len(G[0]), len(P[0]), len(S[0])))))  
        A_new = np.zeros((q, q))
        A_new[:len(G), :len(G[0])] = G
        B_new = np.zeros((q, q))
        B_new[:len(P), :len(P[0])] = P
        C_new = np.zeros((q, q))
        C_new[:len(S), :len(S[0])] = S
        Gp_1 = strassen_nxn(C_new, A_new, n)
        Gp_1_new = np.zeros((q, q))
        Gp_1_new[:len(Gp_1), :len(Gp_1[0])] = Gp_1
        Gp = strassen_nxm(Gp_1_new, B_new, n, m)

        print(f"\t   --> Successfully create matrix Gp[{Gp.shape[0]},{Gp.shape[1]}] = S*G*P")
        return Gp
    
    except ValueError as e:
        print(f"Error from 'create_Gp = S*G*P': {e}")

    return None


def create_inverse_P(matrix):
    try:
        print(f"\t- Creating inverse matrix P^-1 .....")
        matrix_inv = np.linalg.inv(matrix).astype(int)
        print(f"\t   --> Successfully create inverse matrix P^-1")
        return matrix_inv
    
    except ValueError as e:
        print(f"Error from 'create_P^-1': {e}")

    return None


def random_matrix(k, n):
    try:
        print(f"\t- Creating generate random error matrix e .....")
        matrix = np.random.randint(2, size=(k, n))
        print(f"\t   --> Successfully create generate random error matrix e[{k},{n}]")
        return matrix
    
    except ValueError as e:
        print(f"Error from 'Create_error_e[{k},{n}]': {e}")

    return None


def cipherText(Cp, e):
    try:
        print(f"\t- Creating generated ciphertext y .....")
        if Cp.ndim == 1:
            y = np.add(Cp, e)
            print(f"\t   --> Successfully create generated ciphertext y[{y.shape[0]},{y.shape[1]}] = Cp + e")
            return y
        
        elif Cp.ndim > 1 or len(Cp.shape) > 1:
            m, n = Cp.shape
            p, q = e.shape

            if n != q:
                print(f"ERROR CREATE CIPHERTEXT: Cp.shape[1] = {n} != e.shape[1] = {q}. --> Error from create Matrix Cp")
                return None
            
            y = np.zeros((p, n))
            for i in range(m):
                for j in range(n):
                    y[i][j] = Cp[i][j] + e[i][j]

            for i in range(m, p):
                for j in range(n):
                    y[i][j] = e[i][j]

            print(f"\t   --> Successfully create generated ciphertext y[{y.shape[0]},{y.shape[1]}] = Cp + e")
            return y
    
    except ValueError as e:
        print(f"Error from 'Create_y = Cp + e': {e}")

    return None


def multi_matrix(a, b):
    try:
        n = len(a)
        m = b.shape[1]
        q = 2 ** int(np.ceil(np.log2(max(len(a), len(b), len(a[0]), len(b[0])))))  
        A_new = np.zeros((q, q))
        A_new[:len(a), :len(a[0])] = a
        B_new = np.zeros((q, q))
        B_new[:len(b), :len(b[0])] = b
        res = strassen_nxm(A_new, B_new, n, m)
        return res
    
    except ValueError as e:
        print(f"Error from 'matrix_A * matrix_B': {e}")

    return None


#-------------------------------------- STRASSEN ----------------------------------------------
def get_strassen(res):
    try:
        p1 = res[0]
        p2 = res[1]
        p3 = res[2]
        p4 = res[3]
        p5 = res[4]
        p6 = res[5]
        p7 = res[6]
        return p1, p2, p3, p4, p5, p6, p7
    
    except ValueError as e:
        print(f"Error from 'get_strassen': {e}")

    return None

