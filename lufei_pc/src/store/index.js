import Vue from "vue"
import Vuex from "vuex"


Vue.use(Vuex);

export default new Vuex.Store({
  // 数据仓库, 类似vue组件中的data
  state: {
    cart_length: sessionStorage.cart_length || 0
  },
// 数据操作方法, 类似vue里的methods
  mutations: {
    update_cart_length(state, data) {
      state.cart_length = data;
      sessionStorage.cart_length = data;
    }
  }

})
;
