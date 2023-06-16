# Sinh vien 1: Huynh Duy Quang - 19520141
# Sinh vien 2: Tran Xuan Thang - 19524341

from flask import Flask, request, redirect, url_for, render_template, send_file
from sklearn.preprocessing import LabelEncoder
import multiprocessing as mp
from mceliececipher import *
from excel_output import *
from flask_sse import sse
from excel_input import *
from mathutils import *
from compress import *
import numpy as np
import joblib
import os 


from werkzeug.utils import secure_filename
from flask import send_from_directory


ALLOWED_EXTENSIONS = {'txt', 'xlsx'}
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "Side-left_data_cipher")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")

location_save_ciphertext = None
location_save_plaintext = None
direc_cipherText = {}
direc_plaintText = {}
private_key = {}
public_key = {}
orther = {}
text = None
data_line = None
matrix_text = None
already_assigned = None 
t = None
k = None
n = None
encoder = None
text_recovery = None
texts = None
encoder_path = None




# ----------------- FUNCTION --------------------- #
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt'}


def read_output(path_save_read, choose):
    try:
        if choose:
            with open(path_save_read, encoding='utf-8') as f:
                read_output = f.readlines()

            read_output = [line.strip() for line in read_output]  
            return read_output

        else:
            header = list(range(pd.read_excel(path_save_read).shape[1]))
            df = pd.read_excel(path_save_read, header=None)
            df.columns = header + df.columns[len(header):].tolist()

            data = np.array(df)
            return data

    except Exception as e:
        print("ERROR READ OUTPUT FILE: ", e)


def decrypt(k, n, matrix_text, matrix_output, public_key, private_key, orther):
    try:
        S = private_key['S']
        t = public_key['t']
        P_inv = orther['P_inv']
        S_inv = orther['S_inv']
        y = matrix_output

        mc = McElieceCipher(k, n, t)
        mc.decrypt(matrix_text, y, P_inv, S_inv, S)

        direc_plaintText = {
            'vector': mc.y_,
            'xS': mc.xS,   
            'plainText': mc.x
        }
        return direc_plaintText


    except Exception as e:
        print("ERROR DECRYPT:", e)


def backtext(encoder_path, already_assigned, direc_plaintText):
    try:
        plainText = direc_plaintText['plainText']
        encoder = joblib.load(encoder_path)

        if already_assigned is not None:
            X = []
            for i, row in enumerate(plainText):
                if np.all(already_assigned[i, :len(row)]):
                    X.append(list(row))

                elif not np.all(already_assigned[i, :len(row)]):
                    positive_indices = np.where(row >= 0)[0][:len(row)]
                    X.append(list(row[positive_indices]))

            for i in range(len(X)):
                for j in range(len(X[i])):
                    X[i][j] = int(X[i][j])

            texts = []
            for doc in X:
                words = encoder.inverse_transform(doc)
                text = " ".join(words)
                texts.append(text)

        else:
            texts = []
            for doc in plainText:
                words = encoder.inverse_transform(doc)
                text = " ".join(words)
                texts.append(text)
    
        text_final = '\n'.join(texts)
        return text_final, texts

    except Exception as e:
        print("ERROR RECOVERY TEXT:", e)


