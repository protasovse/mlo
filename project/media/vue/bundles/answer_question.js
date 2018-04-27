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
/******/ 	return __webpack_require__(__webpack_require__.s = 354);
/******/ })
/************************************************************************/
/******/ ({

/***/ 27:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var _default = {
  created: function created() {},
  computed: {
    error: function error() {
      return this.$store.state.is_error;
    },
    success: function success() {
      return this.$store.state.is_success;
    },
    error_txt: function error_txt() {
      return this.$store.state.error_txt;
    },
    success_txt: function success_txt() {
      return this.$store.state.success_txt;
    },
    loading: function loading() {
      return this.$store.state.loading;
    },
    error_fields: function error_fields() {
      return this.$store.state.fields;
    }
  },
  beforeMount: function beforeMount() {
    this.$store.commit('init_state');
  },
  methods: {
    save_field_value: function save_field_value(field, value) {
      this.$store.commit('save_field', {
        'key': field,
        'val': value
      });
    },
    set_field_error: function set_field_error(field, txt) {
      this.$store.commit('error_field', {
        'field': field,
        'txt': txt
      });
    },
    start_loading: function start_loading() {
      this.$store.commit('start_loading');
    },
    clear_error_field: function clear_error_field() {
      this.$store.commit('clear_error_field');
    },
    stop_loading: function stop_loading() {
      this.$store.commit('stop_loading');
    },
    password_vaidate: function password_vaidate() {
      if (this.password !== this.re_password) {
        this.set_field_error('re_password', 'Пароли не совпадают');
        throw new Error('Пароли не совпадают');
      }
    },
    password_strength_validate: function password_strength_validate() {
      if (this.password.length < 6) {
        this.set_field_error('password', 'Пароль слишком короткий');
        throw new Error('Длина пароля не должна быть короче 6 символов');
      }
    },
    requires_fields: function requires_fields() {
      var _this = this;

      if (this.get_requires_fields === undefined) {
        return;
      }

      var has_error = false;
      var req_fields = this.get_requires_fields();
      req_fields.forEach(function (field) {
        if (_this[field] === '') {
          _this.set_field_error(field, 'Поле обязательное для заполнения');

          has_error = true;
        }
      });

      if (has_error) {
        throw new Error('Введите данные');
      }
    },
    form_validate: function form_validate(fns) {
      this.clear_error_field();
      fns.forEach(function (fn) {
        fn();
      });
    },
    set_form_error: function set_form_error(txt) {
      this.$store.commit('set_error', {
        txt: txt
      });
      this.stop_loading();
    },
    set_form_success: function set_form_success() {
      var txt = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
      this.$store.commit('set_success', {
        txt: txt
      });
      this.stop_loading();
    },
    process_success: function process_success(r, succes_fn) {
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
    default_error: function default_error() {
      return 'Что-то пошло не так';
    },
    mark_error_fields: function mark_error_fields(r) {
      var _this2 = this;

      r.data.fields.forEach(function (x) {
        _this2.set_field_error(x['field'], x['txt']);
      });
    },
    process_error: function process_error(r) {
      var fn = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
      this.stop_loading();
      this.mark_error_fields(r);

      if (fn === undefined) {
        if (r.data.error !== undefined) {
          throw new Error(r.data.error);
        } else {
          throw new Error(this.default_error());
        }
      } else {
        fn(r);
      }
    },
    get: function get(url, params, fn) {
      var _this3 = this;

      var fn_error = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : undefined;
      this.start_loading();
      this.clear_error_field();
      this.$http.get(url, {
        params: params
      }, {
        emulateJSON: true
      }).then(function (r) {
        _this3.process_success(r, fn);
      }, function (r) {
        _this3.process_error(r, fn_error);
      }).catch(function (e) {
        return _this3.set_form_error(e.message);
      });
    },
    post: function post(url, params, fn) {
      var _this4 = this;

      var fn_error = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : undefined;
      this.start_loading();
      this.clear_error_field();
      this.$http.post(url, params, {
        emulateJSON: true
      }).then(function (r) {
        return _this4.process_success(r, fn);
      }, function (r) {
        return _this4.process_error(r, fn_error);
      }).catch(function (e) {
        return _this4.set_form_error(e.message);
      });
    },
    put: function put(url, params, fn) {
      var _this5 = this;

      var fn_error = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : undefined;
      this.start_loading();
      this.clear_error_field();
      this.$http.put(url, params, {
        emulateJSON: true
      }).then(function (r) {
        return _this5.process_success(r, fn);
      }, function (r) {
        return _this5.process_error(r, fn_error);
      }).catch(function (e) {
        return _this5.set_form_error(e.message);
      });
    },
    get_saved_field: function get_saved_field(field) {
      var f_arr = this.$store.state.values;
      return f_arr[field];
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 354:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _index = _interopRequireDefault(__webpack_require__(355));

var _index2 = _interopRequireDefault(__webpack_require__(47));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var vueSmoothScroll = __webpack_require__(93);

Vue.use(vueSmoothScroll);
var app = new Vue({
  name: 'instance_anser_question',
  'el': '#app',
  store: new Vuex.Store(_index2.default),
  router: new VueRouter({
    mode: 'history',
    routes: _index.default
  })
});

/***/ }),

/***/ 355:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _index = _interopRequireDefault(__webpack_require__(356));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = [{
  path: '/%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81/:qid/',
  component: _index.default,
  props: true
}];
exports.default = _default;

/***/ }),

/***/ 356:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _template = _interopRequireDefault(__webpack_require__(357));

var _form = _interopRequireDefault(__webpack_require__(27));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = {
  mixins: [_form.default],
  template: _template.default,
  props: ['qid'],
  name: 'answer_question',
  data: function data() {
    return {
      full_tree: true,
      content: '',
      answers: [],
      answers_like: [],
      is_authorized: false,
      user_id: false,
      role: false,
      question: [],
      count_answ: {},
      sub_answers_exists: false
    };
  },
  mounted: function mounted() {
    var _this = this;

    this.$http.get('/api/default').then(function (r) {
      _this.full_tree = r.data.data['settings']['answers_expand'];
    });
    this.$http.get('/api/user/check').then(function (r) {
      _this.is_authorized = r.data.success;

      if (_this.is_authorized) {
        _this.role = r.data.data.role;
        _this.user_id = r.data.data.id;
      }
    });
    this.$http.get('/api/question', {
      params: {
        'id': this.qid
      }
    }).then(function (r) {
      _this.question = r.data.data;
    });
    this.$http.get('/api/question/answers', {
      params: {
        'id': this.qid
      }
    }).then(function (r) {
      _this.answers = r.data.data; // to count subanswers

      _this.answers.forEach(function (x) {
        if (x.parent_id) {
          _this.sub_answers_exists = true;
          _this.count_answ[x.parent_id] = (_this.count_answ[x.parent_id] || 0) + 1;
        }
      });
    });
  },
  computed: {
    tree_link_name: function tree_link_name() {
      return this.full_tree ? 'Свернуть' : 'Развернуть';
    }
  },
  methods: {
    like_title: function like_title(id) {
      var answer = this.answers.filter(function (i) {
        return i.id === id;
      })[0];

      if (answer.author.id === this.user_id) {
        return 'Мой ответ';
      }

      return this.role === 'lawyer' ? 'Согласен с ответом' : 'Ответ полезен?';
    },
    expand_all: function expand_all() {
      var _this2 = this;

      this.full_tree = !this.full_tree;
      this.answers = this.answers.map(function (x) {
        if (!x.parent_id) {
          x.is_expand = _this2.full_tree;
        }

        return x;
      });
    },
    expand_answer: function expand_answer(id) {
      var answer = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      answer.is_expand = !answer.is_expand;
    },
    is_possible_expand_answer: function is_possible_expand_answer(id) {
      var answer = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      return !answer.parent_id && this.count_answ[answer.id];
    },
    get_exand_answer_name: function get_exand_answer_name(id) {
      var answer = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      var cnt = this.count_answ[answer.id] || 0;
      return answer.is_expand ? "\u0421\u0432\u0435\u0440\u043D\u0443\u0442\u044C (".concat(cnt, ")") : "\u0420\u0430\u0437\u0432\u0435\u0440\u043D\u0443\u0442\u044C (".concat(cnt, ")");
    },
    get_add_question_link: function get_add_question_link(id) {
      if (!this.is_authorized) {
        return false;
      }

      var answer = this.answers.filter(function (i) {
        return i.id === id;
      })[0];

      if (this.role === 'client') {
        if (this.question.author.id === this.user_id && answer.author.role === 'lawyer' && (!answer.parent_id || answer.is_last_answer)) {
          return 'Задать дополнительный вопрос';
        }
      } else if (this.role === 'lawyer') {
        if (answer.parent_id && answer.is_last_answer && answer.author.role === 'client') {
          var parent_answer = this.answers.filter(function (i) {
            return i.id === answer.parent_id;
          })[0];

          if (parent_answer.author.id === this.user_id) {
            return 'Ответить';
          }
        }
      }

      return false;
    },
    is_show_comment: function is_show_comment(id) {
      var answer = this.answers.filter(function (i) {
        return i.id === id;
      })[0];

      if (!answer.parent_id) {
        return true;
      }

      return this.answers.filter(function (i) {
        return i.id === answer.parent_id;
      })[0].is_expand;
    },
    scrollTo: function scrollTo(refName) {
      var element = this.$refs[refName][0];
      var curtop = 0;
      var curtopscroll = 0;

      if (element.offsetParent) {
        do {
          curtop += element.offsetTop;
          curtopscroll += element.offsetParent ? element.offsetParent.scrollTop : 0;
        } while (element = element.offsetParent);
      }

      this.$SmoothScroll(curtop - curtopscroll - 40, 500);
    },
    save: function save() {
      console.log(this.qid);
    },
    to_like_val: function to_like_val(id, val) {
      var a = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      a['like_count'] += val;
      a['is_can_like'] = false;
    },
    to_like: function to_like(id) {
      var _this3 = this;

      this.$http.post('/api/question/answers/like', {
        'id': id,
        'value': 1
      }, {
        emulateJSON: true
      }).then(function (r) {
        _this3.to_like_val(id, 1);
      });
    },
    to_dislike: function to_dislike(id) {
      var _this4 = this;

      this.$http.post('/api/question/answers/like', {
        'id': id,
        'value': -1
      }, {
        emulateJSON: true
      }).then(function (r) {
        _this4.to_like_val(id, -1);
      });
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 357:
/***/ (function(module, exports) {

module.exports = "<div id=\"answer_block\">\n    <div id=\"form\">\n        <div class=\"form-group\">\n            <label for=\"reply\" class=\"h6 mb-2\">title</label>\n            <textarea class=\"form-control\" v-model=\"content\" :class=\"{'is-invalid': error_fields.content }\" id=\"reply\"\n                      rows=\"5\" placeholder=\"Мой ответ…\"></textarea>\n            <span class=\"invalid-feedback\" v-if=\"error_fields.content\">error_fields.content </span>\n        </div>\n        <div class=\"form-group\">\n            <button @click=\"save\" class=\"btn btn-primary\">Отправить</button>\n            <span class=\"ml-3 normal\"><a href=\"#\"><i class=\"mr-2 icon-folder\"></i>Прикрепить файлы</a></span>\n        </div>\n    </div>\n\n    <div class=\"row question-page_gradient\">\n        <div class=\"question-page_main-part\">\n            <div class=\"row\">\n                <h3 class=\"answer-list-head\" id=\"div-id\">Ответы юристов\n                        <a href=\"javascript:void(0);\" @click=\"expand_all\" v-if=\"sub_answers_exists\">({{ tree_link_name }})</a>\n                    <span class=\"d-none answer__counter\" itemprop=\"answerCount\">2</span>\n                </h3>\n            </div>\n\n\n            <div name=\"x\" v-for=\"answer_data in answers\"\n                 role=\"answer\"\n                 :name=\"answer_data.id\"\n                 :ref=\"answer_data.id\"\n                 :data-answer_id=\"answer_data.id\"\n                 :data-thread=\"answer_data.thread\"\n                 class=\"answer entry\"\n                 :class=\"{'answer-push': answer_data.parent_id }\"\n                 v-if=\"is_show_comment(answer_data.id)\">\n\n                <hr class=\"my-4\"/>\n\n                <header class=\"answer-header\">\n                    <div class=\"question-page_l-col\">\n                        <a class=\"answer-header_photo\" :href=\"answer_data.author.url\">\n                            <img :src=\"answer_data.author.info.photo\" :alt=\"answer_data.author.full_name\" />\n                        </a>\n                    </div>\n\n\n                    <div class=\"question-page_r-col\">\n                        <h6 class=\"mb-0\" itemprop=\"name\">\n                            <a :href=\"answer_data.author.url\">{{ answer_data.author.full_name }}</a>\n                        </h6>\n\n\n                        <div class=\"normal text-muted\" v-if=\"!answer_data.parent_id\">{{ answer_data.author.info.ur_status }}, {{ answer_data.author.city.name}}</div>\n\n                        <div class=\"answer-header_medal mt-3\" v-if=\"!answer_data.parent_id\">\n                            <span class=\"item\" title=\"Рейтинг эксперта\">\n                                <i class=\"icon-star\"></i>\n                                <span class=\"v\">{{ answer_data.author.stat.rating }}</span>\n                            </span>\n                            <span class=\"item\" title=\"Стаж\" v-if=\"0\">\n                                <i class=\"icon-medal\"></i>\n                                <span class=\"v\">охуеть сколько лет</span>\n                            </span>\n                            <span class=\"item\" title=\"Всего консультаций\" >\n                                <i class=\"icon-forum\"></i>\n                                <span class=\"v\">{{ answer_data.author.info.answer_count }}</span>\n                            </span>\n                        </div>\n\n                    </div>\n\n                </header>\n\n\n                <div class=\"row\">\n\n                    <div class=\"question-page_l-col\">\n                        <time class=\"subtitle d-block mt-1\" itemprop=\"dateCreated\" :datetime=\"answer_data.pub_date_c\">{{ answer_data.pub_date }}</time>\n                        <span class=\"d-block\">№ {{ answer_data.id }}</span>\n                    </div>\n\n                    <div class=\"question-page_r-col content\">\n                        <div class=\"text\" itemprop=\"text\" v-html=\"answer_data.content\">\n                            <div class=\"signature\" v-html=\"answer_data.author.signature\"></div>\n                        </div>\n                    </div>\n                </div>\n\n\n                <footer class=\"answer-footer row\">\n\n                    <div class=\"question-page_r-col ml-auto d-flex align-items-center justify-content-between flex-column flex-sm-row\">\n\n                        <div class=\"answer-footer-action normal align-self-start align-self-md-center\">\n                            <a href=\"#\" v-if=\"get_add_question_link(answer_data.id)\">{{ get_add_question_link(answer_data.id)}}</a><br/>\n                            <a href=\"javascript:void(0);\" v-if=\"is_possible_expand_answer(answer_data.id)\" @click=\"expand_answer(answer_data.id)\">{{ get_exand_answer_name(answer_data.id) }}</a>\n                        </div>\n\n                        <div class=\"align-self-end mt-3 mt-sm-0\" v-if=\"!answer_data.parent_id\">\n                            <div class=\"answer-like\">\n                                <div class=\"answer-like-sign dropdown\">{{ like_title(answer_data.id) }}</div>\n                                <div class=\"answer-like-block\">\n                                    <i class=\"icon-dislike order-1\" v-if=\"answer_data.is_can_like\" @click=\"to_dislike(answer_data.id)\"></i>\n                                    <i class=\"icon-like order-3\" v-if=\"answer_data.is_can_like\" @click=\"to_like(answer_data.id)\"></i>\n                                    <span class=\"order-2\"\n                                          :class=\"{'text-success': answer_data.like_count>0, 'text-danger': answer_data.like_count<0}\">\n                                        {{ answer_data.like_count }}</span>\n                                </div>\n                            </div>\n                        </div>\n\n                    </div>\n                    <div class=\"d-none question-page_r-col ml-auto mt-4\"></div>\n                </footer>\n\n            </div>\n        </div>\n\n\n        <aside class=\"question-page_aside-part\">\n            <h4 class=\"mb-4\">Юристы ответившие на этот вопрос:</h4>\n\n            <div class=\"lawyer-list\">\n                <div v-for=\"answer_data in answers\"\n                     v-if=\"!answer_data.parent_id\"\n                     role=\"answers_selector\"\n                     class=\"lawyer-list_item lawyer-list_item-action\"\n                     :data-answer_id=\"answer_data.id\"\n                     @click=\"scrollTo(answer_data.id)\">\n                    <div class=\"lawyer-list_header\">\n                        <span class=\"ph\">\n                            <img :src=\"answer_data.author.info.pic\" :alt=\"answer_data.author.full_name\">\n                        </span>\n                        <div class=\"nm\">{{ answer_data.author.full_name }}</div>\n                    </div>\n                    <p class=\"lawyer-list_body\"> {{ answer_data.short_content }} </p>\n                </div>\n            </div>\n\n        </aside>\n\n\n    </div>\n\n\n</div>";

/***/ }),

/***/ 47:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var _default = {
  namespaced: true,
  state: {
    is_error: false,
    is_success: false,
    error_txt: '',
    success_txt: '',
    loading: false,
    fields: {},
    // сохраненные значения
    values: {}
  },
  mutations: {
    set_error: function set_error(state, error) {
      state.is_error = true;
      state.is_success = false;
      state.error_txt = error.txt;
    },
    start_loading: function start_loading(state) {
      state.loading = true;
      state.is_error = false;
      state.is_success = false;
    },
    stop_loading: function stop_loading(state) {
      state.loading = false;
    },
    set_success: function set_success(state, success) {
      state.is_error = false;
      state.is_success = true;
      state.success_txt = success.txt;
    },
    init_state: function init_state(state) {
      state.is_error = false;
      state.is_success = false;
      state.loading = false;
      state.fields = {};
    },
    error_field: function error_field(state, error) {
      Vue.set(state.fields, error.field, error.txt);
    },
    save_field: function save_field(state, value) {
      Vue.set(state.values, value.key, value.val);
    },
    clear_error_field: function clear_error_field(state) {
      state.fields = {};
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 93:
/***/ (function(module, exports, __webpack_require__) {

(function webpackUniversalModuleDefinition(root, factory) {
	if(true)
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["VueSmoothScroll"] = factory();
	else
		root["VueSmoothScroll"] = factory();
})(this, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	var SmoothScroll = __webpack_require__(1);
	module.exports = {
	    install: function (Vue, options) {
	        options = options || { name: 'smoothscroll' };
	        Vue.directive(options.name, {
	            inserted: function (el, binding) {
	                SmoothScroll(el, binding.value["duration"], binding.value["callback"], binding.value["context"]);
	            }
	        });
	        Object.defineProperty(Vue.prototype, '$SmoothScroll', {
	            get: function () {
	                return SmoothScroll;
	            }
	        });
	    }
	};

/***/ },
/* 1 */
/***/ function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;(function (root, smoothScroll) {
	  'use strict';

	  // Support RequireJS and CommonJS/NodeJS module formats.
	  // Attach smoothScroll to the `window` when executed as a <script>.

	  // RequireJS
	  if (true) {
	    !(__WEBPACK_AMD_DEFINE_FACTORY__ = (smoothScroll), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

	  // CommonJS
	  } else if (typeof exports === 'object' && typeof module === 'object') {
	    module.exports = smoothScroll();

	  } else {
	    root.smoothScroll = smoothScroll();
	  }

	})(this, function(){
	'use strict';

	// Do not initialize smoothScroll when running server side, handle it in client:
	if (typeof window !== 'object') return;

	// We do not want this script to be applied in browsers that do not support those
	// That means no smoothscroll on IE9 and below.
	if(document.querySelectorAll === void 0 || window.pageYOffset === void 0 || history.pushState === void 0) { return; }

	// Get the top position of an element in the document
	var getTop = function(element, start) {
	    // return value of html.getBoundingClientRect().top ... IE : 0, other browsers : -pageYOffset
	    if(element.nodeName === 'HTML') return -start
	    return element.getBoundingClientRect().top + start
	}
	// ease in out function thanks to:
	// http://blog.greweb.fr/2012/02/bezier-curve-based-easing-functions-from-concept-to-implementation/
	var easeInOutCubic = function (t) { return t<.5 ? 4*t*t*t : (t-1)*(2*t-2)*(2*t-2)+1 }

	// calculate the scroll position we should be in
	// given the start and end point of the scroll
	// the time elapsed from the beginning of the scroll
	// and the total duration of the scroll (default 500ms)
	var position = function(start, end, elapsed, duration) {
	    if (elapsed > duration) return end;
	    return start + (end - start) * easeInOutCubic(elapsed / duration); // <-- you can change the easing funtion there
	    // return start + (end - start) * (elapsed / duration); // <-- this would give a linear scroll
	}

	// we use requestAnimationFrame to be called by the browser before every repaint
	// if the first argument is an element then scroll to the top of this element
	// if the first argument is numeric then scroll to this location
	// if the callback exist, it is called when the scrolling is finished
	// if context is set then scroll that element, else scroll window
	var smoothScroll = function(el, duration, callback, context){
	    duration = duration || 500;
	    context = context || window;
	    var start = context.scrollTop || window.pageYOffset;

	    if (typeof el === 'number') {
	      var end = parseInt(el);
	    } else {
	      var end = getTop(el, start);
	    }

	    var clock = Date.now();
	    var requestAnimationFrame = window.requestAnimationFrame ||
	        window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame ||
	        function(fn){window.setTimeout(fn, 15);};

	    var step = function(){
	        var elapsed = Date.now() - clock;
	        if (context !== window) {
	          context.scrollTop = position(start, end, elapsed, duration);
	        }
	        else {
	          window.scroll(0, position(start, end, elapsed, duration));
	        }

	        if (elapsed > duration) {
	            if (typeof callback === 'function') {
	                callback(el);
	            }
	        } else {
	            requestAnimationFrame(step);
	        }
	    }
	    step();
	}

	var linkHandler = function(ev) {
	    ev.preventDefault();

	    if (location.hash !== this.hash) window.history.pushState(null, null, this.hash)
	    // using the history api to solve issue #1 - back doesn't work
	    // most browser don't update :target when the history api is used:
	    // THIS IS A BUG FROM THE BROWSERS.
	    // change the scrolling duration in this call
	    var node = document.getElementById(this.hash.substring(1))
	    if(!node) return; // Do not scroll to non-existing node

	    smoothScroll(node, 500, function(el) {
	        location.replace('#' + el.id)
	        // this will cause the :target to be activated.
	    });
	}

	// We look for all the internal links in the documents and attach the smoothscroll function
	document.addEventListener("DOMContentLoaded", function () {
	    var internal = document.querySelectorAll('a[href^="#"]:not([href="#"])'), a;
	    for(var i=internal.length; a=internal[--i];){
	        a.addEventListener("click", linkHandler, false);
	    }
	});

	// return smoothscroll API
	return smoothScroll;

	});


/***/ }
/******/ ])
});
;

/***/ })

/******/ });