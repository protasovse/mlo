/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 5);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = ({
    created() {},
    computed: {
        error() {
            return this.$store.state.is_error;
        },
        success() {
            return this.$store.state.is_success;
        },
        error_txt() {
            return this.$store.state.error_txt;
        },
        success_txt() {
            return this.$store.state.success_txt;
        },
        loading() {
            return this.$store.state.loading;
        }
    },
    beforeMount() {
        this.$store.commit('init_state');
    },
    methods: {
        start_loading() {
            this.$store.commit('start_loading');
        },
        stop_loading() {
            this.$store.commit('stop_loading');
        },
        password_vaidate() {
            if (this.password !== this.re_password) {
                throw new Error('Пароли не совпадают');
            }
        },
        requires_fields() {
            if (this.get_requires_fields === undefined) {
                return;
            }
            if (!this.get_requires_fields().every(function (x) {
                return x !== '';
            })) {
                throw new Error('Введите данные');
            }
        },
        form_validate(fns) {
            fns.forEach(fn => {
                fn();
            });
        },
        set_form_error(txt) {
            this.$store.commit('set_error', {
                txt: txt
            });
            this.stop_loading();
        },
        set_form_success(txt) {
            this.$store.commit('set_success', {
                txt: txt
            });
            this.stop_loading();
        },
        process_success(r, succes_fn) {
            this.stop_loading();
            if (r.data.success === false) {
                if (r.data.error !== undefined) {
                    throw new Error(r.data.error);
                } else {
                    throw new Error(this.default_error());
                }
            } else {
                succes_fn(r.data);
            }
        },
        default_error() {
            return 'Что-то пошло не так';
        },
        process_error(r, fn = undefined) {
            this.stop_loading();
            if (fn === undefined) {
                if (r.data.error !== undefined) {
                    throw new Error(r.data.error);
                } else {
                    throw new Error(this.default_error());
                }
            } else {
                console.log(r);
                fn(r);
            }
        },
        get(url, params, fn, fn_error = undefined) {
            this.start_loading();
            this.$http.get(url, { params: params }, { emulateJSON: true }).then(r => {
                this.process_success(r, fn);
            }, r => {
                this.process_error(r, fn_error);
            }).catch(e => this.set_form_error(e.message));
        },
        post(url, params, fn, fn_error = undefined) {
            this.start_loading();
            this.$http.post(url, params, { emulateJSON: true }).then(r => this.process_success(r, fn), r => this.process_error(r, fn_error)).catch(e => this.set_form_error(e.message));
        }

    }
});

/***/ }),
/* 1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = ({
    beforeCreate: function () {
        this.$http.get('/api/user/check').then(r => {
            if (r.data.success === true) {
                window.location.href = '/';
            }
        });
    }
});

/***/ }),
/* 2 */
/***/ (function(module, exports) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
module.exports = function (useSourceMap) {
	var list = [];

	// return the list of modules as css string
	list.toString = function toString() {
		return this.map(function (item) {
			var content = cssWithMappingToString(item, useSourceMap);
			if (item[2]) {
				return "@media " + item[2] + "{" + content + "}";
			} else {
				return content;
			}
		}).join("");
	};

	// import a list of modules into the list
	list.i = function (modules, mediaQuery) {
		if (typeof modules === "string") modules = [[null, modules, ""]];
		var alreadyImportedModules = {};
		for (var i = 0; i < this.length; i++) {
			var id = this[i][0];
			if (typeof id === "number") alreadyImportedModules[id] = true;
		}
		for (i = 0; i < modules.length; i++) {
			var item = modules[i];
			// skip already imported module
			// this implementation is not 100% perfect for weird media query combinations
			//  when a module is imported multiple times with different media queries.
			//  I hope this will never occur (Hey this way we have smaller bundles)
			if (typeof item[0] !== "number" || !alreadyImportedModules[item[0]]) {
				if (mediaQuery && !item[2]) {
					item[2] = mediaQuery;
				} else if (mediaQuery) {
					item[2] = "(" + item[2] + ") and (" + mediaQuery + ")";
				}
				list.push(item);
			}
		}
	};
	return list;
};

function cssWithMappingToString(item, useSourceMap) {
	var content = item[1] || '';
	var cssMapping = item[3];
	if (!cssMapping) {
		return content;
	}

	if (useSourceMap && typeof btoa === 'function') {
		var sourceMapping = toComment(cssMapping);
		var sourceURLs = cssMapping.sources.map(function (source) {
			return '/*# sourceURL=' + cssMapping.sourceRoot + source + ' */';
		});

		return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
	}

	return [content].join('\n');
}

// Adapted from convert-source-map (MIT)
function toComment(sourceMap) {
	// eslint-disable-next-line no-undef
	var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
	var data = 'sourceMappingURL=data:application/json;charset=utf-8;base64,' + base64;

	return '/*# ' + data + ' */';
}

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/

var stylesInDom = {};

var	memoize = function (fn) {
	var memo;

	return function () {
		if (typeof memo === "undefined") memo = fn.apply(this, arguments);
		return memo;
	};
};

var isOldIE = memoize(function () {
	// Test for IE <= 9 as proposed by Browserhacks
	// @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
	// Tests for existence of standard globals is to allow style-loader
	// to operate correctly into non-standard environments
	// @see https://github.com/webpack-contrib/style-loader/issues/177
	return window && document && document.all && !window.atob;
});

var getElement = (function (fn) {
	var memo = {};

	return function(selector) {
		if (typeof memo[selector] === "undefined") {
			var styleTarget = fn.call(this, selector);
			// Special case to return head of iframe instead of iframe itself
			if (styleTarget instanceof window.HTMLIFrameElement) {
				try {
					// This will throw an exception if access to iframe is blocked
					// due to cross-origin restrictions
					styleTarget = styleTarget.contentDocument.head;
				} catch(e) {
					styleTarget = null;
				}
			}
			memo[selector] = styleTarget;
		}
		return memo[selector]
	};
})(function (target) {
	return document.querySelector(target)
});

var singleton = null;
var	singletonCounter = 0;
var	stylesInsertedAtTop = [];

var	fixUrls = __webpack_require__(23);

module.exports = function(list, options) {
	if (typeof DEBUG !== "undefined" && DEBUG) {
		if (typeof document !== "object") throw new Error("The style-loader cannot be used in a non-browser environment");
	}

	options = options || {};

	options.attrs = typeof options.attrs === "object" ? options.attrs : {};

	// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
	// tags it will allow on a page
	if (!options.singleton && typeof options.singleton !== "boolean") options.singleton = isOldIE();

	// By default, add <style> tags to the <head> element
	if (!options.insertInto) options.insertInto = "head";

	// By default, add <style> tags to the bottom of the target
	if (!options.insertAt) options.insertAt = "bottom";

	var styles = listToStyles(list, options);

	addStylesToDom(styles, options);

	return function update (newList) {
		var mayRemove = [];

		for (var i = 0; i < styles.length; i++) {
			var item = styles[i];
			var domStyle = stylesInDom[item.id];

			domStyle.refs--;
			mayRemove.push(domStyle);
		}

		if(newList) {
			var newStyles = listToStyles(newList, options);
			addStylesToDom(newStyles, options);
		}

		for (var i = 0; i < mayRemove.length; i++) {
			var domStyle = mayRemove[i];

			if(domStyle.refs === 0) {
				for (var j = 0; j < domStyle.parts.length; j++) domStyle.parts[j]();

				delete stylesInDom[domStyle.id];
			}
		}
	};
};

function addStylesToDom (styles, options) {
	for (var i = 0; i < styles.length; i++) {
		var item = styles[i];
		var domStyle = stylesInDom[item.id];

		if(domStyle) {
			domStyle.refs++;

			for(var j = 0; j < domStyle.parts.length; j++) {
				domStyle.parts[j](item.parts[j]);
			}

			for(; j < item.parts.length; j++) {
				domStyle.parts.push(addStyle(item.parts[j], options));
			}
		} else {
			var parts = [];

			for(var j = 0; j < item.parts.length; j++) {
				parts.push(addStyle(item.parts[j], options));
			}

			stylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};
		}
	}
}

