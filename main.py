import random
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

def display_graph(screen, applicants, picked_applicant_index, first_x):
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

# Example usage
applicants = create_applicants(20)
Screen.wrapper(display_graph, arguments=[applicants, 10, 5])