function addProductReview(){
	// build an object of review data to submit
	var review = { 
		title: $("#id_title").val(),
		content: $("#id_content").val(),
		rating: $("#id_rating").val(),
		slug: $("#id_slug").val() };
	// make request, process response
	$.post("/review/product/add/", review,
		function(response){
			$("#review_errors").empty();
			// evaluate the "success" parameter
			if(response.success == "True"){
				// disable the submit button to prevent duplicates
				$("#submit_review").attr('disabled','disabled');
				// if this is first review, get rid of "no reviews" text
				$("#no_reviews").empty();
				// add the new review to the reviews section
				$("#reviews").prepend(response.html).slideDown();
				// get the newly added review and style it with color 
				new_review = $("#reviews").children(":first");
				new_review.addClass('new_review');
				// hide the review form
				$("#review_form").slideToggle();
			}
			else{
				// add the error text to the review_errors div
				$("#review_errors").append(response.html);
			}
		}, "json");
	
}

function addTag(){
	tag = { tag: $("#id_tag").val(),
			slug: $("#id_slug").val() };
	$.post("/tag/product/add/", tag,
			function(response){
				if (response.success == "True"){
					$("#tags").empty();
					$("#tags").append(response.html);
					$("#id_tag").val("");
				}
		}, "json");
}

// toggles visibility of "write review" link
// and the review form.
function slideToggleReviewForm(){
	$("#review_form").slideToggle();
	$("#add_review").slideToggle();
}

function statusBox(){
	$('<div id="loading">Loading...</div>')
	.prependTo("#main")
	.ajaxStart(function(){$(this).show();})
	.ajaxStop(function(){$(this).hide();})
}

function prepareDocument(){
	//prepare the search box
	$("form#search").submit(function(){
		text = $("#id_q").val();
		if (text == "" || text == "Search"){
			alert("Enter a search term.");
			return false;
		}
	});
	//prepare product review form
	$("#submit_review").click(addProductReview);
	$("#review_form").addClass('hidden');
	$("#add_review").click(slideToggleReviewForm);
	$("#add_review").addClass('visible');
	$("#cancel_review").click(slideToggleReviewForm);
	//tagging functionality
	$("#add_tag").click(addTag);
	$("#id_tag").keypress(function(event){
		if (event.keyCode == 13 && $("#id_tag").val().length > 2){
			addTag();
			event.preventDefault();
		}
	});
	statusBox();
}

$(document).ready(prepareDocument);
