import template from './template.html';
import logged_disallow_mixin from '../../../mixins/logged_disallow';
import form_mixin from '../../../mixins/form';

export default {
    mixins: [logged_disallow_mixin, form_mixin],
    name: 'password_reset',
    template,
    props: ['token'],
    data() {
        return {
            password: '',
            re_password: '',
        }
    },
    methods: {
        default_error() {return 'Не удалось сменить пароль. Ссылка на смену пароля просрочена или некоректна'},
        get_requires_fields() {return ['password', 're_password']},
        save() {
            try {
                this.form_validate([this.requires_fields, this.password_vaidate]);
                this.post('/api/user/reset', {password: this.password, 'token': this.token}, () => {
                    this.set_form_success("Доступы к аккаунту обновлены. Теперь мы можете войти используя новый пароль")
                });
            } catch (err) {
                this.set_form_error(err.message)
            }
        }
    }
}
