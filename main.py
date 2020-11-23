import os
from flask import Flask, render_template,redirect,request,url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
UPLOAD_FOLDER='C:\\Users\\USER\\Pictures'
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/uff_webapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["MP4", "WEBM"]
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
db=SQLAlchemy(app)
class videofiles(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)

@app.route('/')
def home():
    return render_template('home.html')


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload_vid", methods=["GET", "POST"])
def upload_vid():

    if request.method == "POST":

        if request.files:

            if "filesize" in request.cookies:
                f=request.files['inputfile']
                f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
                newdata = videofiles(name=f.filename)
                db.session.add(newdata)
                db.session.commit()
                return redirect(url_for('play'))


                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)

                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                    print("Image saved")

                    return redirect(request.url)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

    return render_template("upload_vid.html")
@app.route('/play')
def play():
        file_data = videofiles.query.all()
        l = []
        for i in file_data:
            l.append(i.name)
            print(i.name)
        print(l)
        return render_template('home.html', videos=l)

if __name__=='__main__':
    app.run()




