$(function() {

	clear_form($(".myform"))

	demo2 = $('.multiselect').bootstrapDualListbox({
		nonSelectedListLabel: 'Non-selected',
		selectedListLabel: 'Selected',
		preserveSelectionOnMove:false,
		moveOnSelect: false,
		nonSelectedFilter: ''
	});

	$("#refresh_list").click(function(){
		$(".spinner-border").show();
		refresh_options();
	})
	$("#save_assembly").click(function(){
		submit_form();
	})
});
function refresh_options(){
	$.ajax({
		url: '/api/item-description',
		type: "get",
		success: function (all_items) {
			demo2.bootstrapDualListbox('getDeselected').remove();
			demo2.bootstrapDualListbox('refresh');
			let selected_options = demo2.bootstrapDualListbox('getSelected');
			for(item of all_items){
				let option_selected = false;
				selected_options.each(function (index, option) {
					if (option.value == item.id){
						option_selected = true;
					}
				})
				if (!option_selected){
					let option = `<option value="${item.id}" data-ev = "${item.estimated_value}">${item.description}</option>`;
					demo2.append(option);
					demo2.bootstrapDualListbox('refresh');
				}
			}
			$(".spinner-border").hide();
			console.log(all_items);
		}
	})
}
function add_to_mirror(options){
	options.each(function(index, option) {
		var $option = $(option);
		let option_str = 
		`
			<tr data-ev="${$option.data('ev')}" data-value="${$option.val()}">
				<td>${$option.html()}</td>
				<td>${$option.data('ev')}</td>
				<td><input type='number' value='1' id='quantity_${$option.val()}' min='0' "></td>
			</tr>
		`;
		$("#mirror").append(option_str)
		$(`#quantity_${$option.val()}`).keyup(function(){
			console.log("here")
			calculate_total();
		})
		$(`#quantity_${$option.val()}`).change(function(){
			console.log("here")
			calculate_total();
		})
	})
	calculate_total()
}
function remove_from_mirror(options){
	options.each(function(index, option) {
		var $option = $(option);
		$("#mirror").find(`[data-value=${$option.val()}]`).remove();
	})
	calculate_total();
}
function optionMoved(obj){
	add_to_mirror(obj);
	// console.log("optionMoved",obj);
}
function optionRemoved(obj){
	remove_from_mirror(obj)
	// console.log("optionRemoved",obj);
}
function allOptionMoved(obj){
	add_to_mirror(obj);
	// console.log("allOptionMoved",obj);
}
function allOptionRemoved(obj){
	remove_from_mirror(obj)
	// console.log("allOptionRemoved",obj);
}

function calculate_total(){
	let total = 0;
	$("#mirror input").each(function(a,quantity){
		quantity_input = $(quantity);
		let tr = quantity_input.parent().parent();
		if (tr.data("ev")){
			total += parseFloat(quantity_input.val()) * parseFloat(tr.data("ev"));
		}
	})
	// console.log(total)
	if (!total){
		total = 0.00;
	}
	$("#total_estimate").html(total);
}
function submit_form(){
	let form = $(".myform");
	let item_json = {};
	let items = [];
	let estimate_value = parseFloat($("#total_estimate").html());
	$("#mirror tr").each(function(i,tr){
		tr = $(tr);
		let pk = tr.data("value");
		let quantity  = tr.find("input").val();
		items.push(pk);
		item_json[pk] = quantity;
	})
	let form_data = {
		"name": $("#name").val(),
		"description": $("#description").val(),
		"item_json":JSON.stringify(item_json),
		"items": items,
		"estimate_value":estimate_value,
	}
	let form_method = "POST";
	let form_url = "/api/assembly";
	console.log(form_data)
	$.ajax({
		url: form_url,
		data : JSON.stringify(form_data),
		type: form_method,
		contentType: "application/json; charset=utf-8",
		success: function (response) {
			console.log(response);
			if (response.success){
				$("#mirror").html("");
				clear_form(form)
			}
		},
		error: function (response) {
			console.log(response);
		}
	})
}