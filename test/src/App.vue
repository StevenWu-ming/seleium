<template>
  <div id="app">
    <TestPanel />
  </div>
</template>

<script>
import TestPanel from './components/TestPanel.vue';

export default {
  name: 'App',
  components: {
    TestPanel,
  },
};
</script>

<style>
#app {
  max-width: 1200px;
  margin: 0 auto;
}
</style>