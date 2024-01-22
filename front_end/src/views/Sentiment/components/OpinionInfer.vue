<!-- /src/views/Sentiment/components/OpinionInfer.vue -->
<template>
  <div class="entity-selector">
    <div class="select-container">
      <el-select v-model="selectedEntity1" placeholder="请选择实体1" class="entity-select">
        <el-option
          v-for="entity in entities"
          :key="entity"
          :label="entity"
          :value="entity">
        </el-option>
      </el-select>

      <el-select v-model="selectedEntity2" placeholder="请选择实体2" class="entity-select">
        <el-option
          v-for="entity in entities"
          :key="entity"
          :label="entity"
          :value="entity">
        </el-option>
      </el-select>
    </div>

    <div class="button-container">
      <el-button type="primary" @click="compareSentiments">比较情感倾向</el-button>
    </div>

    <div v-if="opinionResult" class="result">
      <el-alert
        :title="opinionResult"
        type="success"
        show-icon>
      </el-alert>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "EntitySelector",
  data() {
    return {
      selectedEntity1: '',
      selectedEntity2: '',
      opinionResult: null,
      entities: [] // 假设从某个 API 或父组件获取
    };
  },
  mounted() {
    this.fetchEntities();
  },
  methods: {
    fetchEntities() {
      axios.get('http://localhost:5000/entities')
        .then(response => {
          this.entities = response.data.entities;
        })
        .catch(error => {
          console.error('Error fetching entities:', error);
        });
    },
    compareSentiments() {
      if (this.selectedEntity1 === this.selectedEntity2) {
        alert("请选择不同的实体进行比较！");
        return;
      }
      axios.post('http://localhost:5000/compare-sentiments', {
        entity1: this.selectedEntity1,
        entity2: this.selectedEntity2
      })
      .then(response => {
        this.opinionResult = response.data.opinion;
      })
      .catch(error => {
        console.error('Error during API call:', error);
      });
    }
  }
};
</script>
<style>
.entity-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.select-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.entity-select {
  width: 48%; /* 留出一些空间给间隙 */
}

.button-container {
  margin-top: 20px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.result {
  margin-top: 20px;
  margin-bottom: 20px;
}

</style>
