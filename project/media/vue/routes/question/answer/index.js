import template from './form_reply.html';
import form_mixin from '../../../mixins/form';

/* export default {
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
} */

Vue.component('reply-form', {
    mixins: [form_mixin],
    data() {
        return {
            content: '',
        }
    },

    props: ['question_id', 'parent_id', 'title'],

    methods: {
        get_requires_fields() {
            let fields = ['content'];
            return fields
        },
        save(event) {
            try {
                this.form_validate([this.requires_fields]);
                let data = {
                    content: this.content,
                    question_id: this.question_id,
                    parent_id: this.parent_id,
                };
                console.log(data);
            } catch (err) {
                this.set_form_error(err.message);
            }
        }
    },
    template: template
});