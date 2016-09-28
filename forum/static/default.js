// toggles visibility of the element by id
// input = id of element which visibility will be toggled
toggle_visibility = function(id) {
    var elem = document.getElementById(id);
    if (elem.className.indexOf('invisible') > -1) {
        elem.className = elem.className.replace('invisible', '');
        return true;
    } else {
        elem.className = (elem.className + ' invisible').replace('  ', ' ');
        return false;
    }
}

// toggles visibility of the element
// input = element which visibility will be toggled
toggle_visibility_elem = function(elem) {
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
    frm = document.getElementById('form_' + id);
    toggle_visibility_elem(frm);
    var elems = document.getElementById('m' + id).querySelectorAll('div.text > *:not(header)');
    for (var i = 0; i < elems.length; i++) {
        toggle_visibility_elem(elems[i]);        
    }
}
