import random

def generate_applicants(count, min_score=1, max_score=10000000):
    lower_bound = random.randint(min_score, max_score - 1)
    upper_bound = random.randint(lower_bound + 1, max_score)
    return [random.randint(lower_bound, upper_bound) for _ in range(count)]

def simulate_hiring_strategy(applicant_count, interview_count, trial_count):
    if interview_count >= applicant_count:
        return 0  # Can't hire anyone if we interviewed everyone
    successes = 0
    for _ in range(trial_count):
        applicants = generate_applicants(applicant_count)
        random.shuffle(applicants)
        benchmark = max(applicants[:interview_count])
        if benchmark >= max(applicants[interview_count:]):
            successes += 1
    return successes / trial_count

# Example usage
applicant_count = 100
interview_count = 50
trial_count = 10000

success_rate = simulate_hiring_strategy(applicant_count, interview_count, trial_count)
print(f"Success rate after {trial_count} trials: {success_rate:.4f}")