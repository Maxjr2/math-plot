import tkinter as tk
from simulations import simulate_hiring_strategy
from ui import SimulationUI

def main():
    root = tk.Tk()
    root.geometry("800x800")  # Increased window size for the larger graph
    app = SimulationUI(root, simulate_hiring_strategy)
    root.mainloop()

if __name__ == "__main__":
    main()