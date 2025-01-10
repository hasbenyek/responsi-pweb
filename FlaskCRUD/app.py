from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector 

app = Flask(__name__)

db = connector.connect (
   host = 'ka7ek.h.filess.io', 
    user    = 'dbkuliah1018ref_middlegas',
    port    = '3307',
    password= '37a4eb75bbb353522bba4a906be99f56b42e5991',
    database= 'dbkuliah1018ref_middlegas' 
)

if db.is_connected():
    print('open connection succesful')

@app.route('/')
def halaman_awal():
    cur = db. cursor ()
    cur.execute("select * from mahasiswa ")
    res = cur. fetchall()
    cur.close()
    return render_template('index.html', hasil=res)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['post'])
def proses_tambah():
    nim = request. form['nim']
    nama = request. form['nama']
    asal = request. form['asal']
    cur = db.cursor ()
    cur.execute('INSERT INTO mahasiswa (nim, nama, asal) VALUES (%s, %s, %s) ' , (nim, nama, asal) )
    db.commit()
    return redirect(url_for ('halaman_awal'))

@app.route('/ubah/<nim>', methods=['GET'])
def ubah_data(nim):
    cur = db.cursor()
    cur.execute('SELECT * FROM mahasiswa WHERE nim=%s', (nim,))
    res = cur.fetchall()
    cur.close()
    return render_template('ubah.html', hasil=res)

@app.route('/proses_ubah', methods=['POST'])
def proses_ubah():
    nim_ori = request.form['nim_ori']
    nim = request.form['nim']
    nama = request.form['nama']  
    asal = request.form['asal']
    
    try:
        cur = db.cursor()
        sql = "UPDATE mahasiswa SET nim=%s, nama=%s, asal=%s WHERE nim=%s"
        value = (nim, nama, asal, nim_ori)
        cur.execute(sql, value)
        db.commit()
        cur.close()
        return redirect(url_for('halaman_awal'))
    except Exception as e:
        db.rollback()
        return f"Error: {str(e)}"

@app.route('/hapus/<nim>', methods=['GET'])
def hapus_data(nim):
    try:
        cur = db.cursor()
        cur.execute('DELETE FROM mahasiswa WHERE nim=%s', (nim,))
        db.commit()
        cur.close()
        return redirect(url_for('halaman_awal'))
    except Exception as e:
        db.rollback()
        return f"Error: {str(e)}"
    
if __name__ == '_main_':
    app.run()