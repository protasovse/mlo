import template from './template.html';
import logged_disallow from '../../../mixins/logged_disallow';
import form_mixin from '../../../mixins/form';
import VK_CONFIG from '../../../config/vk';
import FB_CONFIG from '../../../config/fb';



export default {
    mixins: [logged_disallow, form_mixin],
    name: 'auth_login',
    template,
    props: ['token'],
    data() {
        return {
            email: '',
            password: '',
            unactive: false,
        }
    },
    computed: {
        vk_url: function () {
            var buildUrl = require('build-url');
            return buildUrl(VK_CONFIG.VK_AUTHORIZE_URL, {
                queryParams: {
                    client_id: VK_CONFIG.VK_CLIENT_ID,
                    display: VK_CONFIG.VK_DISPLAY,
                    redirect_uri: VK_CONFIG.VK_REDIRECT_URL,
                    scope: VK_CONFIG.VK_SCOPE,
                    response_type: VK_CONFIG.VK_RESPONCE_TYPE,
                    v: VK_CONFIG.VK_API_VERSION
                }
            });
        },
        fb_url: function () {
            var buildUrl = require('build-url');
            return buildUrl(FB_CONFIG.FB_AUTHORIZE_URL, {
                queryParams: {
                    client_id: FB_CONFIG.FB_CLIENT_ID,
                    redirect_uri: FB_CONFIG.FB_REDIRECT_URL,
                    scope: FB_CONFIG.FB_SCOPE,
                }
            });
        }
    },
    mounted() {

        this.$http.get('/api/user/flash').then(
            (r) => {if (r.data.success) {this.set_form_success(r.data.data)}},
            (r) => {
                this.mark_error_fields(r);
                this.set_form_error(r.data.error)
            }
        );
        if (this.token) {
            try {
                this.post('/api/user/activate', {'token': this.token}, () => {
                    this.set_form_success(
                        "Аккаунт успешно активирован. Вы можете войти на сайт, используя данные, указанные при регистрации"
                    )
                });
            } catch (err) {
                this.set_form_error(err.message)
            }
        }

    },
    methods: {
        default_error() {return 'Не удалось авторизироваться. Не верный пароль' },
        get_requires_fields() {return ['email', 'password']},
        save() {
            try {
                this.form_validate([this.requires_fields]);
                this.get('/api/user', {email: this.email, password: this.password},
                    (r) => {window.location.href = '/'},
                    (r) => {
                        this.unactive = (r.data.code === 'unactive');
                        this.process_error(r);
                    }
                );
            } catch (err) {
                this.set_form_error(err.message)
            }
        },
        send_activation() {
            this.get('/api/user/resend', {email: this.email},
                () => {this.set_form_success('Письмо отправлено повторно. Проверьте, пожалуйста, почту.')},
            );
        },
        vk() {
            window.location.href = this.vk_url;
        },
        fb() {
            window.location.href = this.fb_url;
        }
    }
}