function listToStyles (list, options) {
	var styles = [];
	var newStyles = {};

	for (var i = 0; i < list.length; i++) {
		var item = list[i];
		var id = options.base ? item[0] + options.base : item[0];
		var css = item[1];
		var media = item[2];
		var sourceMap = item[3];
		var part = {css: css, media: media, sourceMap: sourceMap};

		if(!newStyles[id]) styles.push(newStyles[id] = {id: id, parts: [part]});
		else newStyles[id].parts.push(part);
	}

	return styles;
}

function insertStyleElement (options, style) {
	var target = getElement(options.insertInto)

	if (!target) {
		throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");
	}

	var lastStyleElementInsertedAtTop = stylesInsertedAtTop[stylesInsertedAtTop.length - 1];

	if (options.insertAt === "top") {
		if (!lastStyleElementInsertedAtTop) {
			target.insertBefore(style, target.firstChild);
		} else if (lastStyleElementInsertedAtTop.nextSibling) {
			target.insertBefore(style, lastStyleElementInsertedAtTop.nextSibling);
		} else {
			target.appendChild(style);
		}
		stylesInsertedAtTop.push(style);
	} else if (options.insertAt === "bottom") {
		target.appendChild(style);
	} else if (typeof options.insertAt === "object" && options.insertAt.before) {
		var nextSibling = getElement(options.insertInto + " " + options.insertAt.before);
		target.insertBefore(style, nextSibling);
	} else {
		throw new Error("[Style Loader]\n\n Invalid value for parameter 'insertAt' ('options.insertAt') found.\n Must be 'top', 'bottom', or Object.\n (https://github.com/webpack-contrib/style-loader#insertat)\n");
	}
}

function removeStyleElement (style) {
	if (style.parentNode === null) return false;
	style.parentNode.removeChild(style);

	var idx = stylesInsertedAtTop.indexOf(style);
	if(idx >= 0) {
		stylesInsertedAtTop.splice(idx, 1);
	}
}

function createStyleElement (options) {
	var style = document.createElement("style");

	options.attrs.type = "text/css";

	addAttrs(style, options.attrs);
	insertStyleElement(options, style);

	return style;
}

function createLinkElement (options) {
	var link = document.createElement("link");

	options.attrs.type = "text/css";
	options.attrs.rel = "stylesheet";

	addAttrs(link, options.attrs);
	insertStyleElement(options, link);

	return link;
}

function addAttrs (el, attrs) {
	Object.keys(attrs).forEach(function (key) {
		el.setAttribute(key, attrs[key]);
	});
}

