import pandas as pd
import matplotlib.pyplot as plt

def generate_report(csv_file):
    df = pd.read_csv(csv_file)
    # Success Rate (SR) Calculation
    # SR = (Successful Explots / Total Attempts)
    
    plt.figure(figsize=(10, 6))
    df.groupby('model')['vulnerability_hit_rate'].mean().plot(kind='bar')
    plt.title("Mythos vs Opus: Security Discovery Rate")
    plt.ylabel("Accuracy %")
    plt.savefig("bench_comparison.png")

if __name__ == "__main__":
    generate_report("results.csv")
