// toggles visibility of element
toggle_visibility = function(id) {
    elem = document.getElementById(id);
    if (elem.className.indexOf('invisible')  -1) {
        elem.className = elem.className.replace('invisible', '');
    } else {
        elem.className += ' invisible';
    }
}