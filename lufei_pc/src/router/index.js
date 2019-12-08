import Vue from "vue"
import Router from "vue-router"

// 导入需要注册路由的组件
import Home from "../components/Home"
// 登录组件导入
import Login from "../components/Login"
import Register from "../components/Register"
import Course from "../components/Course"
import Detail from "@/components/Detail"
import Cart from "../components/Cart"
import Order from "@/components/Order"


Vue.use(Router);

// 配置路由列表
export default new Router({
  mode: "history",
  routes: [
    // 路由列表
    {
      name: "Home",
      path: "/home",
      component: Home,
    },
    {
      name: "Home",
      path: "/",
      component: Home,
    },
    {
      name: "Login",
      path: "/user/login",
      component: Login,
    },
    {
      name: "Register",
      path: "/register",
      component: Register,
    },
    {
      path: '/course',
      name: 'Course',
      component: Course,
    },
    {
      path: '/course/:id',
      name: 'Detail',
      component: Detail,
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart,
    },
    {
      path: '/order',
      name: "Order",
      component: Order,
    },
  ]
})
