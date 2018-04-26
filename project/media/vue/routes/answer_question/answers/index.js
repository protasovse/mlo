import template from './template.html';
import form_mixin from '../../../mixins/form';

export default {
    mixins: [form_mixin],
    template: template,
    props: ['qid'],
    name: 'answer_question',
    data() {
        return {
            full_tree: true,
            content: '',
            answers: [],
            answers_like: []
        }
    },
    mounted() {
        this.$http.get('/api/question/answers',{params: {'id': this.qid}}).then(
            (r) => {this.answers = r.data.data},
        );

    },
    computed: {
       tree_link_name() {
           return this.full_tree ? 'Свернуть': 'Развернуть'
       }
    },
    methods: {
        is_show_comment(id) {
            if (this.full_tree) {
                return true;
            }
            let answer = this.answers.filter(i=>i.id === id)[0];
            return !answer.parent_id
        },
        scrollTo(refName) {
            let element = this.$refs[refName][0];
            let curtop = 0;
            let curtopscroll = 0;
            if (element.offsetParent) {
                do {
                    curtop += element.offsetTop;
                    curtopscroll += element.offsetParent ? element.offsetParent.scrollTop : 0;
                } while (element = element.offsetParent);
            }
            this.$SmoothScroll(curtop - curtopscroll - 40, 500);
        },
        save() {
            console.log(this.qid);
        },
        to_like_val(id, val) {
            let a = this.answers.filter(i=>i.id === id)[0];
            a['like_count'] += val;
            a['is_can_like'] = false;
        },
        to_like(id) {
            this.$http.post('/api/question/answers/like', {'id':id, 'value': 1}, {emulateJSON:true}).then(
                (r) => {this.to_like_val(id, 1)}
            )
        },
        to_dislike(id) {
            this.$http.post('/api/question/answers/like', {'id':id, 'value': -1}, {emulateJSON:true}).then(
                (r) => {this.to_like_val(id, -1)}
            )
        },
    },

}
