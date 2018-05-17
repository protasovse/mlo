export default
{
    computed: {
         file_form_loading: function () {
            return this.loading || (this.$refs.upload && this.$refs.upload.active)
        },
    },
}
