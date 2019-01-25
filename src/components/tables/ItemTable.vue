<template>
  <div class="management-table">
    <div>
      新建条目：  
      <el-input v-model="newItem" placeholder="请输入新条目的名称" size="medium" class="new-item-input"></el-input>
      <el-select v-model="select" placeholder="选择所属分类" size="medium" class="new-item-select">
        <el-option
          v-for="item in options"
          :key="item.id"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
      <el-button type="primary" plain size="medium" class="new-item-button" @click="createNewItem">提交</el-button>
    </div>
    <el-table :data="tableData" class="item-table">
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
  data() {
    return {
      newItem: '',
      select: null,
      tableData: []
    }
  },
  computed: {
    options() {
      return this.$store.state.categories
    }
  },
  methods: {
    fetchItems() {
      const url = '/item'
      this.$axios.get(url).then(res => {
        if (res.data.status == 200) {
          this.tableData = res.data.data
        }else {
          this.$message.error('获取条目失败!')
        }
      })
    },
    handleRename: function(index, row) {
      this.$emit('showEditDialog', row.id, row.name, '更改名称')
    },
    handleDelete: function(index, row) {
      this.$emit('showDeleteDialog', row.id, row.name)
    },
    createNewItem() {
      if (this.select == null) {
        this.$message.error('请选择分类！')
      }else {
        const url = '/category/'+this.select+'/item'
        const formData = new FormData()
        formData.append('name', this.newItem)
        this.$axios.post(url, formData).then(res => {
          if (res.data.status == 201) {
            this.$message.success('创建成功！')
            this.newItem = ''
            this.select = null
            this.fetchItems()
          }else {
            this.$message.error('出错了!')
          }
        })
      }
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
}
.item-table {
  height: calc(100% - 30px);
  overflow-y: auto;
}
.new-item-input {
  display: inline-block;
  width: 400px;
}
.new-item-button, .new-item-select {
  margin-left: 5px;
}
.new-item-select {
  width: 135px;
}
</style>
