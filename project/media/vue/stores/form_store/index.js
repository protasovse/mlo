export default {
    namespaced: true,
    state: {
        is_error: false,
        is_success: false,
        error_txt: '',
        success_txt: '',
        loading: false
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
        }
    }
}
