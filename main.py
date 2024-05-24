import matrix_mult
from random import randint
import numpy as np

# Define the initial shape of the matrix
# Note that the rows=columns
matrix_size = 4

# On every iteration the size of matrix will double
for i in range (2):
    # Set the random seed for reproducibility
    np.random.seed(42)

    # Generating a square matrix with a constant seed with values between 0 and 10000
    A = np.random.randint(0, 10000, size=(matrix_size, matrix_size))
    print("A:")
    print(A)

    # Set the random seed for reproducibility
    np.random.seed(50)

    # Generating a square matrix with a constant seed with values between 0 and 10000
    B = np.random.randint(0, 10000, size=(matrix_size, matrix_size))
    print("B:")
    print(B)

    # Convert numpy arrays to Python lists
    A = A.tolist()
    B = B.tolist()

    print("Result:")
    result = matrix_mult.matrix_mult(A, B)
    result = np.array(result)
    print(result)

    matrix_size *=2 # So that size of matrix can double on every iteration
