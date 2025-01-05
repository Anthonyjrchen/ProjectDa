<script setup>

import { ref } from 'vue';
import anto from '../assets/images/anto.jpg';
import dana from '../assets/images/dana.jpeg';import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import $ from 'jquery';
const visible = ref(false);
const subject = ref('');
const body  = ref('');

function onFormSubmit(){
    visible.value = false;
    $.ajax({
        url:'http://localhost:8000/support/contact',
        type:'get',
        data:{
            subject:subject.value,
            body:body.value,
        },
        success:function(e) {
            alert("Your message has been sent.")
            console.log(e)
        }
    });
}
</script>

<template>
    <div class="container flex flex-row justify-between">
        <div class="dana flex flex-col items-center">
            <h1 class="name text-white">Dana Angela Neria</h1>
            <p class="title text-white">Co-Developer</p>
            <p class="text-white">University of British Columbia</p>
            <a href="https://www.linkedin.com/in/dana-angela-neria/" target="_blank">
                <i class="pi pi-linkedin text-white text-2xl" style="box-shadow: 1px 3px 4px rgba(0, 0, 0, 0.3);"></i>
            </a>
            <img :src="dana" alt="Dana" class="w-[300px] h-[300px] rounded-full m-5 ml-auto mr-auto mt-2">
        </div>

        <div class="myButton flex flex-col items-center justify-center"> 
            <p><button @click="visible = true" class="border-[1px] border-sweet-pink px-3 py-2 rounded-md hover:bg-azalea bg-azalea m-0 p-0">Contact</button></p>
        </div>

        <div class="anto flex flex-col items-center">
            <h1 class="name text-white">Anthony Chen</h1>
            <p class="title text-white">Co-Developer</p>
            <p class="text-white">University of British Columbia</p>
            <a href="https://www.linkedin.com/in/anthony-chen-999804221/" target="_blank">
                <i class="pi pi-linkedin text-light-pink text-2xl" style="box-shadow: 1px 3px 4px rgba(0, 0, 0, 0.3);"></i>
            </a>
            <img :src="anto" alt="Anthony" class="w-[300px] h-[300px] rounded-full m-5 ml-auto mr-auto mt-2">
        </div>
    </div>

    <Dialog v-model:visible="visible" modal header="Edit Profile" class="w-[700px] h-[600px]">
        <span class="text-surface-500 dark:text-surface-400 block mb-8">Update your information.</span>
        <div class="flex items-center gap-4 mb-4">
            <label for="subject" class="font-semibold w-24">Subject</label>
            <InputText v-model="subject" id="subject" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex items-start gap-4 mb-4">
            <label for="body" class="font-semibold w-24">Body</label>
            <Textarea v-model="body" rows="4" cols="65" style="resize:none"></Textarea>
        </div>
        <Button type="button" label="Save" class="right-5 mt-3" style="position:absolute;" @click="onFormSubmit"></Button>
    </Dialog>

</template>

<style scoped>

.container {
    display: flex;  /* This will arrange the cards side by side */
    justify-content: space-between;  /* Space between the cards */
    gap: 50px;  /* Adds a gap between the cards */
    flex-wrap: wrap;  /* Allows the cards to wrap if the screen size is small */
}

.dana {
    width: 500px;
    height: 600px;
    margin-top: 5%;
    margin-left: 8vw;
    margin-right: auto;
    text-align: center;
    background-color: #e7788e !important; 
    border: 5px solid #faccd6 !important;
}

.anto {
    width: 500px;
    height: 600px;
    margin-top: 5%;
    text-align: center;
    background-color: #e7788e !important;
    border: 5px solid #faccd6 !important;
}

.myButton {
    margin-top: 55%;
}

h1 {
    padding-top: 10%;
    font-size: x-large;
    font-weight: 900;
}

.title {
    font-size: 18px;
    font-weight: 400;
}


a {
    font-weight: 400;
    text-decoration: none;
    font-size: 22px;
    color: black;
}


button:hover, a:hover {
    opacity: 0.7;
}

textarea {
    padding: 10px; /* Adjust the padding if needed */
    line-height: 1.5; /* Adjust line height */
    vertical-align: top; /* Align text to the top */
    resize: none; /* To prevent resizing */
    width: 100%;
    height: 100%;
}
</style>