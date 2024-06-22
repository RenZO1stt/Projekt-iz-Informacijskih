from flask import Flask, render_template, request, redirect, url_for, jsonify
from pony.orm import Database, PrimaryKey, Required, db_session, Set, Optional, select

app = Flask(__name__)

from models import Artikl


@app.route('/')
@db_session
def index():
    return render_template('index.html')


@app.route('/catalog', methods=['GET', 'POST'])
@db_session
def catalog():
    if request.method == 'POST':
        filters = {}
        if 'vrsta' in request.form and request.form['vrsta']:
            filters['vrsta'] = request.form['vrsta']
        if 'materijal' in request.form and request.form['materijal']:
            filters['materijal'] = request.form['materijal']
        if 'velicina' in request.form and request.form['velicina']:
            filters['velicina'] = request.form['velicina']
        if 'boja' in request.form and request.form['boja']:
            filters['boja'] = request.form['boja']

        items = list(Artikl.select())
        if filters:
            items = [item for item in items if
                     (filters.get('vrsta') is None or item.vrsta == filters['vrsta']) and
                     (filters.get('materijal') is None or item.materijal == filters['materijal']) and
                     (filters.get('velicina') is None or item.velicina == filters['velicina']) and
                     (filters.get('boja') is None or item.boja == filters['boja'])]
    else:
        items = Artikl.select()[:]

    return render_template('catalog.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
@db_session
def add_item():
    if request.method == 'POST':
        vrsta = request.form['vrsta']
        materijal = request.form['materijal']
        velicina = request.form['velicina']
        boja = request.form['boja']
        Artikl(vrsta=vrsta, materijal=materijal, velicina=velicina, boja=boja)
        return redirect(url_for('catalog'))
    return render_template('add_item.html')


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@db_session
def edit_item(item_id):
    item = Artikl.get(id=item_id)
    if request.method == 'POST':
        item.vrsta = request.form['vrsta']
        item.materijal = request.form['materijal']
        item.velicina = request.form['velicina']
        item.boja = request.form['boja']
        return redirect(url_for('catalog'))
    return render_template('edit_item.html', item=item)


@app.route('/delete/<int:item_id>', methods=['POST'])
@db_session
def delete_item(item_id):
    item = Artikl.get(id=item_id)
    item.delete()
    return redirect(url_for('catalog'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
