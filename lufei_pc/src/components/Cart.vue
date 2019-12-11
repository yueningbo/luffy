<template>
  <div class="cart">
    <Header></Header>
    <div class="cart_info">
      <div class="cart_title">
        <span class="text">我的购物车</span>
        <span class="total">共{{this.course_list.length}}门课程</span>
      </div>
      <div class="cart_table">
        <div class="cart_head_row">
          <span class="doing_row"></span>
          <span class="course_row">课程</span>
          <span class="expire_row">有效期</span>
          <span class="price_row">单价</span>
          <span class="do_more">操作</span>
        </div>
        <div class="cart_course_list">
          <CartItem
            :token="token"
            :key="key"
            :course="course"
            v-for="course,key in course_list"
            @deleteHandler="delete_course"
            @change_course_expire="change_expire"
          ></CartItem>
        </div>
        <div class="cart_footer_row">
          <span class="cart_select"><label> <el-checkbox v-model="checked"></el-checkbox><span>全选</span></label></span>
          <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
          <span class="goto_pay"><router-link to="/order">去结算</router-link></span>
          <span class="cart_total">总计：¥{{total_price.toFixed(2)}}</span>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"
  import CartItem from "./common/CartItem"

  export default {
    name: "Cart",
    data() {
      return {
        course_list: [],
        total_price: 0,
        checked: false,
      }
    },
    created() {
      this.check_user();
      this.get_course();
    },
    methods: {
      check_user() {
        this.token = this.$settings.check_user_login();
        if (!this.token) {
          let self = this;
          this.$alert("对不起，您尚未登录!无法访问购物车！", "路飞学城", {
            callback() {
              self.$router.push("/user/login");
            }
          })
        }
      },
      get_course() {
        // 获取购物车中的商品列表
        this.$axios.get(`${this.$settings.Host}/cart/`, {
          headers: {
            Authorization: "jwt " + this.token,
          }
        }).then(response => {
          this.course_list = response.data;
          // 获取课程列表以后,计算当前购物车中勾选状态的总价格
          this.calc_cart_total();
        }).catch(error => {
          this.$alert("对不起，获取购物车商品列表信息失败！", "路飞学城");
        });
      },
      delete_course(course) {
        // 删除商品
        for (let key in this.course_list) {
          if (course === this.course_list[key]) {
            // 数组.splice(key, length) # 从指定下标key位置删除length个成员
            this.course_list.splice(key, 1);
          }
        }
        // 删除课程以后,也要重新计算总价格
        this.calc_cart_total();
      },
      change_expire(course) {
        // 子组件如果切换勾选状态成功以后, 要通知父组件同步课程的勾选状态并重新计算勾选商品的价格
        for (let key in this.course_list) {
          if (this.course_list[key].course_id === course.course_id) {
            this.course_list.splice(key, 1, course);//替换课程对象
          }
        }
        // 同步了父组件中的对应课程的信息哟呼,重新计算总价格
        this.calc_cart_total();
      },
      calc_cart_total() {
        // 统计整个购物车中，勾选所有商品的总价格
        this.total_price = 0;
        for (let course of this.course_list) {
          if (course.selected) {
            this.total_price += course.real_price;
          }
        }
      }
    },
    components: {
      Header,
      Footer,
      CartItem,
    }
  }
</script>

<style scoped>
  .cart_info {
    width: 1200px;
    margin: 0 auto 200px;
  }

  .cart_title {
    margin: 25px 0;
  }

  .cart_title .text {
    font-size: 18px;
    color: #666;
  }

  .cart_title .total {
    font-size: 12px;
    color: #d0d0d0;
  }

  .cart_table {
    width: 1170px;
  }

  .cart_table .cart_head_row {
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
    padding-right: 30px;
  }

  .cart_table .cart_head_row::after {
    content: "";
    display: block;
    clear: both;
  }

  .cart_table .cart_head_row .doing_row,
  .cart_table .cart_head_row .course_row,
  .cart_table .cart_head_row .expire_row,
  .cart_table .cart_head_row .price_row,
  .cart_table .cart_head_row .do_more {
    padding-left: 10px;
    height: 80px;
    float: left;
  }

  .cart_table .cart_head_row .doing_row {
    width: 78px;
  }

  .cart_table .cart_head_row .course_row {
    width: 530px;
  }

  .cart_table .cart_head_row .expire_row {
    width: 188px;
  }

  .cart_table .cart_head_row .price_row {
    width: 162px;
  }

  .cart_table .cart_head_row .do_more {
    width: 162px;
  }

  .cart_footer_row {
    padding-left: 30px;
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
  }

  .cart_footer_row .cart_select span {
    margin-left: 17px;
    font-size: 18px;
    color: #666;
  }

  .cart_footer_row .cart_delete {
    margin-left: 58px;
  }

  .cart_delete .el-icon-delete {
    font-size: 18px;
  }

  .cart_delete span {
    margin-left: 15px;
    cursor: pointer;
    font-size: 18px;
    color: #666;
  }

  .cart_total {
    float: right;
    margin-right: 62px;
    font-size: 18px;
    color: #666;
  }

  .goto_pay {
    float: right;
    width: 159px;
    height: 80px;
    outline: none;
    border: none;
    background: #ffc210;
    font-size: 18px;
    color: #fff;
    text-align: center;
    cursor: pointer;
  }
</style>
