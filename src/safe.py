import base64

def unsafe(input):
    base64_bytes = input.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    output = message_bytes.decode('utf-8')
    return output

def tosafe(input):
    message_bytes = input.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    output = base64_bytes.decode('utf-8')
    return output
