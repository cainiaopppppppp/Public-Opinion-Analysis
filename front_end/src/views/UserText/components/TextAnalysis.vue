<!-- src\views\UserText\components\TextAnalysis.vue -->
<template>
  <div class="text-analysis-container">
    <div class="input-container">
      <el-input
        type="textarea"
        placeholder="请输入文本"
        v-model="textInput"
        rows="4"
        class="text-input">
      </el-input>
      <el-button class="analyze-button" @click="analyzeText">分析</el-button>
    </div>
    <div ref="graph" id="graph" v-show="graphData" class="graph-container"></div>
    <div v-if="inferenceResult" class="inference-result">
      <p>{{ inferenceResult }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Network } from 'vis-network';

export default {
data() {
  return {
    textInput: '',
    graphData: null,
    inferenceResult: null,
    network: null
  };
},
methods: {
  analyzeText() {
    axios.post('http://localhost:5000/analyze-text', { text: this.textInput })
      .then(response => {
        this.graphData = response.data.graph;
        this.inferenceResult = response.data.inference;
        this.createGraph(this.graphData);
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
.text-analysis-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-container {
  width: 800px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.text-input {
  width: 100%; /* Full width of the container */
  min-height: 160px; /* Fixed height */
}

.analyze-button {
  margin-top: 10px; /* Space between the text input and button */
  align-self: flex-start; /* Align to the left */
}

#graph {
  width: 800px;
  height: 800px;
  border: 1px solid lightgray;
  background-color: #f5f5f5; /* Optional: a background color to indicate the space for the graph */
  margin-top: 20px; /* Space above the graph */
}
</style>
