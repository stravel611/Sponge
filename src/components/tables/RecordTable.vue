<template>
  <div class="management-table">
    <div class="date-picker">
      <span>选择月份：</span>  
      <el-date-picker
      v-model="timeMonth"
      type="month"
      placeholder="选择月">
    </el-date-picker>
    </div>
    <el-table :data="tableData" class="record-table">
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
      timeMonth: 0
    }
  },
  methods: {
    fetchRecords(fromTime, toTime) {
      const url = '/record?from='+fromTime+'&to='+toTime
      this.$axios.get(url).then(res => {
        if (res.data.status == 200) {
          this.tableData = res.data.data
        }else {
          this.$message.error('获取记录失败')
        }
      })
    },
    getTimeRange(date) {
      let y = date.getFullYear()
      let m = date.getMonth()
      const fromTime = new Date(y, m)
      if (m == 12) {
        y++
        m = 1
      }else {
        m++
      }
      const toTime = new Date(y, m)
      return [fromTime.getTime(), toTime.getTime()]
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
      this.$emit('showEditDialog', row.id, row.remark, '修改备注')
    },
    handleDelete: function(index, row) {
      const name = 'id 为 '+row.id+' 的记录'
      this.$emit('showDeleteDialog', row.id, name)
    }
  },
  mounted() {
    const now = new Date()
    this.timeMonth = now
  },
  watch: {
    'timeMonth': function(to) {
      const timeRamge = this.getTimeRange(to)
      this.fetchRecords(timeRamge[0], timeRamge[1])
    }
  }
}
</script>

<style scoped>
.management-table {
  height: calc(100vh - 135px);
}
.record-table {
  height: calc(100% - 30px);
    overflow-y: auto;
}
.el-tag {
  margin-right: 5px;
}
</style>
