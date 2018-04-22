import template from './template.html';
import logged_disallow from '../../../mixins/logged_disallow';
import form_mixin from '../../../mixins/form';
import social_mixin from '../../../mixins/social';


export default {
    mixins: [logged_disallow, form_mixin, social_mixin],
    name: 'auth_login',
    template,
    props: ['token'],
    data() {
        return {
            email: this.get_saved_field('email'),
            password: '',
            unactive: false,
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
                this.post('/api/user/activate', {'token': this.token},
                    () => {
                        this.set_form_success(
                            "Аккаунт успешно активирован. Вы можете войти на сайт, используя данные, указанные при регистрации"
                        )
                    },
                    (r) => {
                        this.unactive = (r.data.code === 'unactive');
                        this.process_error(r);
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
                    (r) => {window.location.href = '/вопросы'},
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
            this.get('/api/user/resend', {email: this.email, token: this.token},
                () => {this.set_form_success('Письмо отправлено повторно. Проверьте, пожалуйста, почту.')},
                () => {this.set_form_error('Нe удалось отрпавить активационное письмо')},
            );
        }
    }
}
