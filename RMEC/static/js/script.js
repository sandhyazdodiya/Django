$(document).ready(function() {
    // $(".filter-btn").on("click", function() {
    //     $('.filter-form').toggle("slow");
    // });
    $(".remove").on("click", function() {
        remove_pID = $(this).parent().attr('class');

        $("#" + remove_pID).val("");

        $('.add_from').submit();

    });

    x = $(window).height();
    $("#t-height").height(x - 175);
    $(".fa-angle-right").attr('title', 'Next');
    $(".fa-angle-left").attr('title', 'Previous');

    $("#from-bind").keyup(function() {
        $("#to-bind").val($("#from-bind").val());




    });
    $(".confirm-hire").on("click", function() {
        alert("Are you sure you want to update job status?");

    });
    $(".confirm-unhire").on("click", function() {
        alert("Are you sure you want to update job status?");

    });
    $(".signup").on("click", function(event) {


        function randomPassword(length) {
            var chars = "abcdefghijklmnopqrstuvwxyz@ABCDEFGHIJKLMNOP1234567890";
            var pass = "";
            for (var x = 0; x < length; x++) {
                var i = Math.floor(Math.random() * chars.length);
                pass += chars.charAt(i);
            }
            return pass;
        }

        event.preventDefault();
        var random_password = randomPassword(8);
        $("#set_password1").val(random_password);
        $("#set_password2").val(random_password);


        $(".rform").submit();


    });

    $(".update_form div div input").addClass("form-control")


});