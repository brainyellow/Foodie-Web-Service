from flask import Flask, jsonify, render_template, request, redirect, url_for
from geocodio import GeocodioClient
from pyzomato import Pyzomato

app = Flask(__name__)
geocod = GeocodioClient('b4ee25bee55b1c4242535b871e3ba7aa031bb7e')
zomato = Pyzomato('14b0003fd0c86f9a5b8d79fba7012571')


@app.route('/', methods=['GET', 'POST'])
def mainPage():
    if request.method == 'POST':
        address = request.form['address']
        return redirect(url_for('restaurants', address=address))
    else:
        return render_template('index.html')


@app.route('/restaurants/<address>')
def restaurants(address):
    location = geocod.geocode(address).coords
    data = zomato.getByGeocode(location[0], location[1])
    rdata = data['nearby_restaurants']

    finalOutput = list()
    for r in rdata:
        output = dict()
        output['name'] = r['restaurant']['name']
        output['address'] = r['restaurant']['location']['address']
        output['cuisines'] = r['restaurant']['cuisines']
        output['rating'] = r['restaurant']['user_rating']['aggregate_rating']
        finalOutput.append(output)
    return jsonify(finalOutput)


if __name__ == "__main__":
    app.run(debug=True)