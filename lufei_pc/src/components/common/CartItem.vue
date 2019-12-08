<template>
  <div class="cart_item">
    <div class="cart_column column_1">
      <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
    </div>
    <div class="cart_column column_2">
      <img :src="course.course_img" alt="">
      <span><router-link :to="`/course/${course.course_id}`">{{course.course_name}}</router-link></span>
    </div>
    <div class="cart_column column_3">
      <el-select v-model="course.expire" size="mini" placeholder="请选择购买有效期" class="my_el_select">
        <el-option v-for="item in course.expire_list" :label="item.expire_text" :value="item.expire_time"
                   :key="item.expire_time"></el-option>
      </el-select>
    </div>
    <div class="cart_column column_4">¥{{course.price.toFixed(2)}}</div>
    <div class="cart_column column_4 delete" @click="deleteHandler">删除</div>
  </div>
</template>

<script>
  export default {
    name: "CartItem",
    props: ["course", "token"],
    data() {
      return {
        checked: false
      }
    },
    watch: {
      "course.selected": function () {
        // 当用户切换商品勾选状态时，同步到服务端
        this.change_course_status();
      },
      "course.expire": function () {
        // 当用户切换商品有效期时，切换对应选项的价格显示在页面中,并同步到服务端
        this.change_course_expire();
      }
    },
    methods: {
      change_course_status() {
        // 切换商品的勾选状态
        this.$axios.put(`${this.$settings.Host}/cart/`, {
          course_id: this.course.course_id,
          selected: this.course.selected,
        }, {
          headers: {
            Authorization: "jwt " + this.token,
          }
        }).then(response => {
          // 当子组件如果切换勾选状态成功以后, 要通知父组件同步课程的勾选状态并重新计算勾选商品的价格
          this.$emit("change_course_expire", this.course);
          this.$message.success("切换勾选状态成功！");
        }).catch(error => {
          this.$message.error("切换勾选状态失败！");
        });
      },
      change_course_expire() {
        // 切换商品的有效期选项
        for (let item of this.course.expire_list) {
          if (item.expire_time === this.course.expire) {
            this.course.price = item.price;
            // 同步到服务端
            this.$axios.patch(`${this.$settings.Host}/cart/`, {
              course_id: this.course.course_id,
              expire_time: item.expire_time,
            }, {
              headers: {
                Authorization: "jwt " + this.token,
              }
            }).then(response => {
              // 当子组件如果切换有效期选项成功以后, 要通知父组件同步课程信息并重新计算勾选商品的价格
              this.$emit("change_course_expire", this.course);
              this.$message.success("切换有效期选项成功！");
              //
            }).catch(error => {
              this.$message.error("切换有效期选项失败！");
            });
          }
        }
      },
      deleteHandler() {
        // 购物车商品的删除操作
        this.$axios.delete(`${this.$settings.Host}/cart/`, {
          params: {
            course_id: this.course.course_id,
          },
          headers: {
            Authorization: "jwt " + this.token,
          }
        }).then(response => {
          this.$message.success("删除商品操作成功!~");
          this.$emit("deleteHandler", this.course);
        }).catch(error => {
          this.$message.error("删除商品操作失败!~");
        })
      }
    }
  }
</script>

<style scoped>
  .cart_item::after {
    content: "";
    display: block;
    clear: both;
  }

  .cart_column {
    float: left;
    height: 250px;
  }

  .cart_item .column_1 {
    width: 88px;
    position: relative;
  }

  .my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
  }

  .cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
  }

  .cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
  }

  .cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
  }

  .my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  .cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
  }

  .delete {
    cursor: pointer;
  }

  .delete:hover {
    color: #aa0000;
  }
</style>
