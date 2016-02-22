var mapPoints = []

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
function geocode(item) {
    var googleGeocoder = new GeocoderJS.createGeocoder({'provider': 'google'});
    googleGeocoder.geocode(item['org'], function(result) {
      		//console.log(result[0].latitude)
      		//console.log(result[0].longitude) 	
      		mapPoints.push({"author":item['author'],"no":item['no'],"org":item['org'],"lat":result[0].latitude, "lon":result[0].longitude})
      		createPoints(mapPoints);
      		//console.log(mapPoints)
    });
}

$('#search-icon').on('click', function(){
  $('#search-box').css("visibility", "visible");
  $("#loadingBackground").css("visibility", "visible");
  $("#close-button").css("visibility", "visible");
  return false;
});
$('#close-button').click(function (e) {
	$("#close-button").css("visibility", "hidden");
	$('#search-box').css("visibility", "hidden");
	$("#loadingBackground").css("visibility", "hidden");
	$('#search-icon').css("visibility", "visible");
});


$("#submit").click(function(e) {
	clearMap()
	$("#close-button").css("visibility", "hidden");
	$('#search-box').css("visibility", "hidden");
	$("#loadingImage").css("visibility", "visible");
	$("#loadingBackground").css("visibility", "visible");
	$("#loadingText").Loadingdotdotdot({
    "speed": 400,
    "maxDots": 3,
    "word": "Loading"
	});
	$("#loadingText").css("visibility", "visible");
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    var author = $('#author').val();
    var keywords = $('#keywords').val();
    var ystart = $('#ystart').val();
    var yend = $('#yend').val();
    var count = 200
    mapPoints = []
    $.ajax({
        url: window.location.href, // the endpoint,commonly same url
        type: "POST", // http method
        data: {
            csrfmiddlewaretoken: csrftoken,
            author: author,
            keywords: keywords,
            ystart: ystart,
            yend: yend,
            count: count
        },

        success: function(json) {
            console.log(json); // another sanity check
            //On success show the data posted to server as a message
            //alert('Number of Authors:' + json['data'].length);
            
            for (i = 0; i < json['data'].length; i++){
            	geocode(json['data'][i]);
            	console.log(json['data'][i]['author'])
            };
            
    		$("#loadingImage").css("visibility", "hidden");
			$("#loadingBackground").css("visibility", "hidden");
            $("#loadingText").css("visibility", "hidden");
            $('.search-box').css("visibility", "hidden");
            alert(json['data'].length + " Co-authored Publications Found!")
        },
        // handle a non-successful response
        error: function(xhr, errmsg, err) {
        	alert("No results!")
            $("#loadingImage").css("visibility", "hidden");
			$("#loadingBackground").css("visibility", "hidden");
            $("#loadingText").css("visibility", "hidden");
        }
    });
});