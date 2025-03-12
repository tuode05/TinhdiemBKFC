from flask import Flask, render_template, request, session
from flask_session import Session
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Cấu hình Flask-Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Hàm tạo và kết nối cơ sở dữ liệu (không cần bảng history)
def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def calculate_score():
    result = None

    if 'user_id' not in session:
        session['user_id'] = datetime.now().strftime('%Y%m%d%H%M%S')

    if request.method == 'POST':
        try:
            method = request.form.get('method')
            diem_dgnl = request.form.get('diem_dgnl')
            
            if method == '1':
                diem_dgnl = float(diem_dgnl) if diem_dgnl else 0
                diem_tnthpt = float(request.form.get('diem_tnthpt'))
                diem_hpt = float(request.form.get('diem_hpt'))

                diem_nang_luc = (diem_dgnl) / 15
                diem_tnthpt_quy_doi = diem_tnthpt / 3 * 10
                diem_hpt_quy_doi = diem_hpt * 10
                diem_hoc_luc = (diem_nang_luc * 0.7) + (diem_tnthpt_quy_doi * 0.2) + (diem_hpt_quy_doi * 0.1)

            else:
                diem_tnthpt = float(request.form.get('diem_tnthpt'))
                diem_hpt = float(request.form.get('diem_hpt'))

                diem_tnthpt_quy_doi = diem_tnthpt / 3 * 10
                diem_hpt_quy_doi = diem_hpt * 10
                diem_nang_luc = diem_tnthpt_quy_doi * 0.75
                diem_hoc_luc = (diem_nang_luc * 0.7) + (diem_tnthpt_quy_doi * 0.2) + (diem_hpt_quy_doi * 0.1)

            diem_xet_tuyen = round(diem_hoc_luc, 2)

            result = {
                'diem_nang_luc': round(diem_nang_luc, 2),
                'diem_tnthpt_quy_doi': round(diem_tnthpt_quy_doi, 2),
                'diem_hpt_quy_doi': round(diem_hpt_quy_doi, 2),
                'diem_xet_tuyen': diem_xet_tuyen
            }

        except ValueError as e:
            result = "Lỗi: Vui lòng nhập đầy đủ và đúng định dạng số!"
        except sqlite3.Error as e:
            result = f"Lỗi cơ sở dữ liệu: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)