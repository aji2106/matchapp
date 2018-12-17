$(function () {
    $("#slider-range").slider({
        range: true,
        min: 0,
        max: 500,
        values: [75, 300],
        slide: function (event, ui) {
            $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });
    $("#amount").val("$" + $("#slider-range").slider("values", 0) +
        " - $" + $("#slider-range").slider("values", 1));
});

////log in and register buttons js

/*$(document).ready( function myFunction() {
var x = document.getElementById("container_login_div");
var y = document.getElementById("container_reg_div");
if (x.style.display === "none") {
  x.style.display = "block";
  y.style.display = "none";
}

else if (x.style.display === "none" && y.style.display === "block"){
  y.style.display = "none";
  x.style.display === "block"
}  else {
  x.style.display = "none";
}
});

$(document).ready(function myFunctionReg() {
  var x = document.getElementById("container_reg_div");
  var y = document.getElementById("container_login_div");
  if (x.style.display === "none") {
    x.style.display = "block";
    y.style.display = "none";
  }
  else if (x.style.display === "none" && y.style.display === "block"){
    y.style.display = "none";
    x.style.display === "block"
  }

  else {
    x.style.display = "none";
  }
});*/

///log in and register buttons js


//navigation bar
function navBar() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}
////password ValidationError
function checkPasswordMatch() {
    var password = $("#id_password").val();
    var confirmPassword = $("#id_re_password").val();

    if (password && confirmPassword)
        if (password != confirmPassword)
            $("#message").html("Passwords do not match!").css('color', 'red');
        else
            $("#message").html("Passwords match.").css('color', 'green');
    else
        $("#message").html(" ");
}

$(document).ready(function () {
    $("#id_password, #id_re_password").keyup(checkPasswordMatch);
});
////////password ValidationError ends
/////////terms and conditions modal

$(document).ready(function () {
    var modal = document.getElementById('myModal');

    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];


    // When the user clicks on the button, open the modal
    btn.onclick = function () {
        modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

});




///////terms and conditions modal

$(document).ready(function () {
    $("#id_dob").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "-100:+100",
        dateFormat: 'yy-mm-dd',
        autoclose: true,
        maxDate: '-18y',

        // You can put more options here.

    });
});
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

/*

function changeImage() {
    //console.log(document.getElementById("imgClickAndChange").src)

    if (document.getElementById("imgClickAndChange").src = "../static/images/like_1.png") {
        //document.getElementById("imgClickAndChange").src = "static/images/like_2.png";
        document.getElementById("imgClickAndChange").src = "../static/images/like_2.png"
        //$('#imgClickAndChange').attr('src', '');
        console.log(document.getElementById("imgClickAndChange").src)

    }
    else {
        document.getElementById("imgClickAndChange").src = "static/images/like_1.png";
    }
}


$(document).ready(function () {
    $('#filterByAge').click(function () {
        document.getElementById("displayContentA").classList.toggle("show");

    });
});

$(document).ready(function () {
    $('#agedropdown').click(function () {
        document.getElementById("displayContentG").classList.toggle("show");

    });
});*/


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

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


$(document).ready(function () {
    $('.heart').click(function () {
        event.preventDefault();
        var match = $('.card-title')[0].id
        var black = '/static/images/like_1.png'
        var red = '/static/images/like_2.png'

        $.ajax({
            type: 'PUT',
            url: '/liked/' + match + '/',
            success: function (data) {
                data = JSON.stringify(data)
                data = JSON.parse(data)
                if (data.liked) {
                    // if its true then red heart
                    $(".heart").attr('src', red);
                }
                else {
                    //empty heart
                    $(".heart").attr('src', black);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr)
            }
        })


    });
});

$('#profile-image-upload').click(function () {
    $("#img_file").click();
});
