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
    <el-dialog
      :title="action"
      :visible.sync="editDialogVisible"
      width="30%"
      :before-close="handleClose">
      <span><el-input v-model="targetName" autofocus></el-input></span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reset">取 消</el-button>
        <el-button type="primary" @click="confirmChange">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="删除项目"
      :visible.sync="deleteDialogVisible"
      width="30%"
      :before-close="handleClose">
      <span>确认删除 {{originName}} 吗？</span>
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
      action: '',
      targetModel: 'category',
      targetId: 0,
      targetName: '',
      originName: 'xxx'
    }
  },
  methods: {
    reset() {
      this.editDialogVisible = false,
      this.deleteDialogVisible = false,
      this.targetId = 0,
      this.targetName = ''
      this.action = ''
    },
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
      this.originName = origin
      if (action == '修改备注') {
        this.targetName = this.originName
      }
      this.editDialogVisible = true
    },
    showDeleteDialog(id, name) {
      this.targetId = id
      this.originName = name
      this.deleteDialogVisible = true
    },
    handleClose() {
      this.reset()
    },
    confirmChange() {
      if (this.action == '添加标签') {
        const url = '/record/'+this.targetId+'/tag'
        const formData = new FormData()
        formData.append('name', this.targetName)
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
          formData.append('name', this.targetName)
        }else {
          formData.append('remark', this.targetName)
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
  }
}
</script>

<style scoped>
.management {
  width: 100%;
  height: 100%;
}
</style>
