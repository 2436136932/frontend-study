<template>
  <div class="user-page">
    <el-card>
      <div class="toolbar">
        <el-input v-model="searchKeyword" placeholder="搜索用户名" clearable class="search-input" @keyup.enter="handleSearch">
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" :icon="Plus" @click="openDialog()">新增用户</el-button>
      </div>

      <el-table :data="tableData" stripe border style="width: 100%; margin-top: 16px">
        <el-table-column type="index" label="#" width="60" align="center" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="realName" label="姓名" min-width="100" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="phone" label="手机号" min-width="140" />
        <el-table-column prop="role" label="角色" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="row.role === '管理员' ? 'danger' : ''" size="small">{{ row.role }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        background
        class="pagination"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新增用户'" width="520px" @close="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="姓名" prop="realName">
          <el-input v-model="form.realName" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="管理员" value="管理员" />
            <el-option label="普通用户" value="普通用户" />
            <el-option label="编辑" value="编辑" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const searchKeyword = ref('')
const tableData = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
let editId = null

const form = reactive({
  username: '',
  realName: '',
  email: '',
  phone: '',
  role: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  realName: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }],
  phone: [{ pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const mockUsers = [
  { id: 1, username: 'admin', realName: '系统管理员', email: 'admin@example.com', phone: '13800000001', role: '管理员', createTime: '2025-01-15' },
  { id: 2, username: 'zhangsan', realName: '张三', email: 'zhangsan@example.com', phone: '13800000002', role: '普通用户', createTime: '2025-03-20' },
  { id: 3, username: 'lisi', realName: '李四', email: 'lisi@example.com', phone: '13800000003', role: '编辑', createTime: '2025-04-10' },
  { id: 4, username: 'wangwu', realName: '王五', email: 'wangwu@example.com', phone: '13800000004', role: '普通用户', createTime: '2025-06-05' },
  { id: 5, username: 'zhaoliu', realName: '赵六', email: 'zhaoliu@example.com', phone: '13800000005', role: '普通用户', createTime: '2025-08-12' },
  { id: 6, username: 'sunqi', realName: '孙七', email: 'sunqi@example.com', phone: '13800000006', role: '编辑', createTime: '2025-09-01' },
  { id: 7, username: 'zhouba', realName: '周八', email: 'zhouba@example.com', phone: '13800000007', role: '普通用户', createTime: '2025-10-15' },
  { id: 8, username: 'wujiu', realName: '吴九', email: 'wujiu@example.com', phone: '13800000008', role: '管理员', createTime: '2025-11-20' },
]

const fetchData = () => {
  let list = [...mockUsers]
  if (searchKeyword.value) {
    list = list.filter(u => u.username.includes(searchKeyword.value))
  }
  total.value = list.length
  const start = (currentPage.value - 1) * pageSize.value
  tableData.value = list.slice(start, start + pageSize.value)
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const openDialog = (row = null) => {
  if (row) {
    isEdit.value = true
    editId = row.id
    Object.assign(form, { ...row })
  } else {
    isEdit.value = false
    editId = null
    resetForm()
  }
  dialogVisible.value = true
}

const resetForm = () => {
  form.username = ''
  form.realName = ''
  form.email = ''
  form.phone = ''
  form.role = ''
  formRef.value?.resetFields()
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  if (isEdit.value) {
    const idx = mockUsers.findIndex(u => u.id === editId)
    if (idx > -1) Object.assign(mockUsers[idx], { ...form, id: editId })
    ElMessage.success('编辑成功')
  } else {
    mockUsers.push({
      id: Date.now(),
      ...form,
      createTime: new Date().toISOString().slice(0, 10)
    })
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  fetchData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除用户「${row.username}」吗？`, '提示', {
    type: 'warning'
  }).then(() => {
    const idx = mockUsers.findIndex(u => u.id === row.id)
    if (idx > -1) mockUsers.splice(idx, 1)
    ElMessage.success('删除成功')
    fetchData()
  }).catch(() => {})
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 12px;
}
.search-input {
  width: 240px;
}
.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}
</style>
