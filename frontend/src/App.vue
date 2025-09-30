<template>
  <div id="app">
    <BorrowerList />
  </div>
</template>

<script>
import BorrowerList from './components/BorrowerList.vue'

export default {
  name: 'App',
  components: {
    BorrowerList
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
