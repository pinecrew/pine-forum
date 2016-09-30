// toggles visibility of the element by id
// input = id of element which visibility will be toggled
toggle_visibility_id = function(id) {
    var el = document.querySelector('#' + id);
    return toggle_visibility(el);
}

// toggles visibility of the element
// input = element which visibility will be toggled
toggle_visibility = function(el) {
    if (el.className.indexOf('invisible') > -1) {
        el.className = el.className.replace('invisible', '');
        return true; // become visible
    } else {
        el.className = (el.className + ' invisible').replace('  ', ' ');
        return false; // become invisible
    }
}

// fade-in by creating a link
// id = id of element which will be shown in front of link
fade_in = function(id) {
    if (toggle_visibility_id(id)) {
        a = document.createElement("a");
        a.className = "fade-in";
        a.onclick = function() { document.body.removeChild(a); toggle_visibility_id(id); return false; };
        document.body.appendChild(a);
    }
}

edit_message = function(id) {
    var form = document.querySelector('#form_' + id);
    var els = document.querySelectorAll('#m' + id + ' div.text > *:not(header)');
    for (var i = 0; i < els.length; i++) {
        toggle_visibility(els[i]);
    }
    if (toggle_visibility(form)) {
        var textarea = form.querySelector('textarea');
        textarea.style.height = textarea.scrollHeight + 'px';
    }
}
