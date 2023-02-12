# linkedin\_jobs\_scraper

## User Guide for LinkedIn Job Scraper

### Introduction

This code is a web scraper built using the Selenium library in Python to extract job details from LinkedIn. The code logs into your LinkedIn account and goes to a specified job search results page to scrape information about the jobs posted there. The data is then saved to a Pandas data frame and can be used for further analysis.

### Requirements

* A LinkedIn account with a valid email and password.
* Google Chrome browser installed on your computer.
* ChromeDriver installed and added to your PATH. The version of ChromeDriver must match the version of your installed Google Chrome browser.
* Python 3 and the following packages installed:
  * Selenium
  * Pandas
  * Time

### Usage

1. Update the file 'user\_credentials.txt' with your LinkedIn email and password, each separated by a newline.
2. Download the appropriate version of ChromeDriver for your installed Google Chrome browser and place it in the same directory as the code.
3. Replace the value of the `executable_link` variable with the link to the LinkedIn job search results page you want to scrape.
4. Run the code using Python 3.

### Output

The code will produce a Pandas data frame with the following columns:

* Job Title
* Company Name
* Company Location
* Work Method
* Post Date
* Work Time
* Job Description

The data frame will be saved as a CSV file named 'LinkedIn\_Jobs.csv' in the same directory as the code. The job Descriptions will be saved as a .txt file.&#x20;

### Notes

* The code is set to scrape job details from pages 2 to 14 of the specified LinkedIn job search results page. You can modify the `range(2, 14)` value to change the number of pages you want to scrape.
* If the LinkedIn job posting doesn't have information for any of the columns, it will be left empty in the data frame.
* The code may not work as expected if LinkedIn makes changes to the structure of their job postings pages. In this case, the XPath selectors in the code may need to be updated.
