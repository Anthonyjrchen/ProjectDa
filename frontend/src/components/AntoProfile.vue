<script setup>

import { ref } from 'vue';
import Dialog from 'primevue/dialog';
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
    <div class="container">
        <div class="dana">
            <h1 class="name text-light-pink">Dana Angela Neria</h1>
            <p class="title text-light-pink">Co-Developer</p>
            <p class="text-light-pink">University of British Columbia</p>
            <a href="#"><i class="fa fa-linkedin"></i></a>
            <p><button @click="visible = true" class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea bg-azalea">Contact</button></p>
        </div>

        <div class="anto">
            <h1 class="name text-light-pink">Anthony Chen</h1>
            <p class="title text-light-pink">Co-Developer</p>
            <p class="text-light-pink">University of British Columbia</p>
            <a href="#"><i class="fa fa-linkedin"></i></a>
            <p><button @click="visible = true" class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea bg-azalea">Contact</button></p>
        </div>
    </div>

    <Dialog v-model:visible="visible" modal header="Edit Profile" class="w-[700px] h-[600px]">
        <span class="text-surface-500 dark:text-surface-400 block mb-8">Update your information.</span>
        <div class="flex items-center gap-4 mb-4">
            <label for="subject" class="font-semibold w-24">Subject</label>
            <InputText v-model="subject" id="subject" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4" mb-4>
            <label for="body" class="font-semibold w-24">Body</label>
            <InputText v-model="body" id="body" class="flex-auto" autocomplete="off" />
        </div>
        <Button type="button" label="Save" class="right-5 mt-3" style="position:absolute;" @click="onFormSubmit"></Button>
    </Dialog>

</template>

<style scoped>

.container {
    display: flex;  /* This will arrange the cards side by side */
    justify-content: space-between;  /* Space between the cards */
    gap: 100px;  /* Adds a gap between the cards */
    flex-wrap: wrap;  /* Allows the cards to wrap if the screen size is small */
}

.dana {
    width: 500px;
    height: 600px;
    margin-top: 10%;
    margin-left: 11vw;
    text-align: center;
    background-color: #e7788e !important;
}

.anto {
    width: 500px;
    height: 600px;
    margin-top: 10%;
    text-align: center;
    background-color: #e7788e !important;
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

button {
    margin-top: 75%;
}

button:hover, a:hover {
    opacity: 0.7;
}
</style>