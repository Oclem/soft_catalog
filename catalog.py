from wsgiref.simple_server import make_server

def hello_world_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'application/javascript')] # HTTP Headers
    start_response(status, headers)
    return ["<script>alert('boo');</script>"]

httpd = make_server('', 8100, hello_world_app)
print("Serving on port 8100...")

# Serve until process is killed
httpd.serve_forever()

