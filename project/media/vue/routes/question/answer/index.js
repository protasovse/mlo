import template from './form_reply.html';
import form_mixin from '../../../mixins/form';


export default {
    mixins: [form_mixin],
    name: 'answer',
    data() {
        return {
            tre: 0
        }
    },


    template: template,
}

Vue.component('answer', {
  props: ['todo'],
  template: template
});