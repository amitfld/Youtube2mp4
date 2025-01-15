from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML file

@app.route('/download', methods=['POST'])
def download():
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
    temp_file.close()  # Close the file so yt_dlp can write to it

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'ffmpeg_location': r'C:\\Users\\amitf\\ffmpeg\\bin',
        'outtmpl': temp_filepath,  # Save directly to the temporary file
        'quiet': True,
        'nooverwrites': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)

        # Ensure the temporary file exists
        if not os.path.exists(temp_filepath):
            return jsonify({"error": "Downloaded file not found"}), 404

        # Append ".mp4" to the custom filename
        final_filename = f"{custom_filename}.mp4"
        print(f"Sending file: {temp_filepath} as {final_filename}")

        # Send the file to the browser
        response = send_file(temp_filepath, as_attachment=True, download_name=final_filename)

        # Delete the temporary file after sending
        @response.call_on_close
        def cleanup():
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)

        return response

    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the full traceback for debugging
        return jsonify({"error": str(e)}), 500


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