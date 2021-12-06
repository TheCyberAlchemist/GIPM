$(function() {

	clear_form($(".myform"))

	demo2 = $('.multiselect').bootstrapDualListbox({
		nonSelectedListLabel: 'Non-selected',
		selectedListLabel: 'Selected',
		preserveSelectionOnMove:false,
		moveOnSelect: false,
		nonSelectedFilter: ''
	});

	$("#refresh_list").on("click",function(){
		$(".spinner-border").show();
		refresh_options();
	})

	$("#save_assembly").on("click",function(){
		save_assembly();
	})
	$("#update_assembly").on("click",function(){
		update_assembly();
	})
	

	// for (i of demo2.val()){
	// 	add_to_mirror($("option[value='"+i+"']").first());
	// }
	$("tr input").on('keyup',function(e){
		calculate_total();
	})
	$("tr input").on("change",function(){
		calculate_total();
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
			<tr data-ev="${$option.data('ev')}" data-pk="${$option.val()}" id="tr_item_${$option.val()}">
				<td>${$option.html()}</td>
				<td>${$option.data('ev')}</td>
				<td><input type='number' class="thickness_input" value='1' min='0'></td>
				<td><input type='number' class="size_input" value='1' min='0'></td>
				<td><input type='number' class="width_input" value='1' min='0'></td>
				<td><input type='number' class="internal_diameter_input" value='1' min='0'></td>
				<td><input type='number' value='1' class = "quantity_input" id='quantity_${$option.val()}' min='0'></td>

			</tr>
		`;
		$("#mirror").append(option_str)
		$(`#tr_item_${$option.val()} input`).on('keyup',function(e){
			calculate_total();
		})
		$(`#tr_item_${$option.val()} input`).on("change",function(){
			calculate_total();
		})
	})
	calculate_total()
}

function remove_from_mirror(options){
	options.each(function(index, option) {
		var $option = $(option);
		$("#mirror").find(`[data-pk=${$option.val()}]`).remove();
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

function get_item_and_json(){
	let item_json = {};
	let items = [];
	$("#mirror tr").each(function(i,tr){
		tr = $(tr);
		let pk = tr.data("pk");
		let quantity = tr.find(".quantity_input").val();
		let size = tr.find(".size_input").val();
		let thickness = tr.find(".thickness_input").val();
		let width = tr.find(".width_input").val();
		let internal_diameter = tr.find(".internal_diameter_input").val();
		// console.log(pk,quantity,shape,thickness,width,internal_diameter);
		items.push(pk);
		item_json[pk] = {
			"quantity": quantity || 0,
			"size": size || 0,
			"thickness": thickness || 0,
			"width": width || 0,
			"internal_diameter": internal_diameter || 0
		};
	})
	return [item_json,items]
}

function calculate_total(){
	let total = 0;
	let [item_json,items] = get_item_and_json();
	$.ajax({
		url: '/api/calculate-estimate',
		data : {"item_json": JSON.stringify(item_json)},
		dataType: 'json',
		success: function (response) {
			console.log(response);
			total = response;
			if (!total){
				total = 0.00;
			}
			$("#total_estimate").html(total);
		},
		error: function (response) {
			console.log(response);
		}
	})

}

function update_assembly(){
	let form = $(".myform");
	let estimate_value = parseFloat($("#total_estimate").html());
	let [item_json,items] = get_item_and_json();
	let form_data = {
		"name": $("#name").val(),
		"description": $("#description").val(),
		"item_json":JSON.stringify(item_json),
		"items": items,
		"estimate_value":estimate_value,
	}
	let form_method = "PUT";
	let form_url = `/api/assembly/${assembly_id}/`;
	// console.log(form_data)
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

function save_assembly(){
	let form = $(".myform");
	let estimate_value = parseFloat($("#total_estimate").html());
	let [item_json,items] = get_item_and_json();
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