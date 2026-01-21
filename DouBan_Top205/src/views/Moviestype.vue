<template>
  <el-container>
    <el-container>
      <NavBar></NavBar>

      <el-main>
        <div>
          <p style="line-height: 10px;font-size: 30px;font-weight: 600;">电影数据分析</p>
          <p style="line-height: 10px;font-size: 20px;">对电影的类型进行数据分析</p>
        </div>
        <div>
          <el-tabs type="border-card">
            <!-- 剧情分类 -->
            <el-tab-pane label="剧情">
              <el-space wrap style="justify-content:space-evenly">
                <el-card v-for="item in paginatedPlot" :key="item.rank" class="box-card" style="width: 250px;">
                  <el-image style="height: 300px" :src="ImgSrc(item)" alt="" />
                  <p style="margin-top: -120px;font-weight: 500;">
                    <a :href="item.link" target="_blank" style="text-decoration: none;">{{ item.title }}</a>
                  </p>
                </el-card>
              </el-space>
              <div style="display: flex;justify-content: center;text-align: center; margin-top: 20px;">
                <el-pagination @size-change="handlePlotSizeChange" @current-change="handlePlotCurrentChange"
                  :current-page="plotCurrentPage" :page-sizes="[5, 10, 18, 24]" :page-size="plotPageSize"
                  layout="total, sizes, prev, pager, next, jumper" :total="Plot.length">
                </el-pagination>
              </div>
            </el-tab-pane>

            <!-- 动作分类 -->
            <el-tab-pane label="动作">
              <el-space wrap style="justify-content:space-evenly">
                <el-card v-for="item in paginatedAction" :key="item.rank" class="box-card" style="width: 250px;">
                  <el-image style="height: 300px" :src="ImgSrc(item)" alt="" />
                  <p style="margin-top: -120px;font-weight: 500;">
                    <a :href="item.link" target="_blank" style="text-decoration: none;">{{ item.title }}</a>

                  </p>
                </el-card>
              </el-space>
              <div style="display: flex;justify-content: center;text-align: center; margin-top: 20px;">
                <el-pagination @size-change="handleActionSizeChange" @current-change="handleActionCurrentChange"
                  :current-page="actionCurrentPage" :page-sizes="[5, 10, 18, 24]" :page-size="actionPageSize"
                  layout="total, sizes, prev, pager, next, jumper" :total="Action.length">
                </el-pagination>
              </div>
            </el-tab-pane>

            <!-- 冒险分类 -->
            <el-tab-pane label="冒险">
              <el-space wrap style="justify-content:space-evenly">
                <el-card v-for="item in paginatedAdventure" :key="item.rank" class="box-card" style="width: 250px;">
                  <el-image style="height: 300px" :src="ImgSrc(item)" alt="" />
                  <p style="margin-top: -120px;font-weight: 500;">
                    <a :href="item.link" target="_blank" style="text-decoration: none;">{{ item.title }}</a>

                  </p>
                </el-card>
              </el-space>
              <div style="display: flex;justify-content: center;text-align: center; margin-top: 20px;">
                <el-pagination @size-change="handleAdventureSizeChange" @current-change="handleAdventureCurrentChange"
                  :current-page="adventureCurrentPage" :page-sizes="[5, 10, 18, 24]" :page-size="adventurePageSize"
                  layout="total, sizes, prev, pager, next, jumper" :total="Adventure.length">
                </el-pagination>
              </div>
            </el-tab-pane>

            <!-- 爱情分类 -->
            <el-tab-pane label="爱情">
              <el-space wrap style="justify-content:space-evenly">
                <el-card v-for="item in paginatedLove" :key="item.rank" class="box-card" style="width: 250px;">
                  <el-image style="height: 300px" :src="ImgSrc(item)" alt="" />
                  <p style="margin-top: -120px;font-weight: 500;">
                    <a :href="item.link" target="_blank" style="text-decoration: none;">{{ item.title }}</a>

                  </p>
                </el-card>
              </el-space>
              <div style="display: flex;justify-content: center;text-align: center; margin-top: 20px;">
                <el-pagination @size-change="handleLoveSizeChange" @current-change="handleLoveCurrentChange"
                  :current-page="loveCurrentPage" :page-sizes="[5, 10, 18, 24]" :page-size="lovePageSize"
                  layout="total, sizes, prev, pager, next, jumper" :total="Love.length">
                </el-pagination>
              </div>
            </el-tab-pane>


            <!-- 自定义分类 -->
            <el-tab-pane label="自定义">
              <el-space wrap style="justify-content:space-evenly">
                <el-card v-for="item in paginatedCustome" :key="item.rank" class="box-card" style="width: 250px;">
                  <el-image style="height: 300px" :src="ImgSrc(item)" alt="" />
                  <p style="margin-top: -120px;font-weight: 500;">
                    <a :href="item.link" target="_blank" style="text-decoration: none;">{{ item.title }}</a>

                  </p>
                </el-card>
              </el-space>
              <div style="display: flex;justify-content: center;text-align: center; margin-top: 20px;">
                <el-pagination @size-change="handleCustomSizeChange" @current-change="handleCustomCurrentChange"
                  :current-page="customCurrentPage" :page-sizes="[5, 10, 18, 24]" :page-size="customPageSize"
                  layout="total, sizes, prev, pager, next, jumper" :total="customData.length">
                </el-pagination>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-main>
      <el-footer>底部</el-footer>
    </el-container>
  </el-container>
  <AIAssistant></AIAssistant>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue';
