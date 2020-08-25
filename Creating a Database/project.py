from flask import Flask, render_template, request, url_for, redirect
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

    # output = f'<h1>{restaurant.name}</h1>'
    # for i in items:
    #     output += i.name
    #     output += '<br>'
    #     output += i.price
    #     output += '<br>'
    #     output += i.description
    #     output += '<p>'
    #
    # # this is the link to add a new menu item
    # output += f'<p><a href="/restaurants/{restaurant.id}/new_item">New Menu Item</a>'
    return render_template('menu.html', restaurant=restaurant, items=items)


# confirmation page to show before deleting menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()

    return "page to delete a menu item. Task 3 complete!"


# this is the page to edit menu items
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('edit_menu_item.html', restaurant=restaurant, menu_item=menu_item)


# creating a page so that you can add a new item to a restaurant
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant.id)
        session.add(new_item)
        session.commit()

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant.id))
    else:
        return render_template('new_menu_item.html', restaurant=restaurant)


# this is the homepage. It just displays the restaurants in a clickable format. When you click, it shows the menu items
@app.route('/')
@app.route('/restaurant/')
@app.route('/restaurants/')
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
