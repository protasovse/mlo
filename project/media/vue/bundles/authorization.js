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
/******/ 	return __webpack_require__(__webpack_require__.s = 131);
/******/ })
/************************************************************************/
/******/ ({

/***/ 131:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _index = _interopRequireDefault(__webpack_require__(132));

var _index2 = _interopRequireDefault(__webpack_require__(47));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var app = new Vue({
  name: 'instance_auth',
  'el': '#app',
  store: new Vuex.Store(_index2.default),
  router: new VueRouter({
    mode: 'history',
    routes: _index.default
  })
});

/***/ }),

/***/ 132:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _index = _interopRequireDefault(__webpack_require__(133));

var _index2 = _interopRequireDefault(__webpack_require__(135));

var _index3 = _interopRequireDefault(__webpack_require__(139));

var _index4 = _interopRequireDefault(__webpack_require__(141));

var _index5 = _interopRequireDefault(__webpack_require__(143));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = [{
  path: '/auth/',
  component: _index5.default,
  name: 'auth',
  children: [{
    path: 'login',
    components: {
      default: _index2.default,
      title: {
        template: '<span>Вход</span>'
      }
    },
    name: 'login'
  }, {
    path: 'registration',
    components: {
      default: _index3.default,
      title: {
        template: '<span>Регистрация юриста</span>'
      }
    },
    name: 'registration'
  }, {
    path: 'forgot',
    components: {
      default: _index.default,
      title: {
        template: '<span>Восстановить пароль</span>'
      }
    },
    name: 'forgot'
  }, {
    path: 'reset/:token',
    name: 'reset',
    components: {
      default: _index4.default,
      title: {
        template: '<span>Создать новый пароль</span>'
      }
    },
    props: {
      default: true
    }
  }, {
    path: 'activate/:token',
    name: 'activate',
    components: {
      default: _index2.default,
      title: {
        template: '<span>Вход</span>'
      }
    },
    props: {
      default: true
    }
  }, {
    path: '*',
    redirect: 'login'
  }]
}];
exports.default = _default;

/***/ }),

/***/ 133:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _template = _interopRequireDefault(__webpack_require__(134));

var _logged_disallow = _interopRequireDefault(__webpack_require__(51));

