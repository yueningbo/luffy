<template>
  <div class="login box">
    <img src="../../static/image/Loginbg.3377d0c.jpg" alt="">
    <div class="login">
      <div class="login-title">
        <img src="../../static/image/Logotitle.1ba5466.png" alt="">
        <p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
      </div>
      <div class="login_box">
        <div class="title">
          <span @click="login_type=0">密码登录</span>
          <span @click="login_type=1">短信登录</span>
        </div>
        <div class="inp" v-if="login_type==0">
          <input v-model="username" type="text" placeholder="用户名 / 手机号码" class="user">
          <input v-model="password" type="password" name="" class="pwd" placeholder="密码">
          <div id="geetest1"></div>
          <div class="rember">
            <p>
              <input type="checkbox" class="no" name="a" v-model="remember"/>
              <span>记住密码</span>
            </p>
            <p>忘记密码</p>
          </div>
          <button class="login_btn" @click="get_geetest_captcha">登录</button>
          <p class="go_login">没有账号
            <router-link to="/register">立即注册</router-link>
          </p>
        </div>
        <div class="inp" v-show="login_type==1">
          <input v-model="username" type="text" placeholder="手机号码" class="user">
          <input v-model="password" type="text" class="pwd" placeholder="短信验证码">
          <button id="get_code">获取验证码</button>
          <button class="login_btn">登录</button>
          <p class="go_login">没有账号
            <router-link to="/register">立即注册</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Login',
    data() {
      return {
        login_type: 0,
        username: "",
        password: "",
        remember: false,
      }
    },

    methods: {
      loginHandler() {
        this.$axios.post(`${this.$settings.Host}/user/login/`, {
          username: this.username,
          password: this.password,
        }).then(response => {
          // 记住密码或者不记住
          if (this.remember) {
            sessionStorage.removeItem("user_token");
            sessionStorage.removeItem("user_id");
            sessionStorage.removeItem("user_name");
            localStorage.user_token = response.data.token;
            localStorage.user_id = response.data.id;
            localStorage.user_name = response.data.username;
          } else {
            localStorage.removeItem("user_token");
            localStorage.removeItem("user_id");
            localStorage.removeItem("user_name");
            sessionStorage.user_token = response.data.token;
            sessionStorage.user_id = response.data.id;
            sessionStorage.user_name = response.data.username;
          }
          let self = this;
          this.$alert("登录成功，欢迎回来！", "路飞学城", {
            callback() {
              self.$router.go(-1);//返回上一页
            }
          })
        }).catch(error => {
          this.$message.error("对不起,登录失败,请确认账号或密码是否正确！")
        })
      },
      get_geetest_captcha() {
        //获取验证码
        this.$axios.get(`${this.$settings.Host}/user/captcha`, {
          params: {
            username: this.username,
          }
        }).then(response => {
          // 使用initGeetest接口
          // 参数1：配置参数
          // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
          let data = JSON.parse(response.data);
          initGeetest({
            gt: data.gt,
            challenge: data.challenge,
            product: "popup",// 产品形式, 包括:float, embed, popup, 只对pc版验证码有效
            offline: !data.success// 表示用户后台检测极验服务器是否宕机, 一般无需关注
          }, this.handlerPopup);
        }).catch(error => {
          this.$alert("对不起,用户不存在!", "路飞学城");
          console.log(error.response);
        })
      },
      handlerPopup(captchaObj) {
        let self = this;
        // 极验验证密码的验证方法
        captchaObj.onSuccess(function () {
          var validate = captchaObj.getValidate();
          // 当用户拖动验证码正确以后，发送请求给后端
          self.$axios.post(`${self.$settings.Host}/user/captcha/`, {
            geetest_challenge: validate.geetest_challenge,
            geetest_validate: validate.geetest_validate,
            geetest_seccode: validate.geetest_seccode
          }).then(response => {
            if (response.data.status) {
              // 验证码通过以后，才发送账号和密码进行登录！
              self.loginHandler();
            }
          }).catch(error => {
            console.log(error.response);
          });
        });

        // 将验证码加到id为geetest1的元素里
        document.getElementById("geetest1").innerHTML = "";
        captchaObj.appendTo("#geetest1");
      }
    },

  };
</script>

<style scoped>
  .box {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
  }

  .box img {
    width: 100%;
    min-height: 100%;
  }

  .box .login {
    position: absolute;
    width: 500px;
    height: 400px;
    top: 0;
    left: 0;
    margin: auto;
    right: 0;
    bottom: 0;
    top: -338px;
  }

  .login .login-title {
    width: 100%;
    text-align: center;
  }

  .login-title img {
    width: 190px;
    height: auto;
  }

  .login-title p {
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
  }

  .login_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
  }

  .login_box .title {
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 50px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
  }

  .login_box .title span:nth-of-type(1) {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
  }

  .inp {
    width: 350px;
    margin: 0 auto;
  }

  .inp input {
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
  }

  .inp input.user {
    margin-bottom: 16px;
  }

  .inp .rember {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
  }

  .inp .rember p:first-of-type {
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
  }

  .inp .rember p:nth-of-type(2) {
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
  }

  .inp .rember input {
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
  }

  .inp .rember p span {
    display: inline-block;
    font-size: 12px;
    width: 100px;
    /*position: absolute;*/
    /*left: 20px;*/

  }

  #geetest {
    margin-top: 20px;
  }

  .login_btn {
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
  }

  .inp .go_login {
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
  }

  .inp .go_login span {
    color: #84cc39;
    cursor: pointer;
  }
</style>
