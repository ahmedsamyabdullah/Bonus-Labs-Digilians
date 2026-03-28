import os
import sys
from flask import Flask, request, jsonify

# --- LAB 1 BLOCKER: Environment Variable Check ---
# The application will immediately crash upon starting if FLASK_ENV is missing.
# This forces the K8s Pod into a CrashLoopBackOff state.
if not os.environ.get('FLASK_ENV'):
    print("FATAL ERROR: FLASK_ENV environment variable is missing.", file=sys.stderr)
    print("Application startup aborted.", file=sys.stderr)
    sys.exit(1) 

app = Flask(__name__)

# --- LAB 2 CONFIGURATION: ConfigMaps and Secrets ---
# These variables will be populated by the K8s ConfigMap and Secret.
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USERNAME', 'default_user')
DB_PASS = os.environ.get('DB_PASSWORD', 'default_pass')

# The target directory for the PersistentVolume mount
UPLOAD_FOLDER = '/app/uploads'

@app.route('/health', methods=['GET'])
def health():
    """Simple health check endpoint to verify routing and config."""
    return jsonify({
        "status": "healthy",
        "environment": os.environ.get('FLASK_ENV'),
        "db_configured": bool(os.environ.get('DB_HOST'))
    }), 200

@app.route('/upload', methods=['POST'])
def upload_image():
    """Endpoint to test PersistentVolumeClaim attachment and permissions."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # --- LAB 2 & 3 BLOCKER: Storage Permissions & Multi-Attach ---
    try:
        # Attempt to create directory or write to the designated volume mount path
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER) 

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path) 

        return jsonify({"message": f"Successfully uploaded {file.filename} to {UPLOAD_FOLDER}"}), 201

    except PermissionError:
        # This triggers the HTTP 500 error required for Lab 2 troubleshooting
        # when the non-root container user lacks write access to the mounted volume.
        return jsonify({"error": "HTTP 500: Permission Denied. Cannot write to the target directory."}), 500
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Binds to all interfaces (0.0.0.0) to ensure K8s networking can route traffic to the container
    app.run(host='0.0.0.0', port=8080)