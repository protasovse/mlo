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
        }
    },
    beforeMount() {
         this.$store.commit('init_state')
    },
    methods: {
        start_loading() {
            this.$store.commit('start_loading')
        },
        stop_loading() {
            this.$store.commit('stop_loading')
        },
        password_vaidate() {
            if (this.password !== this.re_password) {
                throw new Error('Пароли не совпадают')
            }
        },
        requires_fields() {
            if (this.get_requires_fields === undefined) {
                return;
            }
            if (!this.get_requires_fields().every(function (x) {return x !== ''})) {
                throw new Error('Введите данные');
            }
        },
        form_validate(fns) {
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
        process_error(r, fn=undefined) {
            this.stop_loading();
            if (fn === undefined) {
                if (r.data.error !== undefined) {
                    throw new Error(r.data.error)
                } else {
                    throw new Error(this.default_error())
                }
            } else {
                console.log(r);
                fn(r)
            }
        },
        get(url, params, fn, fn_error=undefined) {
            this.start_loading();
            this.$http.get(url, {params: params}, {emulateJSON:true}).then(
                 (r) => {this.process_success(r, fn)},
                 (r) => {this.process_error(r, fn_error)}
             ).catch(e => this.set_form_error(e.message))
        },
        post(url, params, fn, fn_error=undefined) {
            this.start_loading();
            this.$http.post(url, params, {emulateJSON:true}).then(
                r => this.process_success(r, fn),
                r => this.process_error(r, fn_error)
            ).catch(e => this.set_form_error(e.message))
        }

    }
}
