<!-- src/components/MovieQA.vue -->

<template>
  <!-- <div class="chart-container">
    <h2>📊 评分分布</h2>
    <div ref="ratingChartRef" class="chart"></div>
  </div> -->



  <div class="movie-qa">
    <h2>🎬 豆瓣电影智能问答</h2>
    <p>例如：评分高于9分的日本动画有哪些？</p>

    <div class="input-area">
      <input v-model="question" @keyup.enter="handleSubmit" placeholder="请输入你的问题..." :disabled="loading" />
      <button @click="handleSubmit" :disabled="loading">
        {{ loading ? '思考中...' : '提问' }}
      </button>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error">
      ❌ {{ error }}
    </div>

    <!-- 回答区域 -->
    <div v-if="answer" class="answer">
      <div class="summary">
        <strong>AI 回答：</strong>{{ answer.summary }}
      </div>

      <!-- 可折叠查看 SQL（面试展示用） -->
      <details class="sql-details">
        <summary>🔍 查看生成的 SQL</summary>
        <pre><code>{{ answer.sql }}</code></pre>
      </details>

      <!-- 结果表格 -->
      <div v-if="answer.results && answer.results.length > 0" class="results">
        <table>
          <thead>
            <tr>
              <th>排名</th>
              <th>片名</th>
              <th>评分</th>
              <th>年份</th>
              <th>国家</th>
              <th>导演</th>
              <th>剧情</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="movie in answer.results" :key="movie.rank">
              <td>{{ movie.rank }}</td>
              <td>{{ movie.title }}</td>
              <td>{{ movie.rating }}</td>
              <td>{{ movie.year }}</td>
              <td>{{ movie.country }}</td>
              <td>{{ movie.director }}</td>
              <td>{{ movie.genre }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="answer.results" class="no-results">
        📭 未找到相关电影。
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const question = ref('')
const answer = ref(null)
const loading = ref(false)
const error = ref(null)

const ratingChartRef = ref(null)
let ratingChartInst = null

// 窗口大小变化处理
const handleResize = () => {
  ratingChartInst?.resize()
}

// 清理图表实例
onBeforeUnmount(() => {
  if (ratingChartInst) ratingChartInst.dispose()

  window.removeEventListener('resize', handleResize)
})

// 初始化评分分布图
const initRatingChart = async (data) => {
  await nextTick()
  const container = ratingChartRef.value
  if (!container || !data) return

  // 检查容器是否具有有效宽度
  if (container.clientWidth <= 0) {
    console.warn('评分图表容器宽度为 0，延迟初始化...')
    setTimeout(() => initRatingChart(data), 100)
    return
  }

  if (ratingChartInst) ratingChartInst.dispose()
  ratingChartInst = echarts.init(container)
  ratingChartInst.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: data.x },
    yAxis: { type: 'value', name: '电影数量' },
    series: [{ type: 'bar', data: data.y, itemStyle: { color: '#5470c6' } }]
  })
}


// 获取评分分布
const fetchRatingData = (data) => {
  try {
    initRatingChart(data)
  } catch (e) {
    console.error('评分数据加载失败', e)
  } finally {
  }
}

// 初始化
onMounted(() => {
  // fetchRatingData()
  window.addEventListener('resize', handleResize)

})



const handleSubmit = async () => {
  const q = question.value.trim()
  if (!q) return

  // 重置状态
  answer.value = null
  error.value = null
  loading.value = true

  try {
    // 调用你的 FastAPI 后端
    const response = await fetch('http://localhost:8000/api/v1/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question: q })
    })

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}))
      throw new Error(errData.detail || '请求失败')
    }

    const data = await response.json()
    answer.value = data
    fetchRatingData(answer.value.chart_data)
    console.log(answer.value);

  } catch (err) {
    console.error('提问失败:', err)
    error.value = err.message || '网络错误，请检查后端是否运行'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
  .chart {
  width: 100%;
  height: 400px;
}
.chart-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  padding: 20px;
}

.movie-qa {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1.5rem;
  font-family: Arial, sans-serif;
}

.input-area {
  display: flex;
  gap: 10px;
  margin: 1rem 0;
}

.input-area input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.input-area button {
  padding: 10px 20px;
  font-size: 16px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-area button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  color: #f56565;
  margin: 1rem 0;
}

.summary {
  background: #f0f9ff;
  padding: 12px;
  border-left: 4px solid #409eff;
  margin: 1rem 0;
}

.sql-details summary {
  cursor: pointer;
  color: #666;
  margin: 1rem 0;
}

.results table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.results th,
.results td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.results th {
  background-color: #f5f5f5;
}

.no-results {
  text-align: center;
  color: #888;
  margin-top: 1rem;
}
</style>