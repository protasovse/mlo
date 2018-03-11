import template from './template.html';
import form_mixin from '../../../mixins/form';


export default {
    mixins: [form_mixin],
    name: 'ask_question',
    data() {
        return {
            rubric: [],
            options: [],
            base_options: [],
            files: [],
            is_authorized: false,
            is_paid_question: false,
            title: '',
            content: '',
            r_fields: ['title', 'content'],
            email: '',
            name: '',
            phone:'',
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
            console.log(this.is_authorized);
            if (!this.is_authorized) {
                this.r_fields.push('email', 'phone', 'name');
            }
        });
    },

    methods: {
        onSearch(search, loading) {
            this.$http.get('/api/rubric', {params: {'keyword':search}}).then(
                (r) => {
                    this.options = r.data.data;
                },
            );
        },
        optionsInit() {this.options = this.base_options;},
        get_requires_fields() {return this.r_fields},
        save() {
            try {
                this.form_validate([this.requires_fields]);
                let data = {
                    rubric: this.rubric.map(function (x) {return x['id']}),
                    title: this.title,
                    content: this.content,
                    is_paid_question: +this.is_paid_question,
                };
                if (!this.is_authorized) {
                    data = Object.assign(data,  {
                        email: this.email,
                        name: this.name,
                        phone: this.phone
                    });
                }
                this.put('/api/question', data, (r) => {
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
        inputFilter(newFile, oldFile, prevent) {
          if (newFile && !oldFile) {
            if (/(\/|^)(Thumbs\.db|desktop\.ini|\..+)$/.test(newFile.name)) {
              return prevent()
            }
            if (/\.(php5?|html?|jsx?)$/i.test(newFile.name)) {
              return prevent()
            }
          }
        },
        inputFile(newFile, oldFile) {
          if (newFile && !oldFile) {
            console.log('add', newFile)
          }
          if (newFile && oldFile) {
            console.log('update', newFile)
          }
          if (!newFile && oldFile) {
            console.log('remove', oldFile)
          }
        },
    },
    template: template,
}
