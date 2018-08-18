import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'

require('vuetify/src/stylus/app.styl')

import GameList from './components/GameList'


import {
    Vuetify,
    VApp,
    VNavigationDrawer,
    VFooter,
    VList,
    VBtn,
    VIcon,
    VGrid,
    VToolbar,
    transitions
} from 'vuetify'

Vue.use(Vuetify, {
    components: {
        VApp,
        VNavigationDrawer,
        VFooter,
        VList,
        VBtn,
        VIcon,
        VGrid,
        VToolbar,
        transitions
    },
    theme: {
        primary: '#ee44aa',
        secondary: '#424242',
        accent: '#82B1FF',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FFC107'
    }
})


Vue.use(VueRouter)

Vue.config.productionTip = false

const routers = [
    {path: '/', name: 'games', component: GameList}
]

const router = new VueRouter({
    mode: 'history',
    routes: routers
})


new Vue({
    router: router,
    render: h => h(App)
}).$mount('#app')
