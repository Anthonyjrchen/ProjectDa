<script setup>
    import { RouterLink } from 'vue-router'
</script>

<template>
  <main>
    <router-link to="/home">
        <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="submit">Go to home page</button>
    </router-link>
  </main>
</template>

<style scoped>

</style>