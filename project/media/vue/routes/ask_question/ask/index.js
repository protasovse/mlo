import template from './template.html';
import form_mixin from '../../../mixins/form';

export default {
    name: 'ask_question',
    data() {
        return {
            options: ['foo', 'bar', 'baz']
        }
    },
    methods: {
        onSearch(search, loading) {
            loading(true);
            this.search(loading, search, this);
        },
        search: _.debounce((loading, search, vm) => {
      fetch(
        `https://api.github.com/search/repositories?q=${escape(search)}`
      ).then(res => {
        res.json().then(json => (vm.options = json.items));
        loading(false);
      });
    }, 350)
  }
},
    template: template,
}
