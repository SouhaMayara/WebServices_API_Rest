from flask import Flask, request,render_template
import psycopg2
app = Flask(__name__)


@app.route("/test")
def test():
    conn=''
    try:
        print("deb")
        conn = psycopg2.connect("dbname='ex1' user='pstgres' password='admin'")
        print("conn")
        cur = conn.cursor()
        print(cur)
        try:
            cur.execute("""DROP DATABASE foo_test""")
        except:
            return("I can't drop our test database!")
    except:
        return("I am unable to connect to the database.")


@app.route("/")
def index():
    mots = ["bonjour", "à", "toi,", "visiteur."]
    puces = ''.join("<li>{}</li>".format(m) for m in mots)
    return """<!DOCTYPE html>
                    <html>
                        <head>
                            <meta charset="utf-8" />
                            <title>{titre}</title>
                        </head>

                        <body>
                            <h1>{titre}</h1>
                            <ul>
                                {puces}
                            </ul>
                        </body>
                    </html>""".format(titre="Bienvenue !", puces=puces)


    '''try:
        #conn = psycopg2.connect("dbname=ex1 user=postgres password=admin")
        conn = psycopg2.connect(user="postgres",
                                      password="admin",
                                      host="localhost",
                                      port="5433",
                                      database="ex1")
        cursor = conn.cursor()
        # Print PostgreSQL Connection properties
        return(conn.get_dsn_parameters(), "\n")
    except (Exception, psycopg2.Error) as error:
        return("Error while connecting to PostgreSQL", error)
    #cnx = m.connect(host='localhost', user='root', password='admin', database='ex1', port=5433)
    #return "<h2>hellooo!!!!</h2> %s"% request.method'''

@app.route('/tuna',methods=['GET','POST'])
def tuna():
    if request.method=='POST':
        return 'you are using POST'
    else:
        return 'you are probably using GET'



@app.route('/profile/<name>')
def profile(name):
    return render_template("profile.html" ,name=name)


@app.route('/shopping')
def shopping():
    food=["cheese","tuna","beef","toothpaste"]
    return render_template("shopping.html" , food=food)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "<h2>Post ID is %s</h2>" % post_id



if __name__=="__main__":
    app.run(debug=True)
    #app.run(host='149.202.243.51',port=5000,debug=True)