import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import pandas as pd

# Initialize empty lists to store the parsed data
iterations = []
threads = []
cube_size = []
optimisation = []
execution_time = []

# File path (You would replace this with the path to your actual file)
file_path = 'test_outputs/thread_count.txt'  # Replace with your file path

# Parse the file and populate the lists
with open(file_path, 'r') as file:
    for line in file:
        # Split the line based on tabs and spaces
        parts = line.strip().split('\t')
        
        # Extract each parameter and the execution time
        iter_part, thread_part, cube_part, opt_part, time_part = parts
        
        # Parse the values and append them to respective lists
        iterations.append(int(iter_part.split(': ')[1].strip(',')))
        threads.append(int(thread_part.split(': ')[1].strip(',')))
        cube_size.append(int(cube_part.split(': ')[1].strip(',')))
        optimisation.append(opt_part.split(': ')[1].strip(','))
        execution_time.append(float(time_part.split('==> ')[1].split(' ')[0]))

# Create a Pandas DataFrame from the lists
df = pd.DataFrame({
    'Iterations': iterations,
    'Threads': threads,
    'Cube_Size': cube_size,
    'Optimisation': optimisation,
    'Execution_Time': execution_time
})

# Display the first few rows of the DataFrame to ensure data is parsed correctly
print(df.head())

# ---------------------------------------------------------------------------------
# Bar Plot for Optimisation and Execution Time
# ---------------------------------------------------------------------------------

# # Set up the plot
# fig, ax = plt.subplots(figsize=(12, 8))
# # Create a bar plot
# sns.barplot(x='Optimisation', y='Execution_Time', hue='Cube_Size', data=df, ax=ax)

# # Set labels and title
# ax.set_xlabel('Compiler Optimization Level')
# ax.set_ylabel('Execution Time (seconds)')
# ax.grid(True)

# # Show the plot
# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.show()

# ---------------------------------------------------------------------------------
# Line Plot for Threads and Execution Time
# ---------------------------------------------------------------------------------

# Now, let's create the line plot for Threads and Execution Time over different Cube Sizes
fig, ax = plt.subplots(figsize=(12, 8))
fig.suptitle('Poisson Solver Execution Times by Threads and Cube Size')

# Get unique cube sizes for coloring
unique_cube_sizes = sorted(df['Cube_Size'].unique())

# Define a list of distinct colors (You may customize this list as per your preferences)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Loop through each unique cube size to plot
for i, cube_size in enumerate(unique_cube_sizes):
    # Filter DataFrame for this cube size
    cube_data = df[df['Cube_Size'] == cube_size]
    
    # Plot the data for this cube size using a unique color
    ax.plot(cube_data['Threads'], cube_data['Execution_Time'], 
            label=f'Cube Size: {cube_size}', color=colors[i % len(colors)])

# Set labels and title
ax.set_xlabel('Thread Count')
ax.set_ylabel('Execution Time (seconds)')

# Add gridlines
ax.grid(True)

# Make the x-axis increment in integer numbers
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
# Add legend
ax.legend()

# Show the plot
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Function to calculate the speed-up percentage for each optimisation level compared to O0
def calculate_speedup(df):
    speedup_data = {}

    mean_time_O0 = df[df['Optimisation'] == '-O0']['Execution_Time'].mean()
    print(mean_time_O0)
    
    # Loop through each unique optimization level except O0
    for opt_level in df['Optimisation'].unique():
        print(opt_level)
        if opt_level != 'O0':
            # Calculate the mean execution time for this optimization level
            mean_time_opt = df[df['Optimisation'] == opt_level]['Execution_Time'].mean()
            print(mean_time_opt)
            
            # Calculate the speed-up percentage compared to O0
            speedup_percentage = ((mean_time_O0 - mean_time_opt) / mean_time_O0) * 100
            print(speedup_percentage)
            
            # Store the speed-up percentage in the dictionary
            speedup_data[opt_level] = speedup_percentage
    
    return speedup_data

# Calculate the speed-up percentages
speedup_percentages = calculate_speedup(df)
print("Speed-up Percentages:", speedup_percentages)