import random
import matplotlib.pyplot as plt
from asciimatics.screen import Screen

def create_applicants(num_applicants):
    parent_min = 1
    parent_max = 10000000
    
    # Randomly select a sub-range from the parent range
    min_value = random.randint(parent_min, parent_max - 1)
    max_value = random.randint(min_value + 1, parent_max)
    
    applicants = []
    for _ in range(num_applicants):
        applicants.append(random.randint(min_value, max_value))
    
    return applicants

def display_graph_cli(screen, applicants, picked_applicant_index, first_x):
    max_value = max(applicants)
    screen.clear()
    
    for i, value in enumerate(applicants):
        color = Screen.COLOUR_BLUE
        if i == picked_applicant_index:
            color = Screen.COLOUR_RED
        elif i == applicants.index(max_value):
            color = Screen.COLOUR_GREEN
        elif i < first_x:
            color = Screen.COLOUR_WHITE
        
        screen.print_at('█' * (value * screen.width // max_value), 0, i, colour=color)
    
    # Draw a line at the median of the first x applicants
    median_value = sorted(applicants[:first_x])[first_x // 2]
    median_line = '─' * (median_value * screen.width // max_value)
    screen.print_at(median_line, 0, first_x, colour=Screen.COLOUR_WHITE)
    
    screen.refresh()
    screen.wait_for_input(10)

def display_graph_gui(applicants, picked_applicant_index, first_x):
    plt.figure(figsize=(10, 6))
    
    # Plot all applicants
    plt.plot(applicants, color='blue', label='Applicants')
    
    # Highlight the highest score in green
    max_index = applicants.index(max(applicants))
    plt.plot(max_index, applicants[max_index], 'go', label='Highest Score')
    
    # Highlight the picked applicant in red
    plt.plot(picked_applicant_index, applicants[picked_applicant_index], 'ro', label='Picked Applicant')
    
    # Highlight the first x applicants in lighter gray
    plt.plot(range(first_x), applicants[:first_x], color='lightgray', label='First X Applicants')
    
    # Draw a line at the median of the first x applicants
    median_value = sorted(applicants[:first_x])[first_x // 2]
    plt.plot([0, first_x-1], [median_value, median_value], color='gray', linestyle='--', label='Median of First X')
    
    plt.ylabel('Applicant Score')
    plt.xlabel('Applicant Number')
    plt.legend()
    plt.savefig('applicants_plot.png')
    print("Plot saved as 'applicants_plot.png'")

def display_graph(applicants, picked_applicant_index, first_x, mode='gui'):
    if mode == 'cli':
        Screen.wrapper(display_graph_cli, arguments=[applicants, picked_applicant_index, first_x])
    elif mode == 'gui':
        display_graph_gui(applicants, picked_applicant_index, first_x)
    else:
        raise ValueError("Invalid mode. Choose 'cli' or 'gui'.")

def find_best_applicant(applicants, first_x):
    best_so_far = max(applicants[:first_x])
    for i in range(first_x, len(applicants)):
        if applicants[i] > best_so_far:
            return i
    return -1  # If no better applicant is found

# Example usage
applicants = create_applicants(20)
first_x = 3  # Adjust this value to change the number of scores used to calculate the median
best_applicant_index = find_best_applicant(applicants, first_x)
display_graph(applicants, picked_applicant_index=best_applicant_index, first_x=first_x, mode='gui')  # For GUI output
# display_graph(applicants, picked_applicant_index=best_applicant_index, first_x=first_x, mode='cli')  # For CLI output