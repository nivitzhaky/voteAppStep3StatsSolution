from flask import Flask, render_template, request, redirect
from random import randint
import psycopg2
from flask import session
from tempfile import mkdtemp
from flask_session import Session
import json
from os import environ
from scipy import sparse
import implicit
import numpy as np
from ml_metrics import mapk
import pandas as pd
from scipy.sparse import csr_matrix

conn = psycopg2.connect(host="18.118.156.136",
    database="postgres",
    user="postgres",
    password="topSecret")


#Set up website with index.html
app = Flask('app')
db = {};

@app.route('/')
def main_route():
    print ("inside1")
    cursor = conn.cursor()
    cursor.execute("select voted as name,count(*) as count from ofeq_votes group by voted order by count(*) desc limit 10 ")
    recordsByMovie = cursor.fetchall()
    #records.insert(0,["name","count"])
    byMovie = json.dumps({'data':recordsByMovie})

    cursor = conn.cursor()
    cursor.execute("select name as name,count(*) as count from ofeq_votes group by name order by count(*) desc ")
    recordsByName = cursor.fetchall()
    #records.insert(0,["name","count"])
    byName = json.dumps({'data':recordsByName})

    rec_values = []
    if ('username' in db):
      print ("inside")
      cursor.execute("select name as user, voted as product,count(*) as rating from ofeq_votes group by name, voted order by count(*) ")
      records = cursor.fetchall()
      
      
      
      model = implicit.als.AlternatingLeastSquares(factors=50)
      item_user_data, users_map, movies_map, users_rmap, movies_rmap = to_matrix(records)
      model.fit(item_user_data)

      user_items = item_user_data.T.tocsr()
      if (db['username'] in users_map):
        recommendations = model.recommend(users_map[db['username']], user_items)
        rec_values = [movies_rmap[x[0]] for x in recommendations]
    
    
    return render_template('index.html', byMovie = byMovie,byName = byName,rec_values = rec_values, recordsByMovie = recordsByMovie, recordsByName = recordsByName)
@app.route('/submit', methods = ['POST'])
def set_name():
    db['username'] = request.form['username'];
    return redirect("/")

@app.route('/name')
def name_route():
    cursor = conn.cursor()
    cursor.execute("select name,count(*) from ofeq_votes group by name order by count(*) desc limit 5 ")
    records = cursor.fetchall()
    records.insert(0,["name","count"])
    data = json.dumps({'title' : "votes by name" ,'data':records})
    return render_template('index.html', data = data)



def to_matrix(records):
    users_str, movies_str, ranks = list(zip(*records))
    users_map = {k: v for v, k in enumerate(set(users_str))}
    movies_map = {k: v for v, k in enumerate(set(movies_str))}
    users_rmap = {v: k for v, k in enumerate(set(users_str))}
    movies_rmap = {v: k for v, k in enumerate(set(movies_str))}
    mapped = [[users_map[x[0]],movies_map[x[1]],x[2] ] for x in records]

    df = pd.DataFrame(mapped, columns=['userId', 'movieID', 'rating'])
    res = csr_matrix((df.rating, (df.userId , df.movieID)))
    return res , users_map, movies_map, users_rmap, movies_rmap

if 'app' == '__main__':
    app.run()

app.run(host='0.0.0.0', port=8080)