<!-- src/views/Layout/index.vue -->
<script setup>
import LayoutFooter from './components/LayoutFooter.vue'
import StartBody from '../StartBody/StartBody.vue'
</script>

<template>
  <div class="container">
    <div class="layout-header">
      <!-- <LayoutHeader /> -->
    </div>


    <div class="content">
      <StartBody />
      <RouterView style="height: calc(100vh - 140px)" />
    </div>
    <div class = "layout-footer">
      <LayoutFooter />
    </div>
    
  </div>
</template>

<style>
#app {
  padding-top: 90px;
  /* Nav + Header高度 */
}

.container {
  display: grid;
  grid-template-rows: 90px 1fr 60px;
  /* header  content footer */
  grid-template-areas:
    "header"
    "content"
    "footer";
}

.layout-header {
  grid-area: header;
}

.content {
  grid-area: content;
  margin-top: 20px;
}
.layout-footer {
  grid-area: footer;
}
</style>