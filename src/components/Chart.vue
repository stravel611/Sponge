<template>
  <el-card class="box-card chart" :id="chartId"></el-card>
</template>

<script>
var echarts = require("echarts/lib/echarts");
require("echarts/lib/chart/pie");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/title");

export default {
  props: ["chartId", "chartTitle", "defaultDays"],
  data() {
    return {
      chart_data: []
    };
  },
  computed: {
    title() {
      if (!this.chartTitle) {
        let categoryName;
        let self = this;
        self.$store.state.categories.forEach(function(category) {
          if (category.id == self.$route.params.categoryId) {
            categoryName = category.name;
          }
        });
        return categoryName;
      } else {
        return this.chartTitle;
      }
    }
  },
  methods: {
    drawPie() {
      var myChart = echarts.init(document.getElementById(this.chartId));
      var option = {
        title: {
          text: this.title,
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: function(params) {
            let output = "";
            let seconds = params.value % 60;
            if (seconds != 0) {
              output = seconds + "秒";
            }
            let minutes = Math.floor(params.value / 60);
            if (minutes != 0) {
              let _minutes = minutes % 60;
              if (_minutes) {
                output = _minutes + "分钟" + output;
              }
              let hours = Math.floor(minutes / 60);
              if (hours) {
                output = hours + "小时" + output;
              }
            }
            return output;
          }
        },
        series: [
          {
            name: "总时间",
            type: "pie",
            radius: "60%",
            center: ["50%", "55%"],
            data: this.chart_data,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    fetchData(category_id, recallDays) {
      let url;
      if (category_id == 0) {
        url = "/category/calculation?";
      } else {
        url = "/category/" + category_id + "/calculation?";
      }
      if (recallDays == 0) {
        let times = this.$store.state.timeRange;
        if (times[0] != 0) {
          url += "from=" + times[0] + "&";
        }
        if (times[1] != 0) {
          url += "to=" + times[1];
        }
      } else {
        const now = new Date();
        const time = now.getTime() - recallDays * 24 * 3600 * 1000;
        url += "from=" + time;
      }
      this.$axios.get(url).then(res => (this.chart_data = res.data.data));
    }
  },
  watch: {
    "$store.state.current_category": function(to) {
      if (to != null) {
        this.fetchData(to, this.defaultDays);
      }
    },
    chart_data: function(to) {
      if (to.length == 0) {
        this.$message({
          type: "error",
          message: "该时间段没有记录，请选择其他时间段",
          duration: 2000
        });
      } else {
        this.drawPie();
      }
    },
    "$store.state.timeRange": function() {
      this.fetchData(this.$store.state.current_category, 0);
    },
    "$store.state.proceedingId": function(to, from) {
      if (to == null && from > 0) {
        this.fetchData(this.$store.state.current_category, 7);
      }
    }
  }
};
</script>

<style scoped>
.chart {
  width: 100%;
  height: 40vh;
  float: left;
  margin: 5px;
}
</style>
