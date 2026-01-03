function chargerDonnees()
{
    fetch('/donnees')
        .then(response => response.text())
        .then(data => {document.getElementById('donnees').innerHTML = data;})
}

setInterval(chargerDonnees, 1000);

