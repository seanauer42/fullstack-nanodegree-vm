from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# accessing the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

engine = create_engine('sqlite:///restaurantmenu.db')


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    output = f'<h1>{restaurant.name}</h1>'
    for i in items:
        output += i.name
        output += '<br>'
        output += i.price
        output += '<br>'
        output += i.description
        output += '<p>'

    # this is the link to add a new menu item
    output += f'<p><a href="/restaurants/{restaurant.id}/new_item">New Menu Item</a>'
    return output


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/')
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return "page to edit a menu item. Task 2 complete!"


# creating a page so that you can add a new item to a restaurant
@app.route('/restaurants/<int:restaurant_id>/new_item/')
def new_item(restaurant_id):
    first_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    output = ''
    output += '<h1>%s</h1>' % first_restaurant.name
    output += 'this is where the stuff will go. But for now it just says BOOBS'

    return output

# this is the homepage. It just displays the restaurants in a clickable format. When you click, it shows the menu items
@app.route('/')
@app.route('/restaurant')
@app.route('/restaurants')
def restaurants():
    r = session.query(Restaurant)
    output = "<h1>Restaurants</h1><p>"
    for i in r:
        output += '<a href="/restaurants/%s/">' % i.id
        output += i.name
        output += '</a><br>'
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
