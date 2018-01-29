import VK_CONFIG from '../config/vk';
import FB_CONFIG from '../config/fb';

export default
{
    computed: {
         vk_url: function () {
            var buildUrl = require('build-url');
            return buildUrl(VK_CONFIG.VK_AUTHORIZE_URL, {
                queryParams: {
                    client_id: VK_CONFIG.VK_CLIENT_ID,
                    display: VK_CONFIG.VK_DISPLAY,
                    redirect_uri: VK_CONFIG.VK_REDIRECT_URL,
                    scope: VK_CONFIG.VK_SCOPE,
                    response_type: VK_CONFIG.VK_RESPONCE_TYPE,
                    v: VK_CONFIG.VK_API_VERSION
                }
            });
        },
        fb_url: function () {
            var buildUrl = require('build-url');
            return buildUrl(FB_CONFIG.FB_AUTHORIZE_URL, {
                queryParams: {
                    client_id: FB_CONFIG.FB_CLIENT_ID,
                    redirect_uri: FB_CONFIG.FB_REDIRECT_URL,
                    scope: FB_CONFIG.FB_SCOPE,
                }
            });
        }
    },
    methods: {
        vk() {
            window.location.href = this.vk_url;
        },
        fb() {
            window.location.href = this.fb_url;
        }
    }
}
