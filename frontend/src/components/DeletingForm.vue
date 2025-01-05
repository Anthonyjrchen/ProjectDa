<script setup>
import { ref } from 'vue';
import $ from 'jquery';
import Checkbox from 'primevue/checkbox';
import Popover from 'primevue/popover';

let deleteCalendars = ref([{"name":"Backend Not Running Yet.", key:"test"}]);
let deleteCalendarsRemaining = ref([]);
let selectedDeleteCalendars = ref([]); //Need to have Jana selected by default
const allowedCalendars = [] //Add names here that you want to be able to delete from.
const lawyerCalendars = ref([]);
const loading = ref(false);
$.ajax({
    url:'http://127.0.0.1:8000/lawyerCalendars/update',
    type:'get',
    async:false,
    success:function(e){
        lawyerCalendars.value = e
        console.log("Updated lawyer calendars...")
    }
})
$.ajax({
    url:'http://localhost:8000/calendars',
    type:'GET',
    success:function(val) {
        deleteCalendars.value = [{name:"Calendar(jneria@jml.ca)",key:0}];
        for (let i = 0; i < val.calendarList.length; i++) {
            if (lawyerCalendars.value.includes(val.calendarList[i])){
                deleteCalendars.value.push({name:val.calendarList[i], key:i+1})
            } else {
                if(val.calendarList[i]!="Calendar(jneria@jml.ca)"){
                    deleteCalendarsRemaining.value.push({name:val.calendarList[i], key:i+1})
                }
            }
            // if (val[i]==) if val[i](calendarname) == Jana's calendar, add to selectedDeleteCalendars and check her checkbox.
        }
    console.log(deleteCalendars.value)
    }
})


const courtFile = ref('');
const deleteProgress = ref(0);
const deleteTotal = ref(0);
const progressPercentage = ref(0);
function formSubmit(e){
    deleteProgress.value = 0;
    deleteTotal.value = 0;
    progressPercentage.value = 0;
    e.preventDefault();
    console.log("Delete events with caseFileNum: " + courtFile.value)
    loading.value = true;
    $.ajax({
        url: 'http://127.0.0.1:8000/initDelete',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            caseNum: courtFile.value,
            calendars: selectedDeleteCalendars.value,
        }),
        success:function(e){
            loading.value = false;
            let deleteDictKeys = Object.keys(e.deleteDict) //deleteDict = {"calendar_name":128,"calendar2_name":64}
            for (let i = 0; i < deleteDictKeys.length; i++){
                deleteTotal.value+=e.deleteDict[deleteDictKeys[i]].length;
            }

            for (let i = 0; i < deleteDictKeys.length; i++){
                for (var j = e.deleteDict[deleteDictKeys[i]].length-1; j >= 0 ; j--){
                    $.ajax({
                        url: 'http://127.0.0.1:8000/delete',
                        type: 'post',
                        contentType: 'application/json',
                        data: JSON.stringify({
                            calendar: deleteDictKeys[i],
                            curItem: e.deleteDict[deleteDictKeys[i]][j].toString(),
                        }),
                        success:function(e){
                            deleteProgress.value+=1
                            progressPercentage.value = Math.round(deleteProgress.value/deleteTotal.value*100)
                        }
                    });
                }
            }
        }
    });
};
const op = ref();
const members = ref([
    { name: 'Amy Elsner', image: 'amyelsner.png', email: 'amy@email.com', role: 'Owner' },
    { name: 'Bernardo Dominic', image: 'bernardodominic.png', email: 'bernardo@email.com', role: 'Editor' },
    { name: 'Ioni Bowcher', image: 'ionibowcher.png', email: 'ioni@email.com', role: 'Viewer' }
]);

const toggle = (event) => {
    console.log('hi')
    op.value.toggle(event);
}
</script>

<template>
    <head>
        <link href="./output.css" rel="stylesheet">
    </head> 
    <form v-on:submit.prevent="formSubmit">
        <h1 class="text-3xl font-bold">Deleting</h1>
        <div class="container">
            <div class="subContainer">
                <div class="courtFileNumInput">
                    <h2>Court File No.</h2>
                    <input type="text" name="courtFile" v-model="courtFile" class="p-1.5 !border-[1px] !border-brink-pink text-dark-gray !rounded-md focus:outline-none focus:ring-1 focus:ring-white bg-rose-bud" required />
                </div>
                <div class="mt-3">
                    <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea" type="submit">Delete</button>
                    <Transition>
                        <div class="mt-2" v-if="!loading">Progress: {{ deleteProgress }}/{{ deleteTotal }}</div>
                    </Transition>

                    <Transition>
                        <div v-if="!loading"><ProgressBar :value="progressPercentage" :class="'custom-progress-bar'"></ProgressBar></div>
                    </Transition>

                    <Transition>
                        <div class="mt-3" v-if="loading">Progress: <i class="pi pi-spin pi-spinner"></i></div>
                    </Transition>
                </div>
            </div>

            <div class="calendars">
                <h2 class="mt-2">Choose which calendar(s)</h2>
                <div class="card flex justify-left">
                    <div class="flex flex-col gap-2" id="calendarList">
                        <div v-for="deleteCalendar of deleteCalendars" :key="deleteCalendar.key" class="flex items-center gap-2">
                            <Checkbox class="deleteCalendarCheckbox" v-model="selectedDeleteCalendars" :inputId="deleteCalendar.key" name="deleteCalendar" :value="deleteCalendar.name" />
                            <label :for="deleteCalendar.key">{{ deleteCalendar.name }}</label>
                        </div>
                    </div>
                </div>
                
                <button class="border-[1px] border-dark-white px-3 py-1.5 rounded-md hover:bg-azalea mt-3" type="button" v-on:click="toggle" style="display:flex;align-items: center;gap:5px;">
                    <i class="pi pi-bars"></i> Other calendar(s)
                </button>
                <Popover ref="op">
                    <div class="flex flex-col gap-2" id="calendarListRemaining">
                        <div v-for="deleteCalendar of deleteCalendarsRemaining" :key="deleteCalendar.key" class="flex items-center gap-2">
                            <Checkbox class="deleteCalendarCheckbox" v-model="selectedDeleteCalendars" :inputId="deleteCalendar.key" name="deleteCalendar" :value="deleteCalendar.name" />
                            <label :for="deleteCalendar.key">{{ deleteCalendar.name }}</label>
                        </div>
                    </div>
                </Popover>
            </div>
        </div>

        
    </form>
</template>

<style scoped>

h2 {
    margin-top: 10px;
    color: #fadbe1;
}

.container {
  display: flex;
  box-sizing: border-box;
  gap: 300px;
}

.p-progressbar {
    border: 2px solid #fb607f !important;
    background-color: #272526 !important;
    width: 186px;
    height: 25px;
}

.p-progressbar-value {
    background-color: #fb607f !important;
    width: 186px;
    transition: width 0.05s ease; /* Smooth transition */
}


</style>