var _form = _interopRequireDefault(__webpack_require__(27));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = {
  mixins: [_logged_disallow.default, _form.default],
  name: 'auth_forgot',
  template: _template.default,
  data: function data() {
    return {
      email: this.get_saved_field('email')
    };
  },
  methods: {
    default_error: function default_error() {
      return 'Ошибка восстановления доступа';
    },
    get_requires_fields: function get_requires_fields() {
      return ['email'];
    },
    save: function save() {
      var _this = this;

      try {
        this.form_validate([this.requires_fields]);
        this.post('/api/user/forgot', {
          email: this.email
        }, function () {
          _this.set_form_success("Ссылка для восстановления пароля была отправлена на почту");
        });
      } catch (err) {
        this.set_form_error(err.message);
      }
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 134:
/***/ (function(module, exports) {

module.exports = "<div class=\"row\">\n\n    <div class=\"l-col\" method=\"post\">\n\n        <div class=\"form-group\">\n            <input type=\"email\" class=\"form-control\" :class=\"{'is-invalid': error_fields.email }\"\n                   placeholder=\"Электронный ящик\" name=\"email\" v-model=\"email\" @change=\"save_field_value('email', email)\">\n            <span class=\"invalid-feedback\" v-if=\"error_fields.email\">{{ error_fields.email }}</span>\n\n        </div>\n        <button type=\"submit\" @click=\"save\" class=\"btn btn-outline-primary col-12\" :disabled=success>\n            <span v-if=\"loading\">Загрузка...</span>\n            <span v-else-if=\"success\">Письмо отправлено</span>\n            <span v-else>Отправить письмо</span>\n        </button>\n\n        <div class=\"msg\" v-if=\"success\"><!-- .l-col .msg -->\n            <p class=\"suc\">{{ success_txt }}</p>\n        </div>\n\n\n    </div>\n\n    <div class=\"r-col\">\n        <h4>Введите адрес электронной почты и мы вышлем инструкцию для восстановления пароля.</h4>\n    </div>\n\n    <p class=\"reg\">\n        <router-link :to=\"{name: 'login'}\">Вход</router-link>\n        или\n        <router-link :to=\"{name: 'registration'}\">Регистрация юриста</router-link>\n    </p>\n\n</div>\n\n\n";

/***/ }),

/***/ 135:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _template = _interopRequireDefault(__webpack_require__(136));

var _logged_disallow = _interopRequireDefault(__webpack_require__(51));

var _form = _interopRequireDefault(__webpack_require__(27));

var _social = _interopRequireDefault(__webpack_require__(94));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = {
  mixins: [_logged_disallow.default, _form.default, _social.default],
  name: 'auth_login',
  template: _template.default,
  props: ['token'],
  data: function data() {
    return {
      email: this.get_saved_field('email'),
      password: '',
      unactive: false
    };
  },
  mounted: function mounted() {
    var _this = this;

    this.$http.get('/api/user/flash').then(function (r) {
      if (r.data.success) {
        _this.set_form_success(r.data.data);
      }
    }, function (r) {
      _this.mark_error_fields(r);

      _this.set_form_error(r.data.error);
    });

    if (this.token) {
      try {
        this.post('/api/user/activate', {
          'token': this.token
        }, function () {
          _this.set_form_success("Аккаунт успешно активирован. Вы можете войти на сайт, используя данные, указанные при регистрации");
        }, function (r) {
          _this.unactive = r.data.code === 'unactive';

          _this.process_error(r);
        });
      } catch (err) {
        this.set_form_error(err.message);
      }
    }
  },
  methods: {
    default_error: function default_error() {
      return 'Не удалось авторизироваться. Не верный пароль';
    },
    get_requires_fields: function get_requires_fields() {
      return ['email', 'password'];
    },
    save: function save() {
      var _this2 = this;

      try {
        this.form_validate([this.requires_fields]);
        this.get('/api/user', {
          email: this.email,
          password: this.password
        }, function (r) {
          window.location.href = _this2.$route.query.next ? _this2.$route.query.next : '/вопросы';
        }, function (r) {
          _this2.unactive = r.data.code === 'unactive';

          _this2.process_error(r);
        });
      } catch (err) {
        this.set_form_error(err.message);
      }
    },
    send_activation: function send_activation() {
      var _this3 = this;

      this.get('/api/user/resend', {
        email: this.email,
        token: this.token
      }, function () {
        _this3.set_form_success('Письмо отправлено повторно. Проверьте, пожалуйста, почту.');
      }, function () {
        _this3.set_form_error('Нe удалось отрпавить активационное письмо');
      });
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 136:
/***/ (function(module, exports) {

module.exports = "<div class=\"row\">\n    <div class=\"_l-col col-12\">\n        <div class=\"form-group row\">\n            <label class=\"col-sm-4 col-form-label required\">Эл. почта</label>\n            <div class=\"col-sm-8\">\n                <input type=\"email\" class=\"form-control\" :class=\"{'is-invalid': error_fields.email }\"\n                       placeholder=\"login@email.ru\" name=\"email\" v-model=\"email\"\n                       @change=\"save_field_value('email', email)\">\n                <span class=\"invalid-feedback\" v-if=\"error_fields.email\">{{ error_fields.email }}</span>\n            </div>\n        </div>\n        <div class=\"form-group row\">\n            <label class=\"col-sm-4 col-form-label required\">Пароль</label>\n            <div class=\"col-sm-8\">\n                <input type=\"password\" class=\"form-control\" :class=\"{'is-invalid': error_fields.password }\"\n                       placeholder=\"**********\" v-model=\"password\" name=\"password\" @keyup.13=\"save\">\n                <span class=\"invalid-feedback\" v-if=\"error_fields.password\">{{ error_fields.password }}</span>\n            </div>\n        </div>\n\n        <div class=\"form-group row\">\n            <div class=\"col-sm-8 ml-auto\">\n\n                <button type=\"submit\" class=\"btn btn-outline-primary\" @click=\"save\" :disabled=loading>\n                    <span v-if=\"loading\">Загрузка...</span><span v-else>Войти</span>\n                </button>\n\n\n                <div class=\"msg\" v-if=\"success\"><!-- .l-col .msg -->\n                    <p class=\"suc\">{{ success_txt }}</p>\n                </div>\n\n                <div class=\"msg\" v-if=\"error\"><!-- .l-col .msg -->\n                    <p class=\"err\">{{ error_txt }}</p>\n                </div>\n\n                <div class=\"msg\" v-if=\"unactive\"><!-- .l-col .msg -->\n                    <p class=\"err\">\n                        Не пришло письмо с подтверждением?<br/>\n                        <a @click=\"send_activation\" href=\"javascript:void(0)\">Выслать активационное письмо еще раз</a>\n                    </p>\n                </div>\n            </div>\n        </div>\n\n        <div class=\"col-12\">\n            <hr class=\"my-4\">\n            <p class=\"_reg normal text-muted\">\n                Ещё не зарегистрированны?\n                <router-link :to=\"{name: 'registration'}\">Регистрация юриста</router-link><br>\n                <router-link :to=\"{name: 'forgot'}\">Восстановить пароль</router-link>\n            </p>\n        </div>\n    </div>\n\n    <!--div class=\"hr\"></div>\n\n    <div class=\"r-col\">\n        <h4>войти через соцсети:</h4>\n        <button type=\"submit\" class=\"btn-vk\" @click=\"vk\"><span class=\"icon-vk\"></span></button>\n        <!--button type=\"submit\" class=\"btn-od\"><span class=\"icon-od\"></span></button>\n        <button type=\"submit\" class=\"btn-ml\"><span class=\"icon-ml\"></span></button>\n        <button type=\"submit\" class=\"btn-fb\" @click=\"fb\"><span class=\"icon-fb\"></span></button>\n        <button type=\"submit\" class=\"btn-tw\"><span class=\"icon-tw\"></span></button>\n        <button type=\"submit\" class=\"btn-gl\"><span class=\"icon-gl\"></span></button-->\n\n\n    <!--div class=\"msg\" v-if=\"error_fields.social\">\n            <p class=\"err\" v-if=\"error_fields.social\">{{ error_fields.social }}</p>\n        </div-->\n    <!--/div-->\n\n</div>";

/***/ }),

/***/ 137:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var _default = {
  VK_AUTHORIZE_URL: 'https://oauth.vk.com/authorize',
  VK_CLIENT_ID: 3344860,
  VK_DISPLAY: 'page',
  VK_REDIRECT_URL: 'http://xn--h1abiilhh6g.xn--80asehdb:8000/auth/vk',
  VK_RESPONCE_TYPE: 'code',
  VK_SCOPE: 4194304,
  VK_API_VERSION: 5.69
};
exports.default = _default;

/***/ }),

/***/ 138:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var _default = {
  FB_AUTHORIZE_URL: 'https://www.facebook.com/v2.11/dialog/oauth',
  // FB_CLIENT_ID: 1422542761187900,
  FB_CLIENT_ID: 148235395785879,
  // FB_REDIRECT_URL: 'https://xn--h1abiilhh6g.xn--80asehdb/auth/fb',
  FB_REDIRECT_URL: 'http://xn--h1abiilhh6g.xn--80asehdb:8000/auth/fb',
  FB_SCOPE: 'email'
};
exports.default = _default;

/***/ }),

/***/ 139:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _template = _interopRequireDefault(__webpack_require__(140));

var _logged_disallow = _interopRequireDefault(__webpack_require__(51));

var _form = _interopRequireDefault(__webpack_require__(27));

var _social = _interopRequireDefault(__webpack_require__(94));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = {
  mixins: [_logged_disallow.default, _form.default, _social.default],
  name: 'auth_reg',
  template: _template.default,
  data: function data() {
    return {
      email: this.get_saved_field('email'),
      password: '',
      first_name: '',
      last_name: '',
      patronymic: ''
    };
  },
  methods: {
    default_error: function default_error() {
      return 'Не удалось зарегистрироваться';
    },
    get_requires_fields: function get_requires_fields() {
      return ['email', 'password', 'first_name', 'last_name', 'patronymic'];
    },
    save: function save() {
      var _this = this;

      try {
        this.form_validate([this.requires_fields, this.password_strength_validate]);
        this.post('/api/user', {
          email: this.email,
          password: this.password,
          first_name: this.first_name,
          last_name: this.last_name,
          patronymic: this.patronymic
        }, function () {
          _this.set_form_success('Регистрация прошла успешно. Вам на почту было отправлено письмо.  ' + 'Пожауйста, перейдите по ссылке, указанной в письме, и активируйте свой аккаунт.');
        });
      } catch (err) {
        this.set_form_error(err.message);
      }
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 140:
/***/ (function(module, exports) {

module.exports = "<div class=\"row\">\n    <div class=\"_l-col col-12\">\n\n        <div class=\"form-group row\">\n            <label class=\"col-sm-4 col-form-label required\">Фамилия</label>\n            <div class=\"col-sm-8\">\n                <input type=\"text\" class=\"form-control\" placeholder=\"\" v-model=\"last_name\"\n                       name=\"last_name\" :class=\"{'is-invalid': error_fields.last_name }\">\n                <span class=\"invalid-feedback\" v-if=\"error_fields.last_name\">{{ error_fields.last_name }}</span>\n            </div>\n        </div>\n        <div class=\"form-group row\">\n            <label class=\"col-sm-4 col-form-label required\">Имя</label>\n            <div class=\"col-sm-8\">\n                <input type=\"text\" class=\"form-control\" placeholder=\"\" v-model=\"first_name\"\n                       name=\"first_name\" :class=\"{'is-invalid': error_fields.first_name }\">\n                <span class=\"invalid-feedback\" v-if=\"error_fields.first_name\">{{ error_fields.first_name }}</span>\n            </div>\n        </div>\n        <div class=\"form-group row\">\n            <label class=\"col-sm-4 col-form-label required\">Отчество</label>\n            <div class=\"col-sm-8\">\n                <input type=\"text\" class=\"form-control\" placeholder=\"\" v-model=\"patronymic\"\n                       name=\"patronymic\" :class=\"{'is-invalid': error_fields.patronymic }\">\n                <span class=\"invalid-feedback\" v-if=\"error_fields.patronymic\">{{ error_fields.patronymic }}</span>\n            </div>\n        </div>\n        <div class=\"form-group row\">\n            <label class=\"col-sm-4 col-form-label required\">Эл. почта</label>\n            <div class=\"col-sm-8\">\n                <input type=\"email\" class=\"form-control\" placeholder=\"\" v-model=\"email\"\n                       name=\"email\" :class=\"{'is-invalid': error_fields.email }\"\n                       @change=\"save_field_value('email', email)\">\n                <span class=\"invalid-feedback\" v-if=\"error_fields.email\">{{ error_fields.email }}</span>\n            </div>\n        </div>\n        <div class=\"form-group row\">\n            <label class=\"col-sm-4 col-form-label required\">Пароль</label>\n            <div class=\"col-sm-8\">\n                <input type=\"password\" class=\"form-control\" placeholder=\"\" v-model=\"password\"\n                       name=\"password\" @keyup.13=\"save\" :class=\"{'is-invalid': error_fields.password }\">\n                <span class=\"invalid-feedback\" v-if=\"error_fields.password\">{{ error_fields.password }}</span>\n            </div>\n        </div>\n\n        <div class=\"form-group row\">\n            <div class=\"col-sm-4 col-sm-8 ml-auto\">\n                <button type=\"submit\" @click=\"save\" class=\"btn btn-outline-primary mt-4\" :disabled='loading||success'>\n                    <span v-if=\"loading\">Загрузка...</span>\n                    <span v-else-if=\"success\">Успешно</span>\n                    <span v-else>Зарегистрироваться</span>\n                </button>\n\n                <div class=\"msg\" v-if=\"success\"><!-- .l-col .msg -->\n                    <p class=\"suc\">{{ success_txt }}</p>\n                </div>\n\n                <div class=\"msg\" v-if=\"error\"><!-- .l-col .msg -->\n                    <p class=\"err\">{{ error_txt }}</p>\n                </div>\n            </div>\n        </div>\n\n    </div>\n\n    <!--div class=\"hr\"></div-->\n\n    <!--div class=\"r-col\"-->\n    <!--i class=\"icon-logo\"></i-->\n    <!--h4>Что даёт юристу регистрация на Мойюрист.онлайн?</h4>\n    <p>1. Удалённый заработок в удобное время</p>\n    <p>2. Новые клиенты и репутация</p>\n    <p>3. Узнаваемость в Интернете</p>\n    <p>4. Реализация способностей, опыт, общение с коллегами</p>\n    <p>5. Юридическая клиника</p-->\n    <!--h4>войти через соцсети:</h4>\n    <button type=\"submit\" class=\"btn-vk\" @click=\"vk\"><span class=\"icon-vk\"></span></button>\n    <button type=\"submit\" class=\"btn-od\"><span class=\"icon-od\"></span></button>\n    <button type=\"submit\" class=\"btn-ml\"><span class=\"icon-ml\"></span></button>\n    <button type=\"submit\" class=\"btn-fb\" @click=\"fb\"><span class=\"icon-fb\"></span></button>\n    <button type=\"submit\" class=\"btn-tw\"><span class=\"icon-tw\"></span></button>\n    <button type=\"submit\" class=\"btn-gl\"><span class=\"icon-gl\"></span></button-->\n    <!--/div-->\n\n    <div class=\"col-12\">\n        <hr class=\"my-4\">\n        <p class=\"_reg normal text-muted\">Уже зарегистрированны?\n            <router-link :to=\"{name: 'login'}\">Войдите</router-link>\n            <br>\n            <router-link :to=\"{name: 'forgot'}\">Восстановить пароль</router-link>\n        </p>\n    </div>\n</div>\n\n\n\n\n\n";

/***/ }),

/***/ 141:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _template = _interopRequireDefault(__webpack_require__(142));

var _logged_disallow = _interopRequireDefault(__webpack_require__(51));

var _form = _interopRequireDefault(__webpack_require__(27));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = {
  mixins: [_logged_disallow.default, _form.default],
  name: 'password_reset',
  template: _template.default,
  props: ['token'],
  data: function data() {
    return {
      password: '',
      re_password: ''
    };
  },
  methods: {
    default_error: function default_error() {
      return 'Не удалось сменить пароль. Ссылка на смену пароля просрочена или некоректна';
    },
    get_requires_fields: function get_requires_fields() {
      return ['password', 're_password'];
    },
    save: function save() {
      var _this = this;

      try {
        this.form_validate([this.requires_fields, this.password_vaidate, this.password_strength_validate]);
        this.post('/api/user/reset', {
          password: this.password,
          'token': this.token
        }, function () {
          _this.set_form_success("Доступы к аккаунту обновлены. Теперь вы можете войти используя новый пароль");
        });
      } catch (err) {
        this.set_form_error(err.message);
      }
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 142:
/***/ (function(module, exports) {

module.exports = "<div class=\"row\">\n\n    <div class=\"l-col\" method=\"post\">\n\n        <div class=\"form-group\">\n            <input type=\"password\" class=\"form-control\" :class=\"{'is-invalid': error_fields.password }\"\n                   placeholder=\"Пароль\" name=\"password\" v-model=\"password\" @keyup.13=\"save\">\n            <span class=\"invalid-feedback\" v-if=\"error_fields.password\">{{ error_fields.password }}</span>\n        </div>\n\n\n        <div class=\"form-group\">\n            <input type=\"password\" class=\"form-control\" :class=\"{'is-invalid': error_fields.re_password }\"\n                   placeholder=\"Повторите пароль\" name=\"re_password\" v-model=\"re_password\" @keyup.13=\"save\">\n            <span class=\"invalid-feedback\" v-if=\"error_fields.re_password\">{{ error_fields.re_password }}</span>\n        </div>\n\n        <button type=\"submit\" @click=\"save\" class=\"btn btn-outline-primary col-12\" :disabled=success>\n            <span v-if=\"loading\">Загрузка...</span>\n            <span v-else-if=\"success\">Пароль изменен</span>\n            <span v-else>Сменить пароль</span>\n        </button>\n\n    </div>\n\n    <div class=\"r-col\">\n        <h4>Пожалуйста введите новый пароль.</h4>\n        <div class=\"msg\" v-if=\"success\"><!-- .l-col .msg -->\n            <p class=\"suc\">{{ success_txt }}</p>\n        </div>\n        <div class=\"msg\" v-if=\"error\"><!-- .l-col .msg -->\n            <p class=\"err\">{{ error_txt }}</p>\n        </div>\n\n    </div>\n\n     <p class=\"reg\">\n        <router-link :to=\"{name: 'login'}\">Вход</router-link>\n        или\n        <router-link :to=\"{name: 'registration'}\">Регистрация юриста</router-link>\n    </p>\n\n</div>\n\n\n";

/***/ }),

/***/ 143:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _template = _interopRequireDefault(__webpack_require__(144));

var _form = _interopRequireDefault(__webpack_require__(27));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = {
  name: 'auth_wrapper',
  template: _template.default,
  mixins: [_form.default]
};
exports.default = _default;

/***/ }),

/***/ 144:
/***/ (function(module, exports) {

module.exports = "<section class=\"auth-section align-items-center\" style=\"min-height: 100vh;\">\n    <div class=\"win-round\">\n        <div class=\"close\" onclick=\"document.location.href='/';\"><span aria-hidden=\"true\">&times;</span></div>\n        <h2 class=\"logo\">\n            <router-view name=\"title\"></router-view>\n        </h2>\n        <router-view></router-view>\n    </div>\n</section>\n\n\n\n\n\n";

/***/ }),

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

/***/ 51:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var _default = {
  beforeCreate: function beforeCreate() {
    this.$http.get('/api/user/check').then(function (r) {
      if (r.data.success === true) {
        window.location.href = '/';
      }
    });
  }
};
exports.default = _default;

/***/ }),

/***/ 94:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _vk = _interopRequireDefault(__webpack_require__(137));

var _fb = _interopRequireDefault(__webpack_require__(138));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = {
  computed: {
    vk_url: function vk_url() {
      var buildUrl = __webpack_require__(95);

      return buildUrl(_vk.default.VK_AUTHORIZE_URL, {
        queryParams: {
          client_id: _vk.default.VK_CLIENT_ID,
          display: _vk.default.VK_DISPLAY,
          redirect_uri: _vk.default.VK_REDIRECT_URL,
          scope: _vk.default.VK_SCOPE,
          response_type: _vk.default.VK_RESPONCE_TYPE,
          v: _vk.default.VK_API_VERSION
        }
      });
    },
    fb_url: function fb_url() {
      var buildUrl = __webpack_require__(95);

      return buildUrl(_fb.default.FB_AUTHORIZE_URL, {
        queryParams: {
          client_id: _fb.default.FB_CLIENT_ID,
          redirect_uri: _fb.default.FB_REDIRECT_URL,
          scope: _fb.default.FB_SCOPE
        }
      });
    }
  },
  methods: {
    vk: function vk() {
      window.location.href = this.vk_url;
    },
    fb: function fb() {
      window.location.href = this.fb_url;
    }
  }
};
exports.default = _default;

/***/ }),

/***/ 95:
/***/ (function(module, exports, __webpack_require__) {

/**
 * build-url - A small library that builds a URL given its components
 * @version v1.1.1
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
    } else if (typeof(url) === 'object') {
      builtUrl = '';
      options = url;
    } else {
      builtUrl = url;
    }

    if(builtUrl && builtUrl[builtUrl.length - 1] === '/'){
      builtUrl = builtUrl.slice(0, -1);
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
          if (options.queryParams.hasOwnProperty(key)
              && options.queryParams[key] !== void 0) {
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
    if (typeof(module) !== 'undefined' && module.exports) {
      exports = module.exports = buildUrl;
    }
    exports.buildUrl = buildUrl;
  } else {
    root.buildUrl = buildUrl;
  }
}).call(this);


/***/ })

/******/ });