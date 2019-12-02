from rest_framework.pagination import PageNumberPagination


class CourseListPageNumberPagination(PageNumberPagination):
    page_query_param = "page"  # 地址上表示页码的变量名
    page_size = 5  # 每一页显示的数据量, 没有设置页码则不分页
    # 允许客户端通过指定的参数名来设置每一页的数据量大小, 默认是size
    page_size_query_param = "size"
    max_page_size = 20  # 限制每一页最大的展示数据量
