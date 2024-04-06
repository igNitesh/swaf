from flask import Flask, request
from waf_rule_tool import get_blocked_ips,get_blocked_keywords

app = Flask(__name__)

# Define a list of blocked IPs (for demonstration purposes)
blocked_ips = get_blocked_ips()
blocked_words = get_blocked_keywords()

# Function to log requests
def log_request(ip, method, path,body):
    with open('logs/requests.log', 'a') as f:
        f.write(f"IP: {ip}, Method: {method}, Path: {path} Body: {body} \n")

# WAF Middleware
@app.before_request
def waf_middleware():
    ip = request.remote_addr
    if ip in blocked_ips:
        return "Access denied", 403
    
    # Log the request
    log_request(ip, request.method, request.path,body = request.get_data(as_text=True))

    # Perform additional security checks here
    # For example, inspect request headers, parameters, etc.
    # Implement logic to block or allow requests based on security rules

@app.route('/', methods=['GET'])
def hello():
    return  f"<p>hello world</p>"

if __name__ == '__main__':
    app.run(debug=True)

