def parse_request(request_data):
    headers = {}
    lines = request_data.decode().split('\r\n')
    first_line_tokens = lines[0].split(' ')
    if len(first_line_tokens) < 2:
        raise ValueError("Invalid HTTP request")
    headers['method'] = first_line_tokens[0]
    headers['url'] = first_line_tokens[1]
    for line in lines[1:]:
        if not line:
            break
        header_tokens = line.split(': ')
        headers[header_tokens[0]] = header_tokens[1]
    return headers