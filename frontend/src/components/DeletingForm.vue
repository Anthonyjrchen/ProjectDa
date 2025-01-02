<script setup>
import { ref } from 'vue';
import $ from 'jquery';
const courtFile = ref('');
function formSubmit(e){
    e.preventDefault();
    console.log("Delete events with caseFileNum: " + courtFile.value)
    $.ajax({
        url: 'http://127.0.0.1:8000/delete',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            caseNum: courtFile.value,
        }),
        success:function(e){
            if("error" in e) {
                alert(e.error)
            } else {
                alert("Events with the courtFileNum: " + courtFile.value + " was deleted.")
            }
        }
    });
};
</script>

<template>
    <head>
        <link href="./output.css" rel="stylesheet">
    </head> 
    <form class="p-1.5" v-on:submit.prevent="formSubmit">
        <h2>Court File No.</h2>
        <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[1px] !border-dark-white text-white !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-dark-gray" required />
            
        <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-dark-white mt-3 m-1" type="submit">Delete</button>
    </form>

    <div class="p-0.5">
        <router-link to="/home">
            <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-dark-white mt-3" type="submit">Go to Add</button>
        </router-link>
    </div>

</template>

<style scoped>

</style>