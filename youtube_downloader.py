from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import tempfile
import os
import logging

# Set Chromium executable path
os.environ["CHROME_PATH"] = "/usr/bin/chromium"

# Set Chromium data directory
os.environ["CHROME_DATA_DIR"] = "/root/.config/google-chrome"

os.environ["CHROME_EXTRA_ARGS"] = "--password-store=basic"

logging.basicConfig(level=logging.DEBUG)
logging.debug(f"CHROME_PATH: {os.environ['CHROME_PATH']}")
logging.debug(f"CHROME_DATA_DIR: {os.environ['CHROME_DATA_DIR']}")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["POST", "GET"])

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML file

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        video_url = data.get('url')
        custom_filename = data.get('filename')

        if not video_url:
            return jsonify({"error": "No URL provided"}), 400

        if not custom_filename:
            return jsonify({"error": "No file name provided"}), 400

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_filepath = temp_file.name
        temp_file.close()

        logging.debug(f"Temporary file path: {temp_filepath}")
        logging.debug(f"Video URL: {video_url}")
        logging.debug(f"Custom filename: {custom_filename}")

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': temp_filepath,
            'quiet': True,
            'nooverwrites': False,
            'cookiesfrombrowser': ('chrome', None, os.environ["CHROME_DATA_DIR"]),
            'postprocessors': [{
            'key': 'Exec',
            'exec_cmd': '--password-store=basic',  # Add this argument

            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)

        # Ensure the temporary file exists
        if not os.path.exists(temp_filepath):
            return jsonify({"error": "Downloaded file not found"}), 404

        # Append ".mp4" to the custom filename
        final_filename = f"{custom_filename}.mp4"
        logging.debug(f"Sending file: {temp_filepath} as {final_filename}")

        # Send the file to the browser
        response = send_file(temp_filepath, as_attachment=True, download_name=final_filename)

        # Delete the temporary file after sending
        @response.call_on_close
        def cleanup():
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)

        return response

    except yt_dlp.utils.DownloadError as e:
        logging.error("yt_dlp error:", exc_info=True)
        return jsonify({"error": f"Failed to process video: {str(e)}"}), 500
    except Exception as e:
        logging.error("Unexpected server error:", exc_info=True)
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Get the PORT from the environment
    app.run(debug=False, host='0.0.0.0', port=port)


# In order to run it you need to:
# run the server:
# python .\youtube_downloader.py
# enable the http server:
# python -m http.server
# Go to http://127.0.0.1:5000/