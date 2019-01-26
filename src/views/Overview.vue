<template>
  <div id="overview">
    <div class="charts">
      <!-- 最近一周的记录统计饼图 -->
      <div class="chart-container">
        <overview-chart chartId="chart_1" chartTitle="最近一周" defaultDays="7"></overview-chart>
      </div>
      <!-- 最近三天的记录统计饼图 -->
      <div class="chart-container">
        <overview-chart chartId="chart_2" chartTitle="最近三天" defaultDays="3"></overview-chart>
      </div>
    </div>
    <overview-history></overview-history>
  </div>
</template>

<script>
import Chart from "../components/Chart";
import History from "../components/History";

export default {
  components: {
    "overview-chart": Chart,
    "overview-history": History
  },
  mounted() {
    // 挂载时设置当前分类 id 为 0，即所有分类
    this.$store.commit("setCategory", 0);
  }
};
</script>

<style scoped>
#overview {
  width: 100%;
  height: 100%;
}
.charts {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.chart-container {
  display: flex;
  width: 50%;
}
</style>
