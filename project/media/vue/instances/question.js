import routes from '../routes/question/index.js';
import form_store from '../stores/form_store/index.js'

let app = new Vue({
    name: 'instance_auth',
    'el': '#app',
    store: new Vuex.Store(form_store),
    router: new VueRouter({mode: 'history', routes}),
});