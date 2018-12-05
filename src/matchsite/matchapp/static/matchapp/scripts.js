
///password validation starts
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}


function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

$(document).ready(function () {

    $("#update_button").click(function (event) {
        event.preventDefault();
        email = $('#email').text()
        dob = $('#dob').text()
        gender = $('#gender').text()
        hobbies = $('#hobbies').text()


        $.ajax({
            type: "PUT",
            data:
            {
                email: email,
                dob: dob,
                gender: gender,
                hobbies: hobbies,

            },
            url: "/editProfile/",
            dataType: 'application/json',
            success: function (data) {
                data = JSON.stringify(data)
                data = JSON.parse(data)
                $("#email").html(data.email)
                $("#dob").html(data.dob)
                $("#gender").html(data.gender)
                $("#hobbies").html(data.hobbies)
            }

        })

    });

})
$('#profile-image-upload').click(function () {
    $("#img_file").click();
});
/////datepicket displayProfile
$( document ).ready(function() {
  $("#from-datepicker").datepicker({
    format: 'yyyy-mm-dd'

  });
  $("#from-datepicker").on("change", function () {
    var fromdate = $(this).val();
    alert(fromdate);
  });
});


      $(function () {
          $("#slider-range").slider({
              range: true,
              min: 16,
              max: 50,
              values: [21, 30],
              slide: function (event, ui) {
                  console.log($("#age").val());
                  var ageValue = getSecondPart($("#age").val());
                  if (ui.values[1] == '50') {
                      if (ageValue == ' 49' || ageValue == ' 50+') {
                          $("#age").val(ui.values[0] + " - " + "50+");
                      }
                  }
                  else {
                      $("#age").val(ui.values[0] + " - " + ui.values[1]);
                  }
              }
          });

          $("#age").val($("#slider-range").slider("values", 0) +
            " - " + $("#slider-range").slider("values", 1));
      });
      
      function getSecondPart(str) {
          return str.split('-')[1];
      }



////datepicker displayProfile
