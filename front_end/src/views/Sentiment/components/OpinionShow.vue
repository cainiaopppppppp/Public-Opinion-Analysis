<!-- /src/views/Sentiment/components/OpinionShow.vue -->
<template>
  <div class="opinion-show">
    <h2 class="graph-title">情感倾向图</h2>
    <div ref="graph" id="graph"></div>
  </div>
</template>

<script>
import axios from 'axios';
import { Network } from 'vis-network';

export default {
  name: "GraphDisplay",
  data() {
    return {
      network: null,
    };
  },
  mounted() {
    this.fetchGraphData();
  },
  methods: {
    fetchGraphData() {
      axios.get('http://localhost:5000/sentiment')
        .then(response => {
          this.createGraph(response.data);
        })
        .catch(error => {
          console.error('Error during API call:', error);
        });
    },
    createGraph(graphData) {
      this.$nextTick(() => {
        const container = this.$refs.graph;
        const data = {
          nodes: graphData.nodes,
          edges: graphData.edges
        };
        const options = { /* ...options... */ };

        this.network = new Network(container, data, options);
      });
    }
  }
};
</script>

<style>
.opinion-show {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 200px;
}

.graph-title {
  /* margin-top: 1rem; */
  margin-top: 160px;
  margin-bottom: 20px;
}

#graph {
  width: 800px;
  height: 800px;
  border: 1px solid lightgray;
  margin-bottom: 20px;
}
</style>

