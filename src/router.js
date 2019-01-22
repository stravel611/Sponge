import Vue from 'vue'
import Router from 'vue-router'
import Overview from './views/Overview'
import Category from './views/Category'
import Management from './views/Management'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'overview',
      component: Overview
    }, {
      path: '/category/:id',
      name: 'category',
      component: Category
    }, {
      path: '/',
      name: 'management',
      component: Management
    }
  ]
})
