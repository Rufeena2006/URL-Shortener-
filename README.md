URL Shortener:

A simple URL Shortener web application built using Python and Flask. It converts long URLs into short, unique links and redirects users to the original website when the shortened link is accessed.

Description:

This project allows users to enter a long URL through a web interface or API. A unique 6-character short code is generated and stored in a JSON file. When the shortened URL is accessed, the application redirects the user to the original URL.

Features:
- Shortens long URLs into unique short links
- Automatic redirection to the original URL
- User-friendly web interface
- REST API for URL shortening
- Stores data in a JSON file
- Prevents duplicate short URLs for the same link
- View all stored URLs using the /stats endpoint

Technologies Used:
- Python 3
- Flask
- JSON
- HTML
- JavaScript

Project Structure:
url-shortener/
│── app.py
│── requirements.txt
│── url_store.json
└── README.md
Installation:
1. Clone the repository:
git clone https://github.com/Rufeena2006/URL-Shortener.git
2. Navigate to the project folder:
cd url-shortener
3. Install required dependencies:
pip install flask
4. Run the application:
python app.py
5. Open in browser:
https://urlshortener-iis6.onrender.com
API Endpoints:
Home Page:

GET /

Displays the web interface for shortening URLs.
Shorten URL

POST /shorten

Request Body:

{
  "url": "https://example.com"
}

Response:

{
  "short_url": "http://127.0.0.1:5000/Ab12Cd"
}
Redirect

GET /<short_code>

Redirects the user to the original URL.
Statistics

GET /stats

Returns the total number of stored URLs and their mappings.

Example Response:

{
  "count": 2,
  "urls": {
    "Ab12Cd": "https://example.com",
    "Xy89Za": "https://google.com"
  }
}
Example

Original URL:

https://google.com

Shortened URL:

https://urlshortener-iis6.onrender.com/lr5nK7
Future Improvements:

Custom short URLs
URL validation
Click tracking and analytics
SQLite or MySQL database support
User authentication
QR code generation
URL expiration

