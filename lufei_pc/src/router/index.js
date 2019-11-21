import Vue from "vue"
import Router from "vue-router"

// 导入需要注册路由的组件
import Home from "../components/Home"
Vue.use(Router);

// 配置路由列表
export default new Router({
  mode:"history",
  routes:[
    // 路由列表
    {
      name:"Home",
      path: "/home",
      component:Home,
    },
    {
      name:"Home",
      path: "/",
      component:Home,
    }
  ]
})
