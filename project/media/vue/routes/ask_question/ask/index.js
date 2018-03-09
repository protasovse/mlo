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
            id: 0,
            is_authorized: false
        }
    },
    computed: {
        post_action() {
            return '/api/question/' + this.id
        },
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
        onSearch(search, loading) {
            this.$http.get('/api/rubric', {params: {'keyword':search}}).then(
                (r) => {
                    this.options = r.data.data;
                },
            );
        },
        optionsInit()
        {
            this.options = this.base_options;
        },

        save() {
            try {
                this.put('/api/question', {rubric: this.rubric}, () => {
                    for (let i = 0; i < this.$refs.upload.files.length; i++) {
                        this.$refs.upload.files[i].data = {id:3};
                    }
                    this.$refs.upload.active = true
                });

            } catch (err) {
                this.set_form_error(err.message)
            }
        },
        inputFilter(newFile, oldFile, prevent) {
          if (newFile && !oldFile) {
            // Before adding a file
            // 添加文件前
            // Filter system files or hide files
            // 过滤系统文件 和隐藏文件
            if (/(\/|^)(Thumbs\.db|desktop\.ini|\..+)$/.test(newFile.name)) {
              return prevent()
            }
            // Filter php html js file
            // 过滤 php html js 文件
            if (/\.(php5?|html?|jsx?)$/i.test(newFile.name)) {
              return prevent()
            }
          }
        },
        inputFile(newFile, oldFile) {
          if (newFile && !oldFile) {
            // add
            console.log('add', newFile)
          }
          if (newFile && oldFile) {
            // update
            console.log('update', newFile)
          }
          if (!newFile && oldFile) {
            // remove
            console.log('remove', oldFile)
          }
        },
    },
    template: template,
}
