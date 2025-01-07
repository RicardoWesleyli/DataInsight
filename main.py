from typing_extensions import Doc
import streamlit as st
import pandas as pd
import time
import numpy as np

# 浏览器标签
st.set_page_config(
    layout="wide",
    page_title="Data Insight",
    page_icon="📊",
)

# 页面标题
st.title("📊 Data Insight")

# 初始化变量
metric_value = 0
today_sales_value = 0

# 定义处理销量数据的函数
def process_sales(date_column, selected_date, metric_column):
    try:
        # 转换日期列为 datetime 类型
        df[date_column] = pd.to_datetime(df[date_column], errors="coerce").dt.date

        # 确保用户输入的日期为 Pandas 的 Timestamp 类型
        selected_date = pd.Timestamp(selected_date).date()

        # 筛选出指定日期的数据
        filtered_df = df[df[date_column] == selected_date]

        # 检查目标列是否存在
        if metric_column not in df.columns:
            return None, f"列 '{metric_column}' 不存在，请检查！"

        # 统计目标列的合计值
        total_value = round(filtered_df[metric_column].sum(), 2)

        return filtered_df, total_value
    except Exception as e:
        return None, f"处理数据时出错：{str(e)}"

# 侧边栏
with st.sidebar:
    
     # 文件上传组件
    with st.container(border=True):
        uploaded_file = st.file_uploader("从本地上传Excel", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 读取Excel文件
        df = pd.read_excel(uploaded_file)
        
        with st.container(border=True):
        # 添加多选框，用于选择多个筛选条件
            selected_columns = st.multiselect("请选择筛选条件", df.columns, placeholder="请选择")


# 主页面内容
if uploaded_file is not None:
    
    # 展示数据概览
    with st.container():
        colOne, colTwo, colThree,colFour = st.columns(4)
        colOne.metric("今日销售额", "112", "-8.20%",border=True)
        colTwo.metric("近7天销售额", "438", "10.72%",border=True)
        colThree.metric("总销售额", "9010", "2.33%",border=True)
        colFour.metric("无效订单", "20", "4.43%",border=True)

    # 根据选择的筛选条件进行数据筛选
    if selected_columns:
        # 复制原始数据
        filtered_df = df.copy()

        # 搜索条件
        with st.container(border=True):
            # 增加搜索标题
            st.write(":blue[搜索条件]")

            # 增加列容器，使得每行4列
            col_container = st.columns(4)

            # 遍历筛选条件，在每一行中显示一个筛选条件的选择框和筛选后的结果
            for i, column in enumerate(selected_columns):
                with col_container[i % 4]:
                    # 根据多选框选择的筛选条件，使用selectbox对不同的筛选条件进行筛选
                    selected_value = st.selectbox(f"{column}", filtered_df[column].unique(), placeholder="请选择",index=None)

                    # 根据选择的筛选条件，对数据进行筛选
                    if selected_value is not None:
                        filtered_df = filtered_df[filtered_df[column] == selected_value]
    else:
        filtered_df = df.copy()

    # 展示筛选后的结果
    with st.container(border=True):
        # 展示数据
        st.write(":blue[表格数据]")
        st.data_editor(filtered_df, use_container_width=True)

    # 数据可视化
    with st.container(border=True):
        st.write(":blue[数据可视化]")

        # 图表选项卡
        options = {
            0: "柱状图",
            1: "折线图",
            2: "面积图",
        }

        # 筛选条件布局
        col1, col2 = st.columns([1, 3])

        # 在两个列中分别放置横轴和纵轴的选择框
        with col1:
            # 选择图表类型
            chart_type = st.selectbox("图表类型", list(options.values()))
            x_column = st.selectbox("横轴", filtered_df.columns, index=0, placeholder="请选择")
            y_column = st.selectbox("纵轴", filtered_df.columns, index=2, placeholder="请选择")
        with col2:
            # 判断筛选条件不为空
            if x_column and y_column:
                # 根据选择的图表类型展示图表
                if chart_type == "折线图":
                    st.line_chart(filtered_df.set_index(x_column), y=y_column)
                elif chart_type == "柱状图":
                    st.bar_chart(filtered_df.set_index(x_column), y=y_column)
                elif chart_type == "面积图":
                    st.area_chart(filtered_df.set_index(x_column), y=y_column)

    with st.container(border=True):
        st.write(":blue[AI智能分析]")

        st.write("🤖 我是你的智能AI助理，你可以问我任何问题～")

        # 模拟数据
        _LOREM_IPSUM = """
       
        """

        # 模拟流式数据
        def stream_data():
            for word in _LOREM_IPSUM.split(" "):
                yield word + " "
                # time.sleep(0.1)

            # yield pd.DataFrame(
            #     np.random.randn(5, 10),
            #     columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
            # )

            # for word in _LOREM_IPSUM.split(" "):
            #     yield word + " "
            #     time.sleep(0.1)

        # 聊天框
        if prompt := st.chat_input("请输入问题"):
            messages = st.container()
            messages.chat_message("user").write(prompt)
            messages.chat_message("assistant").write_stream(stream_data)

else:
    #显示网络图片
    st.image("https://images.unsplash.com/photo-1627719172038-611c725920bc?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", width=700)
    st.write("请上传Excel文件")