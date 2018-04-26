import routes from '../routes/answer_question/index.js';
import form_store from '../stores/form_store/index.js'


let vueSmoothScroll = require('vue-smoothscroll');
Vue.use(vueSmoothScroll);

let app = new Vue({
    name: 'instance_anser_question',
    'el': '#app',
    store: new Vuex.Store(form_store),
    router: new VueRouter({mode: 'history', routes}),

});

