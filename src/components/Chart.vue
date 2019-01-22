<template>
  <el-card class="box-card chart" :id="chart_id"></el-card>
</template>

<script>
var echarts = require("echarts/lib/echarts");
require("echarts/lib/chart/pie");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/title");

export default {
  props: ["chart_id", "chart_title"],
  data() {
    return {
      chart_data: []
    };
  },
  computed: {
    chartTitle() {
      if (!this.chart_title) {
        return "分类详情";
      } else {
        return this.chart_title;
      }
    }
  },
  methods: {
    drawPie() {
      var myChart = echarts.init(document.getElementById(this.chart_id));
      var option = {
        title: {
          text: this.chartTitle,
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
    // redraw() {
    //   if (this.$store.state.current_)
    // }
    fetchData(category_id) {
      let url;
      if (category_id == 0) {
        url = "/category/calculation?";
      } else {
        url = "/category/" + category_id + "/calculation?";
      }
      let times = this.$store.state.timeRange;
      if (times[0] != 0) {
        url += "from=" + times[0] + "&";
      }
      if (times[1] != 0) {
        url += "to=" + times[1];
      }
      this.$axios.get(url).then(res => (this.chart_data = res.data.data));
    }
  },
  mounted() {},
  watch: {
    "$store.state.current_category": function(to, from) {
      this.fetchData(to);
    },
    chart_data: function(to, from) {
      if (to.length == 0) {
        alert("没有数据");
      } else {
        this.drawPie();
      }
    },
    "$store.state.timeRange": function(to, from) {
      this.fetchData(this.$store.state.current_category);
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
.chart {
  width: 100%;
  height: 40vh;
  float: left;
  margin: 5px;
}
</style>
