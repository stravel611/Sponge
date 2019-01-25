<template>
  <el-card class="history">
    <light-timeline :items="items">
      <template slot="tag" slot-scope="{ item }">{{item.start}}</template>
      <template slot="content" slot-scope="{ item }">
        <el-tag size="small" type="warning">{{item.item.name}}</el-tag>
        <el-tag size="small" type="success">{{ LastingTime(item.finish_stamp, item.start_stamp) }}</el-tag>
        <el-tag size="small" class="history-tag" v-for="tag in item.tags" :key="tag.id">{{tag.name}}</el-tag>
        {{item.remark}}
      </template>
    </light-timeline>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      items: []
    };
  },
  methods: {
    LastingTime: function(finish, start) {
      let output = "";
      const total_seconds = Math.floor((finish - start) / 1000);
      const seconds = total_seconds % 60;
      if (seconds != 0) {
        output = seconds + "秒";
      }
      const total_minuets = Math.floor(total_seconds / 60);
      if (total_minuets != 0) {
        const minutes = total_minuets % 60;
        if (minutes != 0) {
          output = minutes + "分钟" + output;
          const hours = Math.floor(total_minuets / 60);
          if (hours != 0) {
            output = hours + "小时" + output;
          }
        }
      }
      return output;
    },
    fetchData: function(category_id) {
      let url;
      if (category_id == 0) {
        url = "/record?limit=8";
      } else {
        url = "/category/" + category_id + "/record?limit=8";
      }
      this.$axios.get(url).then(res => (this.items = res.data.data));
    }
  },
  watch: {
    "$store.state.current_category": function(to, from) {
      this.fetchData(to);
    },
    "$store.state.proceedingId": function(to, from) {
      if (to == null && from > 0) {
        this.fetchData(this.$store.state.current_category);
      }
    }
  }
};
</script>

<style scoped>
.history {
  height: calc(60vh - 85px);
  margin: 5px;
}
.el-tag {
  margin-left: 5px;
}
</style>

