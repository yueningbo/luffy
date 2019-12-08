export default {
  Host: "http://api.luffycity.cn:8000",
  check_user_login() {
    // 检查用户是否登录了
    let token = sessionStorage.user_token || localStorage.user_token;
    return token;
  },
}

