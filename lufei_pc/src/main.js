// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import settings from "./settings";
import "../static/css/reset.css";
// 导入gt极验
import "../static/js/gt.js";

import store from "./store/index";


import axios from 'axios'; // 从node_modules目录中导入包
// 允许ajax发送请求时附带cookie
axios.defaults.withCredentials = false;

Vue.prototype.$axios = axios; // 把对象挂载vue中

Vue.config.productionTip = false //禁用前端的session
Vue.prototype.$settings = settings

Vue.use(ElementUI);

require("video.js/dist/video-js.css");
require("vue-video-player/src/custom-theme.css");
import VideoPlayer from 'vue-video-player'

Vue.use(VideoPlayer);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});
