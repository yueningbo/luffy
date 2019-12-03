<template>
  <div class="course">
    <Header></Header>
    <div class="main">
      <!-- 筛选条件 -->
      <div class="condition">
        <ul class="cate-list">
          <li class="title">课程分类:</li>
          <li :class="category==0?'this':''" @click="category=0">全部</li>
          <li :class="category==item.id?'this':''" v-for="item in category_list" @click="category=item.id">
            {{item.name}}
          </li>
        </ul>
        <div class="ordering">
          <ul>
            <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选:</li>
            <li class="default" :class="change_cls('id',orders)" @click="change_orders('id')">默认</li>
            <li class="hot" :class="change_cls('students',orders)" @click="change_orders('students')">人气</li>
            <li class="price" :class="change_cls('price',orders)" @click="change_orders('price')">价格</li>
          </ul>
          <p class="condition-result">共{{course_count}}个课程</p>
        </div>

      </div>
      <!-- 课程列表 -->
      <div class="course-list">
        <div class="course-item" v-for="course in course_list">
          <div class="course-image">
            <img :src="course.course_img" :alt="course.name">
          </div>
          <div class="course-info">
            <h3>
              <router-link :to="'/course/'+course.id">{{course.name}}</router-link>
              <span><img src="/static/image/avatar1.svg" alt="">{{course.students}}人已加入学习</span>
            </h3>
            <p class="teather-info">{{course.teacher.name}} {{course.teacher.signature}} {{course.teacher.title}} <span>共{{course.lessons}}课时/{{course.pub_lessons==course.lessons?'更新完成':`已更新${course.pub_lessons}个课时`}}</span>
            </p>
            <ul class="lesson-list">
              <li v-for="lesson, key in course.lesson_list">
                <router-link :to="lesson.section_link">
                  <span class="lesson-title">0{{key+1}} | 第{{lesson.lesson}}节：{{lesson.name}}</span>
                  <span class="free" v-if="lesson.free_trail">免费</span>
                </router-link>
              </li>
            </ul>
            <div class="pay-box">
              <span class="discount-type">限时免费</span>
              <span class="discount-price">￥0.00元</span>
              <span class="original-price">原价：{{course.price}}元</span>
              <span class="buy-now">立即购买</span>
            </div>
          </div>
        </div>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[2,5,10,20]"
          background
          :page-size="size"
          layout="sizes, prev, pager, next, jumper"
          :total="course_count"
        >
        </el-pagination>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
  import Header from "./common/Header"
  import Footer from "./common/Footer"

  export default {
    name: "Course",
    data() {
      return {
        category: 0,
        course_count: 0,
        category_list: [],
        course_list: [{
          teacher: {},
        }],
        orders: "id", // id表示默认正序,-id表示默认倒序，students表示人气正序，...,price表示价格...
        size: 2, // 每一页显示的数据量
        page: 1, // 当前页码
      }
    },
    components: {
      Header,
      Footer,
    },
    watch: {
      category() {
        // 在切换不同分类时，重新组装ajax请求参数，获取课程列表
        this.page = 1;
        this.get_course();
      },
      orders() {
        // 在切换不同的排序方式时，重新组装ajax请求参数，获取课程列表
        this.get_course();
      },
      size() {
        // 在切换不同页面显示数据量大小的时候
        this.page = 1;
        this.get_course();
      },
      page() {
        // 在切换不用页码的时候
        this.get_course();
      }
    },
    created() {
      this.get_course_category();
      this.get_course();
    },
    methods: {
      get_course_category() {
        // 获取课程分类列表
        this.$axios.get(`${this.$settings.Host}/course/category/`).then(response => {
          this.category_list = response.data;
          console.log(this.category_list)
        }).catch(error => {
          this.$alert("网络错误！获取课程分类信息失败！", "路飞学城");
        });
      },
      change_orders(type) {
        // 修改排序方式
        if (this.orders === type) {
          this.orders = "-" + type;
        } else {
          this.orders = type;
        }
      },
      change_cls(type, orders) {
        if (type === "id" && orders === "id") {
          return "this asc";
        } else if (type === "id" && orders === "-id") {
          return "this desc";
        } else if (type === "students" && orders === "students") {
          return "this asc";
        } else if (type === "students" && orders === "-students") {
          return "this desc";
        } else if (type === "price" && orders === "price") {
          return "this asc";
        } else if (type === "price" && orders === "-price") {
          return "this desc";
        }
      },
      get_course() {
        // 获取课程列表
        let filter = {
          ordering: this.orders,
          size: this.size,
          page: this.page,
        };
        if (this.category > 0) {
          filter.course_category = this.category;
        }
        this.$axios.get(`${this.$settings.Host}/course/`, {
          params: filter,
        }).then(response => {
          this.course_list = response.data.results;
          this.course_count = response.data.count;
        }).catch(error => {
          this.$alert("网络错误！获取课程信息失败！", "路飞学城");
        });
      },
      handleSizeChange(size) {
        // 分页组件发生页面数据量大小改动时
        this.size = size;
      },
      handleCurrentChange(page) {
        // 分页组件发生页码改变时
        this.page = page;
      },
    }
  }
</script>