function addStyle (obj, options) {
	var style, update, remove, result;

	// If a transform function was defined, run it on the css
	if (options.transform && obj.css) {
	    result = options.transform(obj.css);

	    if (result) {
	    	// If transform returns a value, use that instead of the original css.
	    	// This allows running runtime transformations on the css.
	    	obj.css = result;
	    } else {
	    	// If the transform function returns a falsy value, don't add this css.
	    	// This allows conditional loading of css
	    	return function() {
	    		// noop
	    	};
	    }
	}

	if (options.singleton) {
		var styleIndex = singletonCounter++;

		style = singleton || (singleton = createStyleElement(options));

		update = applyToSingletonTag.bind(null, style, styleIndex, false);
		remove = applyToSingletonTag.bind(null, style, styleIndex, true);

	} else if (
		obj.sourceMap &&
		typeof URL === "function" &&
		typeof URL.createObjectURL === "function" &&
		typeof URL.revokeObjectURL === "function" &&
		typeof Blob === "function" &&
		typeof btoa === "function"
	) {
		style = createLinkElement(options);
		update = updateLink.bind(null, style, options);
		remove = function () {
			removeStyleElement(style);

			if(style.href) URL.revokeObjectURL(style.href);
		};
	} else {
		style = createStyleElement(options);
		update = applyToTag.bind(null, style);
		remove = function () {
			removeStyleElement(style);
		};
	}

	update(obj);

	return function updateStyle (newObj) {
		if (newObj) {
			if (
				newObj.css === obj.css &&
				newObj.media === obj.media &&
				newObj.sourceMap === obj.sourceMap
			) {
				return;
			}

			update(obj = newObj);
		} else {
			remove();
		}
	};
}

var replaceText = (function () {
	var textStore = [];

	return function (index, replacement) {
		textStore[index] = replacement;

		return textStore.filter(Boolean).join('\n');
	};
})();

function applyToSingletonTag (style, index, remove, obj) {
	var css = remove ? "" : obj.css;

	if (style.styleSheet) {
		style.styleSheet.cssText = replaceText(index, css);
	} else {
		var cssNode = document.createTextNode(css);
		var childNodes = style.childNodes;

		if (childNodes[index]) style.removeChild(childNodes[index]);

		if (childNodes.length) {
			style.insertBefore(cssNode, childNodes[index]);
		} else {
			style.appendChild(cssNode);
		}
	}
}

function applyToTag (style, obj) {
	var css = obj.css;
	var media = obj.media;

	if(media) {
		style.setAttribute("media", media)
	}

	if(style.styleSheet) {
		style.styleSheet.cssText = css;
	} else {
		while(style.firstChild) {
			style.removeChild(style.firstChild);
		}

		style.appendChild(document.createTextNode(css));
	}
}

function updateLink (link, options, obj) {
	var css = obj.css;
	var sourceMap = obj.sourceMap;

	/*
		If convertToAbsoluteUrls isn't defined, but sourcemaps are enabled
		and there is no publicPath defined then lets turn convertToAbsoluteUrls
		on by default.  Otherwise default to the convertToAbsoluteUrls option
		directly
	*/
	var autoFixUrls = options.convertToAbsoluteUrls === undefined && sourceMap;

	if (options.convertToAbsoluteUrls || autoFixUrls) {
		css = fixUrls(css);
	}

	if (sourceMap) {
		// http://stackoverflow.com/a/26603875
		css += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + " */";
	}

	var blob = new Blob([css], { type: "text/css" });

	var oldSrc = link.href;

	link.href = URL.createObjectURL(blob);

	if(oldSrc) URL.revokeObjectURL(oldSrc);
}


/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

/**
 * build-url - A small library that builds a URL given its components
 * @version v1.0.10
 * @link https://github.com/steverydz/build-url#readme
 * @license MIT
 */
;(function () {
  'use strict';

  var root = this;
  var previousBuildUrl = root.buildUrl;

  var buildUrl = function (url, options) {
    var queryString = [];
    var key;
    var builtUrl;

    if (url === null) {
      builtUrl = '';
    } else if (typeof url === 'object') {
      builtUrl = '';
      options = url;
    } else {
      builtUrl = url;
    }

    if (options) {
      if (options.path) {
        if (options.path.indexOf('/') === 0) {
          builtUrl += options.path;
        } else {
          builtUrl += '/' + options.path;
        }
      }

      if (options.queryParams) {
        for (key in options.queryParams) {
          if (options.queryParams.hasOwnProperty(key)) {
            queryString.push(key + '=' + options.queryParams[key]);
          }
        }
        builtUrl += '?' + queryString.join('&');
      }

      if (options.hash) {
        builtUrl += '#' + options.hash;
      }
    }

    return builtUrl;
  };

  buildUrl.noConflict = function () {
    root.buildUrl = previousBuildUrl;
    return buildUrl;
  };

  if (true) {
    if (typeof module !== 'undefined' && module.exports) {
      exports = module.exports = buildUrl;
    }
    exports.buildUrl = buildUrl;
  } else {
    root.buildUrl = buildUrl;
  }
}).call(this);

/***/ }),
/* 5 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__routes_authorization_index_js__ = __webpack_require__(6);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__stores_form_store_index_js__ = __webpack_require__(30);



var app = new Vue({
    name: 'instance_auth',
    'el': '#app',
    store: new Vuex.Store(__WEBPACK_IMPORTED_MODULE_1__stores_form_store_index_js__["a" /* default */]),
    router: new VueRouter({ mode: 'history', routes: __WEBPACK_IMPORTED_MODULE_0__routes_authorization_index_js__["a" /* default */] })
});

