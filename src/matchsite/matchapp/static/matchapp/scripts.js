
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

function gender() {
        document.getElementById("genderDropdown").classList.toggle("show");
}

function age() {
        document.getElementById("ageDropdown").classList.toggle("show");

}


$(document).ready(function () {
    $("#save_button").click(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/filter/',
            success: function (data) {
                console.log("success ")
            }

        })

    });
})


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



$(document).ready(function () {

	$('#reset_button').click(function () {
    	//document.getElementById('genderOption').value='default'
    	document.getElementById('range1').value = ""
        document.getElementById('range2').value = ""
	});

    $('#reset_all').click(function () {
        document.getElementById('genderOption').value='default'
        document.getElementById('range1').value = ""
        document.getElementById('range2').value = ""
    });

});

$(document).ready(function () {

    $('#searchAge').click(function () {
        var range1 = document.getElementById('range1').value;
        var range2 = document.getElementById('range2').value;
        //document.getElementById('genderOption').value='default'
        if (range1 == "")
        {
            alert("enter something ")
        }

        else if(range2 == "")
        {

        }

        else if(range1 == "" && range2 == "")
        {

        }

        //Ajax for search age
        else
        {

        }
    });

});

$(document).ready(function () {

    $('#genderOption').change(function() {
        var val = $("#genderOption option:selected").text();
        if(val == "All")
        {

        }

        if(val == "Male")
        {

        }

        if(val == "Female")
        {

        }
    })

});
////////slush bucket
$(document).ready(function () {
    $('#btnRight').click(function (e) {
        var selectedOpts = $('#lstBox1 option:selected');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }
        $('#lstBox2').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });
    $('#btnAllRight').click(function (e) {
        var selectedOpts = $('#lstBox1 option');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }
        $('#lstBox2').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });
    $('#btnLeft').click(function (e) {
        var selectedOpts = $('#lstBox2 option:selected');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }
        $('#lstBox1').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });
    $('#btnAllLeft').click(function (e) {
        var selectedOpts = $('#lstBox2 option');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }
        $('#lstBox1').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });
}());

////////
$(document).ready(function () {
    $("#from-datepicker").datepicker({
        format:'YYYY-MM-DD'
    });
    $("#from-datepicker").on("change", function () {
        var fromdate = $(this).val();
        alert(fromdate);
    });
});

////
$(document).ready( function() {
    $( "#datepicker" ).datepicker({
      changeMonth:true,
      changeYear: true,
      yearRange: '1900:2018',
      dateFormat:"yy-mm-dd",
      

    });
    $( "#format" ).on( "change", function() {
      $( "#datepicker" ).datepicker( "option", "dateFormat", $( this ).val() );
    });
  } );

////
