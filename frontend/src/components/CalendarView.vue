<script setup>
import { ref, inject, watch } from 'vue';
import $ from 'jquery';
const selectedDate = inject('selectedDate');
function calcDates() {
    console.log("Calculating new dates")
    $.ajax({
        url:"http://127.0.0.1:8000/calcDates",
        type:"get",
        data:{
            year:selectedDate.value.split("-")[0],
            month:selectedDate.value.split("-")[1],
            day:selectedDate.value.split("-")[2],
        },
        success: function(dates) {
            console.log("Received dates: " + dates)
            document.getElementById('ntmf1_due').innerText = dates["date1"]
            document.getElementById('er_due').innerText = dates["date2"]
            document.getElementById('efd_due').innerText = dates["date3"]
            document.getElementById('tbf41_due1').innerText = dates["date4"]
            document.getElementById('tbf41_due2').innerText = dates["date5"]
            document.getElementById('ntaf23_due').innerText = dates["date6"]
            document.getElementById('rr_due').innerText = dates["date7"]
            document.getElementById('tmc_due').innerText = dates["date8"]
            document.getElementById('noo_due').innerText = dates["date9"]
            document.getElementById('tr_due').innerText = dates["date10"]
            document.getElementById('tcf42_due').innerText = dates["date11"]
            document.getElementById('noe_due').innerText = dates["date12"]
            document.getElementById('iopetc_due').innerText = dates["date13"]
            document.getElementById('ntpf43_due').innerText = dates["date14"]

            document.getElementById('ntmf1_rm1').innerText = dates["rm1_date1"]
            document.getElementById('ntmf1_rm2').innerText = dates["rm2_date1"]
            document.getElementById('ntmf1_rm3').innerText = dates["rm3_date1"]
            document.getElementById('ntmf1_rm4').innerText = dates["rm4_date1"]

            document.getElementById('er_rm1').innerText = dates["rm1_date2"]
            document.getElementById('er_rm2').innerText = dates["rm2_date2"]
            document.getElementById('er_rm3').innerText = dates["rm3_date2"]
            document.getElementById('er_rm4').innerText = dates["rm4_date2"]

            document.getElementById('efd_rm1').innerText = dates["rm1_date3"]
            document.getElementById('efd_rm2').innerText = dates["rm2_date3"]
            document.getElementById('efd_rm3').innerText = dates["rm3_date3"]
            document.getElementById('efd_rm4').innerText = dates["rm4_date3"]
            document.getElementById('efd_rm5').innerText = dates["rm5_date3"]

            document.getElementById('tbf41_rm1').innerText = dates["rm1_date4"]
            document.getElementById('tbf41_rm2').innerText = dates["rm2_date4"]

            document.getElementById('tbf41_rm3').innerText = dates["rm1_date5"]
            document.getElementById('tbf41_rm4').innerText = dates["rm2_date5"]

            document.getElementById('ntaf23_rm1').innerText = dates["rm1_date6"]
            document.getElementById('ntaf23_rm2').innerText = dates["rm2_date6"]
            document.getElementById('ntaf23_rm3').innerText = dates["rm3_date6"]
            document.getElementById('ntaf23_rm4').innerText = dates["rm4_date6"]
            
            document.getElementById('rr_rm1').innerText = dates["rm1_date7"]
            document.getElementById('rr_rm2').innerText = dates["rm2_date7"]
            document.getElementById('rr_rm3').innerText = dates["rm3_date7"]
            document.getElementById('rr_rm4').innerText = dates["rm4_date7"]

            document.getElementById('tmc_rm1').innerText = dates["rm1_date8"]
            document.getElementById('tmc_rm2').innerText = dates["rm2_date8"]
            document.getElementById('tmc_rm3').innerText = dates["rm3_date8"]
            document.getElementById('tmc_rm4').innerText = dates["rm4_date8"]
            document.getElementById('tmc_rm5').innerText = dates["rm5_date8"]
            document.getElementById('tmc_rm6').innerText = dates["rm6_date8"]

            document.getElementById('noo_rm1').innerText = dates["rm1_date9"]
            document.getElementById('noo_rm2').innerText = dates["rm2_date9"]
            document.getElementById('noo_rm3').innerText = dates["rm3_date9"]
            document.getElementById('noo_rm4').innerText = dates["rm4_date9"]

            document.getElementById('tr_rm1').innerText = dates["rm1_date10"]
            document.getElementById('tr_rm2').innerText = dates["rm2_date10"]
            document.getElementById('tr_rm3').innerText = dates["rm3_date10"]

            document.getElementById('tcf42_rm1').innerText = dates["rm1_date11"]
            document.getElementById('tcf42_rm2').innerText = dates["rm2_date11"]
            document.getElementById('tcf42_rm3').innerText = dates["rm3_date11"]

            document.getElementById('noe_rm1').innerText = dates["rm1_date12"]
            document.getElementById('noe_rm2').innerText = dates["rm2_date12"]
            document.getElementById('noe_rm3').innerText = dates["rm3_date12"]
            
            document.getElementById('iopetc_rm1').innerText = dates["rm1_date13"]
            document.getElementById('iopetc_rm2').innerText = dates["rm2_date13"]
            document.getElementById('iopetc_rm3').innerText = dates["rm3_date13"]

            document.getElementById('ntpf43_rm1').innerText = dates["rm1_date14"]
            document.getElementById('ntpf43_rm2').innerText = dates["rm2_date14"]
            document.getElementById('ntpf43_rm3').innerText = dates["rm3_date14"]
        }
    })
}
watch(selectedDate, (newVal, oldVal) => {
    console.log("change detected")
    calcDates();
});
</script>