def read_input(path_save_read, choose):
    try:
        if choose: 
            with open(path_save_read, encoding='utf-8') as f:
                data_line = f.readlines()
                        
            with open(path_save_read, encoding='utf-8') as f:
                text = f.read()

            data_line = [line.strip() for line in data_line]  
            tokens = [doc.split() for doc in data_line]
                
            label_encoder = LabelEncoder()
            encoder = label_encoder
            label_encoder.fit([token for doc in tokens for token in doc])
            X = [[label_encoder.transform([token])[0] for token in doc] for doc in tokens]

            already_assigned = None 

            check = can_create_matrix(X)
            if check:
                matrix_text = np.array(X)
            else:
                matrix_text, already_assigned = paddingMatrix(X)

            if matrix_text.ndim == 1:
                t = 1
            elif matrix_text.ndim > 1 or len(matrix_text.shape) > 1:
                t = len(matrix_text)

            input_matrix_col = matrix_text.shape[1]
            return text, data_line, matrix_text, already_assigned, t, matrix_text.shape[0], input_matrix_col, encoder

        else: 
            header = list(range(pd.read_excel(path_save_read).shape[1]))
            df = pd.read_excel(path_save_read, header=None)
            df.columns = header + df.columns[len(header):].tolist()

            df.fillna('', inplace=True)

            data_line = np.array(df)
            for i in range(len(data_line)):
                for j in range(len(data_line[i])):
                    if isinstance(data_line[i][j], int) or isinstance(data_line[i][j], float):
                        data_line[i][j] = str(data_line[i][j])

            label_encoder = LabelEncoder()
            encoder = label_encoder
            label_encoder.fit([token for doc in data_line for token in doc])

            already_assigned = None 
            text = None

            X = [[label_encoder.transform([token])[0] for token in doc] for doc in data_line]
            max_length = max([len(row) for row in X])
            input = np.zeros((len(X), max_length))
            already_assigned = np.zeros_like(input, dtype=bool)

            for i, row in enumerate(X):
                input[i, :len(row)] = row
                already_assigned[i, :len(row)] = True

            matrix_text = input.astype(int)

            if matrix_text.ndim == 1:
                t = 1
            elif matrix_text.ndim > 1 or len(matrix_text.shape) > 1:
                t = len(matrix_text)

            input_matrix_col = matrix_text.shape[1]
            return text, data_line, matrix_text, already_assigned, t, matrix_text.shape[0], input_matrix_col, encoder

    except Exception as e:
        print("ERROR READ INPUT FILE: ", e)

    return None


def key(t, k, n):
    try:
        mc = McElieceCipher(t, k, n)
        mc.generate_create_keys()

        private_key = {
            'S': mc.S,
            'G': mc.G,
            'P': mc.G
        } 
        public_key = {
            't': t,
            'Gp': mc.Gp   
        }
        orther = {
            'Gp_col': mc.Gp_col,
            'Gp_row': mc.Gp_row,
            'P_inv': mc.P_inv,
            'S_inv': mc.S_inv    
        }
        return private_key, public_key, orther

    except Exception as e:
        print("ERROR CREATE KEY:", e)


def create_encrypt(t, k, n, matrix_text, public_key, orther):
    try:
        Gp = public_key['Gp']
        Gp_col = orther['Gp_col']

        mc = McElieceCipher(k, n, t)
        mc.encrypt(matrix_text, Gp, Gp_col, t)

        direc_cipherText = {
            'vector': mc.Cp,
            'e': mc.e,   
            'ciphertext': mc.y
        }
        return direc_cipherText

    except Exception as e:
        print("ERROR ENCRYPT:", e)


def save_cipher_file(new_file_name_finally, path_save_read, choose_type_file, already_assigned, encoder, t, k, n, orther, private_key, direc_cipherText, data_line):
    try:
        print("\n\n\t************************* SAVE DATA CIPHER *************************")
        excel = Excel_input(new_file_name_finally, path_save_read, choose_type_file, already_assigned, encoder, t, k, n, orther, private_key, direc_cipherText, data_line)
        excel.Excel_Write_input()
        return excel.path_location_save, excel.encoder_path

    except Exception as e:
        print("ERROR SAVE DATA CIPHER:", e)


def save_plain_file(new_file_name_finally, path_save_read, choose_type_file, already_assigned, encoder, texts, path_location_save, data_line):
    try:
        print("\n\n\t***************************** SAVE DATA PLAIN ******************************")
        excel = Excel_output(new_file_name_finally, path_save_read, choose_type_file, already_assigned, encoder, texts, path_location_save, data_line)
        excel.Excel_Write_output()
        return excel.path_save_plain

    except Exception as e:
        print("ERROR SAVE DATA PLAIN:", e)





# ----------------RENDER HTML ------------------ #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_2():
    return render_template('index.html')

@app.route('/encrypt.html')
def encrypt():
    return render_template('encrypt.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/help.html')
def help():
    return render_template('help.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')





