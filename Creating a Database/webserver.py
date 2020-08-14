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

            elif self.path.endswith("/hola"):
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

            elif self.path.endswith("/restaurants") | self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>Restaurants</title></head>"
                output += "<body><h1>Restaurants</h1>"
                output += "<p><a href='/restaurants/new'>New Restaurant</a><p>"

                for i in restaurants:
                    output += "<br>" + i.name + "\n"
                    output += "<br><a href='/restaurants/%s/edit'>Edit</a> \n" % i.id
                    output += "<br><a href='/restaurants/%s/delete'>Delete</a><p>" % i.id

                output += "</body></html>"

                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            elif self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>New</title></head>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<h1>New Restaurant</h1>"
                output += "<p>Name of Restaurant  <input name='new_restaurant_name' type='text' >"
                output += "<input type='submit' value='Submit'></form>"

                output += "</body></html>"

                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>Edit</title></head>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant_id

                output += "<h1>Edit %s</h1>" % restaurant.name

                output += "<h2>What would you like me to change?</h2><input name='rename' type='text'>"
                output += "<input type='submit' value='Submit'></form>"

                output += "</body></html>"

                output = output.encode('utf-8')
                self.wfile.write(output)
                print(output)
                return

            elif self.path.endswith('delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                output = ""
                output += "<html><head><meta charset='UTF-8'><title>Edit</title></head>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant_id

                output += "<h1>Really delete %s?</h1>" % restaurant.name
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

            if self.path.endswith('new'):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                print('working so far')
                if ctype == 'multipart/form-data':
                    print('you are in the if statement')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant_name')
                    print('about to add to database name = %s' % messagecontent)
                    new_restaurant = Restaurant(name=messagecontent[0])
                    session.add(new_restaurant)
                    session.commit()
                    print('the dirty deed you requested is done')

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print('everything is done here')

            elif self.path.endswith('edit'):
                restaurant_id = self.path.split('/')[2]
                edited_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                print("you got the restaurant %s" % edited_restaurant.name)
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                if ctype == 'multipart/form-data':
                    print("You're in the if statement")
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('rename')
                    print('changing restaurant name to %s' % messagecontent)
                    edited_restaurant.name = messagecontent[0]
                    session.add(edited_restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print('everything is done here')

            elif self.path.endswith('delete'):
                restaurant_id = self.path.split('/')[2]
                edited_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                print("you got the restaurant %s" % edited_restaurant.name)
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                if ctype == 'multipart/form-data':
                    print("You're in the if statement")
                    session.delete(edited_restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print('everything is done here')

            # ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            # content_len = int(self.headers.get('Content-length'))
            # pdict['CONTENT-LENGTH'] = content_len
            # print(str(pdict))
            # fields = cgi.parse_multipart(self.rfile, pdict)
            # if ctype == 'multipart/form-data' and fields.get('message'):
            #     print('you are in the if statement')
            #     messagecontent = fields.get('message')
            #
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h2>Okay, how about this:  </h2>"
            #     output += "<h1> %s </h1>" % messagecontent[0]
            #     output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            #
            #     output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
            #     output += "<input type='submit' value='Submit'></form>"
            #     output += "</body></html>"
            #     output = output.encode('utf-8')
            #     self.wfile.write(output)
            #     print(output)
            #     return
            #
            # elif ctype == 'multipart/form-data' and fields.get('new'):
            #     print("this is for a new restaurant")
            #     messagecontent = fields.get('new')
            #
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h2> %s </h2>" % messagecontent[0]
            #     output += "<h2>Food item to add?</h2><input name='new_food_title' type='text'>"
            #     output += "<h2>Course?</h2><input name='new_food_course' type='text'>"
            #     output += "<h2>Description</h2><input name='new_food_description' type='text'>"
            #     output += "<h2>Price?</h2><input name='new_food_price' type='text'>"
            #     output += "<input type='submit' value='Submit'></form>"
            #     output += "</body></html>"
            #     output = output.encode('utf-8')
            #     self.wfile.write(output)
            #     print(output)
            #     return
            #
            # elif ctype == 'multipart/form-data' and fields.get('edit'):
            #     print("This is where you can edit restaurants")
            #     messagecontent = fields.get('edit')
            #
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h2>You are editing %s </h2>" % messagecontent[0]
            #     output += "<h2>Something?</h2><input name='edit_second' type='text'>"
            #     output += "<input type='submit' value='Submit'></form>"
            #     output += "</body></html>"
            #     output = output.encode('utf-8')
            #     self.wfile.write(output)
            #     print(output)
            #     return


        except:
            pass


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), WebserverHandler)
        print('Webserver running on %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, exiting server")
        server.socket.close()


if __name__ == '__main__':
    main()
