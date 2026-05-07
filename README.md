# QRFlow | Dynamic QR Code Generator

**Live Demo:** [https://dynamic-qr-code-6864.onrender.com/](https://dynamic-qr-code-6864.onrender.com/)

A Python-based Dynamic QR Code generator that allows you to change the destination URL of a QR code without changing the QR code itself.

## Features
- **Dynamic Links**: Update the destination URL anytime.
- **Premium UI**: Modern dark-mode dashboard with glassmorphism.
- **SQLite Database**: Stores all your QR mappings locally.
- `app.py`: Main Flask application and database models.
- `requirements.txt`: Python dependencies.
- `templates/index.html`: Dashboard template.
- `static/css/style.css`: Premium styling.
- `generated_qrcodes/`: Storage for generated QR images.
- **Instant Generation**: Uses the `qrcode` library to generate high-quality codes.
- **Downloadable**: Save your QR codes as PNG files.

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Dashboard**:
   Open your browser and go to `http://127.0.0.1:5000`

## How it Works
1. When you create a QR code, the app generates a unique **Short Code**.
2. The QR code points to `http://your-server/r/SHORT_CODE`.
3. When someone scans it, the server looks up the current **Target URL** in the database and redirects them.
4. If you update the Target URL, the QR code remains the same because it still points to the same redirect path!

## File Structure
- `app.py`: Main Flask application and database models.
- `requirements.txt`: Python dependencies.
- `templates/index.html`: Dashboard template.
- `static/css/style.css`: Premium styling.
- `Generated QR CODES/`: Storage for generated QR images.
