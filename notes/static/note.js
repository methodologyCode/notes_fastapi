const getForm = document.getElementById('getNoteForm')

getForm.addEventListener('submit', function (event) {
    event.preventDefault();
    getNote();
});


async function getNote() {
    const noteId = document.getElementById('noteId').value;
    const getSecretPhrase = document.getElementById('getSecretPhrase').value;
    const config = {
            method: 'POST',
            body: JSON.stringify({ note_id: noteId, note_secret: getSecretPhrase }),
            headers: {
                'Content-Type': 'application/json'
            }
    }

    const request = await fetch('/get_note', config)
    const data = await request.json()

    if (data.response === "ok") {
        document.location.href = "/note_page/" + data.note_final_text
    }

}