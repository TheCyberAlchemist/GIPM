function edit_locked(link){
	Swal.fire({
		icon: "question",
		title: 'Lock the indents?',
		input: 'text',
		inputAttributes: {
			autocapitalize: 'off'
		},
		showCancelButton: true,
		confirmButtonText: 'Lock',
		showLoaderOnConfirm: true,
		preConfirm: (password) => {
			if (password == "21149"){
				window.open(link,"_self");
			}else{
				swal.close()
			}
		},
		allowOutsideClick: () => !Swal.isLoading()
		})
}
function fill_indent_form(data){
	// fill the form with the data
	$('#material_shape')
		.val(data.material_shape)
		.trigger('change')
	;
	$('#material_type').val(data.material_type);
	$('#size').val(data.size);
	$('#thickness').val(data.thickness);
	$('#width').val(data.width);
	$('#internal_diameter').val(data.internal_diameter);
	$('#description').val(data.description);
	$('#quantity').val(data.quantity);
	$('#unit').val(data.unit);
	$('#value').val(data.value);
	$('#tax').val(data.tax);
	$('#discount').val(data.discount);
	$('#other_expanses').val(data.other_expenses);
}

function call_indent_api(item_description_id){
	// send a ajax get request to the api
	$.ajax({
		url: "/api/get_last_indent/",
		type: "GET",
		data: {
			item_description_id: item_description_id
		},
		success: function(data){
			console.log(data);
			if (data.value != undefined ){
				Swal.fire({
					title: '<strong>Old Indent Found',
					icon: 'info',
					html:
					`Material_shape - <b>${data.material_shape}</b>, ` + '<br>' +
					`Material_type - <b>${data.material_type}</b>, ` + '<br>' +
					`length/Diameter - <b>${data.size}</b>, ` + '<br>' +
					`Thickness - <b>${data.thickness}</b>, ` + '<br>' +
					`Width - <b>${data.width}</b>, ` + '<br>' +
					`Internal_diameter - <b>${data.internal_diameter}</b>, ` + '<br>' +
					`Description - <b>${data.description}</b>, ` + '<br>' +
					`Quantity - <b>${data.quantity}</b>, ` + '<br>' +
					`Unit - <b>${data.unit}</b>, ` + '<br>' +
					`Value - <b>${data.value}</b>, ` + '<br>' +
					`Tax - <b>${data.tax}</b>, ` + '<br>' +
					`Discount - <b>${data.discount}</b>, ` + '<br>' +
					`Other_expenses - <b>${data.other_expenses}</b>, ` + '<br>' +""
					,
					showCloseButton: true,
					showCancelButton: true,
					focusConfirm: false,
					confirmButtonText:
					  "Great add it!",
					cancelButtonText:
					  "No, I'll add it",
				  }).then((result) => {
					/* Read more about isConfirmed, isDenied below */
					if (result.isConfirmed) {
					  fill_indent_form(data);
					}
				  });
				$(".swal2-html-container")
					.css("text-align","inherit")
					.css("padding","1em 6em .3em");

			}
		},
		error: function(data){
			console.log(data);
		}
	});
}

$(document).ready(function() {
	console.log("in");
})