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
Vue.component('file-upload', VueUploadComponent);
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
      default_settings: [],
      full_tree: true,
      content: '',
      answers: [],
      answers_like: [],
      is_authorized: false,
      user_id: false,
      role: false,
      question: {},
      advice: false,
      count_answ: {},
      sub_answers_exists: false,
      is_can_answer: false,
      files: [],
      parent_id: 0,
      thread: 0,
      upload_form: '',
      load_answers: false,
      load_question: false,
      is_show_advice_timeout: false,
      reject: false,
      expert_loading: false,
      load_form: false
    };
  },
  mounted: function mounted() {
    var _this = this;

    this.load_answers = true;
    this.$http.get('/api/default').then(function (r) {
      _this.default_settings = r.data.data;
      _this.full_tree = r.data.data['settings']['answers_expand'];
    });
    this.$http.get('/api/user/check').then(function (r) {
      _this.is_authorized = r.data.success;

      if (_this.is_authorized) {
        _this.role = r.data.data.role;
        _this.user_id = r.data.data.id;

        if (_this.role === 'lawyer') {
          _this.is_can_answer = true;
        }
      }
    });
    this.$http.get("/api/questions/".concat(this.qid)).then(function (r) {
      _this.question = r.data.data;
      _this.load_question = true;

      _this.request_and_load_answers();

      _this.load_advice();
    });
  },
  computed: {
    is_expert_appointed: function is_expert_appointed() {
      return this.advice && this.advice.expert && (this.advice.status === 'inwork' || this.advice.status === 'answered' || this.advice.status === 'addquestion' || this.advice.status === 'closed');
    },
    is_show_button_payment: function is_show_button_payment() {
      return this.is_iam_autor && this.advice && this.advice.status === 'new';
    },
    you_must_confirm_email: function you_must_confirm_email() {
      return !this.question.is_pay && this.question.status === 'blocked';
    },
    you_must_pay: function you_must_pay() {
      return this.question.is_pay && this.question.status === 'blocked';
    },
    is_iam_expert: function is_iam_expert() {
      return this.advice && this.advice.expert && this.advice.expert.id === this.user_id;
    },
    is_iam_autor: function is_iam_autor() {
      return this.question.author.id === this.user_id;
    },
    article_id: function article_id() {
      return "question-".concat(this.qid);
    },
    tree_link_name: function tree_link_name() {
      return this.full_tree ? 'Свернуть' : 'Развернуть';
    },
    post_action: function post_action() {
      return "/api/questions/".concat(this.qid, "/answers");
    },
    is_form_send_done_first: function is_form_send_done_first() {
      return this.upload_form === 'upload_first' && this.is_form_send_done('upload_first');
    },
    is_form_send_done_second: function is_form_send_done_second() {
      return this.upload_form === 'upload_second' && this.is_form_send_done('upload_second');
    },
    file_first_form_loading: function file_first_form_loading() {
      return this.loading || this.get_upload('upload_first') && this.get_upload('upload_first').active;
    },
    file_second_form_loading: function file_second_form_loading() {
      return this.loading || this.get_upload('upload_second') && this.get_upload('upload_second').active;
    },
    answers_total: function answers_total() {
      return this.answers.length;
    }
  },
  watch: {
    is_form_send_done_first: function is_form_send_done_first() {
      if (this.is_form_send_done_first) {
        this.is_can_answer = false;
        this.request_and_load_answers(this.answer_id);
      }
    },
    is_form_send_done_second: function is_form_send_done_second() {
      if (this.is_form_send_done_second) {
        this.is_can_answer = false;
        this.request_and_load_answers(this.answer_id);
      }
    }
  },
  methods: {
    load_advice: function load_advice() {
      var _this2 = this;

      if (this.question.is_pay) {
        this.load_form = true;
        this.$http.get("/api/questions/".concat(this.qid, "/advice")).then(function (r) {
          _this2.advice = r.data.data;

          if (!(_this2.advice.status === 'inwork' && _this2.advice.expert && _this2.advice.expert.id === _this2.user_id)) {
            _this2.is_can_answer = false;
          }

          _this2.load_form = false;
        }, function (err) {
          _this2.load_form = false;
        });
      }
    },
    reject_advice: function reject_advice() {
      var _this3 = this;

      this.expert_loading = true;
      this.$http.post("/api/questions/".concat(this.qid, "/advice/").concat(this.advice.id, "/reject")).then(function (r) {
        _this3.reject = true;
        _this3.expert_loading = false;
      }, function (err) {
        _this3.set_field_error('advice', err.data.error);

        _this3.expert_loading = false;
      });
    },
    confirm_advice: function confirm_advice() {
      var _this4 = this;

      this.expert_loading = true;
      this.$http.post("/api/questions/".concat(this.qid, "/advice/").concat(this.advice.id, "/confirm")).then(function (r) {
        _this4.$http.get("/api/questions/".concat(_this4.qid, "/advice")).then(function (r) {
          _this4.advice = r.data.data;
          _this4.expert_loading = false;
        });
      }, function (err) {
        _this4.set_field_error('advice', err.data.error);

        _this4.expert_loading = false;
      });
    },
    approve_advice: function approve_advice(hours) {
      var _this5 = this;

      this.expert_loading = true;
      this.is_show_advice_timeout = false;
      this.$http.post("/api/questions/".concat(this.qid, "/advice/").concat(this.advice.id, "/approve"), {
        'hours': hours
      }, {
        emulateJSON: true
      }).then(function (r) {
        _this5.$http.get("/api/questions/".concat(_this5.qid, "/advice")).then(function (r) {
          _this5.advice = r.data.data;
          _this5.expert_loading = false;
          _this5.is_can_answer = true;
        });
      }, function (err) {
        _this5.set_field_error('advice', err.data.error);

        _this5.expert_loading = false;
      });
    },
    my_dislike: function my_dislike(answer_data) {
      return answer_data.my_like === -1;
    },
    my_like: function my_like(answer_data) {
      return answer_data.my_like === 1;
    },
    is_form_send_done: function is_form_send_done(upload_name) {
      return this.success && !this.loading && !(this.get_upload(upload_name) && this.get_upload(upload_name).active);
    },
    get_upload: function get_upload(name) {
      var ref = this.$refs[name]; // охуительный костыль. всем костылям костыль

      if (name === 'upload_second') {
        if (ref) {
          ref = ref[0];
        }
      }

      return ref;
    },
    request_and_load_answers: function request_and_load_answers() {
      var _this6 = this;

      var scroll_to_id = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;
      this.$http.get("/api/questions/".concat(this.qid, "/answers")).then(function (r) {
        _this6.count_answ = {};
        _this6.answers = r.data.data; // to count subanswers

        _this6.answers.forEach(function (x) {
          if (x.parent_id) {
            _this6.sub_answers_exists = true;
            _this6.count_answ[x.parent_id] = (_this6.count_answ[x.parent_id] || 0) + 1;
          }

          if (_this6.is_can_answer && x.author.id === _this6.user_id) {
            _this6.is_can_answer = false;
          }
        });

        _this6.load_answers = false;

        if (scroll_to_id) {
          Vue.nextTick(function () {
            _this6.scrollTo(scroll_to_id);
          });
        }
      });
    },
    get_requires_fields: function get_requires_fields() {
      return ['content'];
    },
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
      var _this7 = this;

      this.full_tree = !this.full_tree;
      this.answers = this.answers.map(function (x) {
        if (!x.parent_id) {
          x.is_expand = _this7.full_tree;
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

      if (this.advice && this.advice.status === 'closed') {
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
    sleep: function sleep(ms) {
      return new Promise(function (resolve) {
        return setTimeout(resolve, ms);
      });
    },
    save: function save(upload_name) {
      var _this8 = this;

      this.upload_form = upload_name;
      this.form_validate([this.requires_fields]);
      var data = {
        'parent_id': this.thread,
        'content': this.content
      };
      this.answer_id = false;
      this.put("/api/questions/".concat(this.qid, "/answers"), data, function (r) {
        _this8.answer_id = r.data.id;

        for (var i = 0; i < _this8.get_upload(upload_name).files.length; i++) {
          _this8.get_upload(upload_name).files[i].data = {
            id: _this8.answer_id
          };
        }

        _this8.get_upload(upload_name).active = true;

        if (_this8.is_form_send_done(upload_name)) {
          _this8.request_and_load_answers(_this8.answer_id);
        }

        _this8.set_form_success();
      }, function (err) {
        _this8.set_field_error('content', err.data.error);
      });
    },
    to_like_val: function to_like_val(id, val) {
      var a = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      a['like_count'] += val;
      a['is_can_like'] = false;
      a['my_like'] = val;
    },
    to_like: function to_like(id) {
      this.to_like_val(id, 1);
      this.$http.post("/api/questions/".concat(this.qid, "/answers/").concat(id, "/like"));
    },
    to_dislike: function to_dislike(id) {
      this.to_like_val(id, -1);
      this.$http.post("/api/questions/".concat(this.qid, "/answers/").concat(id, "/dislike"));
    },
    show_form_answer: function show_form_answer(id) {
      if (this.is_show_form_answer(id)) {
        return;
      }

      var a = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      this.thread = a.thread;
      this.content = '';
      this.parent_id = a.parent_id;
      this.files = [];
      this.$store.commit('init_state');
      this.answers.forEach(function (x) {
        return Vue.set(x, 'show_form', x.id === id);
      });
    },
    hide_form_answer: function hide_form_answer(id) {
      var a = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      a.show_form = false;
    },
    is_show_form_answer: function is_show_form_answer(id) {
      var a = this.answers.filter(function (i) {
        return i.id === id;
      })[0];
      return a['show_form'] === true;
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 357:
/***/ (function(module, exports) {

module.exports = "<div class=\"question-page_container\" itemscope itemtype=\"http://schema.org/Question\">\n    <div class=\"row pb-4\">\n\n        <div class=\"question-page_main-part\">\n\n            <article :id=\"article_id\" v-if=\"load_question\" class=\"entry\">\n\n\n                <div class=\"alert alert-warning\" role=\"alert\" v-if=\"you_must_pay\">\n                    <h4>Спасибо, мы получили ваш вопрос</h4>\n                    <p>Пожалуйста, оплатите услугу, что бы вопрос был принят в работу.</p>\n                </div>\n\n                <div class=\"alert alert-warning\" role=\"alert\" v-if=\"you_must_confirm_email\">\n                    <h4>Спасибо, мы получили ваш вопрос</h4>\n                    <p>Но он пока не виден юристам. Для публикации вопроса, подтвердите ваш электронный ящик,\n                    кликнув по ссылки в отправленном письме. Проверьте папку со спамом, если письмо не приходит.</p>\n                </div>\n\n\n\n                <h1 class=\"h2 mb-5\" itemprop=\"name\">{{ question.title }}</h1>\n\n                <div class=\"row\">\n                    <div class=\"question-page_l-col\">\n                        <time class=\"subtitle d-block mt-1\" :datetime=\"question.pub_date_c\"\n                              itemprop=\"dateCreated\">{{ question.pub_date }}</time>\n                        <span class=\"d-block\">№ {{ question.id }}</span>\n                        <span class=\"d-block\">{{ question.author.city.name }}</span>\n                    </div>\n\n                    <div class=\"question-page_r-col mb-4\">\n                        <h5 itemprop=\"author\" itemscope itemtype=\"http://schema.org/Person\"\n                            class=\"my-3 mb-lg-1 mt-lg-0\" :data-user_id=\"question.author.id\">\n                            <span itemprop=\"name\">{{ question.author.full_name }}</span>\n                        </h5>\n\n                        <div class=\"lead\" itemprop=\"text\" v-html=\"question.content\"></div>\n\n                        <div class=\"alert alert-secondary\" v-if=\"question.files\">\n                            <p class=\"file-list-item\" v-for=\"f in question.files\">\n                                <a target=\"_blank\" :href=\"f.path\" v-if=\"f.path\">{{ f.filename }}</a>\n                                <span v-else=\"f.path\">{{ f.filename }}</span>\n                            </p>\n                        </div>\n\n                        <div class=\"rubrics-list mt-4\" v-if=\"question.rubric\">\n                            <span class=\"rubrics-list-item\">\n                                <a :href=\"question.rubric.url\">{{ question.rubric.name }}</a>\n                            </span>\n                        </div>\n\n\n                        <div class=\"small text-muted mt-4\" v-if=\"!is_authorized && !question.reply_count \">\n                            <hr>На этот вопрос юрист ещё не ответил. Если вы знаете\n                                ответ, то можете <a class=\"text-dark\" href=\"/auth/registration/\" >зарегистрироваться</a>\n                                в качестве эксперта и ответить на него.\n\n                        </div>\n\n                        <div class=\"small text-muted mt-4\" v-if=\"is_iam_autor && !question.is_pay && !question.reply_count\"><hr>\n                            На ваш вопрос юрист ещё не ответил. К сожалению, на бесплатный вопрос мы не даём гарантии\n                            ответа.\n                            <!--span v-if=\"default_settings.urls\">\n                                Если вам нужна развернутая гаратированная консультация,\n                                <a  class=\"text-dark\" :href=\"default_settings.urls.ask_question\">задайте вопрос</a> платно.\n                            </span-->\n                        </div>\n\n                    </div>\n\n\n                </div>\n\n            </article>\n\n        </div>\n\n        <aside class=\"question-page_aside-part pt-3\">\n            <div id=\"advice_status\" v-if=\"question.is_pay && advice\">\n                <div class=\"lawyer-list\">\n                    <h5 class=\"consult-state\" :class=\"advice.status\">{{ advice.status_display }}</h5>\n                    <p class=\"subtitle\">Цена консультации</p>\n                    <p class=\"cost rub\">{{ advice.cost }}</p>\n\n                    <div v-if=\"is_expert_appointed\">\n\n                        <p class=\"subtitle\" v-if=\"advice.status != 'closed'\">Консультацию ведёт эксперт</p>\n                        <p class=\"subtitle\" v-if=\"advice.status == 'closed'\">Консультацию провел эксперт</p>\n\n\n                        <div class=\"consult-lawyer \">\n                            <a class=\"pht\" :href=\"advice.expert.url\">\n                                <img :src=\"advice.expert.info.photo\" :alt=\"advice.expert.full_name\"/>\n                            </a>\n                            <h6><a :href=\"advice.expert.url\">{{ advice.expert.full_name }}</a></h6>\n                        </div>\n                    </div>\n                    <div v-else>\n                        <p class=\"subtitle\">Эксперт ещё не назначен</p>\n                    </div>\n\n\n                    <div class=\"normal\" v-if=\"is_show_button_payment\">\n                        <p>Эксперт будет назначен после оплаты.</p>\n                        <form method=\"POST\" action=\"https://money.yandex.ru/quickpay/confirm.xml\">\n                            <input type=\"hidden\" name=\"receiver\" :value=\"default_settings.advice.money_yandex_purse\">\n                            <input type=\"hidden\" name=\"quickpay-form\" value=\"shop\">\n                            <input type=\"hidden\" name=\"formcomment\" :value=\"default_settings.advice.payment_form_title\">\n                            <input type=\"hidden\" name=\"label\" :value=\"'advice.' + question.id\">\n                            <input type=\"hidden\" name=\"targets\"\n                                   :value=\"default_settings.advice.payment_form_target + question.id\">\n                            <input type=\"hidden\" name=\"successURL\"\n                                   :value=\"default_settings.settings.site_protocol+'://'+default_settings.settings.site_url+question.url\">\n                            <input type=\"hidden\" name=\"sum\" :value=\"advice.cost\" data-type=\"number\">\n                            <!--input type=\"hidden\" name=\"paymentType\" value=\"AC\"/-->\n                            <input class=\"btn btn-success btn-block\" type=\"submit\" value=\"Оплатить\">\n                        </form>\n                    </div>\n\n\n                    <div class=\"normal\" v-if=\"is_iam_autor && advice.status == 'paid'\">\n                        <p>Оплачено, ждём подтверждение оплаты.</p>\n                    </div>\n\n                    <div class=\"normal\" v-if=\"!expert_loading && advice.status == 'payment_confirmed'\">\n                        <div v-if=\"is_iam_expert && !reject\">\n                            <p>Вам необходимо принять заявку в течение {{ default_settings.advice.overdue_time }} мин.</p>\n                            <div class=\"d-flex align-items-center\" v-if=\"!error_fields.advice\">\n                                <div class=\"btn-group\">\n                                    <a class=\"btn btn-success btn-sm dropdown-toggle\"\n                                       href=\"javascript:void(0);\"\n                                      @click=\"is_show_advice_timeout = true\">Принять </a>\n                                    <div class=\"dropdown-menu\"\n                                         :class=\"{'d-block': is_show_advice_timeout}\"\n                                        @mouseleave=\"is_show_advice_timeout = false\">\n                                        <div class=\"dropdown-header\">Отвечу через:</div>\n                                        <a class=\"dropdown-item\" href=\"javascript:void(0);\" @click=\"approve_advice(1)\">1 час</a>\n                                        <a class=\"dropdown-item\" href=\"javascript:void(0);\" @click=\"approve_advice(2)\">2 часа</a>\n                                        <a class=\"dropdown-item\" href=\"javascript:void(0);\" @click=\"approve_advice(3)\">3 часа</a>\n                                        <a class=\"dropdown-item\" href=\"javascript:void(0);\" @click=\"approve_advice(4)\">4 часа</a>\n                                        <a class=\"dropdown-item\" href=\"javascript:void(0);\" @click=\"approve_advice(6)\">6 часов</a>\n                                        <a class=\"dropdown-item\" href=\"javascript:void(0);\" @click=\"approve_advice(12)\">12 часов</a>\n                                        <a class=\"dropdown-item\" href=\"javascript:void(0);\" @click=\"approve_advice(24)\">24 часа</a>\n                                    </div>\n                                </div>\n                                <a class=\"text-muted ml-3\" href=\"javascript:void(0);\" @click=\"reject_advice\">Отказаться</a>\n                            </div>\n                        </div>\n                        <div v-else>\n                            <p class=\"mt-3\">Идёт подбор эксперта по данному вопросу (обычно в течении 30 мин.)</p>\n                        </div>\n\n                        <div class=\"text-danger\" v-if=\"reject\">\n                            Вы отказались\n                        </div>\n\n\n\n\n                    </div>\n\n                    <div class=\"normal\" v-if=\"!expert_loading && advice.status == 'inwork'\">\n                        <p class=\"mt-3\" v-if=\"is_iam_expert\">Вы должны ответить до {{ advice.answered_date }} мск.</p>\n                        <p class=\"mt-3\" v-if=\"is_iam_autor\">Эксперт принял вопрос и ответит до {{ advice.answered_date }} мск.</p>\n                    </div>\n\n                    <div class=\"normal\" v-if=\"!expert_loading && advice.status == 'answered' && is_iam_autor && !error_fields.advice\">\n                        <p class=\"mt-3\">Эксперт ответил на вопрос, если у вас нет дополнительных вопросов нажмите на:</p>\n                        <p>\n                            <a class=\"btn btn-success btn-sm\"\n                              href=\"javascript:void(0);\"\n                              @click=\"confirm_advice\">Вопрос решён</a>\n                        </p>\n                    </div>\n\n                    <div class=\"text-danger mt-3\" v-if=\"error_fields.advice\">\n                        <h6>{{ error_fields.advice }}</h6>\n                        <p class=\"small\">При выполнении действия произошла ошибка. Разработчики уже узнали об этом и трудятся над\n                            исправлением.</p>\n                    </div>\n                </div>\n            </div>\n            <div class=\"normal\" v-if=\"expert_loading\">\n                <img src=\"/static/img/preloaders/spinner200.svg\">\n            </div>\n            <h5 class=\"mb-4\">Консультация юриста бесплатно</h5>\n            <p class=\"lead\"><a href=\"tel:84959844607\">8 (495) 984-46-07</a><br><strong class=\"small\">Москва и моск. обл.</strong></p>\n            <p class=\"lead\"><a href=\"tel:88124580471\">8 (812) 458-04-71</a><br><strong class=\"small\">Санкт-Петербург и лен. обл.</strong></p>\n\n        </aside>\n\n\n    </div>\n\n    <div id=\"answer\">\n        <div id=\"answer_block\">\n\n            <div class=\"row\">\n                <div class=\"question-page_main-part\">\n                    <div class=\"row\">\n                        <div class=\"question-page_r-col ml-auto\" v-if=\"!load_form\">\n                            <div id=\"form\" v-if=\"is_can_answer\" class=\"mb-4\">\n                                <hr class=\"mt-0 mb-3\">\n                                <div class=\"form-group\">\n                                    <label for=\"reply\" class=\"h6 mb-3\">Ответить на вопрос:</label>\n                                    <textarea class=\"form-control\"\n                                              v-model=\"content\"\n                                              :class=\"{'is-invalid': error_fields.content }\"\n                                              id=\"reply\"\n                                              rows=\"5\"\n                                              :disabled=\"file_first_form_loading\"\n                                              placeholder=\"\"></textarea>\n                                    <span class=\"invalid-feedback\"\n                                          v-if=\"error_fields.content\">{{ error_fields.content }}</span>\n                                </div>\n                                <div class=\"form-group\">\n                                    <div v-for=\"(file, index) in files\" class=\"file-loader\" :data-filename=\"file.name\">\n                                        <i class=\"bar\" :id=\"file.id\"><i :style=\"{width: file.progress + '%'}\"></i></i>\n                                        <a href=\"#\" @click.prevent=\"$refs.upload_first.remove(file)\" class=\"close\"><i\n                                                class=\"icon-cancel\"></i></a>\n                                    </div>\n\n                                    <button type=\"submit\"\n                                            @click=\"save('upload_first')\"\n                                            class=\"btn btn-primary btn-sm\"\n                                            :disabled='loading||success||($refs.upload_first&&$refs.upload_first.active)'>\n                                        <span v-if=\"loading||($refs.upload_first&&$refs.upload_first.active)\">Загрузка...</span>\n                                        <span v-else-if=\"success\">Успешно</span>\n                                        <span v-else>Отправить</span>\n                                    </button>\n\n                                    <file-upload\n                                            :post-action=\"post_action\"\n                                            class=\"btn btn-link btn-sm m-0\"\n                                            extensions=\"gif,jpg,jpeg,png,webp,pdf,xls\"\n                                            accept=\"image/png,image/gif,image/jpeg,image/webp,application/pdf,application/vnd.ms-excel\"\n                                            :multiple=\"true\"\n                                            :size=\"1024 * 1024 * 100\"\n                                            v-model=\"files\"\n                                            ref=\"upload_first\"><span class=\"icon-folder mr-2\"></span> Прикрепить файлы\n                                    </file-upload>\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n                </div>\n            </div>\n\n\n            <div class=\"row question-page_gradient py-5\" v-if=\"load_answers\">\n                <div class=\"question-page_main-part\">\n                    <img src=\"/static/img/preloaders/spinner200.svg\">\n                </div>\n            </div>\n\n            <div class=\"row question-page_gradient py-5\" v-if=\"answers_total\">\n                <div class=\"question-page_main-part\">\n                    <div class=\"row\">\n                        <h3 class=\"answer-list-head col offset-lg-1\" id=\"div-id\">Ответы юристов\n                            <a href=\"javascript:void(0);\" @click=\"expand_all\"\n                               v-if=\"sub_answers_exists\">({{ tree_link_name }})</a>\n                            <span class=\"d-none answer__counter\" itemprop=\"answerCount\">2</span>\n                        </h3>\n\n                    </div>\n\n\n                    <div name=\"x\" v-for=\"answer_data in answers\" itemprop=\"suggestedAnswer\" itemscope\n                         itemtype=\"http://schema.org/Answer\"\n                         role=\"answer\"\n                         :name=\"answer_data.id\"\n                         :ref=\"answer_data.id\"\n                         :data-answer_id=\"answer_data.id\"\n                         :data-thread=\"answer_data.thread\"\n                         class=\"answer entry\"\n                         :class=\"{'answer-push': answer_data.parent_id }\"\n                         v-if=\"is_show_comment(answer_data.id)\">\n\n                        <hr class=\"my-4\"/>\n\n                        <header class=\"answer-header\">\n                            <div class=\"question-page_l-col\">\n                                <a class=\"answer-header_photo\" :href=\"answer_data.author.url\"\n                                   v-if=\"answer_data.author.role=='lawyer'\">\n                                    <img :src=\"answer_data.author.info.photo\" :alt=\"answer_data.author.full_name\"/>\n                                </a>\n                            </div>\n\n\n                            <div class=\"question-page_r-col\">\n                                <h6 class=\"mb-0\" itemprop=\"name\">\n                                    <a :href=\"answer_data.author.url\"\n                                       v-if=\"answer_data.author.role=='lawyer'\">{{ answer_data.author.full_name }}</a>\n                                    <span v-else>{{ answer_data.author.full_name }}</span>\n                                </h6>\n\n\n                                <div class=\"normal text-muted\"\n                                     v-if=\"!answer_data.parent_id\">{{ answer_data.author.about_me }}</div>\n\n                                <div class=\"answer-header_medal mt-3\" v-if=\"!answer_data.parent_id\">\n                            <span class=\"item\" title=\"Рейтинг эксперта\">\n                                <i class=\"icon-star\"></i>\n                                <span class=\"v\">{{ answer_data.author.stat.rating }}</span>\n                            </span>\n                                    <span class=\"item\" title=\"Стаж\">\n                                <i class=\"icon-medal\"></i>\n                                <span class=\"v\">{{ answer_data.author.info.stage }}</span>\n                            </span>\n                                    <span class=\"item\" title=\"Всего консультаций\">\n                                <i class=\"icon-forum\"></i>\n                                <span class=\"v\">{{ answer_data.author.info.answer_count }}</span>\n                            </span>\n\n                                    <span class=\"item\" title=\"Положительных отзывов\">\n                                <i class=\"icon-like\"></i>\n                                <span class=\"v\">{{ answer_data.author.info.review_count }}</span>\n                            </span>\n\n                                </div>\n                            </div>\n\n                        </header>\n\n                        <div class=\"row\">\n\n                            <div class=\"question-page_l-col\">\n                                <time class=\"subtitle d-block mt-1\" itemprop=\"dateCreated\"\n                                      :datetime=\"answer_data.pub_date_c\">{{ answer_data.pub_date }}</time>\n                                <span class=\"d-block\">№ {{ answer_data.id }}</span>\n                                <span class=\"d-block\"\n                                      v-if=\"answer_data.author.role=='client'\">{{ answer_data.author.about_me }}</span>\n                            </div>\n\n                            <div class=\"question-page_r-col content\">\n                                <div class=\"text\" itemprop=\"text\" v-html=\"answer_data.content\"></div>\n                                <p class=\"text-muted normal\" v-if=\"answer_data.author.info.signature\">\n                                    {{ answer_data.author.info.signature }}\n                                </p>\n\n                                <div class=\"alert alert-secondary\" v-if=\"answer_data.files\">\n                                    <p class=\"file-list-item\" v-for=\"f in answer_data.files\">\n                                        <a target=\"_blank\" :href=\"f.path\" v-if=\"f.path\">{{ f.filename }}</a>\n                                        <span v-else=\"f.path\">{{ f.filename }}</span>\n                                    </p>\n                                </div>\n                            </div>\n\n\n                        </div>\n\n\n                        <footer class=\"answer-footer row\">\n\n                            <div class=\"question-page_r-col ml-auto d-flex align-items-center justify-content-between flex-column flex-sm-row\">\n                                <div class=\"answer-footer-action normal align-self-start align-self-md-center\">\n                                    <a href=\"javascript:void(0);\"\n                                       v-if=\"get_add_question_link(answer_data.id)\"\n                                       @click=\"show_form_answer(answer_data.id)\">\n                                        {{ get_add_question_link(answer_data.id)}}</a><br/>\n                                    <a href=\"javascript:void(0);\" class=\"small text-muted\"\n                                       v-if=\"is_possible_expand_answer(answer_data.id)\"\n                                       @click=\"expand_answer(answer_data.id)\">\n                                        {{ get_exand_answer_name(answer_data.id) }}</a>\n                                </div>\n                                <div class=\"align-self-end mt-3 mt-sm-0\" v-if=\"answer_data.author.role == 'lawyer'\">\n                                    <div class=\"answer-like\">\n                                        <div class=\"answer-like-sign dropdown\">{{ like_title(answer_data.id) }}</div>\n                                        <div class=\"answer-like-block\">\n\n                                            <i class=\"icon-dislike order-1\" v-if=\"answer_data.is_can_like\"\n                                               @click=\"to_dislike(answer_data.id)\"></i>\n\n                                            <i class=\"icon-dislike order-1 noactive\"\n                                               :class=\"{'text-danger':my_dislike(answer_data)}\"\n                                               v-else></i>\n\n\n                                            <i class=\"icon-like order-3\" v-if=\"answer_data.is_can_like\"\n                                               @click=\"to_like(answer_data.id)\"></i>\n\n\n                                            <i class=\"icon-like order-3 noactive\"\n                                               :class=\"{'text-success':my_like(answer_data)}\"\n                                               v-else></i>\n\n\n                                            <span class=\"order-2\"\n                                                  :class=\"{'text-success': answer_data.like_count>0, 'text-danger': answer_data.like_count<0}\">\n                                        {{ answer_data.like_count }}</span>\n                                        </div>\n                                    </div>\n                                </div>\n                            </div>\n\n                            <div class=\"question-page_r-col ml-auto pt-3\">\n                                <div id=\"form\" v-if=\"is_show_form_answer(answer_data.id)\">\n                                    <div class=\"form-group\">\n                                        <!--label for=\"reply\" class=\"h6 mb-2\">Ответ</label-->\n                                        <textarea class=\"form-control normal\"\n                                                  v-model=\"content\"\n                                                  :class=\"{'is-invalid': error_fields.content }\"\n                                                  id=\"reply\"\n                                                  rows=\"5\"\n                                                  :disabled=\"file_second_form_loading\"\n                                                  placeholder=\"\"></textarea>\n                                        <span class=\"invalid-feedback\"\n                                              v-if=\"error_fields.content\">{{ error_fields.content }}</span>\n                                    </div>\n\n                                    <div v-for=\"(file, index) in files\" class=\"file-loader\" :data-filename=\"file.name\">\n                                        <i class=\"bar\" :id=\"file.id\"><i :style=\"{width: file.progress + '%'}\"></i></i>\n                                        <a href=\"#\" @click.prevent=\"$refs.upload_second[0].remove(file)\"\n                                           class=\"close\"><i\n                                                class=\"icon-cancel\"></i></a>\n                                    </div>\n\n                                    <div class=\"form-group d-flex align-items-center\">\n\n                                        <button type=\"submit\"\n                                                @click=\"save('upload_second')\"\n                                                class=\"btn btn-primary btn-sm\"\n                                                :disabled='loading||success||($refs.upload_second&&$refs.upload_second[0]&&$refs.upload_second[0].active)'>\n                                            <span v-if=\"loading||($refs.upload_second&&$refs.upload_second[0]&&$refs.upload_second[0].active)\">Загрузка...</span>\n                                            <span v-else-if=\"success\">Успешно</span>\n                                            <span v-else>Отправить</span>\n                                        </button>\n\n                                        <file-upload\n                                                :post-action=\"post_action\"\n                                                class=\"btn btn-link btn-sm m-0\"\n                                                extensions=\"gif,jpg,jpeg,png,webp,pdf,xls\"\n                                                accept=\"image/png,image/gif,image/jpeg,image/webp,application/pdf,application/vnd.ms-excel\"\n                                                :multiple=\"true\"\n\n                                                :size=\"1024 * 1024 * 100\"\n                                                v-model=\"files\"\n                                                ref=\"upload_second\"><span class=\"icon-folder mr-2\"></span> Прикрепить\n                                            файлы\n                                        </file-upload>\n\n                                        <a href=\"javascript:void(0);\" class=\"text-muted ml-auto small\"\n                                           @click=\"hide_form_answer(answer_data.id)\">Отмена</a>\n\n                                    </div>\n                                </div>\n                            </div>\n\n                        </footer>\n\n\n                    </div>\n                </div>\n\n\n                <aside class=\"question-page_aside-part\">\n                    <h4 class=\"mb-4\">Юристы ответившие на этот вопрос:</h4>\n\n                    <div class=\"lawyer-list\">\n                        <div v-for=\"answer_data in answers\"\n                             v-if=\"!answer_data.parent_id\"\n                             role=\"answers_selector\"\n                             class=\"lawyer-list_item lawyer-list_item-action\"\n                             :data-answer_id=\"answer_data.id\"\n                             @click=\"scrollTo(answer_data.id)\">\n                            <div class=\"lawyer-list_header\">\n                        <span class=\"ph\">\n                            <img :src=\"answer_data.author.info.photo\" :alt=\"answer_data.author.full_name\">\n                        </span>\n                                <div class=\"nm ml-3 text-primary\">{{ answer_data.author.full_name }}</div>\n                            </div>\n                            <p class=\"lawyer-list_body\"> {{ answer_data.short_content }} </p>\n                        </div>\n                    </div>\n\n                </aside>\n\n            </div>\n\n        </div>\n    </div>\n</div>";

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