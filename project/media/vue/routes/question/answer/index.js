import template from './form_reply.html';
import form_mixin from '../../../mixins/form';


export default {
    mixins: [form_mixin],
    name: 'answer',
    data() {
        return {}
    },


    template: template,
}

Vue.component('reply-form', {
    props: ['question', 'parent'],
    template: template
});