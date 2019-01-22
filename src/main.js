import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import LightTimeLine from 'vue-light-timeline'
import 'element-ui/lib/theme-chalk/index.css'
import './plugins/axios'


Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(LightTimeLine)


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
