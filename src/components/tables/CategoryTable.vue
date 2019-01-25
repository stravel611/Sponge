<template>
  <div class="management-table">
    <div>新建分类：
      <el-input
        v-model="newCategory"
        placeholder="请输入新分类的名称"
        size="medium"
        class="new-category-input"
      ></el-input>
      <el-button
        type="primary"
        plain
        size="medium"
        class="new-category-button"
        @click="createNewCategory"
      >提交</el-button>
    </div>
    <el-table :data="tableData" class="category-table">
      <el-table-column prop="id" label="id" width="180"></el-table-column>
      <el-table-column prop="name" label="名称" width="180"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleRename(scope.$index, scope.row)">重命名</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newCategory: ""
    };
  },
  computed: {
    tableData: function() {
      return this.$store.state.categories;
    }
  },
  methods: {
    handleRename: function(index, row) {
      this.$emit("showEditDialog", row.id, row.name, "更改名称");
    },
    handleDelete: function(index, row) {
      this.$emit("showDeleteDialog", row.id, row.name);
    },
    createNewCategory() {
      if (this.newCategory == "") {
        this.$message.error("请输入分类名称！");
      } else {
        const url = "/category";
        const formData = new FormData();
        formData.append("name", this.newCategory);
        this.$axios.post(url, formData).then(res => {
          if (res.data.status == 201) {
            this.$message.success("创建成功！");
            this.$store.dispatch("fetchCategory");
          } else {
            this.$message.error("出错了！");
          }
        });
      }
    }
  }
};
</script>

<style scoped>
.management-table {
  height: calc(100vh - 135px);
}
.category-table {
  height: calc(100% - 30px);
  overflow-y: auto;
}
.new-category-input {
  display: inline-block;
  width: 400px;
}
.new-category-button {
  margin-left: 5px;
}
</style>
