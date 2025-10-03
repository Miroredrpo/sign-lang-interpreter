document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const predictionResult = document.getElementById('prediction-result');

    // Connect to the Socket.IO server
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    // Get access to the webcam
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                video.play();
            })
            .catch(err => {
                console.error("Error accessing webcam: ", err);
            });
    }

    // Send a frame to the server every 100ms
    setInterval(() => {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const data = canvas.toDataURL('image/jpeg');
            socket.emit('image', data);
        }
    }, 100);

    // Receive and display the prediction from the server
    socket.on('prediction_result', data => {
        if (predictionResult) {
            predictionResult.innerHTML = `<h2 class="display-4 text-center">Predicted Letter: ${data.letter}</h2>`;
        }
    });
});