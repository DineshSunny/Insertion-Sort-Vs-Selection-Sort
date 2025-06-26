# plotting_utils.py

import matplotlib.pyplot as plt
import os

def generate_box_plot(data_lists, labels, title, save_path, y_label="Runtime (ms)"):
    plt.figure(figsize=(10, 6))
    plt.boxplot(data_lists, labels=labels, patch_artist=True)
    plt.title(title)
    plt.ylabel(y_label)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"[✔] Box plot saved to: {save_path}")

def generate_all_plots(selection_data, insertion_data, metric_names, output_dir="plots"):
    os.makedirs(output_dir, exist_ok=True)

    for i, metric in enumerate(metric_names):
        sel_metric = selection_data[i]
        ins_metric = insertion_data[i]
        save_path = os.path.join(output_dir, f"{metric.lower().replace(' ', '_')}_boxplot.png")
        generate_box_plot(
            [sel_metric, ins_metric],
            labels=["Selection Sort", "Insertion Sort"],
            title=f"{metric} Comparison",
            save_path=save_path,
            y_label=metric
        )