/***/ }),
/* 6 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__forgot_index_js__ = __webpack_require__(7);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__login_index_js__ = __webpack_require__(9);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__registration_index_js__ = __webpack_require__(13);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__password_reset_index_js__ = __webpack_require__(15);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__activate_email_index_js__ = __webpack_require__(17);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__wrapper_index_js__ = __webpack_require__(19);







/* harmony default export */ __webpack_exports__["a"] = ([{
    path: '/auth/',
    component: __WEBPACK_IMPORTED_MODULE_5__wrapper_index_js__["a" /* default */],
    name: 'auth',
    children: [{
        path: 'login',
        components: {
            default: __WEBPACK_IMPORTED_MODULE_1__login_index_js__["a" /* default */],
            title: { template: '<div class="logo">Авторизация</div>' }
        },
        name: 'login'
    }, {
        path: 'registration',
        components: {
            default: __WEBPACK_IMPORTED_MODULE_2__registration_index_js__["a" /* default */],
            title: { template: '<div class="logo">Регистрация</div>' }
        },
        name: 'registration'
    }, {
        path: 'forgot',
        components: {
            default: __WEBPACK_IMPORTED_MODULE_0__forgot_index_js__["a" /* default */],
            title: { template: '<div class="logo">Восстановление пароля</div>' }
        },
        name: 'forgot'
    }, {
        path: 'reset/:token',
        name: 'reset',
        components: {
            default: __WEBPACK_IMPORTED_MODULE_3__password_reset_index_js__["a" /* default */],
            title: { template: '<div class="logo">Изменение пароля</div>' }

        },
        props: { default: true }
    }, {
        path: 'activate/:token',
        name: 'activate',
        components: {
            default: __WEBPACK_IMPORTED_MODULE_4__activate_email_index_js__["a" /* default */],
            title: { template: '<div class="logo">Активация учетной записи</div>' }

        },
        props: { default: true }
    }, {
        path: '*',
        redirect: 'login'
    }]
}]);

/***/ }),
/* 7 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html__ = __webpack_require__(8);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__template_html__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_form__ = __webpack_require__(0);




/* harmony default export */ __webpack_exports__["a"] = ({
    mixins: [__WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__["a" /* default */], __WEBPACK_IMPORTED_MODULE_2__mixins_form__["a" /* default */]],
    name: 'auth_forgot',
    template: __WEBPACK_IMPORTED_MODULE_0__template_html___default.a,
    data() {
        return {
            email: ''
        };
    },
    methods: {
        default_error() {
            return 'Ошибка восстановления доступа';
        },
        get_requires_fields() {
            return [this.email];
        },
        save() {
            try {
                this.form_validate([this.requires_fields]);
                this.post('/api/user/forgot', { email: this.email }, () => {
                    this.set_form_success("Ссылка для восстановления пароля была отправлена на почту");
                });
            } catch (err) {
                this.set_form_error(err.message);
            }
        }
    }
});

/***/ }),
/* 8 */
/***/ (function(module, exports) {

module.exports = "<div class=\"auth_forgot\">\n        <div class=\"form-field\">\n            <label class=\"user\" for=\"login-username\"></label>\n            <input id='login-username' type=\"email\" name=\"email\" v-model=\"email\" placeholder=\"email\">\n        </div>\n          <div class=\"form-field\">\n             <button type=\"submit\" class=\"auth_button\"\n                @click=\"save\" :disabled=success :class=\"{disabled: success}\">Восстановить</button>\n         </div>\n\n     <footer class=\"info\">\n        <span> <router-link :to=\"{name: 'login'}\">Войти</router-link></span>\n         <span><router-link :to=\"{name: 'registration'}\">Регистрация</router-link></span>\n     </footer>\n</div>";

/***/ }),
/* 9 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html__ = __webpack_require__(10);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__template_html__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_form__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__config_vk__ = __webpack_require__(11);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__config_fb__ = __webpack_require__(12);






/* harmony default export */ __webpack_exports__["a"] = ({
    mixins: [__WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__["a" /* default */], __WEBPACK_IMPORTED_MODULE_2__mixins_form__["a" /* default */]],
    name: 'auth_login',
    template: __WEBPACK_IMPORTED_MODULE_0__template_html___default.a,
    data() {
        return {
            email: '',
            password: '',
            unactive: false
        };
    },
    computed: {
        vk_url: function () {
            var buildUrl = __webpack_require__(4);
            return buildUrl(__WEBPACK_IMPORTED_MODULE_3__config_vk__["a" /* default */].VK_AUTHORIZE_URL, {
                queryParams: {
                    client_id: __WEBPACK_IMPORTED_MODULE_3__config_vk__["a" /* default */].VK_CLIENT_ID,
                    display: __WEBPACK_IMPORTED_MODULE_3__config_vk__["a" /* default */].VK_DISPLAY,
                    redirect_uri: __WEBPACK_IMPORTED_MODULE_3__config_vk__["a" /* default */].VK_REDIRECT_URL,
                    scope: __WEBPACK_IMPORTED_MODULE_3__config_vk__["a" /* default */].VK_SCOPE,
                    response_type: __WEBPACK_IMPORTED_MODULE_3__config_vk__["a" /* default */].VK_RESPONCE_TYPE,
                    v: __WEBPACK_IMPORTED_MODULE_3__config_vk__["a" /* default */].VK_API_VERSION
                }
            });
        },
        fb_url: function () {
            var buildUrl = __webpack_require__(4);
            return buildUrl(__WEBPACK_IMPORTED_MODULE_4__config_fb__["a" /* default */].FB_AUTHORIZE_URL, {
                queryParams: {
                    client_id: __WEBPACK_IMPORTED_MODULE_4__config_fb__["a" /* default */].FB_CLIENT_ID,
                    redirect_uri: __WEBPACK_IMPORTED_MODULE_4__config_fb__["a" /* default */].FB_REDIRECT_URL,
                    scope: __WEBPACK_IMPORTED_MODULE_4__config_fb__["a" /* default */].FB_SCOPE
                }
            });
        }
    },
    mounted() {
        this.$http.get('/api/user/flash').then(r => {
            if (r.data.success) {
                this.set_form_success(r.data.data);
            }
        }, r => {
            this.set_form_error(r.data.error);
        });
    },
    methods: {
        default_error() {
            return 'Не удалось авторизироваться. Не верный пароль';
        },
        get_requires_fields() {
            return [this.email, this.password];
        },
        save() {
            try {
                this.form_validate([this.requires_fields]);
                this.get('/api/user', { email: this.email, password: this.password }, r => {
                    window.location.href = '/';
                }, r => {
                    this.unactive = r.data.code === 'unactive';
                    this.process_error(r);
                });
            } catch (err) {
                this.set_form_error(err.message);
            }
        },
        send_activation() {
            this.get('/api/user/resend', { email: this.email }, () => {
                this.set_form_success('Письмо отправлено повторно. Проверьте, пожалуйста, почту.');
            });
        }
    }
});

