<template>
  <div class="dashboard">
    <h1>🎬 豆瓣电影数据可视化</h1>

    <div class="chart-container">
      <h2>📊 评分分布</h2>
      <div v-show="loading.rating" class="chart-loading">
        <Loading />
      </div>
      <div v-show="!loading.rating" ref="ratingChartRef" class="chart"></div>
    </div>

    <div class="chart-container">
      <h2>🥧 类型分布（Top 10）</h2>
      <div v-show="loading.genre" class="chart-loading">
        <Loading />
      </div>
      <div v-show="!loading.genre" ref="genreChartRef" class="chart"></div>
    </div>

    <div class="chart-container">
      <h2>📈 上映年份趋势</h2>
      <div v-show="loading.year" class="chart-loading">
        <Loading />
      </div>
      <div v-show="!loading.year" ref="yearChartRef" class="chart"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import Loading from '@/components/Loading.vue'

// DOM 引用
const ratingChartRef = ref(null)
const genreChartRef = ref(null)
const yearChartRef = ref(null)

// ECharts 实例引用（用于 dispose 和 resize）
let ratingChartInst = null
let genreChartInst = null
let yearChartInst = null

// 加载状态
const loading = ref({
  rating: true,
  genre: true,
  year: true
})

// 清理图表实例
onBeforeUnmount(() => {
  if (ratingChartInst) ratingChartInst.dispose()
  if (genreChartInst) genreChartInst.dispose()
  if (yearChartInst) yearChartInst.dispose()

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

// 初始化类型分布图
const initGenreChart = async (genres, counts) => {
  await nextTick()
  const container = genreChartRef.value
  if (!container || !genres) return

  if (container.clientWidth <= 0) {
    setTimeout(() => initGenreChart(genres, counts), 100)
    return
  }

  if (genreChartInst) genreChartInst.dispose()
  genreChartInst = echarts.init(container)
  genreChartInst.setOption({
    tooltip: { trigger: 'item' },
    legend: { top: '5%' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 16 }
      },
      data: genres.map((name, i) => ({ name, value: counts[i] }))
    }]
  })
}

// 初始化年份趋势图
const initYearChart = async (years, counts) => {
  await nextTick()
  const container = yearChartRef.value
  if (!container || !years) return

  if (container.clientWidth <= 0) {
    setTimeout(() => initYearChart(years, counts), 100)
    return
  }

  if (yearChartInst) yearChartInst.dispose()
  yearChartInst = echarts.init(container)
  yearChartInst.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: years },
    yAxis: { type: 'value', name: '电影数量' },
    series: [{ type: 'line', data: counts, smooth: true, areaStyle: {} }]
  })
}

// 获取评分分布
const fetchRatingData = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/chart/rating-distribution')
    initRatingChart(res.data)
  } catch (e) {
    console.error('评分数据加载失败', e)
  } finally {
    loading.value.rating = false
  }
}

// 获取类型分布
const fetchGenreData = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/chart/genre-count')
    initGenreChart(res.data.genres, res.data.counts)
  } catch (e) {
    console.error('类型数据加载失败', e)
  } finally {
    loading.value.genre = false
  }
}

// 获取年份趋势
const fetchYearData = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/chart/year-trend')
    initYearChart(res.data.years, res.data.counts)
  } catch (e) {
    console.error('年份数据加载失败', e)
  } finally {
    loading.value.year = false
  }
}

// 窗口大小变化处理
const handleResize = () => {
  ratingChartInst?.resize()
  genreChartInst?.resize()
  yearChartInst?.resize()
}

// 初始化
onMounted(() => {
  fetchRatingData()
  fetchGenreData()
  fetchYearData()

  window.addEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.chart-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  padding: 20px;
}

h2 {
  margin-top: 0;
  color: #444;
}

.chart {
  width: 100%;
  height: 400px;
}

.chart-loading {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>