// matrix_mult.cpp
#include <boost/python.hpp>
#include <vector>
#include <chrono>
#include <iostream>

// Convert Python list to std::vector
std::vector<std::vector<int>> py_list_to_vector(const boost::python::list& py_list) {
    std::vector<std::vector<int>> vec;
    for (int i = 0; i < boost::python::len(py_list); ++i) {
        boost::python::list sublist = boost::python::extract<boost::python::list>(py_list[i]);
        std::vector<int> subvec;
        for (int j = 0; j < boost::python::len(sublist); ++j) {
            subvec.push_back(boost::python::extract<int>(sublist[j]));
        }
        vec.push_back(subvec);
    }
    return vec;
}

// Convert std::vector to Python list
boost::python::list vector_to_py_list(const std::vector<std::vector<int>>& vec) {
    boost::python::list py_list;
    for (const auto& subvec : vec) {
        boost::python::list sublist;
        for (int val : subvec) {
            sublist.append(val);
        }
        py_list.append(sublist);
    }
    return py_list;
}

// Matrix multiplication function
std::vector<std::vector<int>> matrix_mult(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B) {
    size_t rows_A = A.size();
    size_t cols_A = A[0].size();
    size_t rows_B = B.size();
    size_t cols_B = B[0].size();

    if (cols_A != rows_B) {
        throw std::invalid_argument("Number of columns in A must be equal to number of rows in B");
    }

    std::vector<std::vector<int>> result(rows_A, std::vector<int>(cols_B, 0));

    // auto start = std::chrono::high_resolution_clock::now();  // Start timing

    for (size_t i = 0; i < rows_A; ++i) {
        for (size_t j = 0; j < cols_B; ++j) {
            for (size_t k = 0; k < cols_A; ++k) {
                result[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    // auto end = std::chrono::high_resolution_clock::now();  // End timing
    // std::chrono::duration<double> elapsed = end - start;  // Calculate elapsed time
    // std::cout << "Matrix multiplication took " << elapsed.count() << " seconds.\n";  // Print elapsed time

    return result;
}

// Wrapper function to handle Python list inputs and outputs
boost::python::list matrix_mult_py(const boost::python::list& A, const boost::python::list& B) {
    std::vector<std::vector<int>> vec_A = py_list_to_vector(A);
    std::vector<std::vector<int>> vec_B = py_list_to_vector(B);
    std::vector<std::vector<int>> result = matrix_mult(vec_A, vec_B);
    return vector_to_py_list(result);
}

BOOST_PYTHON_MODULE(matrix_mult) {
    using namespace boost::python;
    def("matrix_mult", matrix_mult_py);
}
