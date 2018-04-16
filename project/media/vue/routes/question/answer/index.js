import template from './form_reply.html';
import form_mixin from '../../../mixins/form';

export default {
    mixins: [form_mixin],
    name: 'answer',
    data() {
        return {}
    },
    methods: {
        save() {
            console.log(this)
        }
    },
    template: template,
}

Vue.component('reply-form', {
    data() {
        return {
            content: '',
        }
    },
    props: ['question', 'parent'],
    methods: {
        save(event) {
            console.log(this.content);
            if (event) event.preventDefault();
            try {
                // this.form_validate([this.requires_fields]);
            } catch (err) {
                this.set_form_error(err.message);
            }
            return false;
        }
    },
    template: template
});