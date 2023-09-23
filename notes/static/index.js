const noteForm = document.getElementById('noteForm')

noteForm.addEventListener('submit', function (event) {
    event.preventDefault();
    getRequest();
})


async function getRequest() {
    const secretPhrase = document.getElementById('secretPhrase').value;
    const noteText = document.getElementById('noteText').value;
    const config = {
            method: 'POST',
            body: JSON.stringify({ text: noteText, secret: secretPhrase }),
            headers: {
                'Content-Type': 'application/json'
            }
    }

    const request = await fetch('/create_note', config)
    const data = await request.json()
    
    if (data.response === "ok") {
        document.location.href = "/result/" + data.note_id
    }

    document.getElementById('secretPhrase').value = '';
    document.getElementById('noteText').value = '';

}