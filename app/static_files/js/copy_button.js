function copyToClipboard() {
    let short = document.getElementById("short");
    navigator.clipboard.writeText(short.innerText);
}
