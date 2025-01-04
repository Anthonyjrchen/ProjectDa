<script setup>
import { ref, watch } from 'vue';
import Textarea from 'primevue/textarea';
import $ from 'jquery';
import Button from 'primevue/button';
import { ButtonStyle } from 'primevue';
const holidaysText = ref('');
const ignoredCalendersText = ref('');
const lawyerCalendarsText = ref('');
const holidaysTextOld = ref('');
const ignoredCalendersTextOld = ref('');
const lawyerCalendarsTextOld = ref('');
const isSaveButtonDisabled = ref(true);
function processTexts(e) {
    holidaysText.value = e.holidays
    ignoredCalendersText.value = e.ignoredCalendars
    lawyerCalendarsText.value = e.lawyerCalendars
    holidaysTextOld.value = e.holidays
    ignoredCalendersTextOld.value = e.ignoredCalendars
    lawyerCalendarsTextOld.value = e.lawyerCalendars
    watch([holidaysText, ignoredCalendersText, lawyerCalendarsText], ([newHolidays, newIgnored, newLawyers], [oldHolidays, oldIgnored, oldLawyers]) => {
    if (newHolidays !== oldHolidays || newIgnored !== oldIgnored || newLawyers !== oldLawyers) {
        document.getElementById("saveButton").disabled = false;
    }
    });
    
    watch([holidaysText, ignoredCalendersText, lawyerCalendarsText], ([newHolidays, newIgnored, newLawyers], [oldHolidays, oldIgnored, oldLawyers]) => {
    if (newHolidays == holidaysTextOld.value && newIgnored == ignoredCalendersTextOld.value && newLawyers == lawyerCalendarsTextOld.value) {
    document.getElementById("saveButton").disabled = true;
    }
    });
}

function updateTexts() {
    $.ajax({
        url:'http://localhost:8000/settings',
        type:'get',
        success:function(e) {
            processTexts(e);
        },
    });
}
updateTexts();

function resetTexts() {
    holidaysText.value = holidaysTextOld.value;
    ignoredCalendersText.value = ignoredCalendersTextOld.value;
    lawyerCalendarsText.value = lawyerCalendarsTextOld.value;
}

function saveTexts() {
    $.ajax({
        url:'http://localhost:8000/settings/update',
        type:'get',
        data: {
            holidays:holidaysText.value,
            ignoredCalendars:ignoredCalendersText.value,
            lawyerCalendars:lawyerCalendarsText.value,
        },
        success:function(e) {
            updateTexts();
        }
    });
    // console.log(ignoredCalendersText.value + " :::: and the type is " + typeof(ignoredCalendersText.value))
}

</script>

<template>
    <div class="grid">
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1>
                    Holidays (YYYY-MM-DD)
                </h1>
            </div>
            <Textarea v-model="holidaysText" rows="20" cols="20"></Textarea>
        </div>
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1>
                    Ignored Calendars
                </h1>
            </div>
            <Textarea v-model="ignoredCalendersText" rows="20" cols="20"></Textarea>
        </div>
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1>
                    Lawyers
                </h1>
            </div>
            <Textarea v-model="lawyerCalendarsText" rows="20" cols="20"></Textarea>
        </div>
    </div>
    <div class="buttonWrap">
        <button class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea" @click="resetTexts">Cancel</button>
        <Button :disabled="isSaveButtonDisabled" id="saveButton" class="border-[1px] !border-sweet-pink px-3 py-1.5 rounded-md !bg-azalea" @click="saveTexts">Save Changes</Button>
    </div>
</template>

<style scoped>
.grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
    width: 79.5vw;
    height: 90vh;
   }

.col {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
}

h1 {
    font-size: x-large;
    margin-bottom: 10px; /* Adds some space below the header */
}

textarea {
    resize: none;
    width: 100%;
    height: 100%;
}

.buttonWrap {
    display: flex;
    gap: 10px;
    position: absolute;
    right: 20px; /* Adjust to position horizontally */
    bottom: 20px; /* Adjust for vertical positioning */
}
</style>