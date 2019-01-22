<template>
  <el-card class="box-card time-picker">
    <div class="picker-items">
      <el-row class="picker-item">
        <el-col :span=8>
          <div class="picker-label"><span>选择时间</span></div>
        </el-col>
        <el-col :span=16>
          <el-date-picker
            v-model="timeRange"
            size="large"
            type="daterange"
            align="center"
            unlink-panels
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="pickRange">
          </el-date-picker>
        </el-col>
      </el-row>
      <el-row class="picker-item">
        <el-col :span=8>
          <div class="picker-label"><span>按周选择</span></div>
        </el-col>
        <el-col :span=16>
          <el-date-picker
            v-model="timeWeek"
            type="week"
            format="yyyy 第 WW 周"
            placeholder="选择周"
            @change="pickWeek">
          </el-date-picker>
        </el-col>
      </el-row>
      <el-row class="picker-item">
        <el-col :span=8>
          <div class="picker-label"><span>按月选择</span></div>
        </el-col>
        <el-col :span=16>
          <el-date-picker
            v-model="timeMonth"
            type="month"
            placeholder="选择月"
            @change="pickMonth">
          </el-date-picker>
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      timeRange: [],
      timeWeek: "",
      timeMonth: ""
    };
  },
  methods: {
    pickRange(range) {
      const fromTime = range[0].getTime()
      const toTime = range[1].getTime() + 24 * 3600 * 1000
      this.$store.commit('setTimeRange', [fromTime, toTime])
    },
    pickWeek(time) {
      const fromTime = time.getTime()
      const toTime = fromTime + 7 * 24 * 3600 * 1000
      this.$store.commit('setTimeRange', [fromTime, toTime])
    },
    pickMonth(time) {
      const fromTime = time.getTime()
      const toTime = fromTime + 30 * 24 * 3600 * 1000
      this.$store.commit('setTimeRange', [fromTime, toTime])
    }
  },
  watch: {
  },
  mounted() {
  }
};
</script>

<style scoped>
.time-picker {
  width: 100%;
  height: 40vh;
  float: left;
  margin: 5px;
}
.picker-items {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
.picker-item {
  width: 100%;
  height: 100%;
  display: flex;
  margin: 5px;
}
.picker-label {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.picker-label span {
  line-height: 40px;
  text-align: center;
  height: 100%;
  display: flex;
}
</style>