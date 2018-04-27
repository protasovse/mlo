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
            answers_like: [],
            is_authorized: false,
            user_id: false,
            role: false,
            question: [],
            count_answ: {},
            sub_answers_exists: false
        }
    },
    mounted() {
        this.$http.get('/api/default').then(
            (r) => {
                this.full_tree = r.data.data['settings']['answers_expand'];
            },
        );
        this.$http.get('/api/user/check').then(r=> {
            this.is_authorized = r.data.success;
            if (this.is_authorized) {
                this.role = r.data.data.role;
                this.user_id = r.data.data.id
            }
        });
        this.$http.get('/api/question',{params: {'id': this.qid}}).then(
            (r) => {this.question = r.data.data},
        );
        this.$http.get('/api/question/answers',{params: {'id': this.qid}}).then(
            (r) => {
                this.answers = r.data.data;
                // to count subanswers
                this.answers.forEach(x => {
                    if (x.parent_id) {
                        this.sub_answers_exists = true;
                        this.count_answ[x.parent_id] = (this.count_answ[x.parent_id] || 0) + 1;
                    }
                });
            },
        );

    },
    computed: {
        tree_link_name() {
           return this.full_tree ? 'Свернуть': 'Развернуть'
        },
    },
    methods: {
        like_title(id) {
            let answer = this.answers.filter(i=>i.id === id)[0];
            if (answer.author.id === this.user_id) {
                return 'Мой ответ'
            }
            return this.role === 'lawyer' ? 'Согласен с ответом' : 'Ответ полезен?'
        },
        expand_all()
        {
            this.full_tree = !this.full_tree;
            this.answers = this.answers.map(x => {
                if (!x.parent_id) {
                    x.is_expand = this.full_tree
                }
                return x
            })
        },
        expand_answer(id) {
            let answer = this.answers.filter(i=>i.id === id)[0];
            answer.is_expand = !answer.is_expand
        },
        is_possible_expand_answer(id) {
            let answer = this.answers.filter(i=>i.id === id)[0];
            return !answer.parent_id && this.count_answ[answer.id]
        },
        get_exand_answer_name(id) {
            let answer = this.answers.filter(i=>i.id === id)[0];
            let cnt = this.count_answ[answer.id] || 0;
            return answer.is_expand ? `Свернуть (${cnt})`: `Развернуть (${cnt})`
        },
        get_add_question_link(id) {
            if (!this.is_authorized) {
                return false
            }
            let answer = this.answers.filter(i=>i.id === id)[0];
            if (this.role === 'client') {
                if (this.question.author.id === this.user_id && answer.author.role === 'lawyer' && (!answer.parent_id || answer.is_last_answer))
                {
                    return 'Задать дополнительный вопрос'
                }
            } else if (this.role === 'lawyer') {
                if (answer.parent_id && answer.is_last_answer && answer.author.role === 'client') {
                    let parent_answer = this.answers.filter(i=>i.id === answer.parent_id)[0];
                    if (parent_answer.author.id === this.user_id) {
                        return 'Ответить'
                    }
                }
            }
            return false
        },
        is_show_comment(id) {
            let answer = this.answers.filter(i=>i.id === id)[0];
            if (!answer.parent_id) {
                return true
            }
            return this.answers.filter(i=>i.id === answer.parent_id)[0].is_expand
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
