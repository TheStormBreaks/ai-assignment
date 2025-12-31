import pandas as pd

# ---------------------------------
# 1. Create a dataset
# ---------------------------------
data = {
    "ID": [1, 2, 3, 4, 5],
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "Age": [20, 21, 19, 22, 20],
    "Department": ["CSE", "ECE", "CSE", "ME", "ECE"],
    "Marks": [85, 78, 92, 74, 88]
}

# ---------------------------------
# 2. Build DataFrame
# ---------------------------------
df = pd.DataFrame(data)

# ---------------------------------
# Save dataset as CSV file
# ---------------------------------
df.to_csv("sample_dataset.csv", index=False)
print("Dataset saved as sample_dataset.csv\n")

# ---------------------------------
# 3. Display few entries in dataset
# ---------------------------------
print("First 3 entries of dataset:")
print(df.head(3), "\n")

# ---------------------------------
# 4. Slicing the dataset
# ---------------------------------
print("Slicing rows 1 to 3 and columns Name, Age:")
print(df.loc[1:3, ["Name", "Age"]], "\n")

# ---------------------------------
# 5. Dropping rows and columns
# ---------------------------------
# Drop a row
df_drop_row = df.drop(2)
print("Dataset after dropping row with index 2:")
print(df_drop_row, "\n")

# Drop a column
df_drop_col = df.drop(columns=["Marks"])
print("Dataset after dropping 'Marks' column:")
print(df_drop_col, "\n")

# ---------------------------------
# 6. Getting summary of dataset
# ---------------------------------
print("Summary of dataset:")
print(df.describe(), "\n")

# ---------------------------------
# 7. Finding dimension of dataset
# ---------------------------------
print("Dataset Dimensions (Rows, Columns):", df.shape)
