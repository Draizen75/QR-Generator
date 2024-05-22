from flask import Flask, render_template, request
import segno
from io import BytesIO
import base64

app = Flask(__name__)

# Function to generate QR code using segno
def generate_qr(data):
    qr = segno.make(data, error='L')
    buffer = BytesIO()
    qr.save(buffer, kind='png', scale=10, border=1)
    buffer.seek(0)
    return buffer

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_base64 = None
    if request.method == 'POST':
        data = request.form.get('data')
        if data:
            buffer = generate_qr(data)
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            qr_code_base64 = f"data:image/png;base64,{img_str}"
    return render_template('index.html', qr_code_base64=qr_code_base64)

if __name__ == '__main__':
    app.run(debug=True)
