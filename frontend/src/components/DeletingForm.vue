<script setup>
import { ref } from 'vue';
</script>

<template>
    <head>
        <link href="./output.css" rel="stylesheet">
    </head> 
    <div class="p-1.5">
        <h2>Court File No.</h2>
        <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[1px] !border-dark-white text-black !rounded-md focus:outline-none focus:ring-1 focus:ring-white" required />
            
        <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-dark-white mt-3" type="submit">Delete</button>
    </div>

    <div class="p-0.5">
        <router-link to="/home">
            <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-dark-white mt-3" type="submit">Go to Add</button>
        </router-link>
    </div>

</template>

<style scoped>

</style>