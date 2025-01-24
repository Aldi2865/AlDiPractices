from flask import render_template, request, redirect, url_for, flash
import psycopg2
from app import app
from config import Config

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ammunitionsupplydb",
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASSWORD']
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "ammunitionstock" ORDER BY "ammunitionid";')
    ammunition = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', title='Ammunition Stock', ammunition=ammunition)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        type = request.form['type']
        quantity = request.form['quantity']
        storage_location = request.form['storage_location']
        expiration_date = request.form['expiration_date']

        if not type or not quantity or not storage_location or not expiration_date:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO "ammunitionstock" (type, quantity, storageLocation, expirationDate) VALUES (%s, %s, %s, %s)',
                (type, quantity, storage_location, expiration_date)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash('Ammunition created successfully!')
            return redirect(url_for('index'))

    return render_template('create.html', title='Create Ammunition')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "ammunitionstock" WHERE "ammunitionid" = %s', (id,))
    ammunition = cur.fetchone()
    cur.close()
    conn.close()

    if request.method == 'POST':
        type = request.form['type']
        quantity = request.form['quantity']
        storage_location = request.form['storage_location']
        expiration_date = request.form['expiration_date']

        if not type or not quantity or not storage_location or not expiration_date:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'UPDATE "ammunitionstock" SET type = %s, quantity = %s, storagelocation = %s, expirationdate = %s WHERE "ammunitionid" = %s',
                (type, quantity, storage_location, expiration_date, id)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash('Ammunition updated successfully!')
            return redirect(url_for('index'))

    return render_template('edit.html', title='Edit Ammunition', ammunition=ammunition)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "ammunitionstock" WHERE "ammunitionid" = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Ammunition deleted successfully!')
    return redirect(url_for('index'))