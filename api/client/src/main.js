import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import GameList from './components/GameList'
import Chopping from './components/Chopping'
import Product from './components/Product'

import {
	transitions,
	VApp,
	VAutocomplete,
	VBtn,
	VCard,
	VDataTable,
	VFooter,
	VGrid,
	VIcon,
	VList,
	VNavigationDrawer,
	VPagination,
	VProgressCircular,
	VToolbar,
	Vuetify,
} from 'vuetify'
import { formatDate } from './helper/helper'

require('vuetify/src/stylus/app.styl')

Vue.use(Vuetify, {
    components: {
        Vuetify,
        VApp,
        VNavigationDrawer,
        VFooter,
        VList,
        VBtn,
        VIcon,
        VGrid,
		VCard,
        VToolbar,
        VDataTable,
        transitions,
        VProgressCircular,
        VPagination,
        VAutocomplete,
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
Vue.filter('date', formatDate)

Vue.config.productionTip = false
window.baseUrl = 'http://127.0.0.1:5000/'
window.playstation = 'https://store.playstation.com'

const routers = [
    {path: '/', name: 'games', component: GameList},
    {path: '/chopping', name: 'chopping', component: Chopping},
    {path: '/product/:number', name: 'product', component: Product},
]

const router = new VueRouter({
    mode: 'history',
    routes: routers
})


new Vue({
    router: router,
    render: h => h(App)
}).$mount('#app')