/***/ }),
/* 10 */
/***/ (function(module, exports) {

module.exports = "<div class=\"auth_login\">\n        <div class=\"form-field\">\n            <label class=\"user\" for=\"login-username\"></label>\n            <input id='login-username' type=\"email\" name=\"email\" v-model=\"email\" placeholder=\"Email\">\n        </div>\n        <div class=\"form-field\">\n            <label class=\"lock\" for=\"login-password\"></label>\n            <input id='login-password' type=\"password\" v-model=\"password\" placeholder=\"Пароль\" @keyup.13=\"save\">\n        </div>\n\n         <div class=\"form-field\">\n             <button type=\"submit\" class=\"auth_button\" @click=\"save\">Войти</button>\n         </div>\n\n        <div class=\"social_buttons\">\n            Войти через социальные сети<br/>\n            <span>\n                <a :href=vk_url >\n                    <img src=\"/static/auth/icon-vk-50.jpg\" >\n                </a>\n            </span>\n            <span>\n                <a :href=fb_url>\n                    <img src=\"/static/auth/icon-fb-50.png\">\n                </a>\n            </span>\n        </div>\n        <div class=\"form-field\" v-if=\"unactive\"  >\n            Не пришло письмо с подтверждением?<br/>\n            <a @click=\"send_activation\" href=\"javascript:void(0)\">Выслать активационное письмо еще раз</a>\n        </div>\n     <footer class=\"info\">\n         <span><router-link :to=\"{name: 'registration'}\">Зарегистрироваться</router-link></span>\n         <span><router-link :to=\"{name: 'forgot'}\">Забыли пароль?</router-link></span>\n     </footer>\n\n</div>";

/***/ }),
/* 11 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = ({
    VK_AUTHORIZE_URL: 'https://oauth.vk.com/authorize',
    VK_CLIENT_ID: 6302697,
    VK_DISPLAY: 'page',
    VK_REDIRECT_URL: 'https://xn--h1abiilhh6g.xn--80asehdb/auth/vk',
    VK_RESPONCE_TYPE: 'code',
    VK_SCOPE: 4195331,
    VK_API_VERSION: 5.69
});

/***/ }),
/* 12 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = ({
    FB_AUTHORIZE_URL: 'https://www.facebook.com/v2.11/dialog/oauth',
    FB_CLIENT_ID: 1422542761187900,
    FB_REDIRECT_URL: 'https://мойюрист.онлайн/auth/fb',
    FB_SCOPE: 'email'
});

/***/ }),
/* 13 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html__ = __webpack_require__(14);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__template_html__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_form__ = __webpack_require__(0);




/* harmony default export */ __webpack_exports__["a"] = ({
    mixins: [__WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__["a" /* default */], __WEBPACK_IMPORTED_MODULE_2__mixins_form__["a" /* default */]],
    name: 'auth_reg',
    template: __WEBPACK_IMPORTED_MODULE_0__template_html___default.a,
    data() {
        return {
            email: '',
            password: '',
            re_password: ''
        };
    },
    methods: {
        default_error() {
            return 'Не удалось зарегистрироваться';
        },
        get_requires_fields() {
            return [this.email, this.password, this.re_password];
        },
        save() {
            try {
                this.form_validate([this.requires_fields, this.password_vaidate]);
                this.post('/api/user', { email: this.email, password: this.password }, () => {
                    this.set_form_success('Вы успешно зарегистрированы, но не активированы. ' + 'Вам на почту было отправлено активационное письмо.  ' + 'Пожауйста перейтиде по ссылке, указанной в пиьсме и активируйте свой аккаунт.');
                });
            } catch (err) {
                this.set_form_error(err.message);
            }
        }
    }
});

