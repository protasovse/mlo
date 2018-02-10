import forgot from './forgot/index.js'
import login from './login/index.js'
import registration from './registration/index.js'
import password_reset from './password_reset/index.js'
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
                    title: { template: '<span>Вход</span>' }
                },
                name: 'login',
            },
            {
                path:'registration',
                components: {
                    default: registration,
                    title: { template: '<span>Регистрация юриста</span>' }
                },
                name: 'registration'
            },
            {
                path:'forgot',
                components: {
                    default: forgot,
                    title: { template: '<span>Восстановить пароль</span>' }
                },
                name: 'forgot'
            },
            {
                path:'reset/:token',
                name: 'reset',
                components: {
                    default: password_reset,
                    title: { template: '<span>Создать новый пароль</span>' }

                },
                props: {default:true},
            },
            {
                path:'activate/:token',
                name: 'activate',
                components: {
                    default: login,
                    title: { template: '<span>Вход</span>' }

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