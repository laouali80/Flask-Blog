// setting an enviroment viarable for the app running , Linux set = export
// allow the use of flask run 
set FLASK_APP=flaskblog.py

// setting the running unstop
set FLASK_DEBUG=1

// if we want to run the file with python (inside flaskblog.py) e.g python3 flaskblog.py
if __name__=='__main__':
    app.run(debug=True)

ctrl + shift + r : strong refresh