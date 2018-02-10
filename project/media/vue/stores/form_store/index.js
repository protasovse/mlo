export default {
    namespaced: true,
    state: {
        is_error: false,
        is_success: false,
        error_txt: '',
        success_txt: '',
        loading: false,
        fields: {},
        // сохраненные значения
        values: {}
    },
    mutations: {
        set_error(state, error) {
            state.is_error = true;
            state.is_success = false;
            state.error_txt = error.txt;
        },
        start_loading(state) {
            state.loading = true;
            state.is_error = false;
            state.is_success = false;
        },
        stop_loading(state) {
            state.loading = false;
        },
        set_success (state, success) {
            state.is_error = false;
            state.is_success = true;
            state.success_txt = success.txt;
        },
        init_state(state) {
            state.is_error = false;
            state.is_success = false;
            state.loading = false;
            state.fields = {}
        },
        error_field(state, error) {
            Vue.set(state.fields, error.field, error.txt)
        },
        save_field(state, value) {
            Vue.set(state.values, value.key, value.val)
        },
        clear_error_field(state) {
            state.fields = {}
        }
    }
}
