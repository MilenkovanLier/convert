
const dropArea = document.getElementById('drop-area');
const fileListElement = document.getElementById('fileList'); // Correct reference to fileList
const filesToConvert = []; // Array to hold the files to be converted

// Prevent default behavior (Prevent file from being opened)
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight the drop area when item is dragged over it
dropArea.addEventListener('dragover', () => dropArea.classList.add('hover'));
dropArea.addEventListener('dragleave', () => dropArea.classList.remove('hover'));

// Handle dropped files
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
        
        // Create file name text
        const fileName = document.createElement('span');
        fileName.textContent = files[i].name;
        
        // Create delete button
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.className = 'delete-btn';
        deleteBtn.addEventListener('click', () => {
            // Remove file from the filesToConvert array
            filesToConvert.splice(i, 1);
            // Remove the list item from the DOM
            listItem.remove();
            alert(`File ${files[i].name} has been removed.`);
        });
        
        listItem.appendChild(fileName);
        listItem.appendChild(deleteBtn);
        fileListElement.appendChild(listItem);
    }

    alert(`${filesToConvert.length} files added. Press 'Convert' to process them.`);
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

    // Disable convert button while processing
    document.getElementById('convertBtn').disabled = true;
    document.getElementById('convertBtn').textContent = 'Converting...';

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
    })
    .finally(() => {
        document.getElementById('convertBtn').disabled = false;
        document.getElementById('convertBtn').textContent = 'Convert';
    });
});

document.getElementById('downloadBtn').addEventListener('click', () => {
    window.location.href = '/download';
});
