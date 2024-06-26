import matrix_mult
import numpy as np
import time
import argparse
import pandas as pd

def main(optimization_num: int, number_of_core: int, alpha: float, beta: float, random_seed: int) -> None:
    elapsed_times = []
    if optimization_num == 0:
        optimization = 'No Optimization'
    elif optimization_num == 1:
        optimization = 'Manual Parallelism'
    else:
        optimization = 'Dynamic Scheduling'
    
    number_iteration = 10000


    np.random.seed(random_seed)
    # matrix_sizes = [1024]
    matrix_sizes = [4,8,16,32,64,128,256,512,1024]
    for matrix_size in matrix_sizes:  # Matrix size will double on each iteration
        for j in range(5):
            print(j,'  ', matrix_size)
            # Generate random matrices A, B, and C
            A = np.random.uniform(0, 1000, (matrix_size, matrix_size))
            B = np.random.uniform(0, 1000, (matrix_size, matrix_size))
            C = np.random.uniform(0, 1000, (matrix_size, matrix_size))

            # Convert numpy arrays to Python lists
            A_list = A.tolist()
            B_list = B.tolist()
            C_list = C.tolist()

            # Perform matrix multiplication using the matrix_mult module
            start_time = time.perf_counter()
            result = matrix_mult.matrix_mult(A_list, B_list, C_list, alpha, beta, optimization_num, number_of_core)
            end_time = time.perf_counter()

            elapsed_time_ms = (end_time - start_time) *1000 # Convert to milliseconds

            # Convert result back to numpy array for easy handling
            elapsed_times.append((optimization, matrix_size, elapsed_time_ms))

    df_elapsed_times = pd.DataFrame(elapsed_times, columns=['Optimization Method','Matrix Size', 'Elapsed Time (ms)'])
    # Save the DataFrame to a CSV file
    df_elapsed_times.to_csv(optimization+'_second4_elapsed_times.csv', index=False)
    grouped = df_elapsed_times.groupby(['Optimization Method', 'Matrix Size'])

    # Calculate the required statistics
    stats = grouped['Elapsed Time (ms)'].agg(['min', 'max', 'mean', 'std']).reset_index()
    stats.to_csv(optimization+'_second4_elapsed_time_stats.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Matrix multiplication with optimization options.')
    parser.add_argument('--optimization_num', type=int, choices=[0, 1, 2], default=2, help='Optimization method (0 for no optimization, 1 for parallelism)')
    parser.add_argument('--number_of_core', type=int, default=4, help='Number of core')
    parser.add_argument('--random_seed', type=int, default=42, help='Random seed for matrix generation')
    parser.add_argument('--alpha', type=float, default=1.5, help='Alpha scalar for the GEMM operation')
    parser.add_argument('--beta', type=float, default=1.2, help='Beta scalar for the GEMM operation')

    args = parser.parse_args()

    main(optimization_num=args.optimization_num, alpha=args.alpha, beta=args.beta, random_seed=args.random_seed, number_of_core = args.number_of_core)
