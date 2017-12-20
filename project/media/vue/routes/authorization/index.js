import forgot from './forgot/index.js'
import login from './login/index.js'
import registration from './registration/index.js'
import password_reset from './password_reset/index.js'
import activate_email from './activate_email/index.js'
import wrapper from './wrapper/index.js'


export default [
    {
        path: '/auth/',
        component: wrapper,
        name: 'auth',
        children: [
            {
                path:'login',
                components: {
                    default: login,
                    title: { template: '<div class="logo">Авторизация</div>' }
                },
                name: 'login',
            },
            {
                path:'registration',
                components: {
                    default: registration,
                    title: { template: '<div class="logo">Регистрация</div>' }
                },
                name: 'registration'
            },
            {
                path:'forgot',
                components: {
                    default: forgot,
                    title: { template: '<div class="logo">Восстановление пароля</div>' }
                },
                name: 'forgot'
            },
            {
                path:'reset/:token',
                name: 'reset',
                components: {
                    default: password_reset,
                    title: { template: '<div class="logo">Изменение пароля</div>' }

                },
                props: {default:true},
            },
            {
                path:'activate/:token',
                name: 'activate',
                components: {
                    default: activate_email,
                    title: { template: '<div class="logo">Активация учетной записи</div>' }

                },
                props: {default:true},
            },
            {
                path: '*',
                redirect: 'login'
            }
        ]
    }
]