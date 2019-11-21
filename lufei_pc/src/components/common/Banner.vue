<template>
  <el-carousel height="720px" :interval="3000" arrow="always">
    <el-carousel-item>
      <img src="/static/image/alex.jpeg" alt="">
    </el-carousel-item>
    <el-carousel-item>
      <img src="/static/image/banner1.png" alt="">
    </el-carousel-item>
    <el-carousel-item>
      <img src="/static/image/banner1.png" alt="">
    </el-carousel-item>
  </el-carousel>
</template>

<script>
    export default {
        name: "Banner",
    }
</script>

<style scoped>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>

