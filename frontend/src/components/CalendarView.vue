<script setup>
import { ref } from 'vue';
import $ from 'jquery';
</script>

<template>
    <div class="table-container">
        <table class="scrollable-table">
            <thead>
                <th>Form Name</th>
                <th>Due Date</th>
                <th>Reminder Dates</th>
            </thead>
            <tbody>
                <tr>
                <td>
                    <h3>NOTICE TO MEDIATE, FORM 1</h3>
                    <p>Must serve no later than 120 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 day</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td> 
                </tr>
                <tr>
                <td>
                    <h3>EXPERT'S REPORT</h3>
                    <p>Must serve at least 84 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 day</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>EXAMINATIONS FOR DISCOVERY</h3>
                    <p>*internal deadline* must be held at least 60 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>2 months</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 day</td>
                            <td>...</td>
                        </tr>
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
                        <tr>
                            <td>Plaintiff Due</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>OP Due</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE TO ADMIT, FORM 23</h3>
                    <p>Must serve at least 56 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 day</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>RESPONDING REPORTS</h3>
                    <p>Must serve at least 42 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 day</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>TRIAL MANAGEMENT CONFERENCE</h3>
                    <p>Must be held at least 28 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>4 months</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>3 months</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 months</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE OF OBJECTION</h3>
                    <p>Must be served on the earlier date of the TMC and 21 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 day</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>TRIAL RECORD</h3>
                    <p>Must be filed by party who filed the Notice of Trial at least 14 days before but not more than 28 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>TRIAL CERTIFICATE, FORM 42</h3>
                    <p>Must be filed by all parties at least 14 days before but not more than 28 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE OF EXAMINATION</h3>
                    <p>Must be served at least 7 days before the scheduled date of examination</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>INSPECTION OF PHOTOGRAPHS, ETC.</h3>
                    <p>*internal deadline* at least 7 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
                <tr>
                <td>
                    <h3>NOTICE TO PRODUCE, FORM 43</h3>
                    <p>Must be served at least 2 days before scheduled trial date</p>
                </td>
                <td>...</td>
                <td>
                    <table>
                        <tr>
                            <td>1 month</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>2 weeks</td>
                            <td>...</td>
                        </tr>
                        <tr>
                            <td>1 week</td>
                            <td>...</td>
                        </tr>
                    </table>
                </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>

tr:hover {
    background-color: #1f1f20;
}

th {
    border: 1px solid #52525b;
    padding: 0.5rem 1rem;
    text-align: center;
    font-weight: 900;
}

td {
    border: 1px solid #52525b;
    padding: 0.5rem 1rem; 
    text-align: center; 
}

p {
    font-size: small;
    color:#75757c;
}

.table-container {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  overflow-y: auto;
  height: 800px; /* Fixed height for scrolling */
}

.scrollable-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
}

.scrollable-table th, .scrollable-table td {
  padding: 8px;
  text-align: left;
}

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

 
</style>