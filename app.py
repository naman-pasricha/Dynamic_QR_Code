import os
import uuid
import qrcode
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qrcodes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'generated_qrcodes'

db = SQLAlchemy(app)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class QRCodeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    target_url = db.Column(db.String(500), nullable=False)
    fill_color = db.Column(db.String(50), default='black')
    back_color = db.Column(db.String(50), default='white')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<QRCode {self.label}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    qrcodes = QRCodeData.query.order_by(QRCodeData.created_at.desc()).all()
    return render_template('index.html', qrcodes=qrcodes)

@app.route('/create', methods=['POST'])
def create_qr():
    label = request.form.get('label')
    target_url = request.form.get('target_url')
    
    fill_color = request.form.get('fill_color', 'black')
    back_color = request.form.get('back_color', 'white')
    
    if not label or not target_url:
        return redirect(url_for('index'))

    # Generate a unique short code
    short_code = str(uuid.uuid4())[:8]
    
    new_qr = QRCodeData(
        label=label, 
        short_code=short_code, 
        target_url=target_url,
        fill_color=fill_color,
        back_color=back_color
    )
    db.session.add(new_qr)
    db.session.commit()

    # Generate QR Code image using the Database ID for naming
    base_url = request.host_url.rstrip('/')
    redirect_url = f"{base_url}/r/{short_code}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(redirect_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    # Named as "1", "2", etc.
    img_name = f"{new_qr.id}.png"
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    img.save(img_path)

    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_qr(id):
    qr_entry = QRCodeData.query.get_or_404(id)
    new_target_url = request.form.get('target_url')
    new_label = request.form.get('label')
    new_fill = request.form.get('fill_color')
    new_back = request.form.get('back_color')
    
    if new_target_url:
        qr_entry.target_url = new_target_url
    if new_label:
        qr_entry.label = new_label
    
    # Check if colors changed to regenerate image
    regenerate = False
    if new_fill and new_fill != qr_entry.fill_color:
        qr_entry.fill_color = new_fill
        regenerate = True
    if new_back and new_back != qr_entry.back_color:
        qr_entry.back_color = new_back
        regenerate = True
        
    db.session.commit()

    if regenerate:
        # Regenerate QR image
        base_url = request.host_url.rstrip('/')
        redirect_url = f"{base_url}/r/{qr_entry.short_code}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(redirect_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=qr_entry.fill_color, back_color=qr_entry.back_color)
        img_name = f"{qr_entry.id}.png"
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img.save(img_path)

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_qr(id):
    qr_entry = QRCodeData.query.get_or_404(id)
    # Remove file named after ID
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{qr_entry.id}.png")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(qr_entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/r/<short_code>')
def redirect_to_url(short_code):
    qr_entry = QRCodeData.query.filter_by(short_code=short_code).first_or_404()
    return redirect(qr_entry.target_url)

@app.route('/generated/<filename>')
def serve_qr(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
