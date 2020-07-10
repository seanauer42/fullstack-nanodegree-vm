from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

engine = create_engine('sqlite:///restaurantmenu.db')

class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello World"

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me " \
                          "to say?</h2><input name='message' type='text' ><input type='submit' value='Submit' > </form>"
                output += "</body></html>"

                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Fuck off! <p><a href='/hello'>back to hello</a>"

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me " \
                          "to say?</h2><input name='message' type='text' ><input type='submit' value='Submit' > </form>"
                output += "</body></html>"
                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>Restaurants</title></head>"
                output += "<body><h1>Restaurants</h1>"



        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            print(str(pdict))
            if ctype == 'multipart/form-data':
                print('you are in the if statement')
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this:  </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"

                output += "<h2>What would you like me to say?</h2><input name='message' type='text' >" \
                          "<input type='submit' value='Submit' > </form>"
                output += "</body></html>"
                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print('Webserver running on %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, exiting server")
        server.socket.close()
    

if __name__ == '__main__':
    main()
