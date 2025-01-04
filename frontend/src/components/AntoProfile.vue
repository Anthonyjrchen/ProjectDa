<script setup>

import { ref } from 'vue';


</script>

<template>
    <div class="container">
        <div class="dana">
            <h1 class="name text-light-pink">Dana Angela Neria</h1>
            <p class="title text-light-pink">Co-Developer</p>
            <p class="text-light-pink">University of British Columbia</p>
            <a href="#"><i class="fa fa-linkedin"></i></a>
            <p><button class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea bg-azalea">Contact</button></p>
        </div>

        <div class="anto">
            <h1 class="name text-light-pink">Anthony Chen</h1>
            <p class="title text-light-pink">Co-Developer</p>
            <p class="text-light-pink">University of British Columbia</p>
            <a href="#"><i class="fa fa-linkedin"></i></a>
            <p><button class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea bg-azalea">Contact</button></p>
        </div>
    </div>
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