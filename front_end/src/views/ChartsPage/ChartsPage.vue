  <!-- /src/views/ChartsPage/ChartsPage.vue -->
  <template>
    <div class="charts-container">
      <WordCloudChart :wordData="wordData" />
      <BarChart :chartData="wordData" />
    </div>
  </template>
  
  <script>
  import WordCloudChart from './components/WordCloud.vue';
  import BarChart from './components/BarChart.vue';
  import axios from 'axios';
  
  export default {
    components: {
      WordCloudChart,
      BarChart
    },
    data() {
      return {
        wordData: []
      };
    },
    async mounted() {
      await this.fetchWordData();
    },
    methods: {
      async fetchWordData() {
        try {
          const response = await axios.get('http://localhost:5000/charts');
          this.wordData = response.data;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  .charts-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    width: 800px;
  }
  </style>