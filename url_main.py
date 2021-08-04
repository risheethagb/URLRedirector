from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

hostName = "localhost"
serverPort = 8000


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        l_url = ""
        s_url = ""
        url_dict = {}

        if os.stat("url.txt").st_size != 0:
            f = open("url.txt", "r")
            url_dict = (json.loads(f.read()))
            f.close()

        if self.path in url_dict:

            if url_dict[self.path].startswith("https://"):
                self.send_response(302)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", url_dict[self.path])
                self.end_headers()
            elif url_dict[self.path].startswith("http://"):
                self.send_response(302)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", url_dict[self.path])
                self.end_headers()
            elif url_dict[self.path].startswith("www."):
                self.send_response(302)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "https://" + url_dict[self.path])
                self.end_headers()

        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<h3> Welcome to URL Redirector </h3>", "utf-8"))
            self.wfile.write(bytes(
                "<p> Following the current URL, add a forward slash and your short URL in the address box above to continue </p>",
                "utf-8"))
            self.wfile.write(
                bytes("<p> For example, after \"localhost:8000\" add \"/google\"</p></body></html>", "utf-8"))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<h3>No URL Found for: %s </h3>" % self.path.strip("/"), "utf-8"))
            self.wfile.write(bytes("<form method = \"post\">", "utf-8"))
            self.wfile.write(bytes("Enter the long URL: <input type=\"text\" name=\"long_url\" />", "utf-8"))
            self.wfile.write(bytes("<p></p><input type=\"submit\" value=\"Submit\" />", "utf-8"))
            self.wfile.write(bytes("</form>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data_input = bytes.decode(self.rfile.read(content_length))
        l_url = data_input.split("=")[1]
        if l_url.startswith("https://") or l_url.startswith("http://") or l_url.startswith("www"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            s_url = self.path
            self.wfile.write(
                bytes("<html><body><p> Please reload the page to be redirected to %s </p></body></html>" % l_url, "utf-8"))

            url_dict = {}

            if os.stat("url.txt").st_size != 0:
                try:
                    f = open("url.txt", "r")
                    url_dict = (json.loads(f.read()))
                    f.close()
                except IOError:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
                    self.wfile.write(bytes("<body>", "utf-8"))
                    self.wfile.write(bytes("<h3> Error finding URL </h3>", "utf-8"))

            try:
                f = open("url.txt", "w")
                url_dict[s_url] = l_url
                f.write(json.dumps(url_dict))
                f.close()
            except IOError:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<h3> Error storing URL </h3>", "utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<h3> Improper URL Entered </h3>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
