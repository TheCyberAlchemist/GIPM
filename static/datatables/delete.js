$(document).ready(function () {
	if ($("#del").length) {
		checkSelected(); // if any selected for delete already
	}
});
function checkAll(){

	var parent = document.getElementById('parent');
	var input = document.getElementsByClassName('del_input');
	if(parent.checked == true){	
	  for(var i=0; i<input.length;i++){
		  if(input[i].checked == false ) {
			input[i].checked = true; 
		  }
	  }  
	}
	if(parent.checked == false){
	  for(var i=0; i<input.length;i++){
		  if(input[i].checked ==true){
			input[i].checked = false; 
		  }
	  }
	}
	checkSelected();
}

function checkSelected(){
	// if faculty in user_details then id = del1
	id="del"
	var child = document.getElementsByName(id);
	var del = document.getElementById(id);
	var check = false;
	for(var c in child){
		if(child[c].checked == true){
			del.style.display = "inline";
			check = true;
			break;
		}
	}
	if(!check){
		del.style.display = "none";
	}
}

function delete_entries(reload = true) {
	
	var checked = $('input[name="del"]:checked').map(function () {return this.value;}).get();
	var inner_html = $('input[name="del"]:checked').map(function () {return this.attributes.input_name.value;}).get().toString().split(',');
	console.log(checked);
	let delete_message = "";
	for (i in inner_html){
		delete_message += "<li>" + inner_html[i] + "</li>";
	}
	let state = checked;
	
	if (checked.length) {
		// checkes if one or more are selected or not
		// console.log(state)
		const swalWithBootstrapButtons = Swal.mixin({
			customClass: {
			  confirmButton: 'btn btn-success',
			  cancelButton: 'btn btn-danger'
			},
			buttonsStyling: false
		  })
		  swalWithBootstrapButtons.fire({
			title: `Are you sure?`,
			html:`You won't be able to revert this!<br><ul>`+delete_message+`</ul>`,
			icon: 'warning',
			showCancelButton: true,
			confirmButtonText: 'No, cancel!',
			cancelButtonText: 'Yes, delete it! ',
			reverseButtons: true
		  }).then((result) => {
			if (result.isConfirmed) {
				swalWithBootstrapButtons.fire(
					'Cancelled',
					'Your data is safe :)',
					'error'
					)
				} else if (result.dismiss === Swal.DismissReason.cancel) {
					swalWithBootstrapButtons.fire({
						title:'Deleted!',
						text:'Your data has been deleted.',
						icon:'success',
						showConfirmButton: false,
					})
					$.ajax({
						type: "post",
						data: {'pks':state},
						success: function () {
							// reload page after success of post
							if (reload){
								setTimeout(() => {  location.reload(); }, 1000);
							}else{
								table = $('#example');
								table.DataTable().ajax.reload(null, false);
								// console.log(table);
								setTimeout(() => {  Swal.close() }, 1000);
							}

						},
					});
				}
		  })


		// swal({
		// 	title: "Warning!",
		// 	text:
        // "This Data will be deleted :: \n ->" + delete_message,
		// 	icon: "warning",
		// 	dangerMode: true,
		// 	buttons: ["Cancel", "Delete"],
		// }).then((willDelete) => {
		// 	if (willDelete) {
		// 		swal("", {
		// 			icon: "success",
		// 			text: "Deleted Successfully!",
		// 		});
				// $.ajax({
				// 	type: "post",
				// 	data: state,
				// 	success: function () {
				// 		location.reload(); // reload page after success of post
				// 	},
				// });
		// 	} else {
		// 		swal("Your changes are not saved!");
		// 	}
		// });
	}
}