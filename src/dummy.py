import numpy as np

from tabulate import tabulate
years = list(range(2014, 2026))
classes = ["20-29","30-39", "40-49", "50-59"]

# Create dataset
data = []
for year in years:
    for age_class in classes:
        value = round(np.random.random(), 2)  # random float between 0 and 1
        data.append({"Year": year, "Class": age_class, "Value": value})
print(tabulate(data ))