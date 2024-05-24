import matrix_mult
from random import randint
import numpy as np
import time

# Define the initial shape of the matrix
# Note that the rows=columns
matrix_size = 4

alpha = 1.5
beta = 1.2

# On every iteration the size of matrix will double
for i in range (2):
    # Set the random seed for reproducibility
    np.random.seed(42)

    # Generating a square matrix with a constant seed with values between 0 and 10000
    A = np.random.randint(0, 10000, size=(matrix_size, matrix_size))
    print("A=")
    print(A)

    # Set the random seed for reproducibility
    np.random.seed(50)

    # Generating a square matrix with a constant seed with values between 0 and 10000
    B = np.random.randint(0, 10000, size=(matrix_size, matrix_size))
    print("B=")
    print(B)

    # Set the random seed for reproducibility
    np.random.seed(58)

    # Generating a square matrix with a constant seed with values between 0 and 10000
    C = np.random.randint(0, 10000, size=(matrix_size, matrix_size))
    print("C=")
    print(C)

    # Convert numpy arrays to Python lists
    A = A.tolist()
    B = B.tolist()
    C = C.tolist()

    # Standard GEMM formula is:
    # C = α⋅A⋅B + β⋅C
    start = time.perf_counter()
    result = matrix_mult.matrix_mult(A, B, C, alpha, beta)
    end = time.perf_counter()

    
    result = np.array(result)
    print("Result (C)=")
    print(result)

    elapsed_time_ms = (end - start) * 1000  # Convert to milliseconds
    print(f"============ Elapsed time {matrix_size}x{matrix_size}: {elapsed_time_ms:.3f} ms ============")

    matrix_size *=2 # So that size of matrix can double on every iteration
