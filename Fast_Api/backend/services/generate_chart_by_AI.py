# backend/services/generate_chart_by_AI.py
def generate_chart(question: str, results: list):
    """
    根据问题和查询结果生成图表数据
    """
    print(f"Generating chart for question: {question}")
    
    # 检查问题中是否包含柱状图相关关键词
    question_lower = question.lower()
    bar_chart_keywords = ['柱状图', '柱形图', 'bar', 'bar chart', 'bar graph']
    
    if any(keyword in question_lower for keyword in bar_chart_keywords):
        # 生成评分分布的柱状图数据 (9.0~10.0, 8.0~9.0, ..., 0.0~1.0)
        bins = [0] * 10
        labels = [f"{i}.0-{i+1}.0" for i in range(10)]
        
        for movie in results:
            rating = movie.get('rating')
            if rating is not None:
                # 将评分转换为区间索引 (例如 9.6 -> 区间 9, 8.3 -> 区间 8)
                rating_int = int(rating)
                idx = min(rating_int, 9)  # 确保不会超出范围
                bins[idx] += 1
        
        chart_data = {"x": labels, "y": bins}
        print(f"Generated bar chart data: {chart_data}")
        return chart_data
    
    # 如果问题中没有柱状图关键词，返回空数据
    print("No chart keyword found in question")
    return {}