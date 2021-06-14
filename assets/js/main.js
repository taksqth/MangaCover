const input = document.querySelector('#cover-upload');
const preview = document.querySelector('.preview');
const result = document.querySelector('.result');

input.addEventListener('change', updateImageDisplay);

function updateImageDisplay() {
    while (preview.firstChild) {
        preview.removeChild(preview.firstChild);
    }

    if (input.files.length === 0) {
        const para = document.createElement('p');
        para.textContent = 'No files currently selected for upload';
        preview.appendChild(para);
    } else {
        const file = input.files[0];
        const fileDiv = document.createElement('div');
        const para = document.createElement('p');
        if (validFileType(file)) {
            para.textContent = `File name ${file.name}, file size ${returnFileSize(file.size)}.`;
            const image = document.createElement('img');
            image.src = URL.createObjectURL(file);

            fileDiv.appendChild(image);
            fileDiv.appendChild(para);
        } else {
            para.textContent = `File name ${file.name}: Not a valid file type. Update your selection.`;
            fileDiv.appendChild(para);
        }

        preview.appendChild(fileDiv);
    }
}

const fileTypes = [
    "image/apng",
    "image/bmp",
    "image/gif",
    "image/jpeg",
    "image/pjpeg",
    "image/png",
    "image/svg+xml",
    "image/tiff",
    "image/webp",
    "image/x-icon"
];

function validFileType(file) {
    return fileTypes.includes(file.type);
}

function returnFileSize(number) {
    if (number < 1024) {
        return number + 'bytes';
    } else if (number >= 1024 && number < 1048576) {
        return (number / 1024).toFixed(1) + 'KB';
    } else if (number >= 1048576) {
        return (number / 1048576).toFixed(1) + 'MB';
    }
}

window.addEventListener("load", function () {
    function sendData() {
        const XHR = new XMLHttpRequest();
        const FD = new FormData(form);

        while (result.firstChild) {
            result.removeChild(result.firstChild);
        }

        // Define what happens on successful data submission
        XHR.addEventListener("load", function (event) {
            const para = document.createElement('p');
            para.textContent = event.target.responseText;
            result.appendChild(para);
        });

        // Define what happens in case of error
        XHR.addEventListener("error", function (event) {
            const para = document.createElement('p');
            para.textContent = 'Oops! Something went wrong.';
            result.appendChild(para);
        });

        // Set up our request
        XHR.open("POST", "https://southamerica-east1-manga-classifier.cloudfunctions.net/predict-image");

        // The data sent is what the user provided in the form
        XHR.send(FD);
    }

    // Access the form element...
    const form = document.getElementById("cover-form");

    // ...and take over its submit event.
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        sendData();
    });
});