<template>
    <!-- add icons -->
    <div class="table-container">
        <table class="scrollable-table">
            <thead class="bg-brink-pink text-light-pink">
                <tr class="headers">
                    <th>Form Name</th>
                    <th>Due Date</th>
                    <th>Reminder Dates</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <td>
                    <h3>NOTICE TO MEDIATE, FORM 1</h3>
                    <p>Must serve no later than 120 days before scheduled trial date</p>
                </td>
                <td id="ntmf1_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="ntmf1_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="ntmf1_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="ntmf1_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 day</td>
                                <td id="ntmf1_rm4">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td> 
                </tr>
                <tr>
                <td>
                    <h3>EXPERT'S REPORT</h3>
                    <p>Must serve at least 84 days before scheduled trial date</p>
                </td>
                <td id="er_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="er_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="er_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="er_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 day</td>
                                <td id="er_rm4">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>EXAMINATIONS FOR DISCOVERY</h3>
                    <p>*internal deadline* must be held at least 60 days before scheduled trial date</p>
                </td>
                <td id="efd_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>2 months</td>
                                <td id="efd_rm1">...</td>
                            </tr>
                            <tr>
                                <td>1 month</td>
                                <td id="efd_rm2">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="efd_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="efd_rm4">...</td>
                            </tr>
                            <tr>
                                <td>1 day</td>
                                <td id="efd_rm5">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>TRIAL BRIEF, FORM 41</h3>
                    <p>Must serve at least 56 days before scheduled trial date</p>
                </td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>Plaintiff Due</td>
                                <td id="tbf41_due1">...</td>
                            </tr>
                            <tr>
                                <td>Defendant Due</td>
                                <td id="tbf41_due2">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="tbf41_rm1">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="tbf41_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 month</td>
                                <td id="tbf41_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="tbf41_rm4">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE TO ADMIT, FORM 23</h3>
                    <p>Must serve at least 56 days before scheduled trial date</p>
                </td>
                <td id="ntaf23_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="ntaf23_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="ntaf23_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="ntaf23_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 day</td>
                                <td id="ntaf23_rm4">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>RESPONDING REPORTS</h3>
                    <p>Must serve at least 42 days before scheduled trial date</p>
                </td>
                <td id="rr_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="rr_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="rr_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="rr_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 day</td>
                                <td id="rr_rm4">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>TRIAL MANAGEMENT CONFERENCE</h3>
                    <p>Must be held at least 28 days before scheduled trial date</p>
                </td>
                <td id="tmc_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>4 months</td>
                                <td id="tmc_rm1">...</td>
                            </tr>
                            <tr>
                                <td>3 months</td>
                                <td  id="tmc_rm2">...</td>
                            </tr>
                            <tr>
                                <td>2 months</td>
                                <td id="tmc_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 month</td>
                                <td id="tmc_rm4">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="tmc_rm5">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="tmc_rm6">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE OF OBJECTION</h3>
                    <p>Must be served on the earlier date of the TMC and 21 days before scheduled trial date</p>
                </td>
                <td id="noo_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="noo_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="noo_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="noo_rm3">...</td>
                            </tr>
                            <tr>
                                <td>1 day</td>
                                <td id="noo_rm4">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>TRIAL RECORD</h3>
                    <p>Must be filed by party who filed the Notice of Trial at least 14 days before but not more than 28 days before scheduled trial date</p>
                </td>
                <td id="tr_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="tr_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="tr_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="tr_rm3">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>TRIAL CERTIFICATE, FORM 42</h3>
                    <p>Must be filed by all parties at least 14 days before but not more than 28 days before scheduled trial date</p>
                </td>
                <td id="tcf42_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="tcf42_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="tcf42_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="tcf42_rm3">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE OF EXAMINATION</h3>
                    <p>Must be served at least 7 days before the scheduled date of examination</p>
                </td>
                <td id="noe_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="noe_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="noe_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="noe_rm3">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>INSPECTION OF PHOTOGRAPHS, ETC.</h3>
                    <p>*internal deadline* at least 7 days before scheduled trial date</p>
                </td>
                <td id="iopetc_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="iopetc_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="iopetc_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="iopetc_rm3">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE TO PRODUCE, FORM 43</h3>
                    <p>Must be served at least 2 days before scheduled trial date</p>
                </td>
                <td id="ntpf43_due">...</td>
                <td>
                    <table>
                        <tbody>
                            <tr>
                                <td>1 month</td>
                                <td id="ntpf43_rm1">...</td>
                            </tr>
                            <tr>
                                <td>2 weeks</td>
                                <td id="ntpf43_rm2">...</td>
                            </tr>
                            <tr>
                                <td>1 week</td>
                                <td id="ntpf43_rm3">...</td>
                            </tr>
                        </tbody>
                    </table>
                </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>

