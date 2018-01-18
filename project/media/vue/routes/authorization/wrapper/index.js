import template from './template.html';
import './style.less';
//import './../../../../styles/fonts.less';
//import './../../../../styles/app.less';
//import './../../../../styles/form.less';
import form_mixin from '../../../mixins/form';

export default {
    name: 'auth_wrapper',
    template,
    mixins: [form_mixin],
}
