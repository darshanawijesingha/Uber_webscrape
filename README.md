# 🛒 Uber Grocery Web Scraper for Power BI Integration

This project is a web scraping automation tool built using **Python** and **BeautifulSoup** to extract grocery product data from the **Uber Eats** platform. It is designed to **run in a Chrome browser**, scroll dynamically, and collect relevant product data, which can be **connected to Power BI** for real-time dashboard updates.

---

## 🚀 Features

- Scrapes live data from Uber Grocery stores
- Opens Chrome and scrolls down to dynamically load all items
- Extracts product details such as:
  - Product Name
  - Price
- Cleanly formats scraped data for analysis
- Easily refreshable by Power BI with scheduled scraping

---

## 🧰 Technologies Used

- `Python 3.x`
- `BeautifulSoup` (for HTML parsing)
- `pandas` (for data formatting and export)
- `ChromeDriver` (for browser automation)
- `Power BI` (for data visualization)

---

## ⚙️ How It Works

1. Launches **Chrome** using `webdriver.Chrome`.
2. Navigates to the specified **Uber Grocery Store** URL.
3. Scrolls down slowly to ensure all items are loaded.
4. Parses the DOM with **BeautifulSoup**.
5. Extracts:
   - Item names
   - Prices
   - Stock status (blank, 0, or 1)
6. Saves data to a **CSV or Excel** file.
7. Power BI reads the output file and updates visuals on refresh (2–3 minutes per run).

---


