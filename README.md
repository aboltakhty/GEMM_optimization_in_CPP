# GEMM_optimization_in_CPP

1) Python: Initialize the matrices with a constant seed (4x4, 8x8, 16x16, and so on) and alpha beta constants just like gemm
2) Python: Start the timer and pass these values and matrices to C++ code
3) C++: Do the multiplication just like with and without optimiation (finally if it possible add openmp)
4) Python: Stop the timer and store the time value
---

# How to Run the Project

## Step 1: Create a Virtual Environment

Create a virtual environment using this command:

```bash
python3 -m venv env
```

## Step 2: Activate the Virtual Environment
Activate the environment:

On Unix:

```bash
source env/bin/activate
```

## Step 3: Install the Python dependencies

Run the following command to install the python dependencies for the project:

```bash
pip install -r requirements.txt
```

## Step 4: Build the Project

Run the following command to build the project in place:

```bash
python3 setup.py build_ext --inplace
```

## Step 5: Run the Main Script

If everything is set up correctly, you can run the main script with the default values by executing:

```bash
python3 main.py
```

To customize the parameters, you can use the following command:

```bash
python3 main.py --matrix_size=4 --optimization_num=0 --alpha=1.5 --beta=1.2 --random_seed=42
```

Troubleshooting
If you encounter any errors, you might need to install additional dependencies. Use the following commands:

```bash
sudo apt-get install libboost-python-dev
sudo apt-get install python3-all-dev
```

## Checking Boost Python Version

In setup.py, the boost_python310 module is specified. To check the Boost version on your computer and ensure compatibility, use this command:

```bash
find /usr/lib /usr/local/lib -name "libboost_python*.so"
```
If the Boost version does not match, install the required version.
