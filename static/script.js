const dropArea = document.getElementById('drop-area');
const fileListElement = document.getElementById('fileList');
const filesToConvert = [];
const qualityControl = document.getElementById('quality');
const qualityValueDisplay = document.getElementById('qualityValue');

// Update displayed quality value when slider changes
qualityControl.addEventListener('input', () => {
    qualityValueDisplay.textContent = qualityControl.value;
});

// Prevent default behavior (Prevent file from being opened)
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

dropArea.addEventListener('dragover', () => dropArea.classList.add('hover'));
dropArea.addEventListener('dragleave', () => dropArea.classList.remove('hover'));
dropArea.addEventListener('drop', handleDrop, false);

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
        filesToConvert.push(files[i]);
        const listItem = document.createElement('li');
        
        const fileName = document.createElement('span');
        fileName.textContent = files[i].name;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.className = 'delete-btn';
        deleteBtn.addEventListener('click', () => {
            filesToConvert.splice(i, 1);
            listItem.remove();
        });
        
        listItem.appendChild(fileName);
        listItem.appendChild(deleteBtn);
        fileListElement.appendChild(listItem);
    }
}

document.getElementById('convertBtn').addEventListener('click', () => {
    if (filesToConvert.length === 0) {
        alert("No files to convert. Please drag and drop files first.");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < filesToConvert.length; i++) {
        formData.append('files[]', filesToConvert[i]);
    }

    // Add the selected quality to the form data
    formData.append('quality', qualityControl.value);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.download_link) {
            document.getElementById('downloadLink').href = data.download_link;
            document.getElementById('downloadBtn').style.display = 'block';
            document.getElementById('downloadLink').innerText = `Download ${data.converted_count} photos`;
        } else {
            alert("Error converting files.");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error converting files.");
    });
});

document.getElementById('downloadBtn').addEventListener('click', () => {
    window.location.href = '/download';
});
