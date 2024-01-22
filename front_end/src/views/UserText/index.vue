<!-- src\views\UserText\index.vue -->
<template>
    <div class="user-text-container">
      <TextAnalysis />
      <OpinionInfer />
    </div>
  </template>
  
  <script>
  import TextAnalysis from './components/TextAnalysis.vue';
  import OpinionInfer from './components/OpinionInfer.vue';
  
  export default {
    name: 'UserTextView',
    components: {
      TextAnalysis,
      OpinionInfer
    }
  };
  </script>
  
  <style>
  .user-text-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  
  /* 根据需要，您可以为子组件添加额外的样式 */
  </style>
  