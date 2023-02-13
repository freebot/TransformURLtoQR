from flask import Flask, jsonify, request, make_response
import qrcode
import base64
import io

app = Flask(__name__)

@app.route('/qr-code', methods=['GET'])
def generate_qr_code():
    url = request.args.get('url')
    if url is None:
        return jsonify({'error': 'Please provide a URL'}), 400
    
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    
    response = make_response(buffer.read())
    response.headers.set('Content-Disposition', 'attachment', filename='qr_code.png')
    response.headers.set('Content-Type', 'image/png')
    
    return response

if __name__ == '__main__':
    app.run(debug=True)

