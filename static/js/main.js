function AddTimeSlot(value) {
    // Add line in schedule table
    //============================
    if(typeof(value)==='undefined') value = ["", "", "", "", "", "", "", "", ""];
    
    i = $("#inhere tbody tr").length
    $("#inhere tbody").append('      <tr> \
        <td><INPUT type="text" name="start_time_' + i + '" value = "' + value[0] + '" placeholder="hh:mm:ss"></td> \
        <td><INPUT type="text" name="end_time_' + i + '" value = "' + value[1] + '" placeholder="hh:mm:ss"></td> \
        <td><INPUT type="checkbox" name="monday_' + i + '" value="1" ' + (value[2]? "Checked":"") + '></td> \
        <td><INPUT type="checkbox" name="tuesday_' + i + '" value="1" ' + (value[3]? "Checked":"") + '></td> \
        <td><INPUT type="checkbox" name="wednesday_' + i + '" value="1" ' + (value[4]? "Checked":"") + '></td> \
        <td><INPUT type="checkbox" name="thursday_' + i + '" value="1" ' + (value[5]? "Checked":"") + '></td> \
        <td><INPUT type="checkbox" name="friday_' + i + '" value="1" ' + (value[6]? "Checked":"") + '></td> \
        <td><INPUT type="checkbox" name="saturday_' + i + '" value="1" ' + (value[7]? "Checked":"") + '></td> \
        <td><INPUT type="checkbox" name="sunday_' + i + '" value="1" ' + (value[8]? "Checked":"") + '></td> \
        <td><button type="button" onclick="AddTimeSlot()"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button></td> \
      </tr>');

} // function AddTimeSlot()

