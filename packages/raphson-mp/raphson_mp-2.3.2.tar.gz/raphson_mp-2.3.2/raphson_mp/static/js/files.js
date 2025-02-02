const uploadQueue = [];

async function processQueue() {
    const file = uploadQueue.shift();
    console.debug('files: uploading file', file.name);

    const formData = new FormData();
    formData.append('csrf', document.getElementById('upload_csrf').value);
    formData.append('dir', document.getElementById('upload_dir').value)
    formData.append('upload', file);

    const response = await fetch('/files/upload', {
        method: 'POST',
        body: formData,
        redirect: 'manual',
    });

    if (!response.ok) {
        console.warn('Error during upload, add to queue');
        uploadQueue.push(file);
    }

    if (uploadQueue.length > 0) {
        processQueue();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    return;
    document.getElementById('upload-files-button').addEventListener('click', () => {
        document.getElementById('upload-files-button').setAttribute("disabled", "");
        document.getElementById('create-directory-button').removeAttribute("disabled");
        document.getElementById('upload-files-form').hidden = false;
        document.getElementById('create-directory-form').hidden = true;
    });
    document.getElementById('create-directory-button').addEventListener('click', () => {
        document.getElementById('create-directory-button').setAttribute("disabled", "");
        document.getElementById('upload-files-button').removeAttribute("disabled");
        document.getElementById('create-directory-form').hidden = false;
        document.getElementById('upload-files-form').hidden = true;
    });

    const dropzone = document.getElementById("dropzone");
    dropzone.ondragenter = (event) => {
        //event.stopPropagation();
        event.preventDefault(); // must be called for dropzone to be a valid drop target
        //dropzone.classList.add('hovering');
        console.debug('files: ondragenter');
    }

    dropzone.ondragover = (event) => {
        //event.stopPropagation();
        event.preventDefault(); // must be called for dropzone to be a valid drop target
        event.dataTransfer.dropEffect = 'copy';
        console.debug('files: ondragover');
    }

    dropzone.ondragleave = () => {
        dropzone.classList.remove('hovering');
        console.debug('files: ondragleave');
    }

    dropzone.ondrop = async function(event) {
        event.preventDefault(); // must be called to prevent default behaviour
        dropzone.classList.remove('hovering');

        console.debug('files: ondrop');

        const files = event.dataTransfer.files;
        console.debug('files: number of files', files.length);
        for (const file of files) {
            uploadFile(file);
        }
    }
});