import AIAssistant from '@/components/AIAssistant.vue';
import { useAIStore } from '@/stores/store.js';
import { ref, onMounted, computed, watch } from 'vue';
const store = useAIStore();
let data = ref([]);
let customData = ref([]);

// 分页状态 - 剧情
const plotCurrentPage = ref(1);
const plotPageSize = ref(10);

// 分页状态 - 动作
const actionCurrentPage = ref(1);
const actionPageSize = ref(10);

// 分页状态 - 冒险
const adventureCurrentPage = ref(1);
const adventurePageSize = ref(10);

// 分页状态 - 爱情
const loveCurrentPage = ref(1);
const lovePageSize = ref(10);

// 分页状态 - 自定义
const customCurrentPage = ref(1);
const customPageSize = ref(10);

// 计算分类数据
let Plot = computed(() => {
  return data.value.filter(item => item.genre.includes('剧情'))
});
let Action = computed(() => {
  return data.value.filter(item => item.genre.includes('动作'))
});
let Adventure = computed(() => {
  return data.value.filter(item => item.genre.includes('冒险'))
});
let Love = computed(() => {
  return data.value.filter(item => item.genre.includes('爱情'))
});

// 计算分页后的数据
const paginatedPlot = computed(() => {
  const start = (plotCurrentPage.value - 1) * plotPageSize.value;
  const end = start + plotPageSize.value;
  return Plot.value.slice(start, end);
});

const paginatedAction = computed(() => {
  const start = (actionCurrentPage.value - 1) * actionPageSize.value;
  const end = start + actionPageSize.value;
  return Action.value.slice(start, end);
});

const paginatedAdventure = computed(() => {
  const start = (adventureCurrentPage.value - 1) * adventurePageSize.value;
  const end = start + adventurePageSize.value;
  return Adventure.value.slice(start, end);
});

const paginatedLove = computed(() => {
  const start = (loveCurrentPage.value - 1) * lovePageSize.value;
  const end = start + lovePageSize.value;
  return Love.value.slice(start, end);
});
const paginatedCustome = computed(() => {
  const start = (customCurrentPage.value - 1) * customPageSize.value;
  const end = start + customPageSize.value;
  return customData.value.slice(start, end);
});

// 剧情分页事件处理
const handlePlotSizeChange = (size) => {
  plotPageSize.value = size;
  plotCurrentPage.value = 1; // 重置到第一页
};

const handlePlotCurrentChange = (page) => {
  plotCurrentPage.value = page;
};

// 动作分页事件处理
const handleActionSizeChange = (size) => {
  actionPageSize.value = size;
  actionCurrentPage.value = 1;
};

const handleActionCurrentChange = (page) => {
  actionCurrentPage.value = page;
};

// 冒险分页事件处理
const handleAdventureSizeChange = (size) => {
  adventurePageSize.value = size;
  adventureCurrentPage.value = 1;
};

const handleAdventureCurrentChange = (page) => {
  adventureCurrentPage.value = page;
};

// 爱情分页事件处理
const handleLoveSizeChange = (size) => {
  lovePageSize.value = size;
  loveCurrentPage.value = 1;
};
const handleLoveCurrentChange = (page) => {
  loveCurrentPage.value = page;
};

// 自定义分页事件处理
const handleCustomSizeChange = (size) => {
  lovePageSize.value = size;
  loveCurrentPage.value = 1;
};
const handleCustomCurrentChange = (page) => {
  customCurrentPage.value = page;
};

const ImgSrc = (item) => {
  let rank = String(item.rank).padStart(3, '0');
  // 使用 URL 方式处理模块资源
  try {
    return new URL(`../assets/moviesImg/${rank}_${item.title}.jpg`, import.meta.url).href;
  } catch (e) {
    // 如果图片不存在，返回默认图片
    return new URL('../assets/default-movie.jpg', import.meta.url).href;
  }
};

// 监听 Pinia Store 中的 moviesData 变化
watch(() => store.customData, (newData) => {
  // console.log('AI 助手数据更新:', newData);
  if (newData && Array.isArray(newData) && newData.length > 0) {
    // 如果 AI 返回了数据，使用 AI 的数据作为 allData
    customData.value = newData;
  }
}, { deep: true });

onMounted(async () => {

  if (!store.moviesData.length) {
    await store.getAllData();
  }
  data.value = store.moviesData;
  customData.value = store.customData;
  console.log(store.moviesData);
});
</script>

<style></style>