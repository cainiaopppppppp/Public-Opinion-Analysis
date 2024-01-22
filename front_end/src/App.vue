<!-- src/App.vue -->
<script>
import LayoutNav from "./components/Nav.vue"
export default {
  components: {
    LayoutNav
  }
}
// import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
</script>


<template>
  <div class = 'div'>
    <Nav />
  </div>
  
  <div class="content">
    <RouterView />
  </div>
</template>


<style scoped>

</style>