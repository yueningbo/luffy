<template>
  <el-carousel height="720px" :interval="3000" arrow="always">
    <el-carousel-item :key="key" v-for="banner,key in banner_list">
      <a :href="banner.link" v-if="banner.is_http"><img :src="banner.image" alt=""></a>
      <router-link :to="banner.link" v-else><img :src="banner.image" alt=""></router-link>
    </el-carousel-item>
  </el-carousel>
</template>

<script>
    export default {
        name: "Banner",
        data(){
            return {
                banner_list:[],
            }
        },
        created() {
            this.get_banner();
        },
        methods:{
            get_banner(){
                // 获取轮播广告
                // es6提供了一种允许换行的字符串，叫文档字符串，可以允许在字段中换行并输出js变量
                this.$axios.get(`${this.$settings.Host}/banner/`).then(response=>{
                    this.banner_list = response.data;
                }).catch(error=>{
                   this.$alert("获取轮播图失败!","路飞学城");
                });
            }
        }
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
