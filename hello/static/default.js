// toggles visibility of element
toggle_visibility = function(id) {
    elem = document.getElementById(id);
    if (elem.className.indexOf('invisible') > -1) {
        a = document.createElement("a");
        a.className = "fade-in";
        a.onclick = function() { document.body.removeChild(a); toggle_visibility(id) };
        document.body.appendChild(a);
        elem.className = elem.className.replace('invisible', '');
    } else {
        elem.className += ' invisible';
    }
}