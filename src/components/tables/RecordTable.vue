<template>
  <div class="management-table">
    <el-table :data="tableData">
      <el-table-column prop="id" label="id" width="50"></el-table-column>
      <el-table-column prop="item.name" label="所属条目" width="100"></el-table-column>
      <el-table-column label="标签" width="310">
        <template slot-scope="scope">
          <el-tag v-for="tag in scope.row.tags"
            :key="tag.name"
            @close="deleteTag(scope.row.id, tag.id)" 
            size="mini"
            closable> 
            {{tag.name}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" width="450"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="addTag(scope.$index, scope.row)">添加标签</el-button>
          <el-button
            size="mini"
            @click="modifyRemark(scope.$index, scope.row)">修改备注</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
    }
  },
  methods: {
    fetchRecords() {
      const url = '/record'
      this.$axios.get(url).then(res => {
        if (res.data.status == 200) {
          this.tableData = res.data.data
        }else {
          this.$message.error('获取记录失败')
        }
      })
    },
    addTag(index, row) {
      this.$emit('showEditDialog', row.id, '添加标签')
    },
    deleteTag(recordId, tagId) {
      const url = '/record/'+recordId+'/tag?id='+tagId
      this.$axios.delete(url).then(res => {
        if (res.data.status == 200) {
          this.$message.success('删除成功')
          this.fetchRecords()
        }else {
          this.$message.error('出错了')
        }
      })
    },
    modifyRemark(index, row) {
      this.$emit('showEditDialog', row.id, '修改备注')
    },
    handleDelete: function(index, row) {
      this.$emit('showDeleteDialog', row.id, row.name)
    }
  },
  mounted() {
    this.fetchRecords()
  }
}
</script>

<style scoped>
.management-table {
  height: calc(100vh - 135px);
  overflow-y: auto;
}
.el-tag {
  margin-right: 5px;
}
</style>
