import matrix_mult
from random import randint
import numpy as np

# Define the initial shape of the matrix
# Note that the rows=columns
matrix_size = 4

# Set the random seed for reproducibility
np.random.seed(42)

# Generating a square matrix with a constant seed with values between 0 and 10000
A = np.random.randint(0, 10000, size=(matrix_size, matrix_size))
print(A)

# Set the random seed for reproducibility
np.random.seed(50)

# Generating a square matrix with a constant seed with values between 0 and 10000
B = np.random.randint(0, 10000, size=(matrix_size, matrix_size))
print(B)


result = matrix_mult.matrix_mult(A, B)
print(result)