h3 {
    font-weight: bolder;
}

.headers:hover {
    background-color: #fb607f;
}

tr:hover {
    background-color: black;
}

th {
    padding: 0.5rem 1rem;
    text-align: center;
    font-weight: 900;
}

p {
    font-size: small;
    color:#f9e6ea;
}

.table-container {
    width: 100%;
    max-width: 100%;
    overflow-x: auto;
    overflow-y: auto;
    height: 800px; /* Fixed height for scrolling */
}

/* .table-container thead {
    position:sticky;
    top:0;
    
    border: 1px solid #fb607f !important;
    border-top-left-radius: 7px !important;
    border-top-right-radius: 7px !important;
} */

.scrollable-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;   
}

.scrollable-table thead {
    position: sticky;
    top:0;
    /* border: 2px solid #fb607f !important; */
}

.scrollable-table th {
    padding: 8px;
    text-align: left;
    border-right: 1px solid #faa1af !important;
}

.scrollable-table td {
    padding: 8px;
    text-align: left;
    /* border: 1px solid #faa1af !important; */
    border-bottom: 1px solid #faa1af !important;
    border-right: 1px solid #faa1af !important;
    border-left: 1px solid #faa1af !important;
    border-top: 1px solid #faa1af !important;
}


/* for responsive design */
@media (max-width: 1024px) {
    .table-container {
        flex: 3; /* Reduces space given to calendarView on medium screens */
        max-width: 700px;
    }

    .scrollable-table th, .scrollable-table td {
        white-space: normal;
    }
}

@media (max-width: 800px) {
    .table-container {
        max-height: 100%; /* Reduce height on smaller screens */
        max-width: 35%;
    }
}

@media (max-width: 768px) {
    .table-container {
        max-height: 100%; /* Reduce height on smaller screens */
        max-width: 35%;
    }

    /* Allow table columns to wrap on smaller screens */
    .scrollable-table th, .scrollable-table td {
        white-space: normal;
    }
} 

table h3::before {
    font-family: 'PrimeIcons';
    content: '\e958'; /* Use a Unicode character or icon */
    margin-right: 8px; /* Spacing between icon and text */
    color: #fb607f; /* Optional styling for the icon */
    font-size: 1.5em; /* Adjust icon size */
}
 
</style>