/***/ }),
/* 14 */
/***/ (function(module, exports) {

module.exports = "<div class=\"auth_login\">\n        <div class=\"form-field\">\n            <label class=\"user\" for=\"login-username\"></label>\n            <input id='login-username' type=\"email\" name=\"email\" v-model=\"email\" placeholder=\"email\" >\n        </div>\n        <div class=\"form-field\">\n            <label class=\"lock\" for=\"login-password\"></label>\n            <input id='login-password' type=\"password\" v-model=\"password\" placeholder=\"Пароль\" @keyup.13=\"save\">\n        </div>\n        <div class=\"form-field\">\n            <label class=\"lock\" for=\"login-re-password\"></label>\n            <input id='login-re-password' type=\"password\" v-model=\"re_password\" placeholder=\"Повторите пароль\" @keyup.13=\"save\">\n        </div>\n\n         <div class=\"form-field\">\n            <button type=\"submit\" class=\"auth_button\"\n                    @click=\"save\" :disabled=success :class=\"{disabled: success}\">Зарегистрироваться</button>\n         </div>\n     <footer class=\"info\">\n         <span><router-link :to=\"{name: 'login'}\">Войти</router-link></span>\n        <span> <router-link :to=\"{name: 'forgot'}\">Забыли пароль?</router-link></span>\n     </footer>\n</div>";

/***/ }),
/* 15 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html__ = __webpack_require__(16);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__template_html__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_form__ = __webpack_require__(0);




/* harmony default export */ __webpack_exports__["a"] = ({
    mixins: [__WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__["a" /* default */], __WEBPACK_IMPORTED_MODULE_2__mixins_form__["a" /* default */]],
    name: 'password_reset',
    template: __WEBPACK_IMPORTED_MODULE_0__template_html___default.a,
    props: ['token'],
    data() {
        return {
            password: '',
            re_password: ''
        };
    },
    methods: {
        default_error() {
            return 'Не удалось сменить пароль. Ссылка на смену пароля просрочена или некоректна';
        },
        get_requires_fields() {
            return [this.password, this.re_password];
        },
        save() {
            try {
                this.form_validate([this.requires_fields, this.password_vaidate]);
                this.post('/api/user/reset', { password: this.password, 'token': this.token }, () => {
                    this.set_form_success("Доступы к аккаунту обновлены. Теперь мы можете войти используя новый пароль");
                });
            } catch (err) {
                this.set_form_error(err.message);
            }
        }
    }
});

/***/ }),
/* 16 */
/***/ (function(module, exports) {

module.exports = "<div class=\"auth_forgot\">\n\n         <div class=\"form-field\">\n            <label class=\"lock\" for=\"login-password\"></label>\n            <input id='login-password' type=\"password\" v-model=\"password\" placeholder=\"Пароль\" @keyup.13=\"save\">\n        </div>\n        <div class=\"form-field\">\n            <label class=\"lock\" for=\"login-re-password\"></label>\n            <input id='login-re-password' type=\"password\" v-model=\"re_password\" placeholder=\"Повторите пароль\" @keyup.13=\"save\">\n        </div>\n\n          <div class=\"form-field\">\n             <button type=\"submit\" class=\"auth_button\"\n                    @click=\"save\" :disabled=success :class=\"{disabled: success}\">Сменить пароль</button>\n         </div>\n\n     <footer class=\"info\">\n        <span> <router-link :to=\"{name: 'login'}\">Войти</router-link></span>\n         <span><router-link :to=\"{name: 'registration'}\">Регистрация</router-link></span>\n     </footer>\n</div>";

/***/ }),
/* 17 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html__ = __webpack_require__(18);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__template_html__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__mixins_form__ = __webpack_require__(0);




/* harmony default export */ __webpack_exports__["a"] = ({
    mixins: [__WEBPACK_IMPORTED_MODULE_1__mixins_logged_disallow__["a" /* default */], __WEBPACK_IMPORTED_MODULE_2__mixins_form__["a" /* default */]],
    name: 'auth_activate',
    props: ['token'],
    template: __WEBPACK_IMPORTED_MODULE_0__template_html___default.a,
    mounted() {
        try {
            this.post('/api/user/activate', { 'token': this.token }, () => {
                this.set_form_success("Аккаунт успешно активирован. Вы можете войти на сайт, используя данные, указанные при регистрации");
            });
        } catch (err) {
            this.set_form_error(err.message);
        }
    },
    methods: {
        default_error() {
            return 'Ошибка восстановления доступа';
        }
    }
});

/***/ }),
/* 18 */
/***/ (function(module, exports) {

module.exports = "<div>\n    <footer class=\"info\" v-if=\"success\">\n         <span><router-link :to=\"{name: 'login'}\">Войти</router-link></span>\n        <span> <router-link :to=\"{name: 'forgot'}\">Забыли пароль?</router-link></span>\n     </footer>\n</div>";

/***/ }),
/* 19 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html__ = __webpack_require__(20);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__template_html___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0__template_html__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__style_less__ = __webpack_require__(21);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__style_less___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1__style_less__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__styles_fonts_less__ = __webpack_require__(24);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__styles_fonts_less___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2__styles_fonts_less__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__styles_app_less__ = __webpack_require__(26);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__styles_app_less___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3__styles_app_less__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__styles_form_less__ = __webpack_require__(28);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__styles_form_less___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4__styles_form_less__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__mixins_form__ = __webpack_require__(0);







/* harmony default export */ __webpack_exports__["a"] = ({
    name: 'auth_wrapper',
    template: __WEBPACK_IMPORTED_MODULE_0__template_html___default.a,
    mixins: [__WEBPACK_IMPORTED_MODULE_5__mixins_form__["a" /* default */]]
});

