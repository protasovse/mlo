import routes from '../routes/ask_question/index.js';
import form_store from '../stores/form_store/index.js'

Vue.component('v-select', VueSelect.VueSelect);

var app = new Vue({
    name: 'instance_question',
    'el': '#app',
    store: new Vuex.Store(form_store),
    router: new VueRouter({mode: 'history', routes}),
})

