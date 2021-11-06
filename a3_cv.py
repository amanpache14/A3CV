from flask import Flask,redirect,url_for,request,Response
from flask.templating import render_template
from numpy.lib.utils import source
from werkzeug.utils import secure_filename
import os, time

vfilename = "None"
vsource = None
cowin = Flask(__name__)

@cowin.route("/")
@cowin.route("/home")
def home():
    return render_template("/home/index.html")


@cowin.route("/xray", methods = ['POST','GET'])
def xray(filename = None):
    from xrayd import classify
    UPLOAD_FOLDER = 'final/static/uploads/xray/new'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    cowin.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    
    if request.method == 'POST':
        file = request.files["filename"]
        #print(filename)
        filename  = getFilename(file, ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS)
        prediction, confidence = classify(UPLOAD_FOLDER+"/"+filename)
        result = {"normal":"normal","pneumonia":"pneumonia","covid":"covid"}

        print(result[prediction])

        return render_template("/xray/index.html", res = result[prediction], filename = f'uploads/xray/new/{filename}',confidence =confidence)

    else:
        return render_template("/xray/index.html", x=1)


@cowin.route("/sociald",methods=['POST','GET'])
def sociald():
    if request.method == "POST":
        global vfilename, vsource
        src = {}
        src = request.form["vidsource"]
        print(f"SOURCE:::::::::::::>{src}")
        if src == "video":
            file = request.files["filename"]
            UPLOAD_FOLDER = 'final/static/uploads/sociald/video/'
            ALLOWED_EXTENSIONS = {'mp4','avi'}
            cowin.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
            filename  = getFilename(file, ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS)
            print(f"filename::::::::::::::::::>{filename}")
            vfilename,vsource = filename, src
            return render_template("sociald/index.html", x = 1)
        else:
            vsource = src
            return render_template("sociald/index.html", x = 1)
    else:
        return render_template("sociald/index.html", x = 0)

@cowin.route("/video_feed")
def video_feed():
    #os.environ["CUDA_VISIBLE_DEVICES"]="0"
    from sociald import gen
    return Response(gen(filename = vfilename,source=vsource),mimetype='multipart/x-mixed-replace; boundary=frame')

@cowin.route("/maskd", methods = ['POST','GET'])
def maskd():  
    if request.method == "POST":
        global vfilename, vsource
        src = {}
        src = request.form["vidsource"]
        print(f"SOURCE:::::::::::::>{src}")
        if src == "video":
            file = request.files["filename"]
            UPLOAD_FOLDER = 'final/static/uploads/maskd/video/'
            ALLOWED_EXTENSIONS = {'mp4','avi'}
            cowin.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
            filename  = getFilename(file, ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS)
            print(f"filename::::::::::::::::::>{filename}")
            vfilename,vsource = filename, src
            return render_template("maskd/index.html", x = 1)
        else:
            vsource = src
            return render_template("maskd/index.html", x = 1)
    else:
        return render_template("maskd/index.html", x = 0)
            

@cowin.route("/video_feed2")
def video_feed2():
    #os.environ["CUDA_VISIBLE_DEVICES"]="0"
    from maskd import maskgen
    global vsource, vfilename
    return Response(maskgen(filename = vfilename,source=vsource),mimetype='multipart/x-mixed-replace; boundary=frame')

def getFilename(file,ALLOWED_EXTENSIONS):
    def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(cowin.config['UPLOAD_FOLDER'], filename))
    return filename



    
if __name__ == "__main__":
    cowin.run(debug=True)
    
