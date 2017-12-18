export default {
    beforeCreate: function() {
        this.$http.get('/api/user/check').then(r=>{
            if (r.data.success === true) {
                window.location.href = '/';
            }
        });
    },
}
