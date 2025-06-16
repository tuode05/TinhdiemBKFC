from flask import Flask, render_template, request, session
from flask_session import Session
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Cấu hình Flask-Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET', 'POST'])
def calculate_score():
    result = None

    if request.method == 'POST':
        try:
            method = request.form.get('method')
            diem_dgnl = float(request.form.get('diem_dgnl') or 0)  # Lấy giá trị đã quy đổi
            diem_hpt = float(request.form.get('diem_hpt')) if request.form.get('diem_hpt') else 0
            diem_tnthpt = float(request.form.get('diem_tnthpt'))
            foreign_cert_score = request.form.get('foreign_cert_score') or '0'
            foreign_cert_type = request.form.get('foreign_cert_type') or 'none'

            if method == '1':  # Có Đánh giá Năng lực
                diem_nang_luc = diem_dgnl / 15  # Quy đổi từ 1500 về 100
            elif method == '2':  # Không Đánh giá Năng lực
                diem_nang_luc = (diem_tnthpt / 3 * 10) * 0.75
            elif method == '3':  # Có chứng chỉ quốc tế
                diem_nang_luc = diem_dgnl  # Điểm năng lực = điểm quy đổi thang 100
            elif method == '4':  # Tốt nghiệp THPT nước ngoài
                diem_nang_luc = diem_hpt * 10  # Điểm năng lực = Điểm học THPT quy đổi

            if method == '4':  # Tính Điểm TNTHPT quy đổi cho THPT nước ngoài
                if foreign_cert_type != 'none' and float(foreign_cert_score) > 0:
                    diem_tnthpt_quy_doi = convertByThreshold(float(foreign_cert_score), foreign_cert_type)
                else:
                    diem_tnthpt_quy_doi = diem_hpt * 10  # Nếu không có chứng chỉ
            else:
                diem_tnthpt_quy_doi = diem_tnthpt / 3 * 10

            diem_hpt_quy_doi = diem_hpt * 10
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

# Hàm quy đổi (tạm thời đặt trong Python để minh họa, thực tế đã xử lý ở client-side)
def convertByThreshold(score, certType):
    conversionTable = {
        SAT: { 1600: 100, 1584: 99, 1568: 98, 1552: 97, 1536: 96, 1520: 95, 1504: 94, 1488: 93, 1472: 92, 1456: 91, 1440: 90, 1424: 89, 1408: 88, 1392: 87, 1376: 86, 1360: 85, 1344: 84, 1328: 83, 1312: 82, 1296: 81, 1280: 80, 1264: 79, 1248: 78, 1232: 77, 1216: 76, 1200: 75 },
            ACT: { 36: 100, 35: 98, 34: 95, 33: 93, 32: 90, 31: 88, 30: 86, 29: 84, 28: 82, 27: 81, 26: 78, 25: 76, 24: 74 },
            IB: { 42: 100, 41: 98, 40: 96, 39: 94, 38: 91, 37: 89, 36: 86, 35: 84, 34: 82, 33: 79, 32: 77, 31: 74, 30: 71, 29: 69, 28: 67, 27: 64, 26: 62 },
            'A-Level': { 'A*': 95, 'A': 85, 'B': 75, 'C': 65 }
    }
    if certType == 'none' or score <= 0:
        return 0
    table = conversionTable.get(certType, {})
    scores = sorted([k for k in table.keys() if isinstance(k, (int, float))], reverse=True)
    for s in scores:
        if score >= s:
            return table[s]
    return 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)