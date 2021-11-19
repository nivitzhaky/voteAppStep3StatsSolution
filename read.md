
1. add a new file name.html under templates with this content:

<!doctype html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="">
	<title>Video contest</title>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
	 crossorigin="anonymous">


	<!-- Custom styles for this template -->
	<link href="static/assets/styles.css" rel="stylesheet">
</head>

<body>

	<header class="site-header sticky-top py-1">
		<nav class="container d-flex flex-column flex-md-row justify-content-between">
			<a class="py-2" href="#" aria-label="Product">
				<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
				 stroke-width="2" class="d-block mx-auto" role="img" viewBox="0 0 24 24">
					<title>Product</title>
					<circle cx="12" cy="12" r="10" />
					<path d="M14.31 8l5.74 9.94M9.69 8h11.48M7.38 12l5.74-9.94M9.69 16L3.95 6.06M14.31 16H2.83m13.79-4l-5.74 9.94" />
				</svg>
			</a>
		</nav>
	</header>

	<main class="form-signin">
  <form method="post" action="/login/submit">
    <h1 class="h3 mb-3 fw-normal">What is your name?</h1>

    <div class="form-floating">
      <input class="form-control" id="inputName" placeholder="Name" name="inputName">
      <label for="inputName">Name</label>
    </div>

    <button class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>

  </form>
</main>

	<footer class="container py-5">
		<div class="row">
			<div class="col-12 col-md">
				<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
				 stroke-width="2" class="d-block mb-2" role="img" viewBox="0 0 24 24">
					<title>Product</title>
					<circle cx="12" cy="12" r="10" />
					<path d="M14.31 8l5.74 9.94M9.69 8h11.48M7.38 12l5.74-9.94M9.69 16L3.95 6.06M14.31 16H2.83m13.79-4l-5.74 9.94" />
				</svg>
				<small class="d-block mb-3 text-muted">&copy; 2017–2021</small>
    </div>
  </div>
</footer>


<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

      
  </body>
</html>

2. add this code in main.py under: db ={}
@app.route('/login')
def login_route():
    return render_template('name.html')

@app.route('/login/submit', methods = ['POST'])
def login_submit():
    db['name'] = request.form['inputName'];
    return redirect("/")

3. open the app in new tab, add /login to the url and see if it works

4. in index.html replace
		<h1 class="display-4 fw-normal">What do you like more?</h1>

    with:

    	<h1 class="display-4 fw-normal"> {% if  db['name'] %}{{db['name']}},{% endif %} What do you like more?</h1>

try to login and see your name in the header

5. run the following query (put query text in the line that starts with postgreSQL_select_Query) :
create table [yourname]_votes ( created_at TIMESTAMP DEFAULT NOW(), name varchar(50), voted varchar(500), not_voted varchar(500)) 

6. replace the query with:
select * from [yourname]_votes

7. replace the submit function with (note, replace [yourname] with yourname:
@app.route('/submit', methods = ['POST'])
def sumbit():
  cur = conn.cursor()
  if not 'name' in db.keys():
    db['name'] = 'undefined'
  if (request.form['vote'] == '1'): 
    print("selected1:" + db["url1"])
    cur.execute("INSERT INTO [yourname]_votes (name, voted, not_voted) VALUES (%s, %s, %s)",(db['name'], db["url1"], db["url2"]))
  else:
    print("selected2:" + db["url2"])
    cur.execute("INSERT INTO [yourname]_votes (name, voted, not_voted) VALUES (%s, %s, %s)",(db['name'], db["url2"], db["url1"]))
  conn.commit()
  return main_route()

8. vote . restart the application
 check that you see votes results in the console box

9.
make a session-> (save your main.py on notepad befoe you start)
WE NEED SESSION TO SAVE DATA PER USER
if you login to the app from several windows the name will be changed every time someone logins


10. after definition of app add:
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app) 

19. replace any reference to db['name'] with session['name'] (4 times)

20. replace:
if not 'name' in db.keys():
with 
if not 'name' in session.keys():

21. replace  
return render_template('index.html', db = db)
with:
  return render_template('index.html', db = db, session = session)
22. in index.html replace:
{% if  db['name'] %}{{db['name']}},{% endif %}
with
{% if  session['name'] %}{{session['name']}},{% endif %}

to to access the app from several windows and see that you see different names,

CHALLNGE :
add a logout button