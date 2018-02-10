import template from './template.html';
import logged_disallow_mixin from '../../../mixins/logged_disallow';
import form_mixin from '../../../mixins/form';

export default {
    mixins: [logged_disallow_mixin, form_mixin],
    name: 'auth_forgot',
    template,
     data() {
        return {
            email: this.get_saved_field('email'),
        }
    },
    methods: {
        default_error() {return 'Ошибка восстановления доступа'},
        get_requires_fields() {return ['email']},
        save() {
            try {
                this.form_validate([this.requires_fields]);
                this.post('/api/user/forgot', {email: this.email}, () => {
                    this.set_form_success("Ссылка для восстановления пароля была отправлена на почту")
                });
            } catch (err) {
                this.set_form_error(err.message)
            }
        }
    }
}