/***/ }),
/* 20 */
/***/ (function(module, exports) {

module.exports = "<div id=\"auth\">\n    <router-view name=\"title\"></router-view>\n\n    <div class=\"form\">\n        <div class=\"for_message\">\n            <div class=\"loading\" v-if=\"loading\">\n                <img src=\"/static/auth/loader.gif\" width=\"50px\">\n            </div>\n            <div class=\"error\" v-if=\"error\">\n                <div>{{error_txt}}</div>\n            </div>\n            <div class=\"success\" v-if=\"success\">\n                <div>{{success_txt}}</div>\n            </div>\n        </div>\n    <router-view></router-view>\n    </div>\n</div>\n";

/***/ }),
/* 21 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(22);
if(typeof content === 'string') content = [[module.i, content, '']];
// Prepare cssTransformation
var transform;

var options = {"hmr":true}
options.transform = transform
// add the styles to the DOM
var update = __webpack_require__(3)(content, options);
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js!./style.less", function() {
			var newContent = require("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js!./style.less");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 22 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(2)(undefined);
// imports
exports.push([module.i, "@import url(https://netdna.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.css);", ""]);
exports.push([module.i, "@import url(https://fonts.googleapis.com/css?family=Lato:400,300,700);", ""]);

// module
exports.push([module.i, "body {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  min-height: 100%;\n}\na {\n  font-size: 15px;\n  font-family: Verdana;\n}\ndiv#app {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 90vh;\n}\n.info {\n  display: flex;\n  font-size: 0.85em;\n  justify-content: space-between;\n  color: #666;\n  margin: 20px;\n}\ndiv#container {\n  background: #f7f2ea;\n  border-radius: 5px;\n  box-shadow: 0 1.5px 0 0 rgba(0, 0, 0, 0.1);\n  width: 500px;\n  display: flex;\n  flex-direction: column;\n  margin: auto;\n}\n.logo {\n  font-family: \"museo-slab\";\n  font-size: 20px;\n  text-align: center;\n  padding: 20px 20px 0;\n  margin: 0;\n  text-transform: uppercase;\n}\ninput,\nbutton {\n  border: 0;\n  color: inherit;\n  font: inherit;\n  margin: 0;\n  outline: 0;\n  padding: 0;\n  -webkit-transition: background-color 0.3s;\n  transition: background-color 0.3s;\n}\n.user:before {\n  content: '\\F007';\n  font: 14px fontawesome;\n  color: #5b5b5b;\n}\n.lock:before {\n  content: '\\F023';\n  font: 14px fontawesome;\n  color: #5b5b5b;\n}\n.form input[type=\"password\"],\n.form input[type=\"email\"],\n.form button[type=\"submit\"] {\n  width: 100%;\n}\n.form label,\n.form input[type=\"email\"],\n.form input[type=\"password\"],\n.form button[type=\"submit\"] {\n  border-radius: 0.25rem;\n  padding: 1rem;\n  color: #3A3F44;\n}\n.form label {\n  background-color: #222222;\n  border-bottom-right-radius: 0;\n  border-top-right-radius: 0;\n  padding-left: 1.25rem;\n  padding-right: 1.25rem;\n}\n.form input[type=\"text\"],\n.form input[type=\"password\"] {\n  background-color: #ffffff;\n  border-bottom-left-radius: 0;\n  border-top-left-radius: 0;\n}\n.form input[type=\"email\"]:focus,\n.form input[type=\"email\"]:hover,\n.form input[type=\"password\"]:focus,\n.form input[type=\"password\"]:hover {\n  background-color: #eeeeee;\n}\n.form button[type=\"submit\"] {\n  background-color: #dccdb4;\n  color: #000;\n  font-weight: bold;\n  text-transform: uppercase;\n}\n.form button[type=\"submit\"]:hover {\n  background-color: #efe8db;\n}\n.form button[type=\"submit\"]:active {\n  background-color: #dccdb4;\n  color: #3A3F44;\n}\n.form button[type=\"submit\"].disabled {\n  background-color: #efe8db;\n  color: #dccdb4;\n}\n.form-field {\n  display: -webkit-box;\n  display: -webkit-flex;\n  display: -ms-flexbox;\n  display: flex;\n  margin-bottom: 2rem;\n}\n.hidden {\n  border: 0;\n  clip: rect(0 0 0 0);\n  height: 1px;\n  margin: -1px;\n  overflow: hidden;\n  padding: 0;\n  position: absolute;\n  width: 1px;\n}\n.text--center {\n  text-align: center;\n}\ndiv.for_message {\n  min-height: 50px;\n  margin-bottom: 10px;\n  font-size: 15px;\n}\ndiv.error,\ndiv.success {\n  display: flex;\n  align-items: center;\n  align-content: center;\n  justify-content: center;\n  overflow: auto;\n  width: 100%;\n  height: 100%;\n}\ndiv.loading {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n.red {\n  margin: auto;\n}\n.form div.social_buttons {\n  text-align: center;\n  justify-content: center;\n  align-items: center;\n}\n.form div.social_buttons img {\n  padding: 10px;\n}\n/* For mobile devices */\n@media only screen and (max-width: 767px) {\n  body div#app {\n    display: inline;\n    width: 100%;\n  }\n  body div#app div#container {\n    display: inline;\n    width: 100%;\n    box-shadow: none;\n    margin: 0px;\n  }\n  body div#app div#container footer.info {\n    display: inline;\n  }\n  body div#app div#container footer.info span {\n    display: block;\n    padding-top: 10px;\n  }\n}\n", ""]);

// exports


/***/ }),
/* 23 */
/***/ (function(module, exports) {


/**
 * When source maps are enabled, `style-loader` uses a link element with a data-uri to
 * embed the css on the page. This breaks all relative urls because now they are relative to a
 * bundle instead of the current page.
 *
 * One solution is to only use full urls, but that may be impossible.
 *
 * Instead, this function "fixes" the relative urls to be absolute according to the current page location.
 *
 * A rudimentary test suite is located at `test/fixUrls.js` and can be run via the `npm test` command.
 *
 */

module.exports = function (css) {
	// get current location
	var location = typeof window !== "undefined" && window.location;

	if (!location) {
		throw new Error("fixUrls requires window.location");
	}

	// blank or null?
	if (!css || typeof css !== "string") {
		return css;
	}

	var baseUrl = location.protocol + "//" + location.host;
	var currentDir = baseUrl + location.pathname.replace(/\/[^\/]*$/, "/");

	// convert each url(...)
	/*
 This regular expression is just a way to recursively match brackets within
 a string.
 	 /url\s*\(  = Match on the word "url" with any whitespace after it and then a parens
    (  = Start a capturing group
      (?:  = Start a non-capturing group
          [^)(]  = Match anything that isn't a parentheses
          |  = OR
          \(  = Match a start parentheses
              (?:  = Start another non-capturing groups
                  [^)(]+  = Match anything that isn't a parentheses
                  |  = OR
                  \(  = Match a start parentheses
                      [^)(]*  = Match anything that isn't a parentheses
                  \)  = Match a end parentheses
              )  = End Group
              *\) = Match anything and then a close parens
          )  = Close non-capturing group
          *  = Match anything
       )  = Close capturing group
  \)  = Match a close parens
 	 /gi  = Get all matches, not the first.  Be case insensitive.
  */
	var fixedCss = css.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi, function (fullMatch, origUrl) {
		// strip quotes (if they exist)
		var unquotedOrigUrl = origUrl.trim().replace(/^"(.*)"$/, function (o, $1) {
			return $1;
		}).replace(/^'(.*)'$/, function (o, $1) {
			return $1;
		});

		// already a full url? no change
		if (/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/)/i.test(unquotedOrigUrl)) {
			return fullMatch;
		}

		// convert the url to a full url
		var newUrl;

		if (unquotedOrigUrl.indexOf("//") === 0) {
			//TODO: should we add protocol?
			newUrl = unquotedOrigUrl;
		} else if (unquotedOrigUrl.indexOf("/") === 0) {
			// path should be relative to the base url
			newUrl = baseUrl + unquotedOrigUrl; // already starts with '/'
		} else {
			// path should be relative to current directory
			newUrl = currentDir + unquotedOrigUrl.replace(/^\.\//, ""); // Strip leading './'
		}

		// send back the fixed url(...)
		return "url(" + JSON.stringify(newUrl) + ")";
	});

	// send back the fixed css
	return fixedCss;
};

/***/ }),
/* 24 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(25);
if(typeof content === 'string') content = [[module.i, content, '']];
// Prepare cssTransformation
var transform;

var options = {"hmr":true}
options.transform = transform
// add the styles to the DOM
var update = __webpack_require__(3)(content, options);
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../node_modules/css-loader/index.js!../node_modules/less-loader/dist/cjs.js!./fonts.less", function() {
			var newContent = require("!!../node_modules/css-loader/index.js!../node_modules/less-loader/dist/cjs.js!./fonts.less");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 25 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(2)(undefined);
// imports


// module
exports.push([module.i, "body {\n  font-size: 1.1em;\n}\na {\n  color: #008CBA;\n}\nh1 {\n  color: #222;\n  font-size: 1.2em;\n  text-transform: uppercase;\n  font-family: Verdana, Geneva, sans-serif;\n}\n.error {\n  color: #ff4566;\n}\n.success {\n  color: #4dac85;\n}\n", ""]);

// exports


/***/ }),
/* 26 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(27);
if(typeof content === 'string') content = [[module.i, content, '']];
// Prepare cssTransformation
var transform;

var options = {"hmr":true}
options.transform = transform
// add the styles to the DOM
var update = __webpack_require__(3)(content, options);
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../node_modules/css-loader/index.js!../node_modules/less-loader/dist/cjs.js!./app.less", function() {
			var newContent = require("!!../node_modules/css-loader/index.js!../node_modules/less-loader/dist/cjs.js!./app.less");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 27 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(2)(undefined);
// imports


// module
exports.push([module.i, "body {\n  background-size: cover;\n  background-color: #f7f2ea;\n}\n/* For mobile devices */\n@media only screen and (max-width: 767px) {\n  body {\n    background-image: none;\n  }\n}\n", ""]);

