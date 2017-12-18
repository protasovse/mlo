import template from './template.html';
import logged_disallow_mixin from '../../../mixins/logged_disallow';
import form_mixin from '../../../mixins/form';

export default {
    mixins: [logged_disallow_mixin, form_mixin],
    name: 'auth_activate',
    props: ['token'],
    template,
    mounted() {
        try {
            this.post('/api/user/activate', {'token': this.token}, () => {
                this.set_form_success(
                    "Аккаунт успешно активирован. Вы можете войти на сайт, используя данные, указанные при регистрации"
                )
            });
        } catch (err) {
            this.set_form_error(err.message)
        }
    },
    methods: {
        default_error() {return 'Ошибка восстановления доступа'},
    }
}
