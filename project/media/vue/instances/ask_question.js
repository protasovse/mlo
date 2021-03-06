import 'babel-polyfill';
import routes from '../routes/ask_question/index.js';
import form_store from '../stores/form_store/index.js'
import MaskedInput from 'vue-masked-input';


let vueSmoothScroll = require('vue-smoothscroll');
Vue.use(vueSmoothScroll);
Vue.component('v-select', VueSelect.VueSelect);
Vue.component('file-upload', VueUploadComponent);
Vue.component('masked-input', MaskedInput);

let app = new Vue({
    name: 'instance_question',
    'el': '#app',
    store: new Vuex.Store(form_store),
    router: new VueRouter({mode: 'history', routes}),

});

