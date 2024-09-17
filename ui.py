import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading


class SimulationUI:
    def __init__(self, master, simulation_func):
        self.master = master
        self.simulation_func = simulation_func
        master.title("Parallel Hiring Strategy Simulation")
        self.running = False
        self.create_widgets()

    def create_widgets(self):
        # Input fields
        ttk.Label(self.master, text="Number of Applicants:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.applicant_entry = ttk.Entry(self.master)
        self.applicant_entry.grid(row=0, column=1, padx=5, pady=5)
        self.applicant_entry.insert(0, "100")

        ttk.Label(self.master, text="Max Interviews:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.interview_entry = ttk.Entry(self.master)
        self.interview_entry.grid(row=1, column=1, padx=5, pady=5)
        self.interview_entry.insert(0, "50")

        ttk.Label(self.master, text="Number of Trials:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.trial_entry = ttk.Entry(self.master)
        self.trial_entry.grid(row=2, column=1, padx=5, pady=5)
        self.trial_entry.insert(0, "10000")

        # Run button
        self.run_button = ttk.Button(self.master, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=3, column=0, pady=10)

        # Stop button
        self.stop_button = ttk.Button(self.master, text="Stop Simulation", command=self.stop_simulation,
                                      state=tk.DISABLED)
        self.stop_button.grid(row=3, column=1, pady=10)

        # Result display
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(self.master, textvariable=self.result_var)
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Graph
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.master, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=6, column=0, columnspan=2, sticky="we", padx=10, pady=5)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.master.update_idletasks()

    def run_simulation(self):
        self.running = True
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        thread = threading.Thread(target=self._run_simulation)
        thread.start()

    def _run_simulation(self):
        try:
            applicant_count = int(self.applicant_entry.get())
            max_interview_count = int(self.interview_entry.get())
            trial_count = int(self.trial_entry.get())

            self.progress_var.set(0)
            self.result_var.set("Running parallel simulation...")

            pool_sizes, success_rates = self.simulation_func(
                applicant_count,
                max_interview_count,
                trial_count,
                self.update_progress,
                lambda: self.running
            )

            if self.running:
                self.update_graph(pool_sizes, success_rates, max_interview_count)
            else:
                self.result_var.set("Simulation stopped.")
        except ValueError:
            self.result_var.set("Please enter valid numbers")
        finally:
            self.progress_var.set(0)
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.running = False

    def update_graph(self, pool_sizes, success_rates, max_interview_count):
        self.plot.clear()
        x = range(1, len(pool_sizes) + 1)

        # Convert ratios to percentages
        pool_sizes_percent = [size * 100 for size in pool_sizes]
        success_rates_percent = [rate * 100 for rate in success_rates]

        self.plot.bar(x, pool_sizes_percent, color='gray', alpha=0.5, label='Pool Size (%)')
        self.plot.bar(x, success_rates_percent, color='green', alpha=0.5, label='Success Rate (%)')
        self.plot.set_xlabel('Number of Interviews')
        self.plot.set_ylabel('Percentage')
        self.plot.set_title('Parallel Hiring Strategy Simulation Results')
        self.plot.legend()
        self.plot.set_xlim(0, max_interview_count + 1)
        self.plot.set_ylim(0, 100)  # Set y-axis limit to 100%

        # Add percentage signs to y-axis ticks
        self.plot.yaxis.set_major_formatter(lambda x, p: f"{x:.0f}%")

        self.canvas.draw()

        max_prob = max(success_rates)
        best_interview_count = success_rates.index(max_prob) + 1
        self.result_var.set(
            f"Best strategy: Interview {best_interview_count} applicants. Max probability: {max_prob:.2%}")

    def stop_simulation(self):
        self.running = False
        self.result_var.set("Stopping simulation...")