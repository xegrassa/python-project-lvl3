window.ngs_avc = /(;\s*|^)ngs_avc=(\d+)/.exec(document.cookie + '; ngs_avc=' + (Math.random()*12|0))[2]*1;

var googletag = googletag || {};
googletag.cmd = googletag.cmd || [];
(function() {
    var gads = document.createElement('script');
    gads.async = true;
    gads.src = 'https://www.googletagservices.com/tag/js/gpt.js';
    document.head.appendChild(gads);
})();

var ngs_al = {
    dfpCalls: [],
    dfpSeals: 1,
    dfpProcess: function () {
        if (--ngs_al.dfpSeals) return;

        var callsDone = {};
        [
            /^(?!googletag\.(define|enableServices|display))/,
            /^(?!googletag\.(enableServices|display))/,
            /^(?!googletag\.display)/,
            /^/
        ].forEach(function (re) {
            ngs_al.dfpCalls.forEach(function (dfpCall) {
                if (!callsDone[dfpCall] && re.test(dfpCall)) {
                    callsDone[dfpCall] = googletag.cmd.push(new Function(dfpCall));
                }
            });
        });

        ngs_al.dfpProcess = new Function;
        ngs_al.dfpCalls = {
            push: function () {
                googletag.cmd.push(new Function([].slice.call(arguments).join('\n')));
            }
        }
    }
};

window.addEventListener('DOMContentLoaded', ngs_al.dfpProcess, false);

function albex(pid, w, h, l, t) {
    if (typeof(pid) != 'undefined') {
        var o = document.getElementById('ap' + pid);

        if (o) {
            if (typeof(w) != 'undefined') {
                o.style.position = 'absolute';
                o.style.zIndex = '999';

                if (typeof(l) != 'undefined') {
                    o.style.left = '-' + l + 'px';
                    o.style.top = '-' + t + 'px';
                }

                if (w) {
                    o.style.width = w + 'px';
                }

                if (h) {
                    o.style.height = h + 'px';
                }

                if (typeof o.SetVariable != 'function') {
                    o.SetVariable('expand', '1');
                }

            } else {
                o.style.position = '';
                o.style.zIndex = '';
                o.style.width = '100%';
                o.style.height = o.parentNode.style.height || o.parentNode.parentNode.style.height;
                o.style.left = '0';
                o.style.top = '';

                if (typeof o.SetVariable != 'function') {
                    o.SetVariable('expand', '');
                }
            }
        }
    }
};

function fr3(v, t, into, style) {

    var placeId = /id=\"ap([0-9]+)|pid=([0-9]+)/.exec(t);
    if (placeId) {
        placeId = placeId[1] || placeId[2];
        if (localStorage.getItem('closedPlace'+placeId) > new Date().getTime() - 14400000) {//Баннер скрыли меньше 4х часов назад
            return;
        } else {
            localStorage.removeItem('closedPlace'+placeId);
        }
    }

    if (document.titlebk === undefined) document.titlebk = document.title;

    if (into === undefined) {
        document.write(t);
    } else {
        intoBlk = document.getElementById('ngs-al-' + into);
        if (intoBlk) {
            if (t != '') {
                intoBlk.innerHTML = t;
                if (style) {
                    intoBlk.style.cssText = style + intoBlk.style.cssText;
                }
                intoBlk.style.display = '';
            } else {
                intoBlk.style.display = 'none';
            }
        } else {
            window.ngs_async_banners = window.ngs_async_banners || {};
            window.ngs_async_banners[into] = t;
        }
    }
};

