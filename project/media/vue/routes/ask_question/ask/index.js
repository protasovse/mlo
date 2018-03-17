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
            require_confirm: false
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
        this.$http.get('/api/user/check').then(r=>{
            this.is_authorized = r.data.success;
        });
    },

    methods: {
        getCity(search, loading) {
            this.$http.get('/api/city', {params: {'keyword':search}}).then(
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
        get_requires_fields() {return ['title', 'content', 'email', 'phone', 'name', 'city']},
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
