import template from './template.html';
import form_mixin from '../../../mixins/form';

export default {
    mixins: [form_mixin],
    name: 'ask_question',
    data() {
        return {
            advice_cost: 0,
            completed: [],
            question_id: '',
            question_url: '',
            rubric: 'не выбрано',
            options: [],
            options_city: [],
            main_city:[],
            city:'',
            base_options: [],
            files: [],
            is_authorized: false,
            is_paid_question: false,
            title: '',
            content: '',
            email: '',
            name: '',
            phone:'',
            require_confirm: false,
            default_city: [
                {'id':0, 'name': '-- Город не выбран --'},
                {'id':-1, 'name': "-- Введите название города --"}
            ]

        }
    },

    computed: {
        is_form_send_done() {
            return this.success && (!this.loading) && (!(this.$refs.upload && this.$refs.upload.active))
        },
        post_action() {return '/api/question'},
        is_require_email() {return !this.completed.includes('email')},
        is_require_name() {return !this.completed.includes('name')},
        is_require_phone() {return !this.completed.includes('phone')},
        is_require_city() {return !this.completed.includes('city')},
        is_require_form() {
            return this.is_require_email
                || this.is_require_name
                || this.is_require_phone
                || this.is_require_city
        }
    },
    watch: {
        is_form_send_done: function() {
            if (this.is_form_send_done) {
                  window.location.href = this.question_url;
            }
        }
    },
    mounted() {
        this.$http.get('/api/question/default').then(
            (r) => {
                if (r.data.data['ask_content']) {
                    this.content = r.data.data['ask_content'];
                }
                if (r.data.data['ask_name']) {
                    this.name = r.data.data['ask_name'];
                }
                if (r.data.data['ask_phone']) {
                    this.phone = r.data.data['ask_phone'];
                }
            },
        );
        this.$http.get('/api/default').then(
            (r) => {
                this.question_url = r.data.data['urls']['show_question'];
                this.advice_cost = r.data.data['settings']['advice_cost'];
            },
        );
        this.$http.get('/api/rubric', {params: {'level':0}},).then(
            (r) => {
                this.base_options = r.data.data;
                this.optionsInit()
            },
        );
        this.$http.get('/api/city/ip').then(
            (r) => {
                if (r.data.success) {
                    this.city = r.data.data;
                } else {
                    this.city = this.default_city[0]
                }
            },
        );
        this.$http.get('/api/city/default').then(r=>{
            this.main_city = r.data.data;
            this.options_city = this.default_city.concat(this.main_city);
            this.options_city.tags = true
        });
        this.$http.get('/api/user/check').then(r=>{
            this.is_authorized = r.data.success;
            if (this.is_authorized) {
                this.name = r.data.data.first_name;
                if (this.name) {
                    this.completed.push('name');
                }
                this.phone = r.data.data.phone;
                if (this.phone) {
                    this.completed.push('phone');
                }
                this.email = r.data.data.email;
                if (this.email) {
                    this.completed.push('email');
                }
                this.city = {'id':r.data.data.city['id'], 'name':r.data.data.city['name']};
                if (this.city) {
                    this.completed.push('city');
                }
            }
        });

    },

    methods: {
        cityInptut(payload) {
            if (payload && payload.id === -1) {
                this.city = ''
            }
            this.options_city = this.default_city.concat(this.main_city);
        },
        getCity(search, loading) {
            this.$http.get('/api/city/search', {params: {'keyword':search}}).then(
                (r) => {
                    this.options_city = r.data.data;
                },
            );
        },
        onSearch(search, loading) {
            this.$http.get('/api/rubric', {params: {'keyword':search}}).then(
                (r) => {
                    this.options = r.data.data;
                },
            );
        },
        onInputRubric()
        {
            if (!this.rubric) {
                this.rubric = 'не выбрано'
            }
        },
        optionsInit() {
            this.options = this.base_options;

            //if (this.rubric.length > 1 &&  this.rubric[0] === 'не выбрано') {
            //    this.rubric.shift()
            //}

        },
        get_requires_fields() {
            let fields = ['title', 'content'];
            if (this.is_require_email) {
                fields.push('email')
            }
            if (this.is_require_phone) {
                fields.push('phone')
            }
            if (this.is_require_name) {
                fields.push('name')
            }
            return fields
        },
        save_paid() {
            this.is_paid_question = true;
            this.save()
        },
        save_free() {
            this.is_paid_question = false;
            this.save()
        },
        save() {
            try {
                this.form_validate([this.requires_fields]);

                let data = {
                    rubric: this.rubric,
                    title: this.title,
                    content: this.content,
                    is_paid_question: +this.is_paid_question,
                    email: this.email,
                    name: this.name,
                    phone: this.phone,
                    city: this.city,
                };
                this.put('/api/question', data, (r) => {
                    this.question_id = r.data.id;
                    this.question_url = this.question_url.replace('/0/', '/'+this.question_id+'/');
                    this.require_confirm = (r.data.status === 'blocked');
                    for (let i = 0; i < this.$refs.upload.files.length; i++) {
                        this.$refs.upload.files[i].data = {id:this.question_id}
                    }
                    this.$refs.upload.active = true;
                    this.set_form_success();
                });

            } catch (err) {
                this.set_form_error(err.message);
                this.$SmoothScroll(0, 500);
            }
        },
    },
    template: template,
}
