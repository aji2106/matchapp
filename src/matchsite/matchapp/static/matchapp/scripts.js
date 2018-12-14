
///password validation starts
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}



function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;

}


/*function gender() {
    document.getElementById("displayContentG").classList.toggle("show");
}

function age() {
    document.getElementById("displayContentA").classList.toggle("show");

}*/

$(document).ready( function() {
  $('#id_dob').datepicker({
    print("in datepicker")
    format: 'yyyy-mm-dd',
    clearBtn:true,
    endDate:'-18y',

  });
} );

$(document).ready(function () {
    $('#filterByAge').click(function () {
        document.getElementById("displayContentA").classList.toggle("show");

    });
});

$(document).ready(function () {
    $('#agedropdown').click(function () {
        document.getElementById("displayContentG").classList.toggle("show");

    });
});


$(document).ready(function () {
    $("#filter-form").submit(function (event) {

        //validation for age
        if (parseInt($("#range1").val()) > parseInt($("#range2").val())) {
            document.getElementById("range1").className += " decoratedErrorField ";
            $("#messageValidation").html("Please ensure the first age is lower than the second");
        }

        else {
            //remove the validation
            $("#range1").removeClass("decoratedErrorField");
            $("#messageValidation").empty();

            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    'age-min': $('input[name=age-min]').val(),
                    'age-max': $('input[name=age-max]').val(),
                    'gender': $(".gender:checked").val(),
                },
                success: function (data) {
                    var matches = $("#matches")
                    $("#matches").empty();
                    data = JSON.stringify(data)
                    data = JSON.parse(data)
                    var elements = data.split(',')

                    elements.forEach(function (element) {
                        var val = element.replace(/['"]+/g, '')
                        $('#matches').append(val)
                    });

                    let count = matches[0].children.length
                    $(".subtitle").text("You have " + count + " match(es)");
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    $("#messageValidation").html("Please fill in the fields to filter the matches");
                }

            });
        }
        event.preventDefault();
    });
})


$(".drop-down .selected a").click(function () {
    $(".drop-down .options ul").toggle();
});

//SELECT OPTIONS AND HIDE OPTION AFTER SELECTION
$(".drop-down .options ul li a").click(function () {
    var text = $(this).html();
    $(".drop-down .selected a span").html(text);
    $(".drop-down .options ul").hide();
});


//HIDE OPTIONS IF CLICKED ANYWHERE ELSE ON PAGE
$(document).bind('click', function (e) {
    var $clicked = $(e.target);
    if (!$clicked.parents().hasClass("drop-down"))
        $(".drop-down .options ul").hide();
});


//edit profile
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

//refresh matches list
$(document).ready(function () {
    $('#reset_button').click(function () {
        $.ajax({
            type: "GET",
            url: "/similarHobbies/",
            success: function () {
                location.reload();
            }

        })
    });

});


$('#profile-image-upload').click(function () {
    $("#img_file").click();
});



////



////
