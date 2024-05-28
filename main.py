import matrix_mult
import numpy as np
import time
import argparse

def main(matrix_size: int, optimization_num: int, alpha: float, beta: float, random_seed: int) -> None:
    np.random.seed(random_seed)

    for _ in range(2):  # Matrix size will double on each iteration
        # Generate random matrices A, B, and C
        A = np.random.uniform(0, 10000, (matrix_size, matrix_size))
        B = np.random.uniform(0, 10000, (matrix_size, matrix_size))
        C = np.random.uniform(0, 10000, (matrix_size, matrix_size))

        print(f"Matrix A ({matrix_size}x{matrix_size}):\n{A}")
        print(f"Matrix B ({matrix_size}x{matrix_size}):\n{B}")
        print(f"Matrix C ({matrix_size}x{matrix_size}):\n{C}")

        # Convert numpy arrays to Python lists
        A_list = A.tolist()
        B_list = B.tolist()
        C_list = C.tolist()

        # Perform matrix multiplication using the matrix_mult module
        start_time = time.perf_counter()
        result = matrix_mult.matrix_mult(A_list, B_list, C_list, alpha, beta, optimization_num)
        end_time = time.perf_counter()

        elapsed_time_ms = (end_time - start_time) *1000 # Convert to milliseconds

        # Convert result back to numpy array for easy handling
        result_np = np.array(result)
        print(f"Result matrix C ({matrix_size}x{matrix_size}):\n{result_np}")
        print(f"Elapsed time for {matrix_size}x{matrix_size}: {elapsed_time_ms:.4f} ms")

        matrix_size *= 2  # Double the matrix size for the next iteration

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Matrix multiplication with optimization options.')
    parser.add_argument('--optimization_num', type=int, choices=[0, 1], default=0, help='Optimization method (0 for no optimization, 1 for parallelism)')
    parser.add_argument('--random_seed', type=int, default=42, help='Random seed for matrix generation')
    parser.add_argument('--matrix_size', type=int, default=4, help='Initial matrix size (will double each iteration)')
    parser.add_argument('--alpha', type=float, default=1.5, help='Alpha scalar for the GEMM operation')
    parser.add_argument('--beta', type=float, default=1.2, help='Beta scalar for the GEMM operation')

    args = parser.parse_args()

    main(matrix_size=args.matrix_size, optimization_num=args.optimization_num, alpha=args.alpha, beta=args.beta, random_seed=args.random_seed)
