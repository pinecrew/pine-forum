// toggles class on element
toggle_class = function(el, name) {
    if (el.className.indexOf(name) > -1) {
        el.className = el.className.replace(name, '');
        return true; // added class
    } else {
        el.className = (el.className + ' ' + name).replace('  ', ' ');
        return false; // removed class
    }
};

// toggles visibility of the element by id
// input = id of element which visibility will be toggled
toggle_visibility_id = function(id) {
    var el = document.querySelector('#' + id);
    return toggle_visibility(el);
};

// toggles visibility of the element
// input = element which visibility will be toggled
toggle_visibility = function(el) {
    return toggle_class(el, 'invisible');
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

var div_backup = ''; // stores content of div.innerHTML for cancelling edit_message

message_edit = function(id) {
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
                        '<a href="#" onclick="message_save(' + id + ', true); return false;" />Сохранить</a>' +
                        '<a href="#" onclick="message_save(' + id + ', false); return false;" />Отменить</a>' +
                        '<div/>';
                    div.focus();
                }
            };

            ajax.send(null);
        }
    }
};

message_save = function(id, send) {
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
            toggle_class(div, 'loading');

            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    div.innerHTML = ajax.responseText;
                    toggle_class(div, 'loading');
                }
            };

            ajax.send(text);
        }
    } else {
        div.innerHTML = div_backup;
    }
    wrapper.removeChild(wrapper.querySelector('.controls'));
    div.contentEditable = false;
};

message_del_res = function(id, post) {
    // 'get' = !post = restore message
    // 'post' = post =  delete message
    var wrapper = document.querySelector('#div' + id);

    var ajax = false;
    if (window.XMLHttpRequest) {
        ajax = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
        ajax = new ActiveXObject('Microsoft.XMLHTTP');
    }

    if (ajax) {
        ajax.open(post ? 'POST' : 'GET', '/message/' + id + '_t/');
        if (!post) {
            var link = wrapper.querySelector('.text a');
            toggle_class(link, 'loading');
            link.setAttribute('onclick', 'return false;');
        } else {
            var div = wrapper.querySelector('.content');
            toggle_class(div, 'loading');
            var links = wrapper.querySelectorAll('.actions a:nth-child(n+2)');
            for (var i = 0; i < links.length; i++) {
                links[i].setAttribute('onclick', 'return false;');
            }
        }

        ajax.onreadystatechange = function () {
            if (ajax.readyState == 4 && ajax.status == 200) {
                var temp = document.createElement('div');
                temp.innerHTML = ajax.responseText;
                wrapper.parentNode.replaceChild(temp.firstChild, wrapper);
            }
        };

        ajax.send(null);
    }
};
