<template>
  <el-container class="main-container">
    <el-container>
      <NavBar></NavBar>
      <el-main class="main-content">
        <div class="content-header">
          <h2 class="page-title">豆瓣 Top250 电影列表</h2>
        </div>

        <div class="table-container">
          <el-table :data="currentPageData" stripe style="width: 100%" class="movie-table"
            :header-cell-style="{ background: '#f5f7fa', color: '#606266' }" @sort-change="handleSort">
            <el-table-column prop="rank" label="排名" width="80" sortable>
              <template #default="{ row }">
                <div class="rank-cell">
                  <span :class="getRankClass(row.rank)">{{ row.rank }}</span>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="title" label="名称" width="220" sortable>
              <template #default="{ row }">
                <div class="title-cell">
                  <span class="movie-title">{{ row.title }}</span>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="rating" label="评分" width="200" sortable>
              <template #default="{ row }">
                <el-rate :model-value="parseFloat(row.rating/2)"
                  disabled
                  show-score
                  text-color="#ff9900"
                  :max="5"
                  :allow-half="true"
                  size="small"
                  ></el-rate>
              </template>
            </el-table-column>

            <el-table-column prop="year" label="年份" width="100" sortable />

            <el-table-column prop="country" label="国家" width="150" />

            <el-table-column prop="director" label="导演" />

            <el-table-column prop="genre" label="剧情" width="150" />

            <el-table-column align="right">
              <template #header>
                <el-input v-model="search" size="small" placeholder="搜索电影..." />
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 分页组件 -->
        <div class="pagination-wrapper">
          <el-pagination 
            @size-change="handleSizeChange" 
            @current-change="handleCurrentChange"
            :current-page="currentPage" 
            :page-sizes="[10, 20, 50, 100]" 
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper" 
            :total="filteredData.length">
          </el-pagination>
        </div>
      </el-main>

      <el-footer class="footer">
        <div class="footer-content">
          <p>豆瓣 Top250 电影列表 © 2023</p>
        </div>
      </el-footer>
    </el-container>
  </el-container>
  <AIAssistant></AIAssistant>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue';
import AIAssistant from '@/components/AIAssistant.vue';
import { useAIStore } from '@/stores/store';
import { onMounted, ref, reactive, computed, watch } from 'vue';

const aiStore = useAIStore();

// 分页相关数据
const allData = ref([]) // 存储所有数据
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')
const sortConfig = reactive({
  prop: '',
  order: ''  // 'ascending' or 'descending'
})

// 获取排名样式
const getRankClass = (rank) => {
  if (rank <= 3) return 'top-rank'
  return 'normal-rank'
}

// 获取所有数据
let getAllData = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/getlist?page=1&size=1000', { // 获取所有数据
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}))
      throw new Error(errData.detail || '请求失败')
    }

    const data = await response.json()
    allData.value = data.results || data // 根据实际返回的数据结构调整
    console.log('获取到的数据:', data)
  } catch (e) {
    console.log(e)
  }
}

// 计算过滤后的数据
const filteredData = computed(() => {
  let result = allData.value
  
  // 搜索过滤
  if (searchQuery.value) {
    result = result.filter(
      (data) =>
        data.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        data.director.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        data.country.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        data.genre.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  // 排序
  if (sortConfig.prop && sortConfig.order) {
    result = [...result].sort((a, b) => {
      let valA = a[sortConfig.prop]
      let valB = b[sortConfig.prop]
      
      // 处理数字类型排序
      if (!isNaN(valA) && !isNaN(valB)) {
        valA = Number(valA)
        valB = Number(valB)
      }
      
      // 处理字符串类型排序
      if (typeof valA === 'string' && typeof valB === 'string') {
        valA = valA.toLowerCase()
        valB = valB.toLowerCase()
      }
      
      if (sortConfig.order === 'asc') {
        return valA > valB ? 1 : -1
      } else {
        return valA < valB ? 1 : -1
      }
    })
  }
  
  return result
})

// 当前页面显示的数据
const currentPageData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredData.value.slice(start, end)
})

// 分页大小改变时触发
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

// 当前页改变时触发
const handleCurrentChange = (page) => {
  currentPage.value = page
}

// 排序功能
const handleSort = ({ column, prop, order }) => {
  sortConfig.prop = prop
  sortConfig.order = order === 'ascending' ? 'asc' : order === 'descending' ? 'desc' : ''
}

// 搜索功能
const search = ref('')
watch(search, (newVal) => {
  searchQuery.value = newVal
  currentPage.value = 1 // 搜索时重置到第一页
})

// 监听 Pinia Store 中的 moviesData 变化
watch(() => aiStore.moviesData, (newData) => {
  console.log('AI 助手数据更新:', newData);
  if (newData && Array.isArray(newData) && newData.length > 0) {
    // 如果 AI 返回了数据，使用 AI 的数据作为 allData
    allData.value = newData;
  } else {
    // 否则重新获取原始数据
    getAllData();
  }
}, { deep: true });

onMounted(() => {
  getAllData()
})
</script>

<style scoped>
.main-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
}

.main-content {
  padding: 20px;
  padding-bottom: 0;
}

.content-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.page-title {
  line-height: 1;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.movie-table {
  border-radius: 8px;
}

.movie-table :deep(.el-table__row) {
  transition: background-color 0.3s;
}

.movie-table :deep(.el-table__row:hover) {
  background-color: #f8f9ff;
}

.rank-cell {
  display: flex;
  align-items: center;
  justify-content: center;
}

.top-rank {
  font-weight: bold;
  font-size: 16px;
  color: #e74c3c;
  background: linear-gradient(45deg, #ff9a9e, #fad0c4);
  padding: 2px 8px;
  border-radius: 12px;
  min-width: 30px;
}

.normal-rank {
  font-weight: bold;
  font-size: 14px;
  color: #3498db;
}

.title-cell {
  display: flex;
  align-items: center;
}

.movie-title {
  font-weight: 500;
  color: #2c3e50;
  transition: color 0.3s;
}

.movie-title:hover {
  color: #3498db;
  cursor: pointer;
}

.pagination-wrapper {
  line-height: 4;
  display: flex;
  justify-content: center;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-top: 20px;
  padding: 15px;
}

.footer {
  background-color: #f5f5f5;
  text-align: center;
}

.footer-content p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .search-input {
    width: 100%;
  }

  .page-title {
    font-size: 20px;
  }
}
</style>