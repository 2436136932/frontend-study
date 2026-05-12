<template>
  <div class="dashboard">
    <div class="stat-cards">
      <div class="stat-card" v-for="card in statCards" :key="card.title">
        <div class="stat-icon" :style="{ background: card.bg }">
          <el-icon :size="28"><component :is="card.icon" /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ card.value }}</div>
          <div class="stat-title">{{ card.title }}</div>
        </div>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <span class="chart-title">近7日访问趋势</span>
          </template>
          <div ref="lineChartRef" class="chart-box"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <span class="chart-title">用户分布</span>
          </template>
          <div ref="pieChartRef" class="chart-box"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { User, ShoppingCart, Money, View } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const statCards = [
  { title: '用户总数', value: '1,286', icon: User, bg: '#409EFF' },
  { title: '订单数量', value: '568', icon: ShoppingCart, bg: '#67C23A' },
  { title: '本月营收', value: '¥32,580', icon: Money, bg: '#E6A23C' },
  { title: '访问量', value: '12,426', icon: View, bg: '#F56C6C' }
]

const lineChartRef = ref(null)
const pieChartRef = ref(null)
let lineChart = null
let pieChart = null

onMounted(() => {
  lineChart = echarts.init(lineChartRef.value)
  lineChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
    yAxis: { type: 'value' },
    series: [{
      data: [820, 932, 901, 1290, 1330, 1520, 1620],
      type: 'line',
      smooth: true,
      areaStyle: { color: 'rgba(64,158,255,0.15)' },
      itemStyle: { color: '#409EFF' }
    }]
  })

  pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '45%'],
      data: [
        { value: 435, name: '合肥' },
        { value: 310, name: '南京' },
        { value: 234, name: '上海' },
        { value: 178, name: '杭州' },
        { value: 129, name: '其他' }
      ]
    }]
  })

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  lineChart?.dispose()
  pieChart?.dispose()
})

const handleResize = () => {
  lineChart?.resize()
  pieChart?.resize()
}
</script>

<style scoped>
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}
.stat-title {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
.chart-card {
  margin-bottom: 20px;
}
.chart-title {
  font-weight: 600;
  font-size: 16px;
}
.chart-box {
  width: 100%;
  height: 320px;
}
</style>
