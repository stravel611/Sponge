<template>
  <div class="management-table">
    <el-table :data="tableData">
      <el-table-column prop="id" label="id" width="180"></el-table-column>
      <el-table-column prop="name" label="名称" width="180"></el-table-column>
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
  computed: {
    tableData: function() {
      return this.$store.state.categories
    }
  },
  methods: {
    handleRename: function(index, row) {
      this.$emit('showEditDialog', row.id)
    },
    handleDelete: function(index, row) {
      this.$emit('showDeleteDialog', row.id, row.name)
    }
  }
}
</script>

<style scoped>
.management-table {
  height: calc(100vh - 135px);
  overflow-y: auto;
}
</style>
