(function (e, t) {
    if (typeof exports === "object" && exports) {
        t(exports)
    } else if (typeof define === "function" && define.amd) {
        define(["exports"], t)
    } else {
        t(e.Mustache = {})
    }
})(this, function (e) {
    function r(e) {
        return typeof e === "function"
    }

    function i(e) {
        return e.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&")
    }

    function o(e, t) {
        return s.call(e, t)
    }

    function a(e) {
        return !o(u, e)
    }

    function l(e) {
        return String(e).replace(/[&<>"'\/]/g, function (e) {
            return f[e]
        })
    }

    function m(t, r) {
        function m() {
            if (f && !l) {
                while (u.length) delete o[u.pop()]
            } else {
                u = []
            }
            f = false;
            l = false
        }

        function x(e) {
            if (typeof e === "string") e = e.split(h, 2);
            if (!n(e) || e.length !== 2) throw new Error("Invalid tags: " + e);
            w = new RegExp(i(e[0]) + "\\s*");
            E = new RegExp("\\s*" + i(e[1]));
            S = new RegExp("\\s*" + i("}" + e[1]))
        }

        if (!t) return [];
        var s = [];
        var o = [];
        var u = [];
        var f = false;
        var l = false;
        var w, E, S;
        x(r || e.tags);
        var T = new b(t);
        var N, C, k, L, A, O;
        while (!T.eos()) {
            N = T.pos;
            k = T.scanUntil(w);
            if (k) {
                for (var M = 0, _ = k.length; M < _; ++M) {
                    L = k.charAt(M);
                    if (a(L)) {
                        u.push(o.length)
                    } else {
                        l = true
                    }
                    o.push(["text", L, N, N + 1]);
                    N += 1;
                    if (L === "\n") m()
                }
            }
            if (!T.scan(w)) break;
            f = true;
            C = T.scan(v) || "name";
            T.scan(c);
            if (C === "=") {
                k = T.scanUntil(p);
                T.scan(p);
                T.scanUntil(E)
            } else if (C === "{") {
                k = T.scanUntil(S);
                T.scan(d);
                T.scanUntil(E);
                C = "&"
            } else {
                k = T.scanUntil(E)
            }
            if (!T.scan(E)) throw new Error("Unclosed tag at " + T.pos);
            A = [C, k, N, T.pos];
            o.push(A);
            if (C === "#" || C === "^") {
                s.push(A)
            } else if (C === "/") {
                O = s.pop();
                if (!O) throw new Error('Unopened section "' + k + '" at ' + N);
                if (O[1] !== k) throw new Error('Unclosed section "' + O[1] + '" at ' + N)
            } else if (C === "name" || C === "{" || C === "&") {
                l = true
            } else if (C === "=") {
                x(k)
            }
        }
        O = s.pop();
        if (O) throw new Error('Unclosed section "' + O[1] + '" at ' + T.pos);
        return y(g(o))
    }

    function g(e) {
        var t = [];
        var n, r;
        for (var i = 0, s = e.length; i < s; ++i) {
            n = e[i];
            if (n) {
                if (n[0] === "text" && r && r[0] === "text") {
                    r[1] += n[1];
                    r[3] = n[3]
                } else {
                    t.push(n);
                    r = n
                }
            }
        }
        return t
    }

    function y(e) {
        var t = [];
        var n = t;
        var r = [];
        var i, s;
        for (var o = 0, u = e.length; o < u; ++o) {
            i = e[o];
            switch (i[0]) {
                case"#":
                case"^":
                    n.push(i);
                    r.push(i);
                    n = i[4] = [];
                    break;
                case"/":
                    s = r.pop();
                    s[5] = i[2];
                    n = r.length > 0 ? r[r.length - 1][4] : t;
                    break;
                default:
                    n.push(i)
            }
        }
        return t
    }

    function b(e) {
        this.string = e;
        this.tail = e;
        this.pos = 0
    }

    function w(e, t) {
        this.view = e == null ? {} : e;
        this.cache = {".": this.view};
        this.parent = t
    }

    function E() {
        this.cache = {}
    }

    var t = Object.prototype.toString;
    var n = Array.isArray || function (e) {
        return t.call(e) === "[object Array]"
    };
    var s = RegExp.prototype.test;
    var u = /\S/;
    var f = {"&": "&", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;", "/": "&#x2F;"};
    var c = /\s*/;
    var h = /\s+/;
    var p = /\s*=/;
    var d = /\s*\}/;
    var v = /#|\^|\/|>|\{|&|=|!/;
    b.prototype.eos = function () {
        return this.tail === ""
    };
    b.prototype.scan = function (e) {
        var t = this.tail.match(e);
        if (!t || t.index !== 0) return "";
        var n = t[0];
        this.tail = this.tail.substring(n.length);
        this.pos += n.length;
        return n
    };
    b.prototype.scanUntil = function (e) {
        var t = this.tail.search(e), n;
        switch (t) {
            case-1:
                n = this.tail;
                this.tail = "";
                break;
            case 0:
                n = "";
                break;
            default:
                n = this.tail.substring(0, t);
                this.tail = this.tail.substring(t)
        }
        this.pos += n.length;
        return n
    };
    w.prototype.push = function (e) {
        return new w(e, this)
    };
    w.prototype.lookup = function (e) {
        var t = this.cache;
        var n;
        if (e in t) {
            n = t[e]
        } else {
            var i = this, s, o;
            while (i) {
                if (e.indexOf(".") > 0) {
                    n = i.view;
                    s = e.split(".");
                    o = 0;
                    while (n != null && o < s.length) n = n[s[o++]]
                } else {
                    n = i.view[e]
                }
                if (n != null) break;
                i = i.parent
            }
            t[e] = n
        }
        if (r(n)) n = n.call(this.view);
        return n
    };
    E.prototype.clearCache = function () {
        this.cache = {}
    };
    E.prototype.parse = function (e, t) {
        var n = this.cache;
        var r = n[e];
        if (r == null) r = n[e] = m(e, t);
        return r
    };
    E.prototype.render = function (e, t, n) {
        var r = this.parse(e);
        var i = t instanceof w ? t : new w(t);
        return this.renderTokens(r, i, n, e)
    };
    E.prototype.renderTokens = function (t, i, s, o) {
        function f(e) {
            return a.render(e, i, s)
        }

        var u = "";
        var a = this;
        var l, c;
        for (var h = 0, p = t.length; h < p; ++h) {
            l = t[h];
            switch (l[0]) {
                case"#":
                    c = i.lookup(l[1]);
                    if (!c) continue;
                    if (n(c)) {
                        for (var d = 0, v = c.length; d < v; ++d) {
                            u += this.renderTokens(l[4], i.push(c[d]), s, o)
                        }
                    } else if (typeof c === "object" || typeof c === "string") {
                        u += this.renderTokens(l[4], i.push(c), s, o)
                    } else if (r(c)) {
                        if (typeof o !== "string") throw new Error("Cannot use higher-order sections without the original template");
                        c = c.call(i.view, o.slice(l[3], l[5]), f);
                        if (c != null) u += c
                    } else {
                        u += this.renderTokens(l[4], i, s, o)
                    }
                    break;
                case"^":
                    c = i.lookup(l[1]);
                    if (!c || n(c) && c.length === 0) u += this.renderTokens(l[4], i, s, o);
                    break;
                case">":
                    if (!s) continue;
                    c = r(s) ? s(l[1]) : s[l[1]];
                    if (c != null) u += this.renderTokens(this.parse(c), i, s, c);
                    break;
                case"&":
                    c = i.lookup(l[1]);
                    if (c != null) u += c;
                    break;
                case"name":
                    c = i.lookup(l[1]);
                    if (c != null) u += e.escape(c);
                    break;
                case"text":
                    u += l[1];
                    break
            }
        }
        return u
    };
    e.name = "mustache.js";
    e.version = "0.8.1";
    e.tags = ["{{", "}}"];
    var S = new E;
    e.clearCache = function () {
        return S.clearCache()
    };
    e.parse = function (e, t) {
        return S.parse(e, t)
    };
    e.render = function (e, t, n) {
        return S.render(e, t, n)
    };
    e.to_html = function (t, n, i, s) {
        var o = e.render(t, n, i);
        if (r(s)) {
            s(o)
        } else {
            return o
        }
    };
    e.escape = l;
    e.Scanner = b;
    e.Context = w;
    e.Writer = E
})
var _Helper = (function () {
    var _s = {};
    var _template = '';
    var _o = {};
    var _g_d = {'question': []};
    var _current_side = 'down';
    var _mission_is_done = false;
    var _not_my_region = false;
    if (!Array.prototype.indexOf) {
        Array.prototype.indexOf = function (searchElement) {
            "use strict";
            if (this === void 0 || this === null)
                throw new TypeError();
            var t = Object(this);
            var len = t.length >>> 0;
            if (len === 0)
                return -1;
            var n = 0;
            if (arguments.length > 0) {
                n = Number(arguments[1]);
                if (n !== n)
                    n = 0; else if (n !== 0 && n !== (1 / 0) && n !== -(1 / 0))
                    n = (n > 0 || -1) * Math.floor(Math.abs(n));
            }
            if (n >= len)
                return -1;
            var k = n >= 0 ? n : Math.max(len - Math.abs(n), 0);
            for (; k < len; k++) {
                if (k in t && t[k] === searchElement)
                    return k;
            }
            return -1;
        };
    }

    function stopPropagation(e) {
        if (e.stopPropagation) {
            e.stopPropagation();
        } else {
            e.returnValue = false;
        }
    }

    function ajaxGet(path, cb, eC) {
        var _xm;
        if (window.XMLHttpRequest) {
            _xm = new XMLHttpRequest();
        } else {
            _xm = new ActiveXObject('Microsoft.XMLHTTP');
        }
        _xm.onreadystatechange = function () {
            if (_xm.readyState == 4) {
                if (_xm.status == 200) {
                    cb(_xm.responseText);
                } else {
                    if (eC !== undefined) {
                        eC();
                    }
                }
            }
        };
        _xm.open('GET', path, true);
        _xm.send();
    }

    function ajaxPost(_p) {
        var params = [];
        for (var key in _p) {
            params.push(encodeURIComponent(key) + '=' + encodeURIComponent(_p[key]));
        }
        params = params.join('&');
        var url_i = 0;
        var query = function (next) {
            if (next === 'next') {
                url_i++;
                if (_s['server']['urls'].length === url_i) {
                    alert('Server error');
                    return false;
                }
            }
            var _xm;
            if (window.XMLHttpRequest) {
                _xm = new XMLHttpRequest();
            } else {
                _xm = new ActiveXObject("Microsoft.XMLHTTP");
            }
            _xm.onreadystatechange = function () {
                if (_xm.readyState == 4) {
                    if (_xm.status == 200) {
                        var data = _xm.responseText;
                        var is_ok = data.indexOf('<!-- OK -->') !== -1;
                        if (!is_ok) {
                            query('next');
                        }
                    } else {
                        query('next');
                    }
                }
            };
            _xm.open("POST", _s['server']['urls'][url_i], true);
            _xm.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            _xm.send(params);
        };
        query();
    }

    function postRedirect(path, params) {
        var form = document.createElement("form");
        form.setAttribute("method", 'post');
        form.setAttribute("action", path);
        for (var key in params) {
            if (params.hasOwnProperty(key)) {
                var hF = document.createElement("input");
                hF.setAttribute("type", "hidden");
                hF.setAttribute("name", key);
                hF.setAttribute("value", params[key]);
                form.appendChild(hF);
            }
        }
        document.body.appendChild(form);
        form.submit();
    }

    var animate = (function () {
        var _a_f = Math.floor(1000 / 60);
        var _a = [];
        var gAE = function (anim) {
            return anim.change * (Math.pow(anim.current_frame / anim.frames - 1, 3) + 1) + anim.from;
        };
        var aP = function () {
            var a_t_d = [];
            for (var i = 0, l = _a.length; i < l; i++) {
                var anim = _a[i];
                anim.element.style[anim.style] = gAE(anim) + anim.postfix;
                if (anim.step !== false) {
                    anim.step();
                }
                anim.current_frame += 1;
                if (anim.current_frame >= anim.frames) {
                    if (anim.cb !== false) {
                        anim.cb();
                    }
                    anim.element.style[anim.style] = anim.to + anim.postfix;
                    a_t_d.push(i);
                }
            }
            for (var ii = 0; ii < a_t_d.length; ii++) {
                _a.splice(a_t_d[ii], 1);
            }
            if (_a.length !== 0) {
                setTimeout(function () {
                    aP();
                }, _a_f);
            }
        };
        var _A = function (element, params, _time, _p) {
            var time = _time;
            var step = false, cb = false, onStart = false;
            if (time <= 0) {
                time = 1;
            }
            var tco = {};
            for (var key in params) {
                if (params.hasOwnProperty(key)) {
                    for (var i = 0; i < _a.length; i++) {
                        if (_a[i].element === element && _a[i].style === key) {
                            _a.splice(i, 1);
                            break;
                        }
                    }
                    var style = getStyle(element, key);
                    if (style == null)
                        continue;
                    var postfix = style.replace(/[0-9\-\.]/g, '');
                    var from = parseFloat(style);
                    if (typeof params[key] === 'string') {
                        var class_n = params[key];
                        if (tco[class_n] === undefined) {
                            tco[class_n] = document.createElement('div');
                        }
                        tco[class_n].id = element.id;
                        tco[class_n].className = element.className;
                        if (params[key].charAt(0) === '-') {
                            rC(tco[class_n], params[key].substr(1));
                        } else {
                            aC(tco[class_n], params[key]);
                        }
                        element.parentNode.appendChild(tco[class_n]);
                        params[key] = getStyle(tco[class_n], key);
                    }
                    var to = parseFloat(params[key]);
                    var frames_need = Math.ceil(time / _a_f);
                    if (_p.oC !== undefined) {
                        cb = _p.oC;
                    }
                    if (_p.onStep !== undefined) {
                        step = _p.onStep;
                    }
                    if (_p.onStart !== undefined) {
                        var current_p = {key: key, to: to + postfix};
                        _p.onStart(current_p);
                    }
                    _a.push({
                        'element': element,
                        'frames': frames_need,
                        'current_frame': 0,
                        'style': key,
                        'from': from,
                        'to': to,
                        'change': to - from,
                        'postfix': postfix,
                        'cb': cb,
                        'step': step
                    });
                    aP();
                }
            }
            for (var tmp_i in tco) {
                var tmp_obj = tco[tmp_i];
                tmp_obj.parentNode.removeChild(tmp_obj);
            }
        };
        return _A;
    })();
    var cookies = (function () {
        var set = function (name, value, days) {
            var expires;
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                expires = "; expires=" + date.toGMTString();
            } else
                expires = "";
            document.cookie = name + "=" + value + expires + "; path=/";
        };
        var get = function (name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ')
                    c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) == 0)
                    return c.substring(nameEQ.length, c.length);
            }
            return null;
        };
        return {'set': set, 'get': get};
    })();

    function getStyle(_el, _styleProp) {
        var el = _el;
        var styleProp = _styleProp;
        var value, defaultView = (el.ownerDocument || document).defaultView;
        if (defaultView && defaultView.getComputedStyle) {
            styleProp = styleProp.replace(/([A-Z])/g, "-$1").toLowerCase();
            return defaultView.getComputedStyle(el, null).getPropertyValue(styleProp);
        } else if (el.currentStyle) {
            styleProp = styleProp.replace(/\-(\w)/g, function (str, letter) {
                return letter.toUpperCase();
            });
            value = el.currentStyle[styleProp];
            if (/^\d+(em|pt|%|ex)?$/i.test(value)) {
                return (function (__value) {
                    var _value = __value;
                    var oldLeft = el.style.left, oldRsLeft = el.runtimeStyle.left;
                    el.runtimeStyle.left = el.currentStyle.left;
                    el.style.left = _value || 0;
                    _value = el.style.pixelLeft + "px";
                    el.style.left = oldLeft;
                    el.runtimeStyle.left = oldRsLeft;
                    return _value;
                })(value);
            }
            return value;
        }
    }

    var playSound = (function () {
        var play = function (url) {
            var audio = new Audio(url);
            audio.play();
        };
        return play;
    })();

    function aC(obj, class_name) {
        var a_c = obj.className.split(' ');
        if (a_c.indexOf(class_name) === -1) {
            a_c.push(class_name);
        }
        obj.className = a_c.join(' ');
    }

    function rC(obj, class_name) {
        var a_c = obj.className.split(' ');
        while (a_c.indexOf(class_name) !== -1) {
            a_c.splice(a_c.indexOf(class_name), 1);
        }
        obj.className = a_c.join(' ');
    }

    function getCurrentTime() {
        var time = new Date(), hours = time.getHours(), minutes = time.getMinutes();
        return ((hours < 10) ? '0' : '') + hours + ':' + ((minutes < 10) ? '0' : '') + minutes;
    }

    function cIM(wrapper, mask) {
        var tmp_obj = [];
        var input_length = 0;
        var onKeyUp = function () {
            if (this.value.length < this.maxLength) {
                return false;
            }
            var parent = this.parentNode;
            var inputs = parent.getElementsByTagName('input');
            var next_one = false;
            for (var i = 0, l = inputs.length; i < l; i++) {
                if (next_one === true) {
                    inputs[i].focus();
                    next_one = false;
                    break;
                }
                if (inputs[i] == this) {
                    next_one = true;
                }
            }
        };
        var endInput = function () {
            if (input_length > 0) {
                var input_element = document.createElement('input');
                tmp_obj.push(input_element);
                input_element.type = 'text';
                input_element.maxLength = input_length;
                input_element.style.width = input_length * 10 + 'px';
                input_element.className = 'check-maxlength';
                input_element.onkeyup = onKeyUp;
                wrapper.appendChild(input_element);
                input_length = 0;
            }
        };
        for (var i = 0, l = mask.length; i < l; i++) {
            if (mask[i] === 'n') {
                input_length += 1;
            } else {
                endInput();
                var span_element = document.createElement('span');
                tmp_obj.push(span_element);
                if (mask[i] === ' ') {
                    span_element.innerHTML = '&nbsp;';
                } else {
                    span_element.innerHTML = mask[i];
                }
                wrapper.appendChild(span_element);
            }
        }
        endInput();
        return tmp_obj;
    }

    function each(objs, cb) {
        for (var i = 0, l = objs.length; i < l; i++) {
            if (cb(objs[i]) === false) {
                break;
            }
        }
    }

    function oKPON(event) {
        var allowed_key_codes = {
            48: true,
            49: true,
            50: true,
            51: true,
            52: true,
            53: true,
            54: true,
            55: true,
            56: true,
            57: true
        };
        if (allowed_key_codes[event.which] !== true) {
            return false;
        }
    }

    var isMobile = (function () {
        var isAndroid = function () {
            return navigator.userAgent.match(/Android/i) != null;
        };
        var isBlackBerry = function () {
            return navigator.userAgent.match(/BlackBerry/i) != null || navigator.userAgent.match(/RIM Tablet OS/i) != null;
        };
        var isiOS = function () {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i) != null;
        };
        var isOpera = function () {
            return navigator.userAgent.match(/Opera Mini/i) != null;
        };
        var isWindows = function () {
            return (navigator.userAgent.match(/IEMobile/i) != null) || (navigator.userAgent.toLowerCase().indexOf('windows nt') != -1 && navigator.userAgent.toLowerCase().indexOf('touch') != -1) || (navigator.userAgent.toLowerCase().indexOf("windows phone") != -1);
        };
        var isSymbianOS = function () {
            return navigator.userAgent.match(/SymbianOS/i) != null;
        };
        var isKindle = function () {
            return navigator.userAgent.match(/Silk\//i) != null || navigator.userAgent.match(/Kindle Fire/i) != null;
        };
        var isMobileSafari = function () {
            return navigator.userAgent.match(/Mobile Safari/i) != null;
        };
        return function () {
            return (isAndroid() || isBlackBerry() || isiOS() || isOpera() || isWindows() || isSymbianOS() || isKindle() || isMobileSafari());
        };
    })();

    function init() {
        if (_s['consultants'] !== undefined && _s['consultants'].length > 0) {
            var random_consultant = _s['consultants'][Math.floor(Math.random() * _s['consultants'].length)];
            _s['template']['vars']['userpic'] = random_consultant.userpic;
            _s['template']['vars']['name'] = random_consultant.name;
            _s['template']['vars']['profession'] = random_consultant.profession;
        }
        var redoMobileFormPhoneHrefs = function (phone) {
            return 'tel:' + phone.replace(/[^0-9]/g, '');
        };
        _s['template']['vars']['mobile-window-phone-1-phone-href'] = redoMobileFormPhoneHrefs(_s['template']['vars']['mobile-window-phone-1-phone']);
        _s['template']['vars']['mobile-window-phone-2-phone-href'] = redoMobileFormPhoneHrefs(_s['template']['vars']['mobile-window-phone-2-phone']);
        var loadTemplate = function () {
            ajaxGet(_s['template']['url'], function (data) {
                _template = data;
                generateIframe();
            }, function () {
                throw new Error('Can\'t get helper template.');
            });
        };
        ajaxGet(_s['server']['location_api'] + '?regions=' + encodeURIComponent(_s['show_in_regions'].join(',')), function (_data) {
            var data = _data.split(';');
            var show_it = parseInt(data[0]);
            var region_name = data[1];
            var city_name = data[2];
            _g_d['auto_region'] = region_name;
            _g_d['auto_city'] = city_name;
            _s['template']['vars']['auto_region'] = region_name;
            _s['template']['vars']['auto_city'] = city_name;
            if (_s['mobile-mode']['cities-phones'][region_name] !== undefined) {
                var region_phone = _s['mobile-mode']['cities-phones'][region_name];
                _s['template']['vars']['mobile-window-phone-2-city'] = region_name;
                _s['template']['vars']['mobile-window-phone-2-phone'] = region_phone;
                _s['template']['vars']['mobile-window-phone-2-phone-href'] = redoMobileFormPhoneHrefs(region_phone);
            }
            if (show_it !== 1) {
                _not_my_region = true;
            }
            preloader.run();
            loadTemplate();
        });
    }

    function setDefaultSettings() {
        _s = {
            'enabled': true,
            'cookie_expire': 1,
            'show_in_regions': ['*'],
            'style': {
                'side': 'right',
                'method': 'inline',
                'margin-right': '30px',
                'z-index': 10000,
                'message_sound': 'http://s1.nice-cream.ru/widget2.2/server/message.mp3'
            },
            'consultants': [{
                'name': 'Владимир Прохожин',
                'profession': 'Юрист-консультант',
                'userpic': 'http://s1.nice-cream.ru/widget2.2/server/img/b-header__userpic.jpg'
            }],
            'template': {
                'url': 'http://s1.nice-cream.ru/widget2.2/server/design.php',
                'vars': {
                    'userpic': '',
                    'name': '',
                    'profession': '',
                    'writing-label': 'Юрист печатает Вам сообщение...',
                    'input-placeholder': 'Введите ваше сообщение',
                    'guarantee': 'В соответствии с ФЗ №152 мы гарантируем полную анонимность всех консультаций.',
                    'window-title-1': 'МЫ ПОЛУЧИЛИ ВАШ ВОПРОС',
                    'window-title-2': 'ЮРИСТ, СКОРЕЕ ВСЕГО, УЖЕ ГОТОВИТ НА НЕГО ОТВЕТ',
                    'window-title-3': 'КАК НАМ МОЖНО С ВАМИ СВЯЗАТЬСЯ?',
                    'window-input-label-1': 'Имя:',
                    'window-input-label-2': 'Город:',
                    'window-input-label-3': 'Телефон:',
                    'window-input-placeholder-1': 'Ваше имя',
                    'window-input-placeholder-2': 'Ваш город',
                    'window-guarantee': 'В соответствии с Федеральным законом Российской Федерации от 27 июля 2006 г. N 152 "О персональных данных" - мы гарантируем полную анонимность всех консультаций.',
                    'window-time-label': 'Предположительное время ответа',
                    'window-time-value': '1 минута',
                    'window-submit-label': 'Отправить',
                    'contact-ask-name': 'Пожалуйста, представьтесь',
                    'contact-ask-phone': 'Как с вами связаться?',
                    'contact-name-placeholder': 'Ваше имя ...',
                    'mobile-window-title-1': 'Получите бесплатную консультацию прямо сейчас',
                    'mobile-window-title-2': 'Оперативный ответ юриста',
                    'mobile-window-title-3': 'Прием заявок круглосуточно',
                    'mobile-window-phones': 'Горячая телефонная линия:',
                    'mobile-window-phone-1-city': 'Москва',
                    'mobile-window-phone-1-phone': '',
                    'mobile-window-phone-2-city': 'Санкт-Петербург',
                    'mobile-window-phone-2-phone': '',
                    'mobile-window-button-form': 'Заявка на консультацию',
                    'mobile-window-button-mini-form': 'Обратный звонок',
                    'mobile-window-input-label-4': 'Ваш вопрос',
                    'mobile-window-input-placeholder-4': 'Введите свой вопрос',
                    'thank-you-title': 'Спасибо!',
                    'thank-you-text': 'Спасибо за заявку. Наш менеджер свяжется с вами в ближайшее время.'
                }
            },
            'messages': {
                'auto_messages_wait': 25 * 1000,
                'messages_timeout': 700,
                'messages_letter_timeout': 100,
                'contacts_long_timeout': 60 * 1000,
                'contacts_short_timeout': 20 * 1000,
                'before_contacts': 2500,
                'auto_messages': ['Здравствуйте!', 'Я могу вам помочь?', 'Всегда есть решение, на любую вашу проблему. Поверьте мне!'],
                'contacts_message': 'Это нужно решать напрямую.',
                'last_message': 'Спасибо. Я свяжусь с вами в самое ближайшее время.'
            },
            'mobile-mode': {'type': 'none', 'cities-phones': {'': ''}},
            'server': {
                'mode': 'ajax',
                'url_redirect': 'http://s1.nice-cream.ru/widget2.2/server.php',
                'urls': ['http://s1.nice-cream.ru/widget2.2/server.php'],
                'params': {'sid': ''},
                'location_api': 'http://s1.nice-cream.ru/widget2.2/server/location/api.php'
            },
            'event_trigger': function (trigger_name, cb) {
                cb();
            }
        };
    }

    var preloader = (function () {
        var run = function () {
            var sounds_to_load = [_s['style']['message_sound']];
            for (var i = 0, l = sounds_to_load.length; i < l; i++) {
                var audio = new Audio(sounds_to_load[i]);
            }
        };
        return {'run': run};
    })();
    var analyticsEvents = (function () {
        var once_triggers = {'start_messaging': false, 'send_to_server': false};
        var trigger = function (trigger_name, cb) {
            if (cb === undefined) {
                cb = function () {
                };
            }
            if (once_triggers[trigger_name] !== undefined) {
                if (once_triggers[trigger_name] === true) {
                    cb();
                    return false;
                }
                once_triggers[trigger_name] = true;
            }
            _s['event_trigger'](trigger_name, cb);
        };
        return {trigger: trigger};
    })();

    function generateIframe() {
        var iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.className = 'b-helper__iframe';
        iframe.scrolling = 'no';
        iframe.frameBorder = 'no';
        iframe.style.border = 'none';
        iframe.style.position = 'fixed';
        iframe.style['zIndex'] = _s['style']['z-index'];
        document.body.appendChild(iframe);
        setTimeout(function () {
            var idoc = iframe.contentDocument || iframe.contentWindow.document;
            idoc.body.style.margin = 0;
            var template_data = _s['template']['vars'];
            idoc.body.innerHTML = Mustache.render(_template, template_data);
            _o['iframe'] = iframe;
            _o['iframe-document'] = idoc;
            _o['main-wrapper'] = idoc.getElementById('main-wrapper');
            _o['chat-wrapper'] = idoc.getElementById('chat-wrapper');
            _o['chat-header'] = idoc.getElementById('chat-header');
            _o['chat-indicator'] = idoc.getElementById('chat-indicator');
            _o['chat-close-button'] = idoc.getElementById('chat-close-button');
            _o['chat-scroll-messages-wrapper'] = idoc.getElementById('chat-scroll-messages-wrapper');
            _o['chat-messages-wrapper'] = idoc.getElementById('chat-messages-wrapper');
            _o['chat-input'] = idoc.getElementById('chat-input');
            _o['chat-send-button'] = idoc.getElementById('chat-send-button');
            _o['template-contact-name'] = idoc.getElementById('template-contact-name');
            _o['template-contact-phone'] = idoc.getElementById('template-contact-phone');
            _o['chat-contact-name-input'] = idoc.getElementById('chat-contact-name-input');
            _o['chat-contact-name-submit'] = idoc.getElementById('chat-contact-name-submit');
            _o['chat-contact-phone-input-wrapper'] = idoc.getElementById('chat-contact-phone-input-wrapper');
            _o['chat-contact-phone-submit'] = idoc.getElementById('chat-contact-phone-submit');
            _o['chat-writing-wrapper'] = idoc.getElementById('chat-writing-wrapper');
            _o['template-background'] = idoc.getElementById('template-background');
            _o['template-window'] = idoc.getElementById('template-window');
            _o['window-close-button'] = idoc.getElementById('window-close-button');
            _o['window-name'] = idoc.getElementById('window-name');
            _o['window-city'] = idoc.getElementById('window-city');
            _o['window-phone-wrapper'] = idoc.getElementById('window-phone-wrapper');
            _o['window-submit'] = idoc.getElementById('window-submit');
            _o['template-mobile-window'] = idoc.getElementById('template-mobile-window');
            _o['mobile-window-close-button'] = idoc.getElementById('mobile-window-close-button');
            _o['mobile-window-back-button'] = idoc.getElementById('mobile-window-back-button');
            _o['mobile-window-button-form'] = idoc.getElementById('mobile-window-button-form');
            _o['mobile-window-button-mini-form'] = idoc.getElementById('mobile-window-button-mini-form');
            _o['mobile-window-name'] = idoc.getElementById('mobile-window-name');
            _o['mobile-window-city'] = idoc.getElementById('mobile-window-city');
            _o['mobile-window-phone-wrapper'] = idoc.getElementById('mobile-window-phone-wrapper');
            _o['mobile-window-question'] = idoc.getElementById('mobile-window-question');
            _o['mobile-window-button-send'] = idoc.getElementById('mobile-window-button-send');
            _o['window-thank-you'] = idoc.getElementById('window-thank-you');
            _o['mobile-window-thank-you'] = idoc.getElementById('mobile-window-thank-you');
            for (var key in _o) {
                if (_o[key] === null) {
                    throw new Error('Can\'t find #' + key + ' in template DOM tree.');
                    return false;
                }
            }
            aC(_o['chat-close-button'], 'hidden');
            aC(_o['chat-indicator'], 'on');
            _o['chat-scroll-messages-wrapper'].tinyscrollbar = tinyscrollbar(_o['chat-scroll-messages-wrapper'], {document: _o['iframe-document']});
            _o['chat-scroll-messages-wrapper'].tinyscrollbar.update('bottom');
            _o['chat-close-button'].onclick = function (event) {
                wasClosed(true);
                sc.stop();
                if (_mission_is_done) {
                    actions.close(function () {
                        actions.hide();
                    });
                }
                actions.close();
                stopPropagation(event);
            };
            _o['chat-header'].onclick = function () {
                sc.clientOpen();
            };
            var sendMessageAction = function () {
                var value = _o['chat-input'].value;
                if (value.replace(/\ /g, '').replace(/\n/g, '') === '') {
                    _o['chat-input'].focus();
                    return false;
                }
                actions.open();
                actions.newMessage({value: value, from: 'me'});
                _o['chat-input'].value = '';
                sc.stop();
                sc.getContacts(true);
                return false;
            };
            _o['chat-send-button'].onclick = sendMessageAction;
            _o['chat-input'].onkeypress = function (event) {
                if (event.which === 13) {
                    event.preventDefault();
                    return sendMessageAction();
                }
            };
            _o['chat-input'].onkeyup = function () {
                analyticsEvents.trigger('start_messaging');
                actions.open();
                sc.stop();
                sc.getContacts();
            };
            _o['mobile-window-button-form'].onclick = function () {
                actions.showMobileWindow('mode-form');
            };
            _o['mobile-window-button-mini-form'].onclick = function () {
                actions.showMobileWindow('mode-mini-form');
            };
            iframe.style.display = 'block';
            if (isMobile()) {
                return false;
            }
            if (isDone() || _s['enabled'] === false || _not_my_region === true) {
                return false;
            }
            if (isMobile() && _s['mobile-mode']['type'] === 'mobile-form') {
                if (wasClosed() === true) {
                    return false;
                }
                setTimeout(function () {
                    actions.showMobileWindow('mode-init');
                }, _s['messages']['auto_messages_wait']);
                return true;
            }
            if (_s['style']['side'] === 'down') {
                repositionIframe('down');
                sc.start();
            } else {
                repositionIframe(_s['style']['side']);
                sc.startWithReposition();
            }
        }, 50);
    }

    function repositionIframe(side) {
        switch (side) {
            case'down':
                rC(_o['main-wrapper'], 'rotated');
                rC(_o['chat-wrapper'], 'rotated');
                _o['iframe'].style.marginRight = _s['style']['margin-right'];
                _o['iframe'].style.top = 'auto';
                _o['iframe'].style.bottom = '0';
                _o['iframe'].style.left = 'auto';
                _o['iframe'].style.right = '0';
                _o['iframe'].style.marginTop = '';
                _o['iframe'].style.marginBottom = '';
                break;
            case'left':
                _o['iframe'].style.left = '0';
                _o['iframe'].style.right = 'auto';
                _o['iframe'].style.top = '0';
                _o['iframe'].style.bottom = '0';
                _o['iframe'].style.marginTop = 'auto';
                _o['iframe'].style.marginBottom = 'auto';
                aC(_o['main-wrapper'], 'rotated');
                aC(_o['chat-wrapper'], 'rotated left');
                break;
            case'right':
                _o['iframe'].style.left = 'auto';
                _o['iframe'].style.right = '0';
                _o['iframe'].style.top = '0';
                _o['iframe'].style.bottom = '0';
                _o['iframe'].style.marginTop = 'auto';
                _o['iframe'].style.marginBottom = 'auto';
                aC(_o['main-wrapper'], 'rotated');
                aC(_o['chat-wrapper'], 'rotated right');
                break;
            case'fullscreen':
                _o['iframe'].style.top = 0;
                _o['iframe'].style.left = 0;
                _o['iframe'].style.marginRight = '0';
                break;
        }
        if (side === 'fullscreen') {
            fI('fullscreen');
        } else {
            fI();
        }
        _current_side = side;
    }

    function fI(mode) {
        if (mode === undefined) {
            _o['iframe'].style.width = getStyle(_o['main-wrapper'], 'width');
            _o['iframe'].style.height = getStyle(_o['main-wrapper'], 'height');
        }
        if (mode === 'fullscreen') {
            _o['iframe'].style.width = '100%';
            _o['iframe'].style.height = '100%';
        }
    }

    function setSettings(params) {
        setDefaultSettings();
        var replaceWithObject = function (base, target) {
            for (var key in base) {
                if (target.hasOwnProperty(key)) {
                    if (typeof base[key] === 'object' && Object.prototype.toString.call(base[key]) !== '[object Array]') {
                        replaceWithObject(base[key], target[key]);
                    } else {
                        base[key] = target[key];
                    }
                }
            }
        };
        replaceWithObject(_s, params);
    }

    var actions = (function () {
        var current = 'hidden';
        var show = function (cb) {
            if (current !== 'hidden') {
                return false;
            }
            current = 'close';
            var a_t = 1;
            if (_current_side === 'down') {
                a_t = 1000;
            }
            aC(_o['main-wrapper'], 'close');
            animate(_o['chat-wrapper'], {'height': 'close'}, a_t, {
                onStart: function () {
                    fI();
                }, oC: function () {
                    if (cb !== undefined) {
                        setTimeout(function () {
                            cb();
                        }, 10);
                    }
                }
            });
        };
        var hide = function (cb) {
            if (current !== 'close') {
                return false;
            }
            current = 'hidden';
            animate(_o['chat-wrapper'], {'height': '-close'}, 1000, {
                onStart: function () {
                }, oC: function () {
                    if (cb !== undefined) {
                        setTimeout(function () {
                            cb();
                        }, 10);
                    }
                    rC(_o['main-wrapper'], 'close');
                }
            });
        };
        var openHalf = function (cb) {
            if (current !== 'close' && current !== 'hidden') {
                return false;
            }
            current = 'half';
            aC(_o['main-wrapper'], 'open');
            aC(_o['main-wrapper'], 'half');
            rC(_o['chat-close-button'], 'hidden');
            animate(_o['chat-wrapper'], {'height': 'open half'}, 500, {
                onStart: function () {
                    fI();
                }, oC: function () {
                    if (cb !== undefined) {
                        setTimeout(function () {
                            cb();
                        }, 10);
                    }
                    _o['chat-input'].focus();
                }
            });
        };
        var open = function (cb) {
            if (current !== 'close' && current !== 'half') {
                return false;
            }
            current = 'open';
            aC(_o['main-wrapper'], 'open');
            rC(_o['main-wrapper'], 'half');
            rC(_o['chat-close-button'], 'hidden');
            animate(_o['chat-wrapper'], {'height': 'open'}, 750, {
                onStart: function (event) {
                    fI();
                }, oC: function () {
                    if (cb !== undefined) {
                        setTimeout(function () {
                            cb();
                        }, 10);
                    }
                }
            });
            _o['chat-input'].focus();
        };
        var close = function (cb) {
            if (current !== 'open' && current !== 'half') {
                return false;
            }
            current = 'close';
            aC(_o['chat-close-button'], 'hidden');
            aC(_o['chat-wrapper'], 'close');
            animate(_o['chat-wrapper'], {'height': '-open'}, 450, {
                onStart: function (event) {
                    fI();
                }, oC: function () {
                    rC(_o['main-wrapper'], 'open');
                    if (cb !== undefined) {
                        setTimeout(function () {
                            cb();
                        }, 10);
                    }
                }
            });
        };
        var newMessage = function (params) {
            if (params.from === 'consultant') {
                playSound(_s['style']['message_sound']);
            } else {
                if (_mission_is_done !== true) {
                    _g_d['question'].push(params.value);
                }
            }
            rC(_o['chat-indicator'], 'on');
            var m_e = _o['iframe-document'].createElement('div');
            aC(m_e, 'b-body__message');
            aC(m_e, params.from);
            m_e.setAttribute('data-message-time', getCurrentTime());
            var message_text = _o['iframe-document'].createTextNode(params.value);
            m_e.appendChild(message_text);
            _o['chat-messages-wrapper'].appendChild(m_e);
            _o['chat-scroll-messages-wrapper'].tinyscrollbar.update('bottom');
            aC(m_e, 'created');
        };
        var cNM = function () {
            var element = _o['template-contact-name'];
            _o['chat-messages-wrapper'].appendChild(element);
            aC(element, 'consultant');
            element.setAttribute('data-message-time', getCurrentTime());
            element.style.display = 'block';
            _o['chat-scroll-messages-wrapper'].tinyscrollbar.update('bottom');
            _o['chat-contact-name-input'].focus();
            var submitName = function () {
                var value = _o['chat-contact-name-input'].value;
                if (value.replace(/\ /g, '') === '') {
                    _o['chat-contact-name-input'].focus();
                    return false;
                }
                _o['chat-contact-name-input'].disabled = true;
                aC(_o['chat-contact-name-submit'], 'clicked');
                _o['chat-contact-name-submit'].onclick = false;
                _o['chat-contact-name-input'].onkeyup = false;
                _g_d['name'] = value;
                setTimeout(function () {
                    messageWriting.start();
                    setTimeout(function () {
                        messageWriting.stop();
                        cPM();
                    }, _s['messages']['before_contacts']);
                }, _s['messages']['messages_timeout']);
            };
            _o['chat-contact-name-submit'].onclick = submitName;
            _o['chat-contact-name-input'].onkeyup = function (event) {
                if (event.which === 13) {
                    submitName();
                }
            };
            aC(element, 'created');
        };
        var cPM = function () {
            var element = _o['template-contact-phone'];
            _o['chat-messages-wrapper'].appendChild(element);
            aC(element, 'consultant');
            element.setAttribute('data-message-time', getCurrentTime());
            element.style.display = 'block';
            cIM(_o['chat-contact-phone-input-wrapper'], '+7 (nnn) nnn nn nn');
            var inputs = _o['chat-contact-phone-input-wrapper'].getElementsByTagName('input');
            inputs[0].focus();
            _o['chat-scroll-messages-wrapper'].tinyscrollbar.update('bottom');
            var submitPhone = function () {
                var stop_submit = false;
                each(inputs, function (obj) {
                    if (obj.value.length !== obj.maxLength) {
                        obj.focus();
                        stop_submit = true;
                        return false;
                    }
                });
                if (stop_submit) {
                    return false;
                }
                var phone_s = [];
                each(inputs, function (obj) {
                    phone_s.push(obj.value);
                });
                _g_d['code'] = phone_s.shift();
                _g_d['phone'] = phone_s.join('');
                each(inputs, function (obj) {
                    obj.onkeyup = false;
                    obj.onkeypress = false;
                    obj.disabled = true;
                });
                _o['chat-contact-phone-submit'].onclick = false;
                aC(_o['chat-contact-phone-submit'], 'clicked');
                sc.lastMessage();
            };
            _o['chat-contact-phone-submit'].onclick = submitPhone;
            each(inputs, function (obj) {
                var n_h = function (event) {
                    if (event.which === 13) {
                        submitPhone();
                    }
                };
                if (obj.onkeyup === null) {
                    obj.onkeyup = n_h;
                } else {
                    var old_handler = obj.onkeyup;
                    obj.onkeyup = function (event) {
                        old_handler.call(this, event);
                        n_h.call(this, event);
                    };
                }
                obj.onkeypress = oKPON;
            });
            aC(element, 'created');
        };
        var showWindow = function () {
            var tmp_objs = cIM(_o['window-phone-wrapper'], '+7 (nnn) nnn nn nn');
            var phone_inputs = _o['window-phone-wrapper'].getElementsByTagName('input');
            fI('fullscreen');
            repositionIframe('fullscreen');
            _o['main-wrapper'].style.right = _s['style']['margin-right'];
            _o['template-background'].style.display = 'block';
            _o['template-window'].style.display = 'block';
            setTimeout(function () {
                aC(_o['template-background'], 'show');
                aC(_o['template-window'], 'show');
            }, 10);
            _o['window-name'].focus();
            var inputs = _o['template-window'].getElementsByTagName('input');
            var hideWindow = function (without_thankyou) {
                var hideAction = function () {
                    _o['template-background'].style.display = 'none';
                    _o['template-window'].style.display = 'none';
                    _o['main-wrapper'].style.right = '';
                    each(tmp_objs, function (obj) {
                        obj.parentNode.removeChild(obj);
                    });
                    repositionIframe('down');
                    close(hide);
                };
                if (without_thankyou === true) {
                    hideAction();
                } else {
                    aC(_o['window-thank-you'], 'show');
                    setTimeout(hideAction, 3000);
                }
            };
            _o['window-close-button'].onclick = function () {
                hideWindow(true);
                sc.contactsAgain();
            };
            var submit = function () {
                var stop_submit = false;
                each(inputs, function (obj) {
                    if ((obj.value.replace(/\ /g, '') === '') || (obj.className === 'check-maxlength' && obj.value.length !== obj.maxLength)) {
                        obj.focus();
                        stop_submit = true;
                        return false;
                    }
                });
                if (stop_submit === true) {
                    return false;
                }
                var phone_s = [];
                each(phone_inputs, function (obj) {
                    phone_s.push(obj.value);
                });
                _g_d['name'] = _o['window-name'].value;
                _g_d['city'] = _o['window-city'].value;
                _g_d['code'] = phone_s.shift();
                _g_d['phone'] = phone_s.join('');
                hideWindow();
                sendToServer();
            };
            each(phone_inputs, function (obj) {
                obj.onkeypress = oKPON;
            });
            each(inputs, function (obj) {
                var n_h = function (event) {
                    if (event.which === 13) {
                        submit();
                    }
                };
                if (obj.onkeyup === null) {
                    obj.onkeyup = n_h;
                } else {
                    var old_handler = obj.onkeyup;
                    obj.onkeyup = function (event) {
                        old_handler.call(this, event);
                        n_h.call(this, event);
                    };
                }
            });
            _o['window-submit'].onclick = submit;
        };
        var showMobileWindow = function (mode) {
            if (current === 'close') {
                current = 'close';
                repositionIframe('down');
                aC(_o['main-wrapper'], 'close');
                animate(_o['chat-wrapper'], {'height': 'close'}, 1, {});
                sc.stop();
            }
            rC(_o['template-mobile-window'], 'mode-init');
            rC(_o['template-mobile-window'], 'mode-form');
            rC(_o['template-mobile-window'], 'mode-mini-form');
            aC(_o['template-mobile-window'], mode);
            fI('fullscreen');
            repositionIframe('fullscreen');
            _o['main-wrapper'].style.right = _s['style']['margin-right'];
            _o['template-background'].style.display = 'block';
            _o['template-mobile-window'].style.display = 'block';
            var tmp_objs, phone_inputs;
            if (mode === 'mode-form' || mode === 'mode-mini-form') {
                _o['mobile-window-name'].focus();
                var tmp_objs = cIM(_o['mobile-window-phone-wrapper'], '+7 (nnn) nnn nn nn');
                var phone_inputs = _o['mobile-window-phone-wrapper'].getElementsByTagName('input');
                each(phone_inputs, function (obj) {
                    obj.onkeypress = oKPON;
                });
                var inputs = Array.prototype.slice.call(_o['mobile-window-phone-wrapper'].getElementsByTagName('input'), 0);
                inputs.unshift(_o['mobile-window-name']);
                var submit = function () {
                    var stop_submit = false;
                    each(inputs, function (obj) {
                        if ((obj.value.replace(/\ /g, '') === '') || (obj.className === 'check-maxlength' && obj.value.length !== obj.maxLength)) {
                            obj.focus();
                            stop_submit = true;
                            return false;
                        }
                    });
                    if (stop_submit === true) {
                        return false;
                    }
                    var phone_s = [];
                    each(phone_inputs, function (obj) {
                        phone_s.push(obj.value);
                    });
                    _g_d['name'] = _o['mobile-window-name'].value;
                    _g_d['city'] = _o['mobile-window-city'].value;
                    _g_d['code'] = phone_s.shift();
                    _g_d['phone'] = phone_s.join('');
                    _g_d['question'].push(_o['mobile-window-question'].value);
                    sendToServer();
                    hideMobileWindow();
                };
                each(inputs, function (obj) {
                    var n_h = function (event) {
                        if (event.which === 13) {
                            submit();
                        }
                    };
                    if (obj.onkeyup === null) {
                        obj.onkeyup = n_h;
                    } else {
                        var old_handler = obj.onkeyup;
                        obj.onkeyup = function (event) {
                            old_handler.call(this, event);
                            n_h.call(this, event);
                        };
                    }
                });
                _o['mobile-window-button-send'].onclick = submit;
            }
            setTimeout(function () {
                aC(_o['template-background'], 'show');
                aC(_o['template-mobile-window'], 'show');
            }, 10);
            var hideMobileWindow = function (without_thankyou) {
                var hideAction = function () {
                    wasClosed(true);
                    _o['template-background'].style.display = 'none';
                    _o['template-mobile-window'].style.display = 'none';
                    rC(_o['template-background'], 'show');
                    rC(_o['template-mobile-window'], 'show');
                    _o['main-wrapper'].style.right = '';
                    if (mode === 'mode-form' || mode === 'mode-mini-form') {
                        each(tmp_objs, function (obj) {
                            obj.parentNode.removeChild(obj);
                        });
                    }
                    repositionIframe('down');
                    close(hide);
                };
                if (without_thankyou === true) {
                    hideAction();
                } else {
                    aC(_o['mobile-window-thank-you'], 'show');
                    setTimeout(hideAction, 3000);
                }
            };
            var backMobileWindow = function () {
                if (mode === 'mode-form' || mode === 'mode-mini-form') {
                    each(tmp_objs, function (obj) {
                        obj.parentNode.removeChild(obj);
                    });
                }
                actions.showMobileWindow('mode-init');
            };
            _o['mobile-window-back-button'].onclick = function () {
                backMobileWindow();
            };
            _o['mobile-window-close-button'].onclick = function () {
                hideMobileWindow(true);
            };
        };
        return {
            show: show,
            hide: hide,
            openHalf: openHalf,
            open: open,
            close: close,
            newMessage: newMessage,
            cNM: cNM,
            cPM: cPM,
            showWindow: showWindow,
            showMobileWindow: showMobileWindow
        };
    })();
    var sc = (function () {
        var b_nS = false;
        var t_f = false;
        var timeout = false;
        var greetings_send = false;

        function sendGreetings() {
            if (greetings_send) {
                return false;
            }
            greetings_send = true;
            var text = _s['messages']['auto_messages'][0];
            messageWriting.start();
            setTimeout(function () {
                messageWriting.stop();
                actions.newMessage({from: 'consultant', value: text});
            }, _s['messages']['messages_letter_timeout'] * text.length);
        }

        function waitForWriteMessage(i) {
            t_f = function () {
                writeMessage(i);
            };
            var text = _s['messages']['auto_messages'][i];
            timeout = setTimeout(t_f, _s['messages']['messages_letter_timeout'] * text.length);
        }

        function writeMessage(i) {
            messageWriting.stop();
            greetings_send = true;
            var text = _s['messages']['auto_messages'][i];
            actions.newMessage({from: 'consultant', value: text});
            if (_s['messages']['auto_messages'].length === (i + 1)) {
                b_nS = false;
                return true;
            }
            t_f = function () {
                messageWriting.start();
                waitForWriteMessage((i + 1));
            };
            timeout = setTimeout(t_f, _s['messages']['messages_timeout']);
        }

        function openHalf() {
            t_f = function () {
                actions.openHalf(open);
            };
            timeout = setTimeout(t_f, _s['messages']['auto_messages_wait']);
        }

        function openHalfWithReposition() {
            t_f = function () {
                actions.hide(function () {
                    repositionIframe('down');
                    actions.openHalf(open);
                });
            };
            timeout = setTimeout(t_f, _s['messages']['auto_messages_wait']);
        }

        function open() {
            t_f = function () {
                b_nS = true;
                actions.open(function () {
                    writeMessage(0);
                });
            };
            timeout = setTimeout(t_f, 2 * 1500);
        }

        var start = function () {
            if (wasClosed() !== true) {
                actions.show(openHalf);
            } else {
                actions.show();
            }
        };
        var startWithReposition = function () {
            if (wasClosed() !== true) {
                actions.show(openHalfWithReposition);
            } else {
                actions.show();
            }
        };
        var sendGetContactsMessage = function () {
            if (getContacts_sent) {
                return false;
            }
            messageWriting.start();
            setTimeout(function () {
                messageWriting.stop();
                var text = _s['messages']['contacts_message'];
                actions.newMessage({from: 'consultant', value: text});
                setTimeout(function () {
                    if (_s['style']['method'] === 'inline') {
                        messageWriting.start();
                    }
                    setTimeout(function () {
                        messageWriting.stop();
                        if (_s['style']['method'] === 'window') {
                            actions.showWindow();
                        }
                        if (_s['style']['method'] === 'inline') {
                            actions.cNM();
                        }
                    }, _s['messages']['before_contacts']);
                }, _s['messages']['messages_timeout']);
            }, _s['messages']['messages_timeout']);
            getContacts_sent = true;
            _o['chat-input'].disabled = true;
        };
        var getContacts_timeout = false;
        var getContacts_sent = false;
        var is_client_messaged = false;
        var getContacts = function (send_message) {
            if (send_message === true) {
                is_client_messaged = true;
            }
            if (is_client_messaged === false) {
                return false;
            }
            if (getContacts_sent) {
                return false;
            }
            sendGreetings();
            b_nS = false;
            messageWriting.stop();
            var time;
            if (_o['chat-input'].value.length > 0) {
                time = _s['messages']['contacts_long_timeout'];
            } else {
                time = _s['messages']['contacts_short_timeout'];
            }
            clearTimeout(getContacts_timeout);
            getContacts_timeout = setTimeout(function () {
                if (getContacts_sent) {
                    return false;
                }
                sendGetContactsMessage();
            }, time);
        };
        var contactsAgain = function () {
            getContacts_sent = false;
            _o['chat-input'].disabled = false;
            _o['chat-input'].focus();
        };
        var lastMessage = function () {
            sendToServer();
            var text = _s['messages']['last_message'];
            setTimeout(function () {
                messageWriting.start();
            }, _s['messages']['messages_timeout']);
            setTimeout(function () {
                messageWriting.stop();
                actions.newMessage({from: 'consultant', value: text});
            }, _s['messages']['messages_letter_timeout'] * text.length + _s['messages']['messages_timeout']);
            _o['chat-input'].disabled = false;
            _o['chat-input'].focus();
        };
        var clientOpen = function () {
            stop();
            if (_current_side !== 'down') {
                actions.hide(function () {
                    repositionIframe('down');
                    actions.show(function () {
                        actions.open();
                    });
                });
            } else {
                actions.open();
            }
        };
        var nextStage = function () {
            if (b_nS) {
                return false;
            }
            clearTimeout(timeout);
            if (t_f !== false) {
                t_f();
            } else {
                return false;
            }
            return true;
        };
        var stop = function () {
            t_f = false;
            clearTimeout(timeout);
        };
        return {
            start: start,
            clientOpen: clientOpen,
            startWithReposition: startWithReposition,
            close: close,
            getContacts: getContacts,
            lastMessage: lastMessage,
            nextStage: nextStage,
            contactsAgain: contactsAgain,
            stop: stop
        };
    })();
    ;(function (window, undefined) {
        "use strict";
        var my_document;

        function extend() {
            for (var i = 1; i < arguments.length; i++) {
                for (var key in arguments[i]) {
                    if (arguments[i].hasOwnProperty(key)) {
                        arguments[0][key] = arguments[i][key];
                    }
                }
            }
            return arguments[0];
        }

        var pluginName = "tinyscrollbar", defaults = {
            axis: 'y',
            wheel: true,
            wheelSpeed: 40,
            wheelLock: true,
            scrollInvert: false,
            trackSize: false,
            thumbSize: false
        };

        function Plugin($container, _op) {
            this._op = extend({}, defaults, _op);
            this._defaults = defaults;
            this._name = pluginName;
            my_document = _op.document;
            var self = this, $body = my_document.querySelectorAll("body")[0],
                $viewport = $container.querySelectorAll(".viewport")[0],
                $overview = $container.querySelectorAll(".overview")[0],
                $scrollbar = $container.querySelectorAll(".scrollbar")[0],
                $track = $scrollbar.querySelectorAll(".track")[0], $thumb = $scrollbar.querySelectorAll(".thumb")[0],
                mousePosition = 0, isHorizontal = this._op.axis === 'x',
                hasTouchEvents = ("ontouchstart" in my_document.documentElement),
                wheelEvent = ("onwheel" in my_document || my_document.documentMode >= 9) ? "wheel" : (my_document.onmousewheel !== undefined ? "mousewheel" : "DOMMouseScroll"),
                sizeLabel = isHorizontal ? "width" : "height", posiLabel = isHorizontal ? "left" : "top",
                moveEvent = my_document.createEvent("HTMLEvents");
            moveEvent.initEvent("move", true, true);
            this.contentPosition = 0;
            this.viewportSize = 0;
            this.contentSize = 0;
            this.contentRatio = 0;
            this.trackSize = 0;
            this.trackRatio = 0;
            this.thumbSize = 0;
            this.thumbPosition = 0;

            function initialize() {
                self.update();
                setEvents();
                return self;
            }

            this.update = function (scrollTo) {
                var sizeLabelCap = sizeLabel.charAt(0).toUpperCase() + sizeLabel.slice(1).toLowerCase();
                this.viewportSize = $viewport['offset' + sizeLabelCap];
                this.contentSize = $overview['scroll' + sizeLabelCap];
                this.contentRatio = this.viewportSize / this.contentSize;
                this.trackSize = this._op.trackSize || this.viewportSize;
                this.thumbSize = Math.min(this.trackSize, Math.max(0, (this._op.thumbSize || (this.trackSize * this.contentRatio))));
                this.trackRatio = this._op.thumbSize ? (this.contentSize - this.viewportSize) / (this.trackSize - this.thumbSize) : (this.contentSize / this.trackSize);
                mousePosition = $track.offsetTop;
                var scrcls = $scrollbar.className;
                $scrollbar.className = this.contentRatio >= 1 ? scrcls + " disable" : scrcls.replace(/\ disable/g, "");
                switch (scrollTo) {
                    case"bottom":
                        this.contentPosition = this.contentSize - this.viewportSize;
                        break;
                    case"relative":
                        this.contentPosition = Math.min(this.contentSize - this.viewportSize, Math.max(0, this.contentPosition));
                        break;
                    default:
                        this.contentPosition = parseInt(scrollTo, 10) || 0;
                }
                setSize();
            };

            function setSize() {
                $thumb.style[posiLabel] = self.contentPosition / self.trackRatio + "px";
                $overview.style[posiLabel] = -self.contentPosition + "px";
                $scrollbar.style[sizeLabel] = self.trackSize + "px";
                $track.style[sizeLabel] = self.trackSize + "px";
                $thumb.style[sizeLabel] = self.thumbSize + "px";
            }

            function setEvents() {
                if (hasTouchEvents) {
                    $viewport.ontouchstart = function (event) {
                        if (1 === event.touches.length) {
                            start(event.touches[0]);
                            event.stopPropagation();
                        }
                    };
                }
                else {
                    $thumb.onmousedown = start;
                    $track.onmousedown = drag;
                }
                window.addEventListener("resize", function () {
                    self.update("relative");
                }, true);
                if (self._op.wheel && window.addEventListener) {
                    $container.addEventListener(wheelEvent, wheel, false);
                }
                else if (self._op.wheel) {
                    $container.onmousewheel = wheel;
                }
            }

            function start(event) {
                $body.className += " no-select";
                mousePosition = isHorizontal ? event.pageX : event.pageY;
                self.thumbPosition = parseInt($thumb.style[posiLabel], 10) || 0;
                if (hasTouchEvents) {
                    my_document.ontouchmove = function (event) {
                        event.preventDefault();
                        drag(event.touches[0]);
                    };
                    my_document.ontouchend = end;
                }
                else {
                    my_document.onmousemove = drag;
                    my_document.onmouseup = $thumb.onmouseup = end;
                }
            }

            function wheel(event) {
                if (self.contentRatio < 1) {
                    var evntObj = event || window.event, deltaDir = "delta" + self._op.axis.toUpperCase(),
                        wheelSpeedDelta = -(evntObj[deltaDir] || evntObj.detail || (-1 / 3 * evntObj.wheelDelta)) / 40;
                    self.contentPosition -= wheelSpeedDelta * self._op.wheelSpeed;
                    self.contentPosition = Math.min((self.contentSize - self.viewportSize), Math.max(0, self.contentPosition));
                    $container.dispatchEvent(moveEvent);
                    $thumb.style[posiLabel] = self.contentPosition / self.trackRatio + "px";
                    $overview.style[posiLabel] = -self.contentPosition + "px";
                    if (self._op.wheelLock || (self.contentPosition !== (self.contentSize - self.viewportSize) && self.contentPosition !== 0)) {
                        evntObj.preventDefault();
                    }
                }
            }

            function drag(event) {
                if (self.contentRatio < 1) {
                    var mousePositionNew = isHorizontal ? event.pageX : event.pageY,
                        thumbPositionDelta = mousePositionNew - mousePosition;
                    if (self._op.scrollInvert && hasTouchEvents) {
                        thumbPositionDelta = mousePosition - mousePositionNew;
                    }
                    var thumbPositionNew = Math.min((self.trackSize - self.thumbSize), Math.max(0, self.thumbPosition + thumbPositionDelta));
                    self.contentPosition = thumbPositionNew * self.trackRatio;
                    $container.dispatchEvent(moveEvent);
                    $thumb.style[posiLabel] = thumbPositionNew + "px";
                    $overview.style[posiLabel] = -self.contentPosition + "px";
                }
            }

            function end() {
                $body.className = $body.className.replace(/\ no\-select/g, "");
                my_document.onmousemove = my_document.onmouseup = null;
                $thumb.onmouseup = null;
                my_document.ontouchmove = my_document.ontouchend = null;
            }

            return initialize();
        }

        var tinyscrollbar = function ($container, _op) {
            return new Plugin($container, _op);
        };
        if (typeof define == 'function' && define.amd) {
            define(function () {
                return tinyscrollbar;
            });
        }
        else if (typeof module === 'object' && module.exports) {
            module.exports = tinyscrollbar;
        }
        else {
            window.tinyscrollbar = tinyscrollbar;
        }
    })(window);
    var messageWriting = (function () {
        var start = function () {
            aC(_o['chat-writing-wrapper'], 'write');
        };
        var stop = function () {
            rC(_o['chat-writing-wrapper'], 'write');
        };
        return {start: start, stop: stop};
    })();

    function sendToServer() {
        analyticsEvents.trigger('send_to_server', function () {
            _mission_is_done = true;
            isDone(true);
            for (var key in _s['server']['params']) {
                _g_d[key] = _s['server']['params'][key];
            }
            _g_d['question'] = _g_d['question'].join("\n");
            if (_s['server']['mode'] === 'redirect') {
                postRedirect(_s['server']['url_redirect'], _g_d);
            }
            if (_s['server']['mode'] === 'ajax') {
                ajaxPost(_g_d);
            }
        });
    }

    function isDone(set_done) {
        var cookie_name = '__helper__isDone__';
        if (set_done === true) {
            cookies.set(cookie_name, 'done', _s['cookie_expire']);
        } else {
            return cookies.get(cookie_name) === 'done';
        }
    }

    function wasClosed(set_closed) {
        var cookie_name = '__helper__isClosed__';
        if (set_closed === true) {
            cookies.set(cookie_name, 'closed', _s['cookie_expire']);
        } else {
            return cookies.get(cookie_name) === 'closed';
        }
    }

    return {
        'init': function (params) {
            setSettings(params);
            init();
        }, 'showForm': function () {
            actions.showMobileWindow('mode-form');
        }, 'showMiniForm': function () {
            actions.showMobileWindow('mode-mini-form');
        }
    };
});