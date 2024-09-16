import random

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


def has_no_duplicate(the_list):
  seen = set()
  for x in the_list:
    if x in seen: return False
    seen.add(x)
  return True

my_test = create_applicants(100)
print(my_test)
print(has_no_duplicate(my_test))