// toggles visibility of the element by id
// input = id of element which visibility will be toggled
toggle_visibility_id = function(id) {
    var el = document.querySelector('#' + id);
    return toggle_visibility(el);
};

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
};

// fade-in by creating a link
// id = id of element which will be shown in front of link
fade_in = function(id) {
    if (toggle_visibility_id(id)) {
        a = document.createElement("a");
        a.className = "fade-in";
        a.onclick = function() { document.body.removeChild(a); toggle_visibility_id(id); return false; };
        document.body.appendChild(a);
    }
};

var div_backup = '';

edit_message = function(id) {
    var div = document.querySelector('#div' + id + ' .content');
    var wrapper = document.querySelector('#div' + id + ' .text');
    if (!wrapper.querySelector('.controls')) {
        div_backup = div.innerHTML;
        
        var ajax = false;
        if (window.XMLHttpRequest) {
            ajax = new XMLHttpRequest();
        } else if (window.ActiveXObject) {
            ajax = new ActiveXObject('Microsoft.XMLHTTP');
        }
        
        if (ajax) {
            ajax.open('GET', '/message/' + id);
            
            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    div.contentEditable = true;
                    div.innerText = ajax.responseText;
                    wrapper.innerHTML += '<div class="controls">' +
                        '<a href="#" onclick="save_message(' + id + ', true); return false;" />Сохранить</a>' +
                        '<a href="#" onclick="save_message(' + id + ', false); return false;" />Отменить</a>' +
                        '<div/>';
                    div.focus();
                }
            };
            
            ajax.send(null);
        }
    }
};

save_message = function(id, send) {
    var div = document.querySelector('#div' + id + ' .content');
    var wrapper = document.querySelector('#div' + id + ' .text');
    if (send) {
        var text = div.innerText;
        
        var ajax = false;
        if (window.XMLHttpRequest) {
            ajax = new XMLHttpRequest();
        } else if (window.ActiveXObject) {
            ajax = new ActiveXObject('Microsoft.XMLHTTP');
        }
        
        if (ajax) {
            ajax.open('POST', '/message/' + id + '/');
            ajax.setRequestHeader('Content-Type', 'text/plain');
            
            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    div.innerHTML = ajax.responseText;
                    console.log(ajax.responseText);
                }
            };
            
            ajax.send('message_text=' + text);
        }
    } else {
        div.innerHTML = div_backup;
    }
    wrapper.removeChild(wrapper.querySelector('.controls'));
    div.contentEditable = false;
};
