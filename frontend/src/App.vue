<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HeaderBar from './components/HeaderBarView.vue'
import DeletingForm from './components/DeletingForm.vue';
import 'primeflex/primeflex.css'
</script>

<template>
  <!-- <div class="grid">
    <HeaderBar />
    <RouterView />
  </div> -->
  <div class="grid">
      <div class="col">
          <HeaderBar />
      </div>
  </div>
  <div class="grid" style="width:100vw;height:100vh; background-color: grey">
      <div class="col-fixed" style="width:100px;">
          <div class="text-center p-3 border-round-sm font-bold" style="background-color: aqua;">100px</div>
      </div>
      <div class="col">
          <div class="text-center p-3 border-round-sm font-bold" style="background-color: aqua;">auto</div>
      </div>
  </div>
</template>

<style scoped>

</style>
