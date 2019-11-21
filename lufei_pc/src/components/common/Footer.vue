<template>
  <div class="footer">
    <el-container>
      <el-row>
        <el-col :span="4"><router-link to="">关于我们</router-link></el-col>
        <el-col :span="4"><router-link to="">联系我们</router-link></el-col>
        <el-col :span="4"><router-link to="">商务合作</router-link></el-col>
        <el-col :span="4"><router-link to="">帮助中心</router-link></el-col>
        <el-col :span="4"><router-link to="">意见反馈</router-link></el-col>
        <el-col :span="4"><router-link to="">新手指南</router-link></el-col>
        <el-col :span="24"><p class="copyright">Copyright © luffycity.com版权所有 | 京ICP备17072161号-1</p></el-col>
      </el-row>
    </el-container>
  </div>
</template>

<script>
  export default {
    name:"Footer",
    data(){
      return {}
    }
  }
</script>


<style scoped>
.footer{
  width: 100%;
  height: 128px;
  background: #25292e;
}
.footer .el-container{
  width: 1200px;
  margin: auto;
}
.footer .el-row {
  align-items: center;
  padding: 0 200px;
  padding-bottom: 15px;
  width: 100%;
  margin-top: 38px;
}
.footer .el-row a{
  color: #fff;
  font-size: 14px;
}
.footer .el-row .copyright{
  text-align: center;
  color: #fff;
  font-size: 14px;
}
</style>
