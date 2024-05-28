from setuptools import setup, Extension

boost_python_include = '/usr/include'  # Adjust path to your Boost.Python include directory
boost_python_lib = '/usr/lib'  # Adjust path to your Boost.Python library directory

module = Extension(
    'matrix_mult',
    sources=['matrix_mult.cpp'],
    include_dirs=[boost_python_include],
    library_dirs=[boost_python_lib],
    libraries=['boost_python310'],  # Adjust depending on your Python version
    extra_compile_args=['-Wno-deprecated-declarations'],  # Add this line to suppress deprecation warnings
)

setup(
    name='matrix_mult',
    version='1.0',
    ext_modules=[module],
)
