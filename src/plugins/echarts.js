import Vue from 'vue';
var _echarts = require('echarts/lib/chart/pie')

Plugin.install = function(Vue, options) {
  Vue.echarts = _echarts;
  window.echarts = _echarts;
  Object.defineProperties(Vue.prototype, {
    echarts: {
      get() {
        return _echarts;
      }
    },
    $echarts: {
      get() {
        return _echarts;
      }
    },
  });
};

Vue.use(Plugin)

export default Plugin;
