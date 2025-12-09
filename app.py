"启动streamlit run app.py"
import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import json
import random
from typing import Dict, List, Tuple


class MathAIAssistant:
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
        self.problems = self.load_problems()

    def load_knowledge_base(self) -> Dict:
        """加载数学知识库"""
        try:
            with open('knowledge_base.md', 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content}
        except:
            return {"content": "默认知识库"}

    def load_problems(self) -> List[Dict]:
        """加载数学题目"""
        try:
            with open('math_problems.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def solve_derivative(self, expression: str, variable: str = 'x') -> str:
        """求解导数"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            derivative = sp.diff(expr, x)
            return f"函数 f({variable}) = {expression} 的导数为：\n\nf'({variable}) = {derivative}"
        except Exception as e:
            return f"求解导数时出错：{e}"

    def solve_integral(self, expression: str, variable: str = 'x') -> str:
        """求解积分"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            integral = sp.integrate(expr, x)
            return f"函数 f({variable}) = {expression} 的不定积分为：\n\n∫f({variable})d{variable} = {integral} + C"
        except Exception as e:
            return f"求解积分时出错：{e}"

    def plot_function(self, expression: str, variable: str = 'x', x_range: Tuple = (-10, 10)):
        """绘制函数图像"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            f = sp.lambdify(x, expr, 'numpy')

            x_vals = np.linspace(x_range[0], x_range[1], 400)
            y_vals = f(x_vals)

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f({variable}) = {expression}')
            ax.set_xlabel(variable, fontsize=12)
            ax.set_ylabel(f'f({variable})', fontsize=12)
            ax.set_title(f'函数图像: f({variable}) = {expression}', fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend()

            return fig
        except Exception as e:
            st.error(f"绘制图像时出错：{e}")
            return None

    def generate_problem(self, difficulty: str = 'easy') -> Dict:
        """生成数学题目"""
        problems = [p for p in self.problems if p['difficulty'] == difficulty]
        if problems:
            return random.choice(problems)
        else:
            return {
                "question": "计算函数 f(x) = x² 在 x=2 处的导数",
                "answer": "4",
                "solution": "使用幂函数求导法则：d/dx(xⁿ) = n*xⁿ⁻¹"
            }


def main():
    st.set_page_config(
        page_title="AI数学学习助手",
        page_icon="🧮",
        layout="wide"
    )

    st.title("🧮 AI工具在数学学习中的应用")
    st.markdown("---")

    # 初始化AI助手
    if 'assistant' not in st.session_state:
        st.session_state.assistant = MathAIAssistant()

    assistant = st.session_state.assistant

    # 侧边栏
    st.sidebar.title("功能导航")
    app_mode = st.sidebar.selectbox(
        "选择功能",
        ["首页", "导数计算", "积分计算", "函数绘图", "题目练习", "知识库"]
    )

    if app_mode == "首页":
        st.header("欢迎使用AI数学学习助手")
        st.markdown("""
        ### 🌟 功能特色

        - **智能计算**：自动求解导数、积分等数学问题
        - **可视化学习**：动态绘制函数图像
        - **个性化练习**：根据难度生成练习题
        - **知识库支持**：丰富的数学知识资源

        ### 🚀 快速开始

        1. 选择左侧导航栏的功能
        2. 输入数学表达式
        3. 获取详细的解题步骤
        4. 通过可视化加深理解
        """)

    elif app_mode == "导数计算":
        st.header("📈 导数计算器")
        col1, col2 = st.columns([2, 1])

        with col1:
            expression = st.text_input("输入函数表达式", "x**2 + 3*x + 1")
            variable = st.text_input("变量", "x")

            if st.button("计算导数"):
                if expression:
                    result = assistant.solve_derivative(expression, variable)
                    st.success("计算完成！")
                    st.code(result, language='latex')

        with col2:
            st.markdown("### 💡 示例")
            st.markdown("""
            - `x**2` → 2x
            - `sin(x)` → cos(x)
            - `exp(x)` → exp(x)
            - `log(x)` → 1/x
            """)

    elif app_mode == "积分计算":
        st.header("📊 积分计算器")
        col1, col2 = st.columns([2, 1])

        with col1:
            expression = st.text_input("输入函数表达式", "2*x + 1", key="integral_expr")
            variable = st.text_input("变量", "x", key="integral_var")

            if st.button("计算积分"):
                if expression:
                    result = assistant.solve_integral(expression, variable)
                    st.success("计算完成！")
                    st.code(result, language='latex')

        with col2:
            st.markdown("### 💡 示例")
            st.markdown("""
            - `2*x` → x²
            - `cos(x)` → sin(x)
            - `1/x` → log|x|
            - `exp(x)` → exp(x)
            """)

    elif app_mode == "函数绘图":
        st.header("📊 函数图像绘制")

        col1, col2 = st.columns([1, 2])

        with col1:
            expression = st.text_input("输入函数表达式", "sin(x)", key="plot_expr")
            variable = st.text_input("变量", "x", key="plot_var")
            x_min = st.number_input("x最小值", value=-10.0)
            x_max = st.number_input("x最大值", value=10.0)

            if st.button("绘制图像"):
                if expression:
                    fig = assistant.plot_function(expression, variable, (x_min, x_max))
                    if fig:
                        st.pyplot(fig)

        with col2:
            st.markdown("### 📈 绘图示例")
            st.markdown("""
            **常用函数：**
            - 多项式：`x**2 - 4*x + 4`
            - 三角函数：`sin(x)`, `cos(2*x)`
            - 指数函数：`exp(x)`, `2**x`
            - 对数函数：`log(x)`
            """)

    elif app_mode == "题目练习":
        st.header("🎯 数学题目练习")

        difficulty = st.selectbox("选择难度", ["easy", "medium", "hard"])

        if 'current_problem' not in st.session_state:
            st.session_state.current_problem = assistant.generate_problem(difficulty)

        problem = st.session_state.current_problem

        st.subheader("题目：")
        st.info(problem['question'])

        user_answer = st.text_input("你的答案：")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("提交答案"):
                if user_answer.strip() == problem['answer']:
                    st.success("✅ 回答正确！")
                else:
                    st.error("❌ 回答错误，请再试一次")

        with col2:
            if st.button("显示解析"):
                st.markdown(f"**正确答案：** {problem['answer']}")
                st.markdown(f"**解题步骤：** {problem['solution']}")

        if st.button("下一题"):
            st.session_state.current_problem = assistant.generate_problem(difficulty)
            st.rerun()

    elif app_mode == "知识库":
        st.header("📚 数学知识库")

        st.markdown(assistant.knowledge_base["content"])

        # 添加搜索功能
        search_term = st.text_input("搜索知识点")
        if search_term:
            st.info(f"搜索关键词: {search_term}")
            # 这里可以添加实际的搜索逻辑


if __name__ == "__main__":
    main()