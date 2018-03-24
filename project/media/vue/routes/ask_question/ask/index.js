import template from './template.html';
import form_mixin from '../../../mixins/form';


export default {
    mixins: [form_mixin],
    name: 'ask_question',
    data() {
        return {
            completed: [],
            question_id: '',
            question_url: '',
            rubric: [],
            options: [],
            options_city: [],
            city:'',
            base_options: [],
            files: [],
            is_authorized: false,
            is_paid_question: true,
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
        post_action() {return '/api/question'},
        is_completed_email() {return this.completed.includes('email')},
        is_completed_name() {return this.completed.includes('name')},
        is_completed_phone() {return this.completed.includes('phone')},
        is_completed_city() {return this.completed.includes('city')},
        is_completed() {
            return this.is_completed_email
                && this.is_completed_name
                && this.is_completed_phone
                && this.is_completed_city
        }
    },
    mounted() {
        this.$http.get('/api/default').then(
            (r) => {
                this.question_url = r.data.data['urls']['show_question'];
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
            this.options_city = this.default_city.concat(r.data.data);
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
        optionsInit() {this.options = this.base_options;},
        get_requires_fields() {
            let fields = ['title', 'content'];
            if (!this.is_completed_email) {
                fields.push('email')
            }
            if (!this.is_completed_phone) {
                fields.push('phone')
            }
            if (!this.is_completed_name) {
                fields.push('name')
            }
            return fields
        },
        save() {
            try {
                this.form_validate([this.requires_fields]);
                let data = {
                    rubric: this.rubric.map(function (x) {return x['id']}),
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
                    this.question_url = this.question_url.replace('0', this.question_id);
                    this.require_confirm = (r.data.status === 'blocked');
                    for (let i = 0; i < this.$refs.upload.files.length; i++) {
                        this.$refs.upload.files[i].data = {id:this.question_id}
                    }
                    if (!this.require_confirm) {
                        window.location.href = this.question_url
                    }
                    this.$refs.upload.active = true;
                    this.set_form_success();
                });

            } catch (err) {
                this.set_form_error(err.message)
            }
        },
    },
    template: template,
}
