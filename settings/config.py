import os

## App settings
name = "Married Women\'s Economic Rights Reform, 1835-1920"

host = "0.0.0.0"

port = int(os.environ.get("PORT", 5000))

debug = False

contacts = "https://www.linkedin.com/in/aaron-stopher/"

code = "https://github.com/aastopher"

fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

## File system
root = os.path.dirname(os.path.dirname(__file__)) + "/"