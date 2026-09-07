import pandas as pd

data = {
    "Project Name": [
        "Road Construction",
        "Water Supply Project",
        "Community Hall"
    ],
    "District": [
        "Haridwar",
        "Dehradun",
        "Nainital"
    ],
    "Sanctioned Amount": [
        1000000,
        2500000,
        1500000
    ],
    "Status": [
        "Ongoing",
        "Completed",
        "Ongoing"
    ]
}

df = pd.DataFrame(data)

df.to_excel("data/raw/sample_projects.xlsx", index=False)

print("Excel file created successfully!")