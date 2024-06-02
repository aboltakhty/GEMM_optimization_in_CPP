#define BOOST_BIND_GLOBAL_PLACEHOLDERS
#include <boost/python.hpp>
#include <vector>
#include <chrono>
#include <iostream>
#include <omp.h>

#define ENABLE_BOOST_PRECISION_TIMER 0

// Convert Python list to std::vector
std::vector<std::vector<double>> py_list_to_vector(const boost::python::list& py_list) {
    std::vector<std::vector<double>> vec;
    for (int i = 0; i < boost::python::len(py_list); ++i) {
        boost::python::list sublist = boost::python::extract<boost::python::list>(py_list[i]);
        std::vector<double> subvec;
        for (int j = 0; j < boost::python::len(sublist); ++j) {
            subvec.push_back(boost::python::extract<double>(sublist[j]));
        }
        vec.push_back(subvec);
    }
    return vec;
}

// Convert std::vector to Python list
boost::python::list vector_to_py_list(const std::vector<std::vector<double>>& vec) {
    boost::python::list py_list;
    for (const auto& subvec : vec) {
        boost::python::list sublist;
        for (double val : subvec) {  // Fix type to double
            sublist.append(val);
        }
        py_list.append(sublist);
    }
    return py_list;
}

void matrix_mult_threading(const std::vector<std::vector<double>>& A, const std::vector<std::vector<double>>& B, std::vector<std::vector<double>>& C,
const double& alpha, const double& beta) {
    
    uint64_t rows_A = A.size();

    // Setting the maxinum of threads to half the number of rows
    // In this way a single thread has to worry about only 2 rows of the result matrix
    omp_set_num_threads(rows_A / 2);

    uint64_t cols_A = A[0].size();
    uint64_t cols_B = B[0].size();

    std::vector<std::vector<double>> result(rows_A, std::vector<double>(cols_B, 0));

    #pragma omp parallel
    {
        int T_ID = omp_get_thread_num();
        auto max_threads = omp_get_num_threads();   
        // std::cout << "max threads = " << max_threads << std::endl;
        auto range = rows_A / max_threads;

        // Perform matrix multiplication and scaling
        for (auto i = range * T_ID; i < (T_ID == max_threads - 1 ? rows_A : range * (T_ID + 1)); ++i) {
            for (uint64_t j = 0; j < cols_B; ++j) {
                for (uint64_t l = 0; l < cols_A; ++l) {
                    result[i][j] += A[i][l] * B[l][j];
                }
                result[i][j] *= alpha; // Scale the result by alpha
            }
        }

        // Scale matrix C by beta and add to the result
        #pragma omp barrier

        for (auto i = range * T_ID; i < (T_ID == max_threads - 1 ? rows_A : range * (T_ID + 1)); ++i) {
            for (uint64_t j = 0; j < cols_B; ++j) {
                C[i][j] = beta * C[i][j] + result[i][j];
            }
        }
    }


}

// Standard GEMM formula is:
// C = α⋅A⋅B + β⋅C
// Matrix multiplication function matrix_mult(vec_A, vec_B, vec_C, alpha, beta);
void matrix_mult(const std::vector<std::vector<double>>& A, const std::vector<std::vector<double>>& B, std::vector<std::vector<double>>& C,
const double& alpha, const double& beta) {
    uint64_t rows_A = A.size();
    uint64_t cols_A = A[0].size();

    uint64_t rows_B = B.size();
    uint64_t cols_B = B[0].size();

    uint64_t rows_C = C.size();
    uint64_t cols_C = C[0].size();

    if ((cols_A != rows_B) || (rows_A != rows_C || cols_B != cols_C)) {
        throw std::invalid_argument("Number of columns in A must be equal to number of rows in B");
    }

    std::vector<std::vector<double>> result(rows_A, std::vector<double>(cols_B, 0));

#if ENABLE_BOOST_PRECISION_TIMER
    auto start = std::chrono::high_resolution_clock::now();  // Start timing
#endif

   // Perform matrix multiplication and scaling
    for (uint64_t i = 0; i < rows_A; ++i) {
        for (uint64_t j = 0; j < cols_B; ++j) {
            for (uint64_t l = 0; l < cols_A; ++l) {
                result[i][j] += A[i][l] * B[l][j];
            }
            result[i][j] *= alpha;
        }
    }

    // Scale matrix C by beta and add to the result
    for (uint64_t i = 0; i < rows_A; ++i) {
        for (uint64_t j = 0; j < cols_B; ++j) {
            C[i][j] = beta * C[i][j] + result[i][j];
        }
    }

#if ENABLE_BOOST_PRECISION_TIMER
    auto end = std::chrono::high_resolution_clock::now();  // End timing
    std::chrono::duration<double> elapsed = end - start;  // Calculate elapsed time
    std::cout << "Matrix multiplication took " << elapsed.count() << " seconds.\n";  // Print elapsed time
#endif
}

// Wrapper function to handle Python list inputs and outputs
boost::python::list matrix_mult_py(const boost::python::list& A, const boost::python::list& B, const boost::python::list& C,
const double& alp, const double& be, const unsigned int& optimization_num) {
    std::vector<std::vector<double>> vec_A = py_list_to_vector(A);
    std::vector<std::vector<double>> vec_B = py_list_to_vector(B);
    std::vector<std::vector<double>> vec_C = py_list_to_vector(C);
    
    double alpha = alp;
    double beta = be;

    switch (optimization_num)
    {
        case 0:
        matrix_mult(vec_A, vec_B, vec_C, alpha, beta);
        break;

        case 1: // WIP (Murtaza)
        matrix_mult_threading(vec_A, vec_B, vec_C, alpha, beta);
        break;

        case 2:
        // WIP
        break;

        default:
        throw std::invalid_argument("Choose a correct optimization number");
    }

    
    return vector_to_py_list(vec_C); // vec_C will store the result
}

BOOST_PYTHON_MODULE(matrix_mult) {
    using namespace boost::python;
    def("matrix_mult", matrix_mult_py);
}
