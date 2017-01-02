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
toggle_visibility_id = function(id) {
    var el = document.querySelector('#' + id);
    return toggle_visibility(el);
};

// toggles visibility of the element
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

// changes fontsize due to element width
change_fontsize = function (el, fcr) {
    var factor = fcr || 6 / 11;
    var fontsize = el.offsetWidth / (el.innerText.length * factor);
    el.style.fontSize = (fontsize > 19) ? '19px' : (fontsize < 10) ? '10px' : fontsize + 'px';
    return el.style.fontSize;
};

// onscroll event handler
window.onscroll = function() {
    var offset = window.pageYOffset || document.documentElement.scrollTop;
    var titlespan = document.querySelector('header .thread-title');
    var titleh1 = document.querySelector('h1.thread-title');
    if (titleh1) {
        if (offset > titleh1.offsetHeight + 8) {
            if (!titlespan) {
                var title = titleh1.innerHTML;
                titlespan = document.createElement('span');
                titlespan.className = 'thread-title';
                titlespan.innerHTML = title;
                titlespan = document.querySelector('header').appendChild(titlespan);
                change_fontsize(titlespan);
            }
        } else {
            if (titlespan) {
                titlespan.remove();
            }
        }
    }
};

// returns false if value of element is empty
check_empty = function(id) {
    text = document.querySelector('#' + id).value;

    return check_empty_string(text);
};

// returns false if string is empty
check_empty_string = function(str) {
    if (str.replace(/\s/g, '').length === 0) {
        return false;
    } else {
        return true;
    }
};

/* ------------------------------ ajax part ------------------------------ */

var div_backup = ''; // stores content of div.innerHTML for cancelling edit_message

message_edit = function(id) {
    var div = document.querySelector('#div' + id + ' .content');
    var wrapper = document.querySelector('#div' + id + ' .text');
    var actions = wrapper.querySelector('.actions');
    var links = actions.querySelectorAll('a');
    var checkbox = '<input type="checkbox" id="edit' + id + '"TODO><label for="edit' + id + '">Открыто для редактирования</label>';
    if (links.length < 5) {
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
                    var response = ajax.responseText;
                    var todo = response.slice(-4);
                    if (todo == "True") {
                        response = response.slice(0, -4);
                        todo = " checked";
                    } else {
                        response = response.slice(0, -5);
                        todo = "";
                    }
                    div.innerText = response;
                    for (i = 0; i < links.length; i++) {
                        toggle_visibility(links[i]);
                    }
                    actions.innerHTML = checkbox.replace('TODO', todo) + actions.innerHTML + '<a href="#" onclick="message_save(' + id +
                        ', false); return false;" /><i class="fa fa-times"></i></a>' + '<a href="#" onclick="message_save(' + id +
                        ', true); return false;" /><i class="fa fa-check"></i></a>';
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
        if (check_empty_string(div.innerText)) {
            var text = div.innerText;
            var editable = wrapper.querySelector('.actions input').checked;

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

                ajax.send([text, editable]);
            }
            var links = wrapper.querySelectorAll('.actions a');
            for (i = 0; i < links.length; i++) {
                toggle_visibility(links[i]);
            }
            var links = wrapper.querySelectorAll('.actions a.invisible');
            for (i = 0; i < links.length; i++) {
                links[i].remove();
            }
            wrapper.querySelector('.actions input').remove();
            wrapper.querySelector('.actions label').remove();
            div.contentEditable = false;
        }
    } else {
        div.innerHTML = div_backup;
        var links = wrapper.querySelectorAll('.actions a');
        for (i = 0; i < links.length; i++) {
            toggle_visibility(links[i]);
        }
        var links = wrapper.querySelectorAll('.actions a.invisible');
        for (i = 0; i < links.length; i++) {
            links[i].remove();
        }
        div.contentEditable = false;
    };
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
            link.style.cursor = 'default';
        } else {
            var div = wrapper.querySelector('.content');
            toggle_class(div, 'loading');
            var links = wrapper.querySelectorAll('.actions a:nth-child(n+2)');
            for (var i = 0; i < links.length; i++) {
                links[i].setAttribute('onclick', 'return false;');
                links[i].style.cursor = 'default';
            }
        }

        ajax.onreadystatechange = function () {
            if (ajax.readyState == 4 && ajax.status == 200) {
                var temp = document.createElement('div');
                temp.innerHTML = ajax.responseText;
                wrapper.parentNode.replaceChild(temp.firstElementChild, wrapper);
            }
        };

        ajax.send(null);
    }
};
