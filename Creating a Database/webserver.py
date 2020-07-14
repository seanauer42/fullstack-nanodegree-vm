from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me"
                output += " to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
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

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me"
                output += " to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurants") | self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>Restaurants</title></head>"
                output += "<body><h1>Restaurants</h1>"
                output += "<p><a href='/restaurants/new'>New Restaurant</a><p>"

                for i in restaurants:
                    output += "<p>" + i.name + "\n"
                    output += "<p><a href='/restaurants/edit'>Edit</a> \n"
                    output += "<p>Delete<p>"

                output += "</body></html>"

                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>New</title></head>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<h1>New Restaurant</h1>"
                output += "<p>Name of Restaurant  <input name='message' type='text' >"
                output += "<input type='submit' value='Submit'></form>"

                output += "</body></html>"

                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # veggie_burger = session.query(MenuItem).filter_by(name='Veggie Burger')
                restaurant = session.query(Restaurant).filter_by(name="Pizza Palace").first()
                # print(restaurant)
                items = session.query(MenuItem).filter_by(restaurant=restaurant)
                for i in items:
                    print(i.restaurant.name)

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>Edit</title></head>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/edit'>"

                output += "<h1>Edit Restaurant</h1>"

                for i in items:
                    output += "<p>" + i.name
                    output += "<p>" + i.price

                output += "<h2>What would you like me to change?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"

                output += "</body></html>"

                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return


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
            fields = cgi.parse_multipart(self.rfile, pdict)
            if ctype == 'multipart/form-data' and fields.get('message') != "":
                print('you are in the if statement')
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this:  </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"

                output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
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
