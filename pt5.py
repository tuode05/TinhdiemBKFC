from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Hàm tạo và kết nối cơ sở dữ liệu
def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    method TEXT,
                    diem_dgnl REAL,
                    diem_tnthpt REAL,
                    diem_hpt REAL,
                    diem_nang_luc REAL,
                    diem_tnthpt_quy_doi REAL,
                    diem_hpt_quy_doi REAL,
                    diem_hoc_luc REAL,
                    diem_xet_tuyen REAL,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def calculate_score():
    result = None
    history = []

    try:
        conn = sqlite3.connect('history.db')
        c = conn.cursor()
        c.execute("SELECT * FROM history ORDER BY timestamp DESC")
        history = c.fetchall()
    except sqlite3.Error as e:
        print(f"Lỗi SQLite: {e}")
    finally:
        conn.close()

    if request.method == 'POST':
        try:
            method = request.form.get('method')
            diem_dgnl = request.form.get('diem_dgnl')  # Lấy giá trị, có thể là None
            
            if method == '1':
                diem_dgnl = float(diem_dgnl) if diem_dgnl else 0  # Chuyển thành số, mặc định 0 nếu trống
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
                diem_hoc_luc = diem_nang_luc

            diem_hoc_luc = round(diem_hoc_luc, 2)
            diem_xet_tuyen = diem_hoc_luc

            result = {
                'diem_nang_luc': round(diem_nang_luc, 2),
                'diem_tnthpt_quy_doi': round(diem_tnthpt_quy_doi, 2),
                'diem_hpt_quy_doi': round(diem_hpt_quy_doi, 2),
                'diem_hoc_luc': diem_hoc_luc,
                'diem_xet_tuyen': round(diem_xet_tuyen, 2)
            }

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect('history.db')
            c = conn.cursor()
            c.execute('''INSERT INTO history (method, diem_dgnl, diem_tnthpt, diem_hpt, diem_nang_luc, diem_tnthpt_quy_doi, diem_hpt_quy_doi, diem_hoc_luc, diem_xet_tuyen, timestamp)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (method, diem_dgnl, diem_tnthpt, diem_hpt, diem_nang_luc, diem_tnthpt_quy_doi, diem_hpt_quy_doi, diem_hoc_luc, diem_xet_tuyen, timestamp))
            conn.commit()

            c.execute("SELECT * FROM history ORDER BY timestamp DESC")
            history = c.fetchall()

        except ValueError as e:
            result = "Lỗi: Vui lòng nhập đầy đủ và đúng định dạng số!"
        except sqlite3.Error as e:
            result = f"Lỗi cơ sở dữ liệu: {e}"
        finally:
            conn.close()

    return render_template('index.html', result=result, history=history)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)