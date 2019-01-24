<template>
  <div class="management-table">
    <el-table :data="tableData">
      <el-table-column prop="id" label="id" width="180"></el-table-column>
      <el-table-column prop="name" label="名称" width="180"></el-table-column>
      <el-table-column prop="category.name" label="所属分类" width="180"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleRename(scope.$index, scope.row)">重命名</el-button>
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
  name: 'ds',
  data() {
    return {
      tableData: []
    }
  },
  methods: {
    fetchItems() {
      console.log('fetching')
      const url = '/item'
      this.$axios.get(url).then(res => {
        if (res.data.status == 200) {
          this.tableData = res.data.data
        }else {
          this.$message.error('获取条目失败')
        }
      })
    },
    handleRename: function(index, row) {
      this.$emit('showEditDialog', row.id)
    },
    handleDelete: function(index, row) {
      this.$emit('showDeleteDialog', row.id, row.name)
    }
  },
  mounted() {
    this.fetchItems()
  },
  created() {
      this.$on('fetchItems2', function() {
      this.fetchItems()
    })
  }
}
</script>

<style scoped>
.management-table {
  height: calc(100vh - 135px);
  overflow-y: auto;
}
</style>
