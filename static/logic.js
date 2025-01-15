const form = document.getElementById('downloadForm');
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const url = document.getElementById('youtubeUrl').value;
    const filename = document.getElementById('filename').value;

    try {
        const response = await fetch('https://youtube2mp4.onrender.com/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url, filename }),
        });

        if (!response.ok) {
            throw new Error('Server error');
        }

        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = downloadUrl;
        a.download = `${filename}.mp4`; // Use the provided filename
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (error) {
        alert('Error: Unable to process your request. ' + error.message);
    }
});
