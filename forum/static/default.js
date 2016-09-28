// toggles visibility of the element
// id = id of element which visibility will be toggled
toggle_visibility = function(id) {
    elem = document.getElementById(id);
    console.log(elem.className.indexOf('invisible'));
    if (elem.className.indexOf('invisible') > -1) {
        elem.className = elem.className.replace('invisible', '');
        return true;
    } else {
        elem.className = (elem.className + ' invisible').replace('  ', ' ');
        return false;
    }
}

// fade-in by creating a link
// id = id of element which will be shown in front of link
fade_in = function(id) {
    if (toggle_visibility(id)) {
        a = document.createElement("a");
        a.className = "fade-in";
        a.onclick = function() { document.body.removeChild(a); toggle_visibility(id); return false; };
        document.body.appendChild(a);
    }
}

edit_message = function(id) {
    elem = document.getElementById('form_' + id);
    div = document.getElementById('m' + id).querySelectorAll('div.text')[0];
    toggle_visibility(div);
    toggle_visibility(elem);
}
