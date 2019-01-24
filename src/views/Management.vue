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
      <el-tab-pane label="记录管理" name="record">记录管理</el-tab-pane>
    </el-tabs>
    <el-dialog
      title="更改名称"
      :visible.sync="editDialogVisible"
      width="30%"
      :before-close="handleClose">
      <span><el-input v-model="targetName"></el-input></span>
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

export default {
  components: {
    'category-table': CategoryTable,
    'item-table': ItemTable
  },  
  data() {
    return {
      editDialogVisible: false,
      deleteDialogVisible: false,
      targetModel: 'category',
      targetId: 0,
      targetName: '',
      originName: ''
    }
  },
  methods: {
    reset() {
      this.editDialogVisible = false,
      this.deleteDialogVisible = false,
      this.targetId = 0,
      this.targetName = ''
    },
    setModel(tab) {
      this.targetModel = tab.name
    },
    showEditDialog(id) {
      this.targetId = id
      this.editDialogVisible = true
    },
    showDeleteDialog(id, name) {
      this.targetId = id
      this.originName = name
      this.deleteDialogVisible = true
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(() => {
          done();
        })
        .catch(() => {});
    },
    confirmChange() {
      const url = '/'+this.targetModel+'/'+this.targetId
      const formData = new FormData()
      formData.append('name', this.targetName)
      this.$axios.put(url, formData).then(res => {
        if (res.data.status == 200) {
          this.$message.success('更新成功')
          this.$store.dispatch('fetchCategory')
        }else {
          this.$message.error('出错了')
        }
      })
      this.reset()
    },
    confirmDelete() {
      const url = '/'+this.targetModel+'/'+this.targetId
      this.$axios.delete(url).then(res => {
        if (res.data.status == 200) {
          this.$message.success('更新成功')
          if (this.targetModel == 'category') {
            this.$store.dispatch('fetchCategory')
          }else if (this.targetModel == 'item') {
            this.$refs.itemTable.fetchItems()
          }
        }else {
          this.$message.error('出错了')
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
