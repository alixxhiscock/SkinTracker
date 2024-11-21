from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the target webpage
url = "https://hypixel-skyblock.fandom.com/wiki/Fire_Sale#2023"
driver.get(url)

# Wait for the page to load (adjust as needed)
time.sleep(5)  # Wait for initial page load (you might need to wait longer if the page is slow)

# Print page source to help debug
print(driver.page_source)

# Find all <tr> elements where the id ends with "_Skin"
tr_elements = driver.find_elements(By.XPATH, "//*[contains(@id, '_Skin')]")

# Initialize the variable to store the current year
current_year = None

# Extract data from each matching <tr>
for tr in tr_elements:
    # Use a more direct way of accessing each column
    year_column = tr.find_elements(By.XPATH, ".//td[1]")  # Year is in the first column
    skin_name = tr.find_elements(By.XPATH, ".//td[2]")  # Skin Name is in the second column
    release_date = tr.find_elements(By.XPATH, ".//td[3]")  # Release Date is in the third column
    quantity = tr.find_elements(By.XPATH, ".//td[4]")  # Quantity is in the fourth column

    # Check if these elements are found and extract their text
    year_text = year_column[0].text.strip() if year_column else "N/A"
    skin_name_text = skin_name[0].text.strip() if skin_name else "N/A"
    release_date_text = release_date[0].text.strip() if release_date else "N/A"
    quantity_text = quantity[0].text.strip() if quantity else "N/A"

    # Print or store the extracted data
    print(f"Year: {year_text}, Skin Name: {skin_name_text}, Release Date: {release_date_text}, Quantity: {quantity_text}")

# Close the browser after scraping
driver.quit()
