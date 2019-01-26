<template>
  <div class="management">
    <el-tabs type="border-card" @tab-click="setModel" activeName="category">
      <el-tab-pane label="分类管理" name="category">
        <category-table @showEditDialog="showEditDialog" @showDeleteDialog="showDeleteDialog">
        </category-table>
      </el-tab-pane>
      <el-tab-pane label="条目管理" name="item">
        <item-table @showEditDialog="showEditDialog" @showDeleteDialog="showDeleteDialog" ref="itemTable">
        </item-table>
      </el-tab-pane>
      <el-tab-pane label="记录管理" name="record">
        <record-table @showEditDialog="showEditDialog" @showDeleteDialog="showDeleteDialog" ref="recordTable">
        </record-table>
      </el-tab-pane>
    </el-tabs>
    <!-- 重命名、修改记录备注的模态框 -->
    <el-dialog
      :title="action"
      :visible.sync="editDialogVisible"
      width="30%"
      :before-close="handleClose">
      <span><el-input v-model="targetValue" autofocus></el-input></span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reset">取 消</el-button>
        <el-button type="primary" @click="confirmChange">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 删除项目的模态框 -->
    <el-dialog
      title="删除项目"
      :visible.sync="deleteDialogVisible"
      width="30%"
      :before-close="handleClose">
      <span>确认删除 {{originValue}} 吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reset">取 消</el-button>
        <el-button type="primary" @click="confirmDelete">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import CategoryTable from '../components/tables/CategoryTable'
import ItemTable from '../components/tables/ItemTable'
import RecordTable from '../components/tables/RecordTable'

export default {
  components: {
    'category-table': CategoryTable,
    'item-table': ItemTable,
    'record-table': RecordTable
  },  
  data() {
    return {
      editDialogVisible: false,
      deleteDialogVisible: false,
      action: '',                   // 展示 editDialog 的标题，表示要执行的动作
      targetModel: 'category',      // 操作的目标模型
      targetId: 0,                  // 操作的目标 id
      targetValue: '',              // 修改类的操作的目标值
      originValue: ''               // 修改类的操作的原始值
    }
  },
  methods: {
    // 重设状态
    reset() {
      this.editDialogVisible = false,
      this.deleteDialogVisible = false,
      this.targetId = 0,
      this.targetValue = ''
      this.action = ''
    },
    // 刷新表格数据
    refresh() {
      if (this.targetModel == 'category') {
        this.$store.dispatch('fetchCategory')
      }else if (this.targetModel == 'item') {
        this.$refs.itemTable.fetchItems()
      }else if (this.targetModel == 'record') {
        this.$refs.recordTable.fetchRecords()
      }
    },
    setModel(tab) {
      this.targetModel = tab.name
    },
    showEditDialog(id, origin, action) {
      this.action = action
      this.targetId = id
      this.originValue = origin
      if (action == '修改备注') {
        this.targetValue = this.originValue
      }
      this.editDialogVisible = true
    },
    showDeleteDialog(id, name) {
      this.targetId = id
      this.originValue = name
      this.deleteDialogVisible = true
    },
    handleClose() {
      this.reset()
    },
    // 根据目标动作从相应 api 获取数据并更新
    confirmChange() {
      if (this.action == '添加标签') {
        const url = '/record/'+this.targetId+'/tag'
        const formData = new FormData()
        formData.append('name', this.targetValue)
        this.$axios.post(url, formData).then(res => {
          if (res.data.status == 201) {
            this.$message.success('更新成功')
            this.refresh()
          }else {
            this.$message.error('出错了')
          }
        })
      }else {
        const url = '/'+this.targetModel+'/'+this.targetId
        const formData = new FormData()
        if (this.action == '更改名称') {
          formData.append('name', this.targetValue)
        }else {
          formData.append('remark', this.targetValue)
        }
        this.$axios.put(url, formData).then(res => {
          if (res.data.status == 200) {
            this.$message.success('更新成功！')
            this.refresh()
          }else {
            this.$message.error('出错了！')
          }
        })
      }
      this.reset()
    },
    confirmDelete() {
      const url = '/'+this.targetModel+'/'+this.targetId
      this.$axios.delete(url).then(res => {
        if (res.data.status == 200) {
          this.$message.success('删除成功！')
          this.refresh()
        }else {
          this.$message.error('出错了！')
        }
      this.reset()
      })
    }
  },
  // 挂载时将当前分类重设为 null，方便返回总览页面时，
  // 总览页面组件可以监听到当前分类的变化，更新数据
  mounted() {
    this.$store.commit('setCategory', null)
  }
}
</script>

<style scoped>
.management {
  width: 100%;
  height: 100%;
}
</style>
