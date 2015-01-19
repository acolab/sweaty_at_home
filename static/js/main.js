function AddTimeSlot() {
    // Add line in schedule table
    //============================
    
    i = $("#inhere tbody tr").length
    $("#inhere tbody").append('      <tr> \
        <td><INPUT type="text" name="start_time_' + i + '"></td> \
        <td><INPUT type="text" name="end_time_' + i + '"></td> \
        <td><INPUT type="checkbox" name="monday_' + i + '" value="1"></td> \
        <td><INPUT type="checkbox" name="tuesday_' + i + '" value="1"></td> \
        <td><INPUT type="checkbox" name="wednesday_' + i + '" value="1"></td> \
        <td><INPUT type="checkbox" name="thursday_' + i + '" value="1"></td> \
        <td><INPUT type="checkbox" name="friday_' + i + '" value="1"></td> \
        <td><INPUT type="checkbox" name="saturday_' + i + '" value="1"></td> \
        <td><INPUT type="checkbox" name="sunday_' + i + '" value="1"></td> \
        <td><button type="button" onclick="AddTimeSlot()">+</button></td> \
      </tr>');

} // function AddTimeSlot()

