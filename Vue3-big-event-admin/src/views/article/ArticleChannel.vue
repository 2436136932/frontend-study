<script setup>
import { ref } from 'vue'
import { Edit, Delete } from '@element-plus/icons-vue'
import { artGetChannelsService, artDelChannelService } from '../../api/article'
import ChannelEdit from './components/ChannelEdit.vue'
import { ElMessage } from 'element-plus'
import { ElMessageBox } from 'element-plus'
const channelList = ref([])
const loading = ref(false)
const dialog = ref()
// 列表查询参数：分页 + 搜索条件
const params = ref({
  pagenum: 1, // 当前页
  pagesize: 10, // 每页条数
  cate_name: '', // 分类名称（搜索用）
  cate_alias: '', // 分类别名（搜索用）
})

const total = ref(0)
// 全量数据：后端一次返回所有分类，前端自己做搜索 + 切片分页
const fullList = ref([])

const getChannelList = async () => {
  loading.value = true
  const res = await artGetChannelsService({})
  fullList.value = res.data.data

  // 1) 前端按名称 / 别名模糊匹配
  const keyword = params.value.cate_name.trim()
  const alias = params.value.cate_alias.trim()
  const filtered = fullList.value.filter((item) => {
    const matchName = keyword ? item.cate_name.includes(keyword) : true
    const matchAlias = alias ? item.cate_alias.includes(alias) : true
    return matchName && matchAlias
  })

  // 2) 前端切片分页
  total.value = filtered.length
  const start = (params.value.pagenum - 1) * params.value.pagesize
  const end = start + params.value.pagesize
  channelList.value = filtered.slice(start, end)

  loading.value = false
}
getChannelList()

// 搜索：按当前条件重新查，从第 1 页开始
const onSearch = () => {
  params.value.pagenum = 1
  getChannelList()
}

// 重置：清空搜索条件 + 回到第 1 页
const onReset = () => {
  params.value.pagenum = 1
  params.value.cate_name = ''
  params.value.cate_alias = ''
  getChannelList()
}

// 每页条数变化
const onSizeChange = (size) => {
  params.value.pagenum = 1
  params.value.pagesize = size
  getChannelList()
}

// 当前页变化
const onCurrentChange = (page) => {
  params.value.pagenum = page
  getChannelList()
}

const onDelChannel = async (row) => {
  await ElMessageBox.confirm('你确认要删除该分类么', '温馨提示', {
    type: 'warning',
    confirmButtonText: '确认',
    cancelButtonText: '取消',
  })
  await artDelChannelService(row.id)
  ElMessage.success('删除成功')
  getChannelList()
}
const onEditChannel = (row) => {
  dialog.value.open(row)
}
const onAddChannel = () => {
  dialog.value.open({})
}
const onSuccess = () => {
  getChannelList()
}
</script>

<template>
  <page-container title="文章分类">
    <template #extra>
      <el-button @click="onAddChannel">添加分类</el-button>
    </template>

    <el-form inline>
      <el-form-item label="分类名称:">
        <el-input
          v-model="params.cate_name"
          placeholder="请输入分类名称"
          clearable
          style="width: 180px"
        ></el-input>
      </el-form-item>
      <el-form-item label="分类别名:">
        <el-input
          v-model="params.cate_alias"
          placeholder="请输入分类别名"
          clearable
          style="width: 180px"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table v-loading="loading" :data="channelList" style="width: 100%">
      <el-table-column type="index" label="序号" width="100"></el-table-column>
      <el-table-column prop="cate_name" label="分类名称"></el-table-column>
      <el-table-column prop="cate_alias" label="分类别名"></el-table-column>
      <el-table-column label="操作" width="150">
        <!-- row 就是 channelList 的一项， $index 下标 -->
        <template #default="{ row, $index }">
          <el-button
            :icon="Edit"
            circle
            plain
            type="primary"
            @click="onEditChannel(row, $index)"
          ></el-button>
          <el-button
            :icon="Delete"
            circle
            plain
            type="danger"
            @click="onDelChannel(row, $index)"
          ></el-button>
        </template>
      </el-table-column>

      <template #empty>
        <el-empty description="没有数据"></el-empty>
      </template>
    </el-table>

    <!-- 分页区域 -->
    <div class="pagination-wrap">
      <el-pagination
        v-model:current-page="params.pagenum"
        v-model:page-size="params.pagesize"
        :page-sizes="[2, 5, 10, 20]"
        :background="true"
        layout="jumper, total, sizes, prev, pager, next"
        :total="total"
        @size-change="onSizeChange"
        @current-change="onCurrentChange"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </div>

    <channel-edit ref="dialog" @success="onSuccess"></channel-edit>
  </page-container>
</template>

<style lang="scss" scoped>
.pagination-wrap {
  display: flex;
  justify-content: flex-end;
}
</style>
