# https://github.com/UDC-GAC/polybench-python/blob/master/benchmarks/linear_algebra/blas/gemm/gemm.py
def GEM_kernel(alpha: float, beta: float, C: list, A: list, B: list):
# scop begin
    NI = len(C)
    NJ = len(C[0])
    NK = len(A[0])

    for i in range(0, NI):
        for j in range(0, NJ):
            C[i][j] *= beta

        for k in range(0, NK):
            for j in range(0, NJ):
                C[i][j] += alpha * A[i][k] * B[k][j]
    
    return C

# scop end