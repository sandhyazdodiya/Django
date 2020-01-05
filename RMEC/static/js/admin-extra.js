$(document).ready(function() {

    $("#form-submit").on("click", function() {
        var firstnameData = $("#firstname").val();
        var lastnameData = $("#lastname").val();
        var docNoData = $("#docNo").val();
        var correctionalFacilityData = $("#correctionalFacility").val();
        var homeAddressData = $("#homeAddress").val();
        var cityData = $("#city").val();
        var stateData = $("#state").val();
       
        var zipCodeData = $("#zipCode").val();
        var phoneData = $("#phone").val();
        var emailData = $("#email").val();

        var educationData = $("#education").val();
        var certificateData = $("#certificate").val().toString().replace(/,/g, ' ');
        var workAreaData = $("#workArea").val().toString().replace(/,/g, ' ');

        var ishiredData = $("#job_status").val();
        var hiredDateFromData = $("#hiredDateFrom").val();
        var hiredDateToData = $("#hiredDateTo").val();
        // var createdDateData = $("#createdDate").val();
        // var updatedDateData = $("#updatedDate").val();


        //  alert(firstnameData);
        //  alert(lastnameData);
        //  alert(docNoData);
        //  alert(correctionalFacilityData);
        //  alert(homeAddressData);
        //  alert(cityData);
        //  alert(zipCodeData);
        //  alert(emailData);

        //  alert(educationData);
        //  alert(certificateData);
        //  alert(workAreaData);
        //alert(ishiredData);
        // alert(hiredDateFromData);
        // alert(hiredDateToData);
        //  alert(createdDateData);
        //  alert(updatedDateData);
        if (firstnameData != "") {

            $('#send').append("<input type='text' name='first_name' value='" + firstnameData + "' />");
        }

        if (lastnameData != "") {

            $('#send').append("<input type='text' name='last_name' value='" + lastnameData + "' />");
        }
        if (docNoData != "") {

            $('#send').append("<input type='text' name='doc_no' value='" + docNoData + "' />");
        }

        if (correctionalFacilityData != "") {
            $('#send').append("<input type='text' name='correctional_facility' value='" + correctionalFacilityData + "' />");
        }
        if (homeAddressData != "") {

            $('#send').append("<input type='text' name='home_address' value='" + homeAddressData + "' />");
        }

        if (cityData != "") {

            $('#send').append("<input type='text' name='city' value='" + cityData + "' />");
        }
        if (stateData != "") {

            $('#send').append("<input type='text' name='state' value='" + stateData + "' />");
        }
        if (zipCodeData != "") {

            $('#send').append("<input type='text' name='zip_code' value='" + zipCodeData + "' />");
        }

        if (phoneData != "") {
            $('#send').append("<input type='text' name='phone' value='" + phoneData + "' />");
        }
        if (emailData != "") {

            $('#send').append("<input type='text' name='email' value='" + emailData + "' />");
        }


        if (educationData != "") {

            $('#send').append("<input type='text' name='education' value='" + educationData + "' />");
        }

        if (certificateData != "") {
            $('#send').append("<input type='text' name='certificate' value='" + certificateData + "' />");
        }
        if (workAreaData != "") {

            $('#send').append("<input type='text' name='work_area' value='" + workAreaData + "' />");
        }

        if (ishiredData != "") {

            $('#send').append("<input type='text' name='job_status' value='" + ishiredData + "' />");
        }
        if (hiredDateFromData != "") {

            $('#send').append("<input type='text' name='hired_date__range__gte' value='" + hiredDateFromData + "' />");
        }
        if (hiredDateToData != "") {

            $('#send').append("<input type='text' name='hired_date__range__lte' value='" + hiredDateToData + "' />");
        }

       
        $("#send").submit();
    });
    $(".addlink").html("Add participants");
    $(".colM h1").html("Add participants");
});