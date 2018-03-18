import template from './template.html';
import form_mixin from '../../../mixins/form';


export default {
    mixins: [form_mixin],
    name: 'ask_question',
    data() {
        return {
            rubric: [],
            options: [],
            options_city: [],
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
        post_action() {return '/api/question'},
    },
    mounted() {
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
                this.phone = r.data.data.phone;
                this.email = r.data.data.email;
                this.city = {'id':r.data.data.city['id'], 'name':r.data.data.city['name']};
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
        get_requires_fields() {return ['title', 'content', 'email', 'phone', 'name']},
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
                    this.require_confirm = (r.data.status === 'blocked');
                    for (let i = 0; i < this.$refs.upload.files.length; i++) {
                        this.$refs.upload.files[i].data = {id:r.data.id};
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
