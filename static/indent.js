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
$(document).ready(function() {
	console.log("in")
})