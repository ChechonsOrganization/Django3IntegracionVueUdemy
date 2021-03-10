import Vue from 'vue'
import App from './App.vue'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import VueRouter from 'vue-router'

// RUTAS PARA ROUTER VUE
import List from './components/List.vue'
import Detail from './components/Detail.vue'
import ListCategory from './components/ListCategory.vue'
import ListType from './components/ListType.vue'


Vue.use(VueRouter)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.config.productionTip = false

const routes = [
  {path:'/', component: List, name: 'list'},
  {path:'/detail/:id', component: Detail, name: 'detail'},
  {path:'/category/:id/elements', component: ListCategory, name: 'list-category'},
  {path:'/type/:id/elements', component: ListType, name: 'list-type'}
]

const router = new VueRouter({
  mode: 'history',
  routes
})

//AÑADIMOS router
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
