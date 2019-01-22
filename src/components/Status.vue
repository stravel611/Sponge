<template>
  <div class="status">
    <div class="time-counter">
      <span>{{hour|clock}}:{{minute|clock}}:{{second|clock}}</span>
    </div>
    <div class="item-selector">
      <el-cascader
        expand-trigger="hover"
        :options="options"
        v-model="selectedOptions"
        :disabled="proceeding"
      ></el-cascader>
    </div>
    <div class="actions">
      <div class="action">
        <el-button type="danger" v-if="proceeding" @click="endRecord">结束计时</el-button>
        <el-button type="primary" v-else @click="startRecord" :disabled="notSelected">开始计时</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hour: 0,
      minute: 0,
      second: 0,
      selectedOptions: [],
      timer: null
    };
  },
  computed: {
    options: function() {
      let output = [];
      let categories = this.$store.state.categories;
      categories.forEach(function(e) {
        let items = [];
        e.items.forEach(function(i) {
          items.push({
            value: i.id,
            label: i.name
          });
        });
        output.push({
          value: e.id,
          label: e.name,
          children: items
        });
      });
      return output;
    },
    proceeding: function() {
      const proceeding = this.$store.state.proceeding;
      if (proceeding == null) {
        return false;
      } else {
        return true;
      }
    },
    notSelected: function() {
      if (this.selectedOptions.length == 0) {
        return true;
      } else {
        return false;
      }
    }
  },
  filters: {
    clock: function(value) {
      if (value < 10) {
        return "0" + value;
      } else {
        return value;
      }
    }
  },
  methods: {
    startRecord: function() {
      const itemId = this.selectedOptions[1]
      const url = '/item/'+itemId+'/record'
      this.$axios.post(url).then((res) => {
        this.$store.dispatch('fetchProceeding')
      })
    },
    endRecord: function() {
      const endTime = new Date
      const recordId = this.$store.state.proceedingId
      const url = '/record/'+recordId
      const formData = new FormData()
      formData.append('finish', endTime.getTime())
      this.$axios.put(url, formData).then((res) => {
        this.clearTimer()
        this.$store.dispatch('fetchProceeding')
      })
    },
    checkTimer: function(count, unit) {
      if (count == 60) {
        if (unit == 'second') {
          this.second = 0
          this.minute++
        }else {
          this.minute = 0
          this.hour++
        }
      }
    },
    setTimer: function() {
      return setInterval(() => {
        this.second++
      }, 1000)
    },
    clearTimer: function() {
      clearInterval(this.timer)
    }
  },
  watch: {
    "$store.state.proceeding": function(to, from) {
      if (to == null) {
        this.second = this.minute = this.hour = 0
      }else {
        const now = new Date();
        const gap = Math.floor((now - to) / 1000);
        this.second = gap % 60;
        this.minute = Math.floor(gap / 60) % 60;
        this.hour = Math.floor(gap / 3600);
        this.timer = this.setTimer()
      }
    },
    'second': function(to, from) {
      this.checkTimer(to, 'second')
    },
    'minute': function(to, from) {
      this.checkTimer(to, 'minute')
    }
  }
};
</script>

<style scoped>
.status {
  width: 100%;
  height: calc((100vh - 60px) / 2 - 1px);
  border-bottom: solid 1px #e6e6e6;
  display: flex;
  flex-direction: column;
}
.status > div {
  display: flex;
}
.time-counter {
  height: 50%;
  font-size: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.time-counter > span {
  display: inline-block;
  margin: auto;
}
.item-selector {
  height: 20%;
  display: flex;
  justify-content: center;
}
.actions {
  height: 30%;
}
.action {
  margin: auto;
}
</style>
