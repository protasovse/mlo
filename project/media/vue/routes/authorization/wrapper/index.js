import template from './template.html';
import form_mixin from '../../../mixins/form';

export default {
    name: 'auth_wrapper',
    template,
    mixins: [form_mixin],
}
