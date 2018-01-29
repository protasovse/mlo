import template from './template.html';
import logged_disallow from '../../../mixins/logged_disallow';
import form_mixin from '../../../mixins/form';
import social_mixin from '../../../mixins/social';


export default {
    mixins: [logged_disallow, form_mixin, social_mixin],
    name: 'auth_reg',
    template,
    data() {
        return {
            email: '',
            password: '',
            first_name: '',
            second_name: '',
            patronymic: ''
        }
    },
    methods: {
        default_error() {return 'Не удалось зарегистрироваться'},
        get_requires_fields() {return ['email', 'password', 'first_name', 'last_name', 'patronymic']},
        save() {
            try {
                this.form_validate([this.requires_fields]);
                this.post('/api/user', {
                    email: this.email,
                    password: this.password,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    patronymic: this.patronymic,
                }, () => {
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
