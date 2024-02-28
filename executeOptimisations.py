import subprocess
import time

# optimization_flags  = ["-O0", "-O1", "-O2", "-O3", "-Ofast"]
optimization_flags  = ["-O3"]
domain_sizes        = [301, 501, 701]
threads             = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
iterations          = [100]

# Function to compile and execute the program using the Makefile and return the execution time
def execute_program(threads, iterations, n, opt):
    # Measure the execution time
    compile_process = subprocess.Popen(["cc", "-g", "-pthread", "-fopenmp", opt, "poisson.c", "-o", "poisson"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    compile_process.communicate()

    start_time = time.time()
    execution_process = subprocess.Popen(["./poisson", "-t", str(threads), "-i", str(iterations), "-n", str(n)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Replace "your_executable" with the actual name of the executable
    execution_process.communicate()
    end_time = time.time()

    # Calculate the execution time in seconds
    execution_time = end_time - start_time

    return execution_time

# Perform multiple executions and save the execution times to a text file
file_path = "test_outputs/thread_count.txt"
with open(file_path, "w") as file:
    for iteration in iterations:
        for n in domain_sizes:
            for opt in optimization_flags:
                for thread in threads:
                    execution_time = execute_program(thread, iteration, n, opt)
                    output_str = f"i: {iteration},\tt: {thread},\tn: {n},\topt: {opt}\t==> {execution_time:010.6f} seconds"
                    print(output_str)
                    file.write(output_str + '\n')

print("Execution times have been saved to " + "file_path" + ".")