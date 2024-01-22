<!-- /src/views/Sentiment/index.vue -->
<template>
  <div class="container">
    <OpinionShow />
    <OpinionInfer />
  </div>
</template>

<script>
import OpinionShow from './components/OpinionShow.vue';
import OpinionInfer from './components/OpinionInfer.vue';

export default {
name: 'SentimentView',
components: {
  OpinionShow,
  OpinionInfer
}
};
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}


/* 如果需要，您可以为子组件添加额外的样式 */
</style>
