import sqlite3
import argparse

# Function to initialize the SQLite database
def initialize_database():
    conn = sqlite3.connect('waf_rules.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS blocked_ips (
                        id INTEGER PRIMARY KEY,
                        ip_address TEXT UNIQUE
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (
                        id INTEGER PRIMARY KEY,
                        keyword TEXT UNIQUE
                    )''')
    conn.commit()
    conn.close()

# Function to add a blocked IP address to the database
def add_blocked_ip(ip_address):
    conn = sqlite3.connect('waf_rules.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO blocked_ips (ip_address) VALUES (?)', (ip_address,))
    conn.commit()
    conn.close()

# Function to add a keyword to the database
def add_keyword(keyword):
    conn = sqlite3.connect('waf_rules.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO keywords (keyword) VALUES (?)', (keyword,))
    conn.commit()
    conn.close()

# Function to view blocked IP addresses
def view_blocked_ips():
    conn = sqlite3.connect('waf_rules.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ip_address FROM blocked_ips')
    blocked_ips = cursor.fetchall()
    conn.close()

    if blocked_ips:
        print("Blocked IP addresses:")
        for ip in blocked_ips:
            print(ip[0])
    else:
        print("No IP addresses are blocked.")

# Function to view blocked keywords
def view_blocked_keywords():
    conn = sqlite3.connect('waf_rules.db')
    cursor = conn.cursor()
    cursor.execute('SELECT keyword FROM keywords')
    keywords = cursor.fetchall()
    conn.close()

    if keywords:
        print("Blocked keywords:")
        for keyword in keywords:
            print(keyword[0])
    else:
        print("No keywords are blocked.")
# Function to get blocked IP addresses from the database
def get_blocked_ips():
    conn = sqlite3.connect('waf_rules.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ip_address FROM blocked_ips')
    blocked_ips = [row[0] for row in cursor.fetchall()]
    conn.close()
    return blocked_ips
def get_blocked_keywords():
    conn = sqlite3.connect('waf_rules.db')
    cursor = conn.cursor()
    cursor.execute('SELECT keyword FROM keywords')
    blocked_keywords = [row[0] for row in cursor.fetchall()]
    conn.close()
    return blocked_keywords


# Command-line interface
def main():
    parser = argparse.ArgumentParser(description='WAF Rule Management Tool')
    parser.add_argument('--block-ip', help='Block an IP address')
    parser.add_argument('--add-keyword', help='Add a keyword to block')
    parser.add_argument('--view-blocked-ips', action='store_true', help='View blocked IP addresses')
    parser.add_argument('--view-blocked-keywords', action='store_true', help='View blocked keywords')

    args = parser.parse_args()

    if args.block_ip:
        add_blocked_ip(args.block_ip)
        print(f"Blocked IP address {args.block_ip} added successfully.")
    elif args.add_keyword:
        add_keyword(args.add_keyword)
        print(f"Keyword '{args.add_keyword}' added successfully.")
    elif args.view_blocked_ips:
        view_blocked_ips()
    elif args.view_blocked_keywords:
        view_blocked_keywords()

if __name__ == '__main__':
    initialize_database()
    main()
