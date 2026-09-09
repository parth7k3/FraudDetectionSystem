import pandas as pd


data = {
    "Project ID": [
        "P001",
        "P002",
        "P003"
    ],

    "Project Name": [
        "Road Construction",
        "Water Supply Project",
        "Community Hall"
    ],

    "District": [
        "Haridwar",
        "Nainital",
        "Dehradun"
    ],

    "State": [
        "Uttarakhand",
        "Uttarakhand",
        "Uttarakhand"
    ],

    "Sanctioned Amount": [
        "₹ 10,00,000",
        "25 lakh",
        "₹1,500,000"
    ],

    "Amount Released": [
        "₹ 8,00,000",
        "20 lakh",
        "₹1,500,000"
    ],

    "Amount Spent": [
        "₹ 7,50,000",
        "18 lakh",
        "₹1,400,000"
    ],

    "Status": [
        "ONGOING",
        "Completed",
        "Completed"
    ],

    "Start Date": [
        "15/01/2025",
        "2025/03/10",
        "01-06-2024"
    ],

    "Expected Completion Date": [
        "15-01-2026",
        "10 Aug 2025",
        "June 1 2025"
    ],

    "Actual Completion Date": [
        "",
        "08/08/2025",
        "2025-05-28"
    ],

    "Completion Percentage": [
        75,
        100,
        95
    ]
}


df = pd.DataFrame(data)


df.to_csv(
    "data/raw/sample_projects.csv",
    index=False
)


print("Test CSV created successfully!")