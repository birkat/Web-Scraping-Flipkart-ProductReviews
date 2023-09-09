Web Scraping Flipkart Product Reviews

Overview
This Flask web application allows users to search for a product on Flipkart and scrape its reviews. It provides an interface where users can enter a search term, and it fetches the reviews for the top result from Flipkart.

Features
Search for Products: Users can enter a product name or search term in the provided input field.

Web Scraping: The application uses web scraping techniques to extract product reviews from Flipkart's website. It navigates through the pages of reviews to gather a comprehensive dataset.

Pagination Support: It supports navigating through multiple pages of reviews, providing a more extensive set of data.

Export to CSV: The scraped reviews are saved to a CSV file, making it easy to analyze the data later.

How it Works
Users enter a product name or search term and submit the form.

The application constructs a URL to search for the product on Flipkart and sends a request to Flipkart's website.

It parses the Flipkart search results page to find the link to the top product.

It follows the link to the product's page and extracts the review URLs for that product.

The application then iterates through the review pages, scraping customer names, ratings, review headings, and comments.

The scraped data is stored in a CSV file named after the search term for further analysis.

Prerequisites:
Python
Flask
BeautifulSoup
Requests
Flask-CORS

Usage:
Clone the repository.
Install the required libraries using pip install flask beautifulsoup4 requests flask-cors.
Run the Flask application using python app.py.
Access the web application in your browser.

Contributions
Contributions to this project are welcome. If you have ideas for improvements or bug fixes, feel free to open an issue or submit a pull request.