<style scoped>
  .course {
    background: #f6f6f6;
  }

  .course .main {
    width: 1100px;
    margin: 35px auto 0;
  }

  .course .condition {
    margin-bottom: 35px;
    padding: 25px 30px 25px 20px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 4px 0 #f0f0f0;
  }

  .course .cate-list {
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51, 51, 51, .05);
    padding-bottom: 18px;
    margin-bottom: 17px;
  }

  .course .cate-list::after {
    content: "";
    display: block;
    clear: both;
  }

  .course .cate-list li {
    float: left;
    font-size: 16px;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
    border: 1px solid transparent; /* transparent 透明 */
  }

  .course .cate-list .title {
    color: #888;
    margin-left: 0;
    letter-spacing: .36px;
    padding: 0;
    line-height: 28px;
  }

  .course .cate-list .this {
    color: #ffc210;
    border: 1px solid #ffc210 !important;
    border-radius: 30px;
  }

  .course .ordering::after {
    content: "";
    display: block;
    clear: both;
  }

  .course .ordering ul {
    float: left;
  }

  .course .ordering ul::after {
    content: "";
    display: block;
    clear: both;
  }

  .course .ordering .condition-result {
    float: right;
    font-size: 14px;
    color: #9b9b9b;
    line-height: 28px;
  }

  .course .ordering ul li {
    float: left;
    padding: 6px 15px;
    line-height: 16px;
    margin-left: 14px;
    position: relative;
    transition: all .3s ease;
    cursor: pointer;
    color: #4a4a4a;
  }

  .course .ordering .title {
    font-size: 16px;
    color: #888;
    letter-spacing: .36px;
    margin-left: 0;
    padding: 0;
    line-height: 28px;
  }

  .course .ordering .this {
    color: #ffc210;
    position: relative;
  }

  .course .ordering .this::before,
  .course .ordering .this::after {
    cursor: pointer;
    content: "";
    display: block;
    width: 0px;
    height: 0px;
    border: 5px solid transparent;
    position: absolute;
    right: 0;
  }

  .course .ordering .this::before {
    border-bottom: 5px solid #aaa;
    margin-bottom: 2px;
    top: 2px;
  }

  .course .ordering .this::after {
    border-top: 5px solid #aaa;
    bottom: 2px;
  }

  .course .ordering .asc::before {
    border-bottom: 5px solid #ffc210;
  }

  .course .ordering .desc::after {
    border-top: 5px solid #ffc210;
  }

  .course .course-item:hover {
    box-shadow: 4px 6px 16px rgba(0, 0, 0, .5);
  }

  .course .course-item {
    width: 1050px;
    background: #fff;
    padding: 20px 30px 20px 20px;
    margin-bottom: 35px;
    border-radius: 2px;
    cursor: pointer;
    box-shadow: 2px 3px 16px rgba(0, 0, 0, .1);
    /* css3.0 过渡动画 hover 事件操作 */
    transition: all .2s ease;
  }

  .course .course-item::after {
    content: "";
    display: block;
    clear: both;
  }

  /* 顶级元素 父级元素  当前元素{} */
  .course .course-item .course-image {
    float: left;
    width: 423px;
    height: 210px;
    margin-right: 30px;
  }

  .course .course-item .course-image img {
    width: 100%;
  }

  .course .course-item .course-info {
    float: left;
    width: 596px;
  }

  .course-item .course-info h3 {
    font-size: 26px;
    color: #333;
    font-weight: normal;
    margin-bottom: 8px;
  }

  .course-item .course-info h3 span {
    font-size: 14px;
    color: #9b9b9b;
    float: right;
    margin-top: 14px;
  }

  .course-item .course-info h3 span img {
    width: 11px;
    height: auto;
    margin-right: 7px;
  }

  .course-item .course-info .teather-info {
    font-size: 14px;
    color: #9b9b9b;
    margin-bottom: 14px;
    padding-bottom: 14px;
    border-bottom: 1px solid #333;
    border-bottom-color: rgba(51, 51, 51, .05);
  }

  .course-item .course-info .teather-info span {
    float: right;
  }

  .course-item .lesson-list::after {
    content: "";
    display: block;
    clear: both;
  }

  .course-item .lesson-list li {
    float: left;
    width: 44%;
    font-size: 14px;
    color: #666;
    padding-left: 22px;
    /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
    background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
    margin-bottom: 15px;
  }

  .course-item .lesson-list li .lesson-title {
    /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    display: inline-block;
    max-width: 200px;
  }

  .course-item .lesson-list li:hover {
    background-image: url("/static/image/play-icon-yellow.svg");
    color: #ffc210;
  }

  .course-item .lesson-list li .free {
    width: 34px;
    height: 20px;
    color: #fd7b4d;
    vertical-align: super;
    margin-left: 10px;
    border: 1px solid #fd7b4d;
    border-radius: 2px;
    text-align: center;
    font-size: 13px;
    white-space: nowrap;
  }

  .course-item .lesson-list li:hover .free {
    color: #ffc210;
    border-color: #ffc210;
  }

  .course-item .pay-box::after {
    content: "";
    display: block;
    clear: both;
  }

  .course-item .pay-box .discount-type {
    padding: 6px 10px;
    font-size: 16px;
    color: #fff;
    text-align: center;
    margin-right: 8px;
    background: #fa6240;
    border: 1px solid #fa6240;
    border-radius: 10px 0 10px 0;
    float: left;
  }

  .course-item .pay-box .discount-price {
    font-size: 24px;
    color: #fa6240;
    float: left;
  }

  .course-item .pay-box .original-price {
    text-decoration: line-through;
    font-size: 14px;
    color: #9b9b9b;
    margin-left: 10px;
    float: left;
    margin-top: 10px;
  }

  .course-item .pay-box .buy-now {
    width: 120px;
    height: 38px;
    background: transparent;
    color: #fa6240;
    font-size: 16px;
    border: 1px solid #fd7b4d;
    border-radius: 3px;
    transition: all .2s ease-in-out;
    float: right;
    text-align: center;
    line-height: 38px;
  }

  .course-item .pay-box .buy-now:hover {
    color: #fff;
    background: #ffc210;
    border: 1px solid #ffc210;
  }
</style>
