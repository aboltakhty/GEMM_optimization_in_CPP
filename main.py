# python setup.py build_ext --inplace
# sudo apt-get install libboost-python-dev
# find /usr/lib /usr/local/lib -name "libboost_python*.so"
# sudo apt install python3-all-dev


import matrix_mult
from random import randint


# 1) Python: Initialize the matrices with a constant seed (4x4, 8x8, 16x16, and so on) and alpha beta constants just like gemm
# 2) Python: Start the timer and pass these values and matrices to C++ code
# 3) C++: Do the multiplication just like with and without optimiation (finally if it possible add openmp)
# 4) Python: Stop the timer and store the time value


def matrix_random_number(n_row, n_columnas):
    return [[randint(0,100) for _ in range(n_row)] for _ in range(n_columnas)]





A = matrix_random_number(70, 10)
B = matrix_random_number(10, 70)

result = matrix_mult.matrix_mult(A, B)
print(result)
