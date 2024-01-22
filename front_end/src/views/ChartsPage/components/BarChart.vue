<template>
  <div ref="barChart" style="width: 100%; height: 400px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'BarChart',
  props: {
    chartData: Array
  },
  watch: {
    chartData: {
      immediate: true,
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.initChart();
        }
      }
    }
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.barChart);
      const option = {
        title: {
          text: '频次柱状图',
          left: 'center' // 标题居中
        },
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            // 显示标签和值
            return `${params.name}: ${params.value}`;
          }
        },
        xAxis: {
          type: 'category',
          data: this.chartData.map(item => item.name),
          axisLabel: {
            interval: 0, // 根据需要调整
            rotate: 45, // 旋转标签避免重叠
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: this.chartData,
          type: 'bar',
          itemStyle: {
            color: '#3398DB' // 根据需要调整颜色
          }
        }]
      };
      chart.setOption(option);
    }
  }
}
</script>