function fr3ck() {
    if (window.ngs_async_banners) {
        for (var into in window.ngs_async_banners) {
            var t = window.ngs_async_banners[into];
            intoBlk = document.getElementById('ngs-al-' + into);
            if (intoBlk) {
                if (t != '') {
                    intoBlk.innerHTML = t;
                    intoBlk.style.display = '';
                } else {
                    intoBlk.style.display = 'none';
                }
            }
        }
    }

    window.setTimeout(
        function(){
            if (document.titlebk !== undefined) document.title = document.titlebk;

            if (document.getElementsByClassName) {
                var o = document.getElementsByClassName('advplace-num');
                if (o.length) {
                    o[0].scrollIntoView(false);
                }
            }

            var adp_params = /(?:(?:_adpreview|_apx|_aph)=[^&]+&?){3,}/.exec(window.location.search);
            if (adp_params) {
                var script = document.createElement('script');
                script.src = '//reklama.ngs.ru/placen.js?' + adp_params[0];
                document.body.appendChild(script);
            }

            if (document.cookie.indexOf('_adpreview=') != -1) {
                var o = document.getElementById('ap' + /(;\s*|^)_adpreview=(\d+)/.exec(document.cookie)[2]);
                if (o) {
                    o.scrollIntoView(false);
                } else {
                    document.body.parentNode.removeChild(document.body);
                }
            }
        },
        500
    );

    window.advSizeUp = window.setInterval(
        function () {
            var f = false;
            var objs = document.getElementsByTagName('div');
            if (objs.length) {
                var o, s, i = 0;
                while (o = objs.item(i++)) {
                    if (o.className.match(/^advplace-preview/) && (s = o.getElementsByTagName('span')) && s[0].className == 'size') {
                        s[0].innerHTML = ' / ' + o.scrollWidth + '*' + o.scrollHeight;
                        f = true;
                    }
                }
            }
            if (!f) {
                window.clearInterval(window.advSizeUp);
            }
        },
        500
    );

    document.cookie = 'ngs_avc='+((ngs_avc+1)%12)+'; expires='+(new Date((new Date()).getTime() + 600000000)).toGMTString()+'; path=/';
};

function ngs_adplace(pid, params, into) {
    if (/string|number/.test(typeof params)) {
        into = params;
        params = {}
    }

    params = params || {};

    var qs = 'pid=' + pid;

    qs += '&sn=' + (params['sn'] || location.hostname);

    qs += '&hh=' + location.hostname;

    qs += '&ru=' + (params['ru'] || location.pathname).slice(1);

    qs += '&ts=' + (new Date().getTime() / 1000 | 0);

    qs += '&avc=' + ngs_avc;

    var adp_params = /(?:(?:_adpreview|_apx|_aph)=[^&]+&?)+/.exec(window.location.search);
    if(adp_params) {
        qs = adp_params[0] + '&' + qs;
    }

    if (into === undefined) {
        document.write('<script src="//reklama.ngs.ru/ap-js/?' + qs + '"></script>');
    } else {
        qs += '&asb=' + into;

        var s = document.createElement("script");
        s.src = '//reklama.ngs.ru/ap-js/?' + qs;
        s.async = true;
        s.addEventListener('load', ngs_al.dfpProcess, false);
        s.addEventListener('error', ngs_al.dfpProcess, false);
        document.body.appendChild(s);
        ngs_al.dfpSeals++;
    }
}

window.addEventListener('load', fr3ck, false);

window.alLoadUnload = function me () {
    if (me.locked) {
        if (!me.waiting) {
            me.waiting = true;
            setTimeout(function () {me.locked = false; me();}, 200);
        }
        return;
    }
    me.locked = true;
    me.waiting = false;
    var objs = document.getElementsByTagName('iframe');
    if (objs.length) {
        var o, i = 0;
        while (o = objs.item(i++)) {
            if (!o.getAttribute('data-src-al')) {
                continue;
            }

            var rect = o.getBoundingClientRect();

            var vpHeight = window.innerHeight || document.documentElement.clientHeight;
            var vpWidth = window.innerWidth || document.documentElement.clientWidth;

            if (
                rect.bottom >= (-vpHeight / 2) &&
                rect.right >= (-vpWidth / 2) &&
                rect.top <= (vpHeight * 1.5) &&
                rect.left <= (vpWidth * 1.5)
            ) {
                if (!o.alActive) {
                    o.contentWindow.location.replace(o.getAttribute('data-src-al'));
                    o.alActive = true;
                } else {
                    //o.contentWindow.postMessage('start', '*');
                }
            } else {
                if (rect.width * rect.height > 100000 && rect.width > rect.height && rect.width < rect.height * 3) {
                    continue;
                }

                if (o.alActive) {
                    o.contentWindow.location.replace('about:blank');
                    o.alActive = false;
                }
                //o.contentWindow.postMessage('pause', '*');
            }
        }
    }
};

['DOMContentLoaded', 'load', 'scroll', 'resize', 'visibilitychange'].forEach(function (e) {
    (e == 'visibilitychange' ? document : window).addEventListener(e, window.alLoadUnload, false);
});
