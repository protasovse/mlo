import template from './template.html';
import logged_disallow from '../../../mixins/logged_disallow';
import form_mixin from '../../../mixins/form';


export default {
    mixins: [logged_disallow, form_mixin],
    name: 'auth_reg',
    template,
    data() {
        return {
            email: '',
            password: '',
            re_password: '',
        }
    },
    methods: {
        default_error() {return 'Не удалось зарегистрироваться'},
        get_requires_fields() {return ['email', 'password', 're_password']},
        save() {
            try {
                this.form_validate([this.requires_fields, this.password_vaidate]);
                this.post('/api/user', {email: this.email, password: this.password}, () => {
                    this.set_form_success(
                        'Вы успешно зарегистрированы, но не активированы. ' +
                        'Вам на почту было отправлено активационное письмо.  ' +
                        'Пожауйста перейтиде по ссылке, указанной в пиьсме и активируйте свой аккаунт.'
                    );
                });
            } catch (err) {
                this.set_form_error(err.message)
            }
        }
    }
}