# ---------------- ACTION FORM CIPHER UPLOAD FILE ------------------ #
@app.route('/cipher', methods=['POST'])
def upload_file():
    # kiểm tra có upload lên hay không và có rỗng không
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    # tạo mới thư mục Side-left_data_cipher neus chưa tồn tại
    dir_path = os.path.join(os.getcwd(), "Side-left_data_cipher")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # lấy index lớn nhất của thư mục con
    max_index = 0
    for f in os.listdir(dir_path):
        if f.startswith("Read_turn_") and os.path.isdir(os.path.join(dir_path, f)):
            index = int(f.split("_")[2])
            if index > max_index:
                max_index = index

    # tạo mới thư mục con Read_turn_(max_index)
    new_dir_path = os.path.join(dir_path, "Read_turn_" + str(max_index + 1))
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    # lưu file vừa upload từ giao diện vào thư mục Read_turn_(max_index)
    filename = secure_filename(file.filename)
    file.save(os.path.join(new_dir_path, filename))
    path_save_read = os.path.join(new_dir_path, filename)

    # kiểm tra đây là file gì (txt hay xlsx)
    choose = allowed_file(file.filename)  

    # đọc file vưa upload và trả về các giá trị tương ứng
    global direc_cipherText 
    global private_key 
    global public_key
    global orther 
    global text 
    global data_line 
    global matrix_text 
    global already_assigned
    global t 
    global k 
    global n 
    global encoder 
    text, data_line, matrix_text, already_assigned, t, k, n, encoder =  read_input(path_save_read, choose)

    # tạo khóa
    private_key, public_key, orther = key(t, k, n)

    # mã hóa
    direc_cipherText = create_encrypt(t, k, n, matrix_text, public_key, orther)

    # lưu file khi đã tạo cipher file
    global location_save_ciphertext
    global encoder_path
    name, ext = os.path.splitext(filename)
    new_file_name_finally = name + '_CipherText_McEliece' + ext  

    location_save_ciphertext, encoder_path = save_cipher_file(new_file_name_finally, new_dir_path, choose, already_assigned, encoder, t, k, n, orther, private_key, direc_cipherText, data_line)

    # Trả về kết quả dưới dạng phần tử HTML div
    result = f'{new_file_name_finally}'
    return result


@app.route('/plain', methods=['POST'])
def upload_file_2():
    # kiểm tra có upload lên hay không và có rỗng không
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    # tạo mới thư mục Side-left_data_cipher neus chưa tồn tại
    dir_path = os.path.join(os.getcwd(), "Side-right_data_plain")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # lấy index lớn nhất của thư mục con
    max_index = 0
    for f in os.listdir(dir_path):
        if f.startswith("Read_turn_") and os.path.isdir(os.path.join(dir_path, f)):
            index = int(f.split("_")[2])
            if index > max_index:
                max_index = index

    # tạo mới thư mục con Read_turn_(max_index)
    new_dir_path = os.path.join(dir_path, "Read_turn_" + str(max_index + 1))
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    # lưu file vừa upload từ giao diện vào thư mục Read_turn_(max_index)
    filename = secure_filename(file.filename)
    file.save(os.path.join(new_dir_path, filename))
    path_save_read = os.path.join(new_dir_path, filename)

    # kiểm tra đây là file gì (txt hay xlsx)
    choose = allowed_file(file.filename)  

    global location_save_ciphertext
    global location_save_plaintext
    global direc_cipherText 
    global private_key 
    global public_key
    global orther 
    global text 
    global data_line 
    global matrix_text 
    global already_assigned
    global t 
    global k 
    global n 
    global encoder
    global direc_plaintText
    global text_recovery
    global texts
    global encoder_path

    # đọc file vưa upload và trả về các giá trị tương ứng
    matrix_output = read_output(path_save_read, choose)

    # giải mã
    direc_plaintText = decrypt(k, n, matrix_text, matrix_output, public_key, private_key, orther)

    # khôi phục văn bản
    text_recovery, texts = backtext(encoder_path, already_assigned, direc_plaintText)

    # lưu bản khôi phục
    name, ext = os.path.splitext(filename)
    new_file_name_finally = name + '_PlainText_McEliece' + ext    
    location_save_plaintext = save_plain_file(new_file_name_finally, new_dir_path, choose, already_assigned, encoder, texts, location_save_ciphertext, data_line)
    
    # Trả về kết quả dưới dạng phần tử HTML div
    result = f'{new_file_name_finally}'
    return result


@app.route('/download-cipher', methods=['GET'])
def download():
    global location_save_ciphertext
    file_path = location_save_ciphertext  # Đường dẫn tới tệp tin cần tải xuống
    return send_file(file_path, as_attachment=True)


@app.route('/download-plain', methods=['GET'])
def download_2():
    global location_save_plaintext
    print("PATHHHHHHHHHHHHHHHHHH", location_save_plaintext)
    file_path = location_save_plaintext  # Đường dẫn tới tệp tin cần tải xuống
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False)


