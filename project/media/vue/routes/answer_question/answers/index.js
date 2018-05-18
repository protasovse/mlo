import template from './template.html';
import form_mixin from '../../../mixins/form';
import upload_mixin from '../../../mixins/upload';

export default {
    mixins: [form_mixin, upload_mixin],
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
        }
    },
    mounted() {
        this.start_loading();
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
        this.$http.get('/api/question',{params: {'id': this.qid}}).then(
            (r) => {this.question = r.data.data},
        );
        this.request_and_load_answers()

    },
    computed: {
        tree_link_name() {
           return this.full_tree ? 'Свернуть': 'Развернуть'
        },
        post_action() {
            return '/api/question/answers'
        },
        is_form_send_done_first() {
            return this.upload_form === 'upload_first' && this.is_form_send_done('upload_first')
        },
        is_form_send_done_second() {
            return this.upload_form === 'upload_second' && this.is_form_send_done('upload_second')
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
        is_form_send_done(upload_name) {
            return this.success && (!this.loading) && (!(this.get_upload(upload_name) && this.get_upload(upload_name).active))
        },
        get_upload(name) {
            let ref = this.$refs[name];
            // охуительный костыль. всем костылям костыль
            if (name === 'upload_second') {
                ref = ref[0];
            }
            return ref;
        },
        request_and_load_answers(scroll_to_id=false) {
            this.$http.get('/api/question/answers',{params: {'id': this.qid}}).then(
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
                    this.stop_loading();
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
                'id': this.qid,
                'parent_id': this.thread,
                'content': this.content
            };
            this.answer_id = false;
            this.put('/api/question/answers', data, (r) => {
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
        is_show_form_answer(id)
        {
            let a = this.answers.filter(i=>i.id === id)[0];
            return a['show_form'] === true;
        },


    },

}
