from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_score():
    result = None
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            method = request.form.get('method')
            
            if method == '1':
                # Thi sinh CÔNG
                diem_dgnl = float(request.form.get('diem_dgnl'))
                diem_tnthpt = float(request.form.get('diem_tnthpt'))
                diem_hpt = float(request.form.get('diem_hpt'))

                # Tính điểm năng lực
                diem_nang_luc = (diem_dgnl) / 15

                # Tính điểm TNTHPT quy đổi
                diem_tnthpt_quy_doi = diem_tnthpt / 3 * 10

                # Tính điểm học tập quy đổi
                diem_hpt_quy_doi = diem_hpt * 10

                # Tính điểm học lực
                diem_hoc_luc = (diem_nang_luc * 0.7) + (diem_tnthpt_quy_doi * 0.2) + (diem_hpt_quy_doi * 0.1)

            else:
                # Thi sinh KHÔNG
                diem_tnthpt = float(request.form.get('diem_tnthpt'))
                diem_hpt = float(request.form.get('diem_hpt'))

                # Tính điểm TNTHPT quy đổi
                diem_tnthpt_quy_doi = diem_tnthpt / 3 * 10

                # Tính điểm học tập quy đổi
                diem_hpt_quy_doi = diem_hpt * 10

                # Tính điểm năng lực
                diem_nang_luc = diem_tnthpt_quy_doi * 0.75

                # Tính điểm học lực
                diem_hoc_luc = diem_nang_luc

            # Làm tròn điểm học lực đến 0.01
            diem_hoc_luc = round(diem_hoc_luc, 2)

            # Điểm xét tuyển giờ chỉ là điểm học lực (không cộng điểm ưu tiên)
            diem_xet_tuyen = diem_hoc_luc

            # Chuẩn bị kết quả
            result = {
                'diem_nang_luc': round(diem_nang_luc, 2),
                'diem_tnthpt_quy_doi': round(diem_tnthpt_quy_doi, 2),
                'diem_hpt_quy_doi': round(diem_hpt_quy_doi, 2),
                'diem_hoc_luc': diem_hoc_luc,
                'diem_xet_tuyen': round(diem_xet_tuyen, 2)
            }

        except ValueError:
            result = "Lỗi: Vui lòng nhập đầy đủ và đúng định dạng số!"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)