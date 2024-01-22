<template>
    <div>
      <el-input v-model="searchQuery" placeholder="请输入搜索内容" @keyup.enter="fetchGraphData"></el-input>
      <el-button @click="fetchGraphData">搜索</el-button>
      <div id="network"></div>
    </div>
  </template>
  
  <script>
  import { Network } from "vis-network";
  import axios from "axios";
  
  export default {
    data() {
      return {
        searchQuery: "",
        network: null,
      };
    },
    methods: {
      fetchGraphData() {
        axios
          .get("http://localhost:5000/graph", {
            params: { query: this.searchQuery },
          })
          .then((response) => {
            this.createGraph(response.data);
          })
          .catch((error) => {
            console.error("Error fetching graph data:", error);
          });
      },
      createGraph(graphData) {
        const container = document.getElementById("network");
        const data = {
          nodes: graphData.nodes,
          edges: graphData.edges,
        };
        const options = {
        nodes: {
            shape: 'dot',
            size: 20,
            font: {
            size: 15,
            color: '#ffffff'
            },
            borderWidth: 2
        },
        edges: {
            width: 2,
            color: '#ffffff',
            arrows: {
            to: { enabled: true, scaleFactor: 1 }
            },
            smooth: {
            enabled: true,
            type: "dynamic",
            roundness: 0.5
            }
        },
        physics: {
            forceAtlas2Based: {
            gravitationalConstant: -26,
            centralGravity: 0.005,
            springLength: 230,
            springConstant: 0.18
            },
            maxVelocity: 146,
            solver: 'forceAtlas2Based',
            timestep: 0.35,
            stabilization: { iterations: 150 }
        }
        };

        this.network = new Network(container, data, options);
      },
    },
  };
  </script>
  
  <style scoped>
  #network {
    width: 800px;
    height: 800px;
    border: 1px solid lightgray;
  }
  </style>