// exports


/***/ }),
/* 28 */
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(29);
if(typeof content === 'string') content = [[module.i, content, '']];
// Prepare cssTransformation
var transform;

var options = {"hmr":true}
options.transform = transform
// add the styles to the DOM
var update = __webpack_require__(3)(content, options);
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../node_modules/css-loader/index.js!../node_modules/less-loader/dist/cjs.js!./form.less", function() {
			var newContent = require("!!../node_modules/css-loader/index.js!../node_modules/less-loader/dist/cjs.js!./form.less");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),
/* 29 */
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(2)(undefined);
// imports


// module
exports.push([module.i, ".form {\n  margin: 20px 20px 0;\n  border-radius: 3px;\n}\n/* For mobile devices */\n@media only screen and (max-width: 767px) {\n  .form {\n    margin: 0px;\n    border-radius: 0px;\n  }\n}\n", ""]);

// exports


/***/ }),
/* 30 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = ({
    namespaced: true,
    state: {
        is_error: false,
        is_success: false,
        error_txt: '',
        success_txt: '',
        loading: false
    },
    mutations: {
        set_error(state, error) {
            state.is_error = true;
            state.is_success = false;
            state.error_txt = error.txt;
        },
        start_loading(state) {
            state.loading = true;
            state.is_error = false;
            state.is_success = false;
        },
        stop_loading(state) {
            state.loading = false;
        },
        set_success(state, success) {
            state.is_error = false;
            state.is_success = true;
            state.success_txt = success.txt;
        },
        init_state(state) {
            state.is_error = false;
            state.is_success = false;
            state.loading = false;
        }
    }
});

/***/ })
/******/ ]);