<template>
  <div ref="wordCloudChart" style="width: 100%; height: 400px;"></div>
</template>

<script>
import * as echarts from 'echarts';
import 'echarts-wordcloud';

export default {
  name: 'WordCloudChart',
  props: {
    wordData: Array
  },
  data() {
    return {
      chartInstance: null,
    };
  },
  watch: {
    wordData: {
      immediate: true,
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.initChart();
          this.$nextTick(this.resizeChart);
        }
      }
    }
  },
  methods: {
    initChart() {
      this.chartInstance = echarts.init(this.$refs.wordCloudChart);
      const option = {
        title: {
          text: '词云图',
          left: 'center' // 标题居中
        },
        series: [{
          type: 'wordCloud',
          data: this.wordData,
          sizeRange: [12, 60],
          rotationRange: [-90, 90],
          shape: 'circle',
          gridSize: 8
        }]
      };
      this.chartInstance.setOption(option);
    },
    resizeChart() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    }
  },
  mounted() {
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
  }
}
</script>
