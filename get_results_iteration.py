import matrix_mult
import numpy as np
import time
import argparse
import pandas as pd
from gem import GEM_kernel
def main(optimization_num: int, number_of_core: int, alpha: float, beta: float, random_seed: int) -> None:
    elapsed_times = []
    if optimization_num == 0:
        optimization = 'No Optimization'
    elif optimization_num == 1:
        optimization = 'Manual Parallelism'
    elif optimization_num == 2: 
        optimization = 'Dynamic Scheduling'

    elif optimization_num == 3:
        optimization = 'GEMM Python'

    print('Method: ',optimization)
    number_iteration = 20
    print('number iteration: ',number_iteration)
    print('number of core: ',number_of_core)

    np.random.seed(random_seed)
    # matrix_sizes = [1024]
    matrix_sizes = [4,8,16,32,64,128,256,512,2048]
    # matrix_sizes = [512]
    # matrix_sizes = [128,256,512,1024]
    for matrix_size in matrix_sizes:  # Matrix size will double on each iteration
        elapsed_time_ms = 0
        A = np.random.uniform(0, 1000, (matrix_size, matrix_size))
        B = np.random.uniform(0, 1000, (matrix_size, matrix_size))
        C = np.random.uniform(0, 1000, (matrix_size, matrix_size))

        # Convert numpy arrays to Python lists
        A_list = A.tolist()
        B_list = B.tolist()
        C_list = C.tolist()

        for j in range(number_iteration):
            # print(j,'  ', matrix_size)
            # Generate random matrices A, B, and C

            # Perform matrix multiplication using the matrix_mult module
            if optimization_num == 3:
                start_time = time.perf_counter()
                GEM_kernel(alpha, beta, C, A, B)
                end_time = time.perf_counter()
            else:
                start_time = time.perf_counter()
                result = matrix_mult.matrix_mult(A_list, B_list, C_list, alpha, beta, optimization_num, number_of_core)
                end_time = time.perf_counter()

            elapsed_time_ms += (end_time - start_time) *1000 # Convert to milliseconds
        print(f"matrix size : {matrix_size} \t time in milisecond: {elapsed_time_ms/20}")
    #         # Convert result back to numpy array for easy handling
    #         elapsed_times.append((optimization, matrix_size, elapsed_time_ms))

    # df_elapsed_times = pd.DataFrame(elapsed_times, columns=['Optimization Method','Matrix Size', 'Elapsed Time (ms)'])
    # # Save the DataFrame to a CSV file
    # df_elapsed_times.to_csv(optimization+'_second4_elapsed_times.csv', index=False)
    # grouped = df_elapsed_times.groupby(['Optimization Method', 'Matrix Size'])

    # # Calculate the required statistics
    # stats = grouped['Elapsed Time (ms)'].agg(['min', 'max', 'mean', 'std']).reset_index()
    # stats.to_csv(optimization+'_second4_elapsed_time_stats.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Matrix multiplication with optimization options.')
    parser.add_argument('--optimization_num', type=int, choices=[0, 1, 2], default=0, help='Optimization method (0 for no optimization, 1 for parallelism)')
    parser.add_argument('--number_of_core', type=int, default=4, help='Number of core')
    parser.add_argument('--random_seed', type=int, default=42, help='Random seed for matrix generation')
    parser.add_argument('--alpha', type=float, default=1.5, help='Alpha scalar for the GEMM operation')
    parser.add_argument('--beta', type=float, default=1.2, help='Beta scalar for the GEMM operation')

    args = parser.parse_args()
    # for number_of_core in [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50,55,60,65,70,71,72,73,80,85,90,10]:
    # for number_of_core in [85]:
    # for optimization_num in [2,1]:
    main(optimization_num=1, alpha=args.alpha, beta=args.beta, random_seed=args.random_seed, number_of_core = 1)
        # main(optimization_num=optimization_num, alpha=args.alpha, beta=args.beta, random_seed=args.random_seed, number_of_core = number_of_core)
