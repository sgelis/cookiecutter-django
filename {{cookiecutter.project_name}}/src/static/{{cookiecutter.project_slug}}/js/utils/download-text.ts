export default function(fileName: string, fileContent: string): void {
    const elt = document.createElement("a");
    elt.setAttribute("href", `data:text/plain;charset=utf-8,${encodeURIComponent(fileContent)}`);
    elt.setAttribute("download", fileName);
    elt.style.display = "none";
    document.body.appendChild(elt);

    elt.click();

    document.body.removeChild(elt);
}
