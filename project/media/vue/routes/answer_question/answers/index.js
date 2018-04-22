import template from './template.html';
import form_mixin from '../../../mixins/form';

export default {
    mixins: [form_mixin],
    template: template,
    props: ['qid'],
    name: 'answer_question',
    data() {
        return {
            content: '',
            answers: [],
        }
    },
    computed: {

    },
    watch: {
    },
    mounted() {
         this.$http.get('/api/question/answers',{params: {'id': this.qid}}).then(
            (r) => {this.answers = r.data.data},
        );
    },
    methods: {
        save() {
            console.log(this.qid);
        }
    },

}
