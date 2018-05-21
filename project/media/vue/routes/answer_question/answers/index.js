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
            sub_answers_exists: false,
            is_can_answer: false,
            files: [],
            parent_id: 0,
            thread: 0,
            upload_form: '',
            load_answers: false,
        }
    },

    beforeMount() {
        this.load_answers = true;
        this.$http.get('/api/default').then(
            (r) => {
                this.full_tree = r.data.data['settings']['answers_expand'];
            },
        );
        this.$http.get('/api/user/check').then(r=> {
            this.is_authorized = r.data.success;
            if (this.is_authorized) {
                this.role = r.data.data.role;
                this.user_id = r.data.data.id;

                if (this.role === 'lawyer') {
                    this.is_can_answer = true
                }
            }

        });
        this.$http.get(`/api/questions/${this.qid}`).then(
            (r) => {
                this.question = r.data.data;
                this.request_and_load_answers()
            },
        );


    },
    computed: {
        tree_link_name() {
           return this.full_tree ? 'Свернуть': 'Развернуть'
        },
        post_action() {
            return `/api/questions/${this.qid}/answers`
        },
        is_form_send_done_first() {
            return this.upload_form === 'upload_first' && this.is_form_send_done('upload_first')
        },
        is_form_send_done_second() {
            return this.upload_form === 'upload_second' && this.is_form_send_done('upload_second')
        },
        file_first_form_loading: function () {
            return this.loading || (this.get_upload('upload_first') && this.get_upload('upload_first').active)
        },
        file_second_form_loading: function () {
            return this.loading || (this.get_upload('upload_second') && this.get_upload('upload_second').active)
        },
        answers_total() {
            return this.answers.length;
        }
    },
    watch: {
        is_form_send_done_first: function() {
            if (this.is_form_send_done_first) {
                this.is_can_answer = false;
                this.request_and_load_answers(this.answer_id);
            }
        },
        is_form_send_done_second: function() {
            if (this.is_form_send_done_second) {
                this.is_can_answer = false;
                this.request_and_load_answers(this.answer_id);
            }
        }
    },
    methods: {
        my_dislike(answer_data) {
           return answer_data.my_like === -1;
        },
        my_like(answer_data) {
           return answer_data.my_like === 1;
        },
        is_form_send_done(upload_name) {
            return this.success && (!this.loading) && (!(this.get_upload(upload_name) && this.get_upload(upload_name).active))
        },
        get_upload(name) {
            let ref = this.$refs[name];
            // охуительный костыль. всем костылям костыль
            if (name === 'upload_second') {
                if (ref) {
                    ref = ref[0];
                }
            }
            return ref;
        },
        request_and_load_answers(scroll_to_id=false) {
            this.$http.get(`/api/questions/${this.qid}/answers`).then(
                (r) => {
                    this.count_answ = {};
                    this.answers = r.data.data;
                    // to count subanswers
                    this.answers.forEach(x => {
                        if (x.parent_id) {
                            this.sub_answers_exists = true;
                            this.count_answ[x.parent_id] = (this.count_answ[x.parent_id] || 0) + 1;
                        }
                        if (this.is_can_answer && x.author.id === this.user_id) {
                            this.is_can_answer = false
                        }
                    });
                    this.load_answers = false;
                    if (scroll_to_id) {
                        Vue.nextTick(() => {
                            this.scrollTo(scroll_to_id);
                        });
                    }
                },
            );
        },
        get_requires_fields() {
            return ['content']
        },
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
        sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
        save(upload_name) {
            this.upload_form = upload_name;
            this.form_validate([this.requires_fields]);

            let data = {
                'parent_id': this.thread,
                'content': this.content
            };
            this.answer_id = false;
            this.put(`/api/questions/${this.qid}/answers`, data, (r) => {
                    this.answer_id = r.data.id;

                    for (let i = 0; i < this.get_upload(upload_name).files.length; i++) {
                        this.get_upload(upload_name).files[i].data = {id:this.answer_id};
                    }

                    this.get_upload(upload_name).active = true;

                    if (this.is_form_send_done(upload_name)) {
                        console.log('123');
                        this.request_and_load_answers(this.answer_id);
                    }
                    this.set_form_success();

            });
        },
        to_like_val(id, val) {
            let a = this.answers.filter(i=>i.id === id)[0];
            a['like_count'] += val;
            a['is_can_like'] = false;
            a['my_like'] = val;
        },
        to_like(id) {
            this.to_like_val(id, 1);
            this.$http.post(`/api/questions/${this.qid}/answers/${id}/like`)
        },
        to_dislike(id) {
            this.to_like_val(id, -1);
            this.$http.post(`/api/questions/${this.qid}/answers/${id}/dislike`)
        },
        show_form_answer(id)
        {

            if (this.is_show_form_answer(id)) {
                return;
            }
            let a = this.answers.filter(i=>i.id === id)[0];
            this.thread = a.thread;
            this.content = '';
            this.parent_id = a.parent_id;
            this.files = [];
            this.$store.commit('init_state');
            this.answers.forEach(x => Vue.set(x, 'show_form', x.id === id));
        },
        hide_form_answer(id)
        {
            let a = this.answers.filter(i=>i.id === id)[0];
            a.show_form = false;
        },
        is_show_form_answer(id)
        {
            let a = this.answers.filter(i=>i.id === id)[0];
            return a['show_form'] === true;
        },


    },

}
