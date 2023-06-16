# from flask import Flask, render_template, request
# import os

# app = Flask(__name__)

# # Đường dẫn tới thư mục chứa tệp tin đã tải lên
# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# # Thiết lập thư mục tải lên
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Đường dẫn tải lên tệp tin
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']

#         # Kiểm tra tệp tin có tồn tại không
#         if file:
#             # Lưu tệp tin vào thư mục UPLOAD_FOLDER
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#             return 'File uploaded successfully!'
#     return render_template('upload.html')

# if __name__ == '__main__':
#     app.run(debug=False)


#------------------------------------------------------------------------------------------------------------------------

from flask import Flask, request, redirect, url_for
import os

ALLOWED_EXTENSIONS = {'txt', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
        <html>
            <body>
                <h1>Upload file xlsx</h1>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        print("dung loai file yeu cau")
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("save file thanh cong")
        return redirect(url_for('index'))
    
    else:
        return '''
            <html>
                <body>
                    <h1>Upload file xlsx</h1>
                    <p>Only .txt or .xlsx files are allowed.</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file">
                        <input type="submit" value="Upload">
                    </form>
                </body>
            </html>
        '''
# '<p>File uploaded successfully!</p>'
if __name__ == '__main__':
    app.run(debug=False)



