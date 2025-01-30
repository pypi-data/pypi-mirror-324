def p1():
  #DataFrame
  ## ## 1. Create a data frame “df_emp” with a minimum of 10 records of employee displaying employee id, employee name, salary, designation.
  code='''
import pandas as pd

data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
df = pd.DataFrame(data)

# Store the data in a text file (e.g., CSV)
file_path = 'output.txt'  
df.to_csv(file_path, index=False, sep='\t')  

# Read data from text file
df_loaded = pd.read_csv(file_path, sep='\t')

# Print the loaded data
df_loaded
  '''
  print(code)





def p2():
  code = '''
import requests

def get_weather(api_key, location, units="metric"):
  url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}"
  response = requests.get(url).json()
  print(response)
  return {
      "location": response.get('name', 'Unknown Location'),
      "visibility": response.get('visibility'),
      "weather_type": response.get('weather', [{}])[0].get('main', {})
  }


api_key = 'b811a4b25c6c7f5a2f1845e793524bc7'
location = "mumbai"

get_weather(api_key, location)


# prac 2b
import requests
from bs4 import BeautifulSoup

# function to scrape a webpage
def scrape_website(url):
  response = requests.get(url)
  if response.status_code != 200:
    return f"failed to retrieve page: status code: {response.status_code}"

  soup = BeautifulSoup(response.content,"html.parser")
  tags = soup.find_all("h3")
  return [tag.get_text().strip() for tag in tags]

url = "https://www.scrapethissite.com/pages/"

content = scrape_website(url)
print(content)
'''
  print(code)



def p3():
  code = '''
import pandas as pd
import numpy as np
# Step 1: Load the dataset
file_path = "/content/data_cleaning_demo.csv" 
df = pd.read_csv(file_path)
print("Original Data:")
print(df)
# Step 2: Handle missing values
df['Age'].fillna(df['Age'].mean(), inplace=True) # Fill missing Age with mean
df['Email'].fillna("unknown@example.com", inplace=True) # Fill missing Email
df.dropna(subset=['Name'], inplace=True) # Drop rows with missing Name
# Step 3: Remove duplicates
df.drop_duplicates(inplace=True)
# Step 4: Convert data types
df['Joining_Date'] = pd.to_datetime(df['Joining_Date'], errors='coerce') # Convert to datetime
# Step 5: Rename columns
df.rename(columns={'Salary': 'Annual_Salary'}, inplace=True)
# Step 6: Filter data (e.g., keep rows with Age > 20)
df = df[df['Age'] > 20]
# Step 7: Export cleaned data
output_file = "cleaned_data.csv"
df.to_csv(output_file, index=False)
print("\nCleaned Data:")
print(df)
print(f"\nCleaned data saved to {output_file}")
'''
  print(code)


def p4():
  codes='''
import pandas as pd
import numpy as np
import os
data = {
"Transaction_ID": [1, 2, 3, 4, 5],
"Product": ["A", "B", "C", "A", "B"],
"Quantity": [10, -5, 20, 15, 8],
"Price": [15.0, 20.0, 25.0, None, 30.0],
"Date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
}
df = pd.DataFrame(data)
print(f"Task 1: Loaded Dataset\n{df.head()}")
missing_cols = df.columns[df.isnull().any()]
df.fillna(0, inplace=True)
print(f"\nTask 2: Missing Values - After Handling\n{df}")
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].abs()
print(f"\nTask 3: Negative Values - After Handling\n{df}")
df["Date"] = pd.to_datetime(df["Date"])
print(f"\nTask 4: Converted 'Date' column to DateTime format\n{df}")
df["Day"] = df["Date"].dt.day
df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year
print(f"\nTask 5: Extracted day, month, and year information from 'Date'\n{df}")
df["Total Sales"] = df["Quantity"] * df["Price"]
print(f"\nTask 6: Calculated 'Total Sales'\n{df}")
grouped_df = (df.groupby("Product").agg({"Quantity": "sum", "Total Sales": "sum"}).reset_index())
print(f"\nTask 7: Grouped and Aggregated Data by 'Product'\n {grouped_df}")
wrangled_file_path = os.path.abspath("wrangled_dataset.csv")
df.to_csv(wrangled_file_path, index=False)
print("\nTask 8: Saved the wrangled Dataset to ", wrangled_file_path)
transformed_file_path =os.path.abspath("transformed_dataset.csv")
df.to_csv(transformed_file_path, index=False)
print("\nTask 9: Saved the Transformed Dataset to ", transformed_file_path)
transposed_df = df.transpose()
transposed_file_path = os.path.abspath("transposed_dataset.csv")
  '''
  print(codes)



def p5():
  codes='''
import pandas as pd
import numpy as np
# Step 1: Load the dataset
file_path = "/content/data_cleaning_demo.csv" 
df = pd.read_csv(file_path)
print("Original Data:")
print(df)
# Step 2: Handle missing data
# Drop rows with missing 'Name'
df.dropna(subset=['Name'], inplace=True)
# Fill missing 'Email' with a placeholder
df['Email'].fillna("noemail@example.com", inplace=True)
# Step 3: String Manipulation
# Strip whitespace from 'Name' column
df['Name'] = df['Name'].str.strip()
# Convert 'Name' to title case
df['Name'] = df['Name'].str.title()
# Extract domain from 'Email'
df['Email_Domain'] = df['Email'].str.extract(r'@([a-zA-Z0-9.-]+)')
# Replace missing 'Joining_Date' with today's date
df['Joining_Date'].fillna(pd.Timestamp.today().strftime('%Y-%m-%d'), inplace=True)
# Step 4: Export cleaned data
output_file = "cleaned_data_with_strings.csv"
df.to_csv(output_file, index=False)
print("\nCleaned Data:")
print(df)
print(f"\nCleaned data saved to {output_file}")
'''

  print(codes)



