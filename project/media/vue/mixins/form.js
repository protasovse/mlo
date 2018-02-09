export default {
    created() {

    },
    computed: {
        error() {
            return this.$store.state.is_error;
        },
        success() {
            return this.$store.state.is_success;
        },
        error_txt() {
            return this.$store.state.error_txt;
        },
        success_txt() {
            return this.$store.state.success_txt;
        },
        loading() {
            return this.$store.state.loading;
        },
        error_fields() {
            return this.$store.state.fields;
        },
    },
    beforeMount() {
         this.$store.commit('init_state')
    },
    methods: {
        set_field_error(field, txt) {
            this.$store.commit('error_field', {
                'field': field,
                'txt': txt
            });
        },
        start_loading() {
            this.$store.commit('start_loading')
        },
        clear_error_field() {
            this.$store.commit('clear_error_field')
        },
        stop_loading() {
            this.$store.commit('stop_loading')
        },
        password_vaidate() {
            if (this.password !== this.re_password) {
                this.set_field_error('re_password','Пароли не совпадают');
                throw new Error('Пароли не совпадают')
            }
        },
        password_strength_validate()
        {
            if (this.password.length < 6) {
                this.set_field_error('password', 'Пароль слишком короткий');
                throw new Error('Длина пароля не должна быть короче 6 символов')
            }
        },
        requires_fields() {
            if (this.get_requires_fields === undefined) {
                return;
            }
            let has_error = false;
            let req_fields = this.get_requires_fields();
            req_fields.forEach((field) => {
                if (this[field] === '') {
                    this.set_field_error(field, 'Поле обязательное для заполнения');
                    has_error = true;
                }
            });
            if (has_error) {
                throw new Error('Введите данные');
            }
        },

        form_validate(fns) {
            this.clear_error_field();
            fns.forEach((fn) => {fn()})
        },
        set_form_error(txt) {
            this.$store.commit('set_error', {
                txt: txt
            });
            this.stop_loading();
        },
        set_form_success(txt) {
            this.$store.commit('set_success', {
                txt: txt
            });
            this.stop_loading();
        },
        process_success(r, succes_fn) {
            this.stop_loading();
            if(r.data.success === false) {
                 if (r.data.error !== undefined) {
                    throw new Error(r.data.error)
                 } else {
                     throw new Error(this.default_error())
                 }
            } else {
                 succes_fn(r.data)
            }
        },
        default_error() {
            return 'Что-то пошло не так';
        },
        mark_error_fields(r) {
            r.data.fields.forEach((x) => {
                this.set_field_error(x['field'], x['txt']);
            });
        },
        process_error(r, fn=undefined) {
            this.stop_loading();
            this.mark_error_fields(r);
            if (fn === undefined) {
                if (r.data.error !== undefined) {
                    throw new Error(r.data.error)
                } else {
                    throw new Error(this.default_error())
                }
            } else {
                fn(r)
            }
        },

        get(url, params, fn, fn_error=undefined) {
            this.start_loading();
            this.clear_error_field();
            this.$http.get(url, {params: params}, {emulateJSON:true}).then(
                 (r) => {this.process_success(r, fn)},
                 (r) => {this.process_error(r, fn_error)}
             ).catch(e => this.set_form_error(e.message))
        },
        post(url, params, fn, fn_error=undefined) {
            this.start_loading();
            this.clear_error_field();
            this.$http.post(url, params, {emulateJSON:true}).then(
                r => this.process_success(r, fn),
                r => this.process_error(r, fn_error)
            ).catch(e => this.set_form_error(e.message))
        }

    }
}
