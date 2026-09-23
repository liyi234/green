import streamlit as st
import pandas as pd

st.set_page_config(page_title="绿色物流数字化协同平台", layout="wide")

st.title("🚚 绿色物流数字化协同平台")

# 读取 Excel（不使用缓存）
df_orders = pd.read_excel('data.xlsx', sheet_name='外卖订单')
df_vending = pd.read_excel('data.xlsx', sheet_name='贩卖机')
df_vehicles = pd.read_excel('data.xlsx', sheet_name='车辆')
df_package = pd.read_excel('data.xlsx', sheet_name='包装')
df_carbon = pd.read_excel('data.xlsx', sheet_name='碳排放')

# 6个标签页
tab_order, tab_vending, tab_vehicle, tab_package, tab_carbon = st.tabs(
    ["📦 外卖订单", "🏪 贩卖机补货", "🚛 车辆管理", "♻ 包装管理", "🌱 碳管理"]
)

# ===================== 外卖订单 =====================
with tab_order:
    st.subheader("外卖订单列表")
    st.dataframe(df_orders, use_container_width=True, hide_index=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 订单分区", use_container_width=True, type="primary"):
            st.toast("外卖订单分区完成", icon="📊")
    with c2:
        if st.button("🔗 订单合并", use_container_width=True):
            st.toast("外卖订单合并完成", icon="🔗")

# ===================== 贩卖机补货 =====================
with tab_vending:
    st.subheader("自动贩卖机补货看板")
    
    # 筛选器
    filter_option = st.selectbox("筛选状态", ["全部", "仅看需补货"])
    
    if filter_option == "仅看需补货":
        # 筛选补货状态为“需补货”的记录
        display_df = df_vending[df_vending['补货状态'] == '需补货']
    else:
        display_df = df_vending
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    if st.button("🚚 生成补货任务", use_container_width=True, type="primary"):
        st.toast("补货任务已生成", icon="✅")

# ===================== 车辆管理 =====================
with tab_vehicle:
    st.subheader("车辆列表")
    st.dataframe(df_vehicles, use_container_width=True, hide_index=True)

    st.write("")
    if st.button("📋 任务分配", use_container_width=True, type="primary"):
        st.toast("任务分配完成", icon="✅")

# ===================== 包装管理 =====================
with tab_package:
    st.subheader("包装回收记录")
    st.dataframe(df_package, use_container_width=True, hide_index=True)

# ===================== 碳管理 =====================
with tab_carbon:
    st.subheader("碳管理看板")

    # 取最后一行数据
    last_row = df_carbon.iloc[-1]

    # 动态匹配列名（容错处理）
    energy_col = next((c for c in df_carbon.columns if '能耗' in c), None)
    emission_col = next((c for c in df_carbon.columns if '碳排放' in c), None)
    reduction_col = next((c for c in df_carbon.columns if '减排' in c), None)

    # 三个核心指标
    m1, m2, m3 = st.columns(3)
    
    if energy_col:
        m1.metric("今日能耗", str(last_row[energy_col]))
    else:
        m1.metric("今日能耗", "-")

    if emission_col:
        m2.metric("碳排放", str(last_row[emission_col]))
    else:
        m2.metric("碳排放", "-")

    if reduction_col:
        m3.metric("减排量", str(last_row[reduction_col]))
    else:
        m3.metric("减排量", "-")

    # 碳排放图表
    if emission_col and reduction_col:
        st.write("#### 减排对比图")
        chart_data = df_carbon[[emission_col, reduction_col]].copy()
        chart_data.columns = ['碳排放量', '减排量']
        st.bar_chart(chart_data)
    else:
        st.warning("碳排工作表缺少碳排放或减排量列，无法绘制图表")