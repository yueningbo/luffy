<template>
  <div class="cart">
    <Header/>
    <div class="cart-info">
      <h3 class="cart-top">购物车结算 <span>共1门课程</span></h3>
      <div class="cart-title">
        <el-row>
          <el-col :span="2">&nbsp;</el-col>
          <el-col :span="10">课程</el-col>
          <el-col :span="8">有效期</el-col>
          <el-col :span="4">价格</el-col>
        </el-row>
      </div>
      <div class="cart-item" v-for="course in course_list">
        <el-row>
          <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
          <el-col :span="10" class="course-info">
            <img :src="course.course_img" alt="">
            <span>{{course.course_name}}</span>
          </el-col>
          <el-col :span="8"><span>{{course.expire_text}}</span></el-col>
          <el-col :span="4" class="course-price">¥{{course.price.toFixed(2)}}</el-col>
        </el-row>
      </div>

      <div class="calc">
        <el-row class="pay-row">
          <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
          <el-col :span="8">
            <span class="alipay" v-if="pay_type==1" @click="pay_type=1"><img src="/static/image/alipay2.png"
                                                                             alt=""></span>
            <span class="alipay" v-else @click="pay_type=1"><img src="/static/image/alipay.png" alt=""></span>
            <span class="alipay wechat" v-if="pay_type==2" @click="pay_type=2"><img src="/static/image/wechat2.png"
                                                                                    alt=""></span>
            <span class="alipay wechat" v-else @click="pay_type=2"><img src="/static/image/wechat.png" alt=""></span>
          </el-col>
          <el-col :span="8" class="count">实付款： <span>¥99.50</span></el-col>
          <el-col :span="4" class="cart-pay"><span @click="payhander">{{pay_type===1?'支付宝':'微信'}}支付</span></el-col>
        </el-row>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"

  export default {
    name: "Order",
    data() {
      return {
        token: "",
        pay_type: 1,
        credit: 0, // 本次订单使用的积分
        coupon: 0, // 本次订单使用的优惠券ID
        course_list: [],
        total_price: 0,
      }
    },
    components: {
      Header,
      Footer,
    },
    created() {
      this.check_user();
      this.get_selected_course();
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
      get_selected_course() {
        // 获取购物车中勾选的商品信息
        this.$axios.get(`${this.$settings.Host}/cart/order/`, {
          headers: {
            Authorization: "jwt " + this.token,
          }
        }).then(response => {
          this.course_list = response.data;
        }).catch(error => {
          let self = this;
          this.$alert("获取购物车数据失败!请联系客服工作人员!", "路飞学城", {
            callback() {
              self.$router.go(-1);
            }
          });
        });
      },
      payhander() {
        // 订单生成
        this.$axios.post(`${this.$settings.Host}/order/`, {
          pay_type: this.pay_type,
          coupon: this.coupon,
          credit: this.credit,
        }, {
          headers: {
            Authorization: "jwt " + this.token,
          }
        }).then(response => {
          // 去支付
          console.log(response.data);
        }).catch(error => {
          // 失败
          this.$message.error("对不起，下单失败！请联系客服工作人员！");
        });


      }
    }
  }
</script>

<style scoped>
  .cart {
    margin-top: 80px;
  }

  .cart-info {
    overflow: hidden;
    width: 1200px;
    margin: auto;
  }

  .cart-top {
    font-size: 18px;
    color: #666;
    margin: 25px 0;
    font-weight: normal;
  }

  .cart-top span {
    font-size: 12px;
    color: #d0d0d0;
    display: inline-block;
  }

  .cart-title {
    background: #F7F7F7;
    height: 70px;
  }

  .calc {
    margin-top: 25px;
    margin-bottom: 40px;
  }

  .calc .count {
    text-align: right;
    margin-right: 10px;
    vertical-align: middle;
  }

  .calc .count span {
    font-size: 36px;
    color: #333;
  }

  .calc .cart-pay {
    margin-top: 5px;
    width: 110px;
    height: 38px;
    outline: none;
    border: none;
    color: #fff;
    line-height: 38px;
    background: #ffc210;
    border-radius: 4px;
    font-size: 16px;
    text-align: center;
    cursor: pointer;
  }

  .cart-item {
    height: 120px;
    line-height: 120px;
    margin-bottom: 30px;
  }

  .course-info img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
  }

  .alipay {
    display: inline-block;
    height: 48px;
  }

  .alipay img {
    height: 100%;
    width: auto;
  }

  .pay-text {
    display: block;
    text-align: right;
    height: 100%;
    line-height: 100%;
    vertical-align: middle;
    margin-top: 20px;
  }
</style>
