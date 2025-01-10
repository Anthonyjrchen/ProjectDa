<script setup>
import { ref, watch } from 'vue';
import Textarea from 'primevue/textarea';
import $ from 'jquery';
import Button from 'primevue/button';
import { ButtonStyle } from 'primevue';
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
const holidaysText = ref('');
const ignoredCalendersText = ref('');
const lawyerCalendarsText = ref('');
const holidaysTextOld = ref('');
const ignoredCalendersTextOld = ref('');
const lawyerCalendarsTextOld = ref('');
const isSaveButtonDisabled = ref(true);
const confirm = useConfirm();
const toast = useToast();

const confirm1 = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to proceed?',
        icon: 'pi pi-exclamation-triangle',
        rejectProps: {
            label: 'Cancel',
            severity: 'secondary',
            outlined: true
        },
        acceptProps: {
            label: 'Save'
        },
        accept: () => {
            saveTexts()
            toast.add({ severity: 'info', summary: 'Saved', detail: 'Changes saved.', life: 3000 });
        },
        reject: () => {
            //doesn't save texts
            toast.add({ severity: 'error', summary: 'Cancelled', detail: 'Did not save changes.', life: 3000 });
        }
    });
};

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
}

</script>

<template>
    <div class="grid">
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1 class="m-0">
                    Holidays 
                </h1>
                <p class="m-0">(YYYY-MM-DD)</p>
            </div>
            <Textarea v-model="holidaysText" rows="20" cols="20" spellcheck="false"></Textarea>
        </div>
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1 class="m-0">
                    Ignored Calendars
                </h1>
                <p class="m-0">(Calendar Display Name)</p>
            </div>
            <Textarea v-model="ignoredCalendersText" rows="20" cols="20" spellcheck="false"></Textarea>
        </div>
        <div class="col">
            <div class="text-center p-3 border-round-sm bg-azalea font-bold mb-[20px] mt-[15px]">
                <h1 class="m-0">
                    Lawyers
                </h1>
                <p class="m-0">(Calendar Display Name)</p>
            </div>
            <Textarea v-model="lawyerCalendarsText" rows="20" cols="20" spellcheck="false"></Textarea>
        </div>
    </div>
    <div class="buttonWrap">
        <button class="border-[1px] border-sweet-pink px-3 py-1.5 rounded-md hover:bg-azalea" @click="resetTexts">Reset Changes</button>
        <Toast />
        <ConfirmDialog class="pt-5"></ConfirmDialog>
        <Button :disabled="isSaveButtonDisabled" id="saveButton" class="border-[1px] !border-sweet-pink px-3 py-1.5 rounded-md !bg-azalea !text-brink-pink" @click="confirm1($event)">Save Changes</Button>
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