<template>
  <div id="overview">
    <div class="charts">
      <div class="chart-container">
      <category-chart chart_id='chart_1' defaultDays="7"></category-chart>
      </div>
      <div class="picker-container">
      <category-time-picker></category-time-picker>
      </div>
    </div>
    <category-history></category-history>
  </div>
</template>

<script>
import Chart from '../components/Chart'
import History from '../components/History'
import TimePicker from '../components/TimePicker'

export default {
  components: {
    'category-chart': Chart,
    'category-history': History,
    'category-time-picker': TimePicker
  },
  data() {
    return {
      // categories: [],
    }
  },
  computed: {
  },
  methods: {
  },
  watch: {
    // 路由变化时，设置当前分类 id
    '$route' (to, from) {
      this.$store.commit('setCategory', to.params.categoryId)
    },
  },
  mounted() {
    // 直接加载时，设置当前分类 id
    this.$store.commit('setCategory', this.$route.params.categoryId)
  } 
}
</script>

<style scoped>
.charts {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.chart-container, .picker-container {
  display: flex;
  width: 50%;
}
</style>
