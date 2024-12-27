<script setup>
import { ref } from 'vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Checkbox from 'primevue/checkbox';

const date = ref(null);
const eventName = ref('');

const categories = ref([
{name: "Calendar 1", key: "A"},
{name: "Calendar 2", key: "B"},
{name: "Calendar 3", key: "C"},
{name: "Calendar 4", key: "D"}
]);

const selectedCategories = ref(['']);

</script>

<template>
    <form>
        <h1>Adding</h1>
        <h2>Date of event</h2>
        <VueDatePicker v-model="date" class="datepicker"></VueDatePicker>
        <h2>Name of event</h2>
        <input type="text" v-model="eventName" required />
        <h2>Choose which calendar/s</h2>
        <div class="card flex justify-center">
            <div class="flex flex-col gap-4">
                <div v-for="category of categories" :key="category.key" class="flex items-center gap-2">
                    <Checkbox class="calendarCheckbox" v-model="selectedCategories" :inputId="category.key" name="category" :value="category.name" />
                    <label :for="category.key">{{ category.name }}</label>
                </div>
            </div> 
        </div>

        <button class="submit" type="submit">Add item</button>
    </form>
</template>

<style scoped>

button {
    font-family: inherit;
}

.datepicker {
    width: 150px;
    height: 40px;
}

.submit {
    margin-top: 10px;
}
</style>