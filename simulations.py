import random
from multiprocessing import Pool, cpu_count


def generate_applicants(count, min_score=1, max_score=10000000):
    lower_bound = random.randint(min_score, max_score - 1)
    upper_bound = random.randint(lower_bound + 1, max_score)
    return [random.randint(lower_bound, upper_bound) for _ in range(count)]


def simulate_single_run(args):
    applicant_count, interview_count, trial_count = args
    success_count = 0
    for _ in range(trial_count):
        applicants = generate_applicants(applicant_count)
        random.shuffle(applicants)
        benchmark = max(applicants[:interview_count])
        for i in range(interview_count, applicant_count):
            if applicants[i] > benchmark:
                if applicants[i] == max(applicants[i:]):
                    success_count += 1
                break
    return interview_count, success_count


def simulate_hiring_strategy(applicant_count, max_interview_count, trial_count, progress_callback=None,
                             should_continue=None):
    results = []
    successes = []

    # Determine the number of processes to use (leave one core free)
    num_processes = max(1, cpu_count() - 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Prepare the arguments for each process
        args = [(applicant_count, i, trial_count) for i in range(1, max_interview_count + 1)]

        # Map the simulation function to the pool of workers
        for i, (interview_count, success_count) in enumerate(pool.imap_unordered(simulate_single_run, args)):
            if should_continue and not should_continue():
                pool.terminate()
                break

            results.append(interview_count / applicant_count)
            successes.append(success_count / trial_count)

            if progress_callback:
                progress_callback((i + 1) / max_interview_count * 100)

    # Sort results and successes based on interview count
    results, successes = zip(*sorted(zip(results, successes)))

    return list(results), list